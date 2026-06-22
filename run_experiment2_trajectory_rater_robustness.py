"""Run an isolated Experiment 2 trajectory-rater robustness check."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from scripts.env_utils import load_local_env


load_local_env()

import run_gemini_trajectory_rater_experiment1 as engine


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "experiment2_hard_controls_v1.csv"
PREFERRED_PROMPT_PATH = ROOT / "prompts" / "trajectory_rater_prompt.md"
FALLBACK_PROMPT_PATH = ROOT / "prompts" / "blind_rater_prompt.md"
RUBRIC_PATH = ROOT / "rubric.md"
VALIDATOR_PATH = ROOT / "scripts" / "check_experiment2_hard_controls_v1.py"
RESPONSES_PATH = ROOT / "robustness" / "experiment2_trajectory_rater_responses_robustness.md"
ERRORS_PATH = ROOT / "robustness" / "experiment2_trajectory_rater_errors_robustness.md"
DEFAULT_MODEL = "gemini-3.5-flash"
PRIMARY_MODEL = "gemini-3.1-flash-lite"
DEFAULT_SLEEP_SECONDS = 5.0
EXPECTED_COUNT = 20

MODEL_RE = re.compile(r"(?m)^- model:\s*`?([^`\r\n]+)`?\s*$")
RUN_TYPE_RE = re.compile(r"(?m)^- run_type:\s*`?([^`\r\n]+)`?\s*$")


def validate_dataset() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode:
        raise RuntimeError("Experiment 2 validation failed; no API calls were made")


def run_type_for(model: str) -> str:
    return "repeated_run_stability" if model == PRIMARY_MODEL else "second_model_robustness"


def metadata_header(model: str, run_type: str) -> str:
    return (
        "# Experiment 2 Trajectory Rater Robustness Responses\n\n"
        f"- model: `{model}`\n"
        f"- run_type: `{run_type}`\n"
    )


def ensure_ledger_metadata(model: str, run_type: str) -> None:
    RESPONSES_PATH.parent.mkdir(exist_ok=True)
    if not RESPONSES_PATH.exists():
        RESPONSES_PATH.write_text(metadata_header(model, run_type), encoding="utf-8")
        return
    content = RESPONSES_PATH.read_text(encoding="utf-8-sig")
    model_match = MODEL_RE.search(content)
    type_match = RUN_TYPE_RE.search(content)
    sections = engine.read_markdown_sections(RESPONSES_PATH)
    if not model_match or not type_match:
        if sections:
            raise RuntimeError("robustness ledger has responses but no model metadata")
        RESPONSES_PATH.write_text(metadata_header(model, run_type), encoding="utf-8")
        return
    recorded_model = model_match.group(1).strip()
    recorded_type = type_match.group(1).strip()
    if recorded_model != model or recorded_type != run_type:
        raise RuntimeError(
            "robustness ledger configuration mismatch: "
            f"recorded {recorded_model}/{recorded_type}, requested {model}/{run_type}"
        )


def ensure_error_ledger(model: str, run_type: str) -> None:
    if not ERRORS_PATH.exists():
        ERRORS_PATH.write_text(
            "# Experiment 2 Trajectory Rater Robustness Errors\n\n"
            f"- model: `{model}`\n"
            f"- run_type: `{run_type}`\n",
            encoding="utf-8",
        )


def load_prompt() -> tuple[str, Path]:
    path = PREFERRED_PROMPT_PATH if PREFERRED_PROMPT_PATH.exists() else FALLBACK_PROMPT_PATH
    if path == FALLBACK_PROMPT_PATH:
        print(
            "WARNING: prompts/trajectory_rater_prompt.md is absent; "
            "using official prompts/blind_rater_prompt.md"
        )
    return path.read_text(encoding="utf-8-sig"), path


def build_prompt(template: str, trajectory: dict[str, object]) -> str:
    numbered_steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(trajectory["steps"], start=1)
    )
    blind_prompt = template.replace("{{TRAJECTORY_STEPS}}", numbered_steps).rstrip()
    rubric = RUBRIC_PATH.read_text(encoding="utf-8-sig").rstrip()
    return (
        f"{blind_prompt}\n\n"
        f"## Full project rubric\n\n{rubric}\n\n"
        f"trajectory_id: {trajectory['trajectory_id']}\n"
    )


def is_hard_quota_or_billing_error(error: Exception) -> bool:
    message = str(error).lower()
    daily_markers = (
        "generaterequestsperdayperprojectpermodel-freetier",
        "daily quota",
        "per day",
        "perday",
    )
    billing_markers = (
        "billing",
        "payment required",
        "insufficient credits",
        "credit balance",
        "quota has been exhausted",
    )
    return (
        engine.is_rate_limit_error(error)
        and any(marker in message for marker in daily_markers)
    ) or any(marker in message for marker in billing_markers)


def is_model_unavailable_error(error: Exception) -> bool:
    message = str(error).lower()
    return any(
        marker in message
        for marker in (
            "model not found",
            "model is not found",
            "model is unavailable",
            "not supported for generatecontent",
            "404 not found",
            "404 not_found",
            " is not found",
            "invalid model",
        )
    )


def load_completed_ids(trajectories: list[dict[str, object]]) -> set[str]:
    by_id = {str(item["trajectory_id"]): item for item in trajectories}
    completed = set()
    for trajectory_id, body in engine.read_markdown_sections(RESPONSES_PATH).items():
        trajectory = by_id.get(trajectory_id)
        if trajectory is None:
            print(f"WARNING: ignoring response for unknown ID {trajectory_id}")
            continue
        try:
            parsed = json.loads(body)
            engine.validate_response(parsed, trajectory_id, len(trajectory["steps"]))
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            print(f"WARNING: existing response for {trajectory_id} is invalid: {error}")
            continue
        completed.add(trajectory_id)
    return completed


def main() -> int:
    validate_dataset()
    model = os.getenv("GEMINI_ROBUSTNESS_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    run_type = run_type_for(model)
    print(f"Robustness model: {model}")
    print(f"Run type: {run_type}")
    ensure_ledger_metadata(model, run_type)

    engine.DATA_PATH = DATA_PATH
    trajectories = engine.load_trajectories()
    if len(trajectories) != EXPECTED_COUNT:
        raise ValueError(f"expected {EXPECTED_COUNT} trajectories, found {len(trajectories)}")
    template, prompt_path = load_prompt()
    completed_ids = load_completed_ids(trajectories)
    remaining = [
        item for item in trajectories if str(item["trajectory_id"]) not in completed_ids
    ]
    engine.DEFAULT_SLEEP_SECONDS = DEFAULT_SLEEP_SECONDS
    sleep_seconds = engine.request_sleep_seconds()
    print(f"Prompt path: {prompt_path}")
    print(f"Already completed: {len(completed_ids)}")
    print(f"Remaining: {len(remaining)}")
    print(f"API request sleep delay: {sleep_seconds:.1f} seconds")
    if not remaining:
        print("All robustness responses are complete; no API calls were made.")
        return 0

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set; no API calls were made.")
        return 2

    from google import genai

    engine.is_daily_quota_error = is_hard_quota_or_billing_error
    generator = engine.PacedGenerator(genai.Client(api_key=api_key), model, sleep_seconds)
    existing_errors = engine.read_markdown_sections(ERRORS_PATH)
    successes = 0
    failures = 0
    hard_stop = False
    hard_stop_reason = ""

    for trajectory in remaining:
        trajectory_id = str(trajectory["trajectory_id"])
        prompt = build_prompt(template, trajectory)
        raw_outputs: list[str] = []
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                response = generator.generate(
                    prompt if attempt == 0 else prompt + engine.JSON_ONLY_RETRY
                )
                raw = response.text or ""
                raw_outputs.append(raw)
                validated = engine.validate_response(
                    json.loads(raw), trajectory_id, len(trajectory["steps"])
                )
                engine.append_markdown(
                    RESPONSES_PATH,
                    trajectory_id,
                    json.dumps(validated, indent=2, ensure_ascii=False),
                )
                engine.remove_markdown_section(ERRORS_PATH, trajectory_id)
                successes += 1
                last_error = None
                print(f"Rated {trajectory_id}")
                break
            except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
                last_error = error
                if attempt == 0:
                    print(f"Retrying {trajectory_id} after invalid JSON response")
                    continue
            except engine.DailyQuotaExhausted as error:
                last_error = error
                hard_stop = True
                hard_stop_reason = "hard quota or billing exhaustion"
                break
            except Exception as error:
                last_error = error
                if is_model_unavailable_error(error):
                    hard_stop = True
                    hard_stop_reason = "model unavailable"
                break

        if last_error is not None:
            ensure_error_ledger(model, run_type)
            error_body = (
                f"Error: {type(last_error).__name__}: {last_error}\n\n"
                + "\n\n--- Retry output ---\n\n".join(
                    output or "(empty output)" for output in raw_outputs
                )
            )
            if trajectory_id not in existing_errors:
                engine.append_markdown(ERRORS_PATH, trajectory_id, error_body)
                existing_errors[trajectory_id] = error_body
            failures += 1
            print(f"ERROR {trajectory_id}: {type(last_error).__name__}: {last_error}")
        if hard_stop:
            print(f"Stopping cleanly: {hard_stop_reason}")
            break

    print(f"Rows attempted this run: {successes + failures}")
    print(f"Successful JSON responses this run: {successes}")
    print(f"Errors this run: {failures}")
    print(f"Response path: {RESPONSES_PATH}")
    return 2 if hard_stop else (0 if not failures else 1)


if __name__ == "__main__":
    raise SystemExit(main())

