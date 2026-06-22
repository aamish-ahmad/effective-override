"""Run resumable last-two and last-three-step Experiment 2 baselines."""

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
PROMPT_PATH = ROOT / "prompts" / "baseline_ladder_rater_prompt.md"
RUBRIC_PATH = ROOT / "rubric.md"
VALIDATOR_PATH = ROOT / "scripts" / "check_experiment2_hard_controls_v1.py"
MODEL = "gemini-3.1-flash-lite"
DEFAULT_SLEEP_SECONDS = 5.0
EXPECTED_COUNT = 20

CONDITIONS = {
    "last_2_steps": {
        "window_size": 2,
        "responses": ROOT / "baseline_ladder" / "experiment2_last2_responses_gemini_3_1_flash_lite.md",
        "errors": ROOT / "baseline_ladder" / "experiment2_last2_errors_gemini_3_1_flash_lite.md",
    },
    "last_3_steps": {
        "window_size": 3,
        "responses": ROOT / "baseline_ladder" / "experiment2_last3_responses_gemini_3_1_flash_lite.md",
        "errors": ROOT / "baseline_ladder" / "experiment2_last3_errors_gemini_3_1_flash_lite.md",
    },
}

REQUIRED_FIELDS = {
    "trajectory_id",
    "baseline_condition",
    "crossing_present",
    "crossing_step",
    "reason",
    "confidence",
}
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "trajectory_id": {"type": "string"},
        "baseline_condition": {
            "type": "string",
            "enum": ["last_2_steps", "last_3_steps"],
        },
        "crossing_present": {
            "type": "string",
            "enum": ["yes", "no", "uncertain"],
        },
        "crossing_step": {
            "anyOf": [{"type": "integer"}, {"type": "null"}]
        },
        "reason": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "required": sorted(REQUIRED_FIELDS),
    "additionalProperties": False,
}
JSON_ONLY_RETRY = """

Your previous response was invalid. Return exactly one JSON object matching the
required schema, with no Markdown or explanatory text.
"""
MODEL_RE = re.compile(r"(?m)^- model:\s*`?([^`\r\n]+)`?\s*$")
CONDITION_RE = re.compile(r"(?m)^- baseline_condition:\s*`?([^`\r\n]+)`?\s*$")


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


def ledger_header(condition: str, title: str) -> str:
    return (
        f"# {title}\n\n"
        f"- model: `{MODEL}`\n"
        f"- baseline_condition: `{condition}`\n"
    )


def ensure_ledger(path: Path, condition: str, title: str) -> None:
    path.parent.mkdir(exist_ok=True)
    if not path.exists():
        path.write_text(ledger_header(condition, title), encoding="utf-8")
        return
    content = path.read_text(encoding="utf-8-sig")
    sections = engine.read_markdown_sections(path)
    model_match = MODEL_RE.search(content)
    condition_match = CONDITION_RE.search(content)
    if not model_match or not condition_match:
        if sections:
            raise RuntimeError(f"{path} has responses but no ledger metadata")
        path.write_text(ledger_header(condition, title), encoding="utf-8")
        return
    if model_match.group(1).strip() != MODEL:
        raise RuntimeError(f"{path} contains a different model")
    if condition_match.group(1).strip() != condition:
        raise RuntimeError(f"{path} contains a different baseline condition")


def visible_step_numbers(step_count: int, window_size: int) -> set[int]:
    return set(range(step_count - window_size + 1, step_count + 1))


def validate_response(
    value: object,
    trajectory_id: str,
    condition: str,
    step_count: int,
    window_size: int,
) -> dict:
    if not isinstance(value, dict):
        raise ValueError("response is not a JSON object")
    if set(value) != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - set(value))
        extra = sorted(set(value) - REQUIRED_FIELDS)
        raise ValueError(f"field mismatch; missing={missing}, extra={extra}")
    if value["trajectory_id"] != trajectory_id:
        raise ValueError("trajectory_id differs from requested ID")
    if value["baseline_condition"] != condition:
        raise ValueError("baseline_condition differs from requested condition")
    label = str(value["crossing_present"]).strip().lower()
    if label not in {"yes", "no", "uncertain"}:
        raise ValueError("crossing_present must be yes, no, or uncertain")
    value["crossing_present"] = label
    step = value["crossing_step"]
    if label == "yes":
        if isinstance(step, bool) or not isinstance(step, int):
            raise ValueError("yes requires an integer crossing_step")
        if step not in visible_step_numbers(step_count, window_size):
            raise ValueError("crossing_step must be an original visible step number")
    elif step is not None:
        raise ValueError("no/uncertain requires crossing_step=null")
    if not isinstance(value["reason"], str):
        raise ValueError("reason must be a string")
    confidence = value["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("confidence must be numeric")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return value


def build_prompt(
    template: str,
    trajectory: dict[str, object],
    condition: str,
    window_size: int,
) -> str:
    steps = trajectory["steps"]
    start_index = len(steps) - window_size
    visible = "\n".join(
        f"{index + 1}. {steps[index]}" for index in range(start_index, len(steps))
    )
    prompt = template.replace("{{BASELINE_CONDITION}}", condition)
    prompt = prompt.replace("{{VISIBLE_WINDOW}}", visible)
    rubric = RUBRIC_PATH.read_text(encoding="utf-8-sig").rstrip()
    return (
        f"{prompt.rstrip()}\n\n"
        f"## Full project rubric\n\n{rubric}\n\n"
        f"trajectory_id: {trajectory['trajectory_id']}\n"
    )


def is_hard_quota_or_billing_error(error: Exception) -> bool:
    message = str(error).lower()
    hard_markers = (
        "generaterequestsperdayperprojectpermodel-freetier",
        "daily quota",
        "per day",
        "perday",
        "billing",
        "payment required",
        "insufficient credits",
        "credit balance",
        "quota has been exhausted",
    )
    return any(marker in message for marker in hard_markers)


def completed_ids(
    path: Path,
    trajectories: list[dict[str, object]],
    condition: str,
    window_size: int,
) -> set[str]:
    by_id = {str(item["trajectory_id"]): item for item in trajectories}
    completed = set()
    for trajectory_id, body in engine.read_markdown_sections(path).items():
        trajectory = by_id.get(trajectory_id)
        if trajectory is None:
            print(f"WARNING: ignoring unknown response ID {trajectory_id}")
            continue
        try:
            validate_response(
                json.loads(body),
                trajectory_id,
                condition,
                len(trajectory["steps"]),
                window_size,
            )
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            print(f"WARNING: invalid existing {condition} response {trajectory_id}: {error}")
            continue
        completed.add(trajectory_id)
    return completed


def main() -> int:
    validate_dataset()
    engine.DATA_PATH = DATA_PATH
    trajectories = engine.load_trajectories()
    if len(trajectories) != EXPECTED_COUNT:
        raise ValueError(f"expected {EXPECTED_COUNT} trajectories, found {len(trajectories)}")
    template = PROMPT_PATH.read_text(encoding="utf-8-sig")
    for condition, config in CONDITIONS.items():
        ensure_ledger(
            config["responses"], condition, f"Experiment 2 {condition} Responses"
        )
    completed = {
        condition: completed_ids(
            config["responses"],
            trajectories,
            condition,
            config["window_size"],
        )
        for condition, config in CONDITIONS.items()
    }
    total_remaining = sum(EXPECTED_COUNT - len(ids) for ids in completed.values())
    for condition in CONDITIONS:
        print(f"{condition} already completed: {len(completed[condition])}")
    print(f"Total remaining: {total_remaining}")
    if total_remaining == 0:
        print("All baseline-ladder responses are complete; no API calls were made.")
        return 0

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set; no API calls were made.")
        return 2

    from google import genai

    engine.DEFAULT_SLEEP_SECONDS = DEFAULT_SLEEP_SECONDS
    sleep_seconds = engine.request_sleep_seconds()
    engine.RESPONSE_SCHEMA = RESPONSE_SCHEMA
    engine.is_daily_quota_error = is_hard_quota_or_billing_error
    generator = engine.PacedGenerator(genai.Client(api_key=api_key), MODEL, sleep_seconds)
    successes = 0
    failures = 0
    hard_stop = False

    for condition, config in CONDITIONS.items():
        response_path = config["responses"]
        error_path = config["errors"]
        existing_errors = engine.read_markdown_sections(error_path)
        for trajectory in trajectories:
            trajectory_id = str(trajectory["trajectory_id"])
            if trajectory_id in completed[condition]:
                continue
            prompt = build_prompt(
                template, trajectory, condition, config["window_size"]
            )
            raw_outputs: list[str] = []
            last_error: Exception | None = None
            for attempt in range(2):
                try:
                    response = generator.generate(
                        prompt if attempt == 0 else prompt + JSON_ONLY_RETRY
                    )
                    raw = response.text or ""
                    raw_outputs.append(raw)
                    validated = validate_response(
                        json.loads(raw),
                        trajectory_id,
                        condition,
                        len(trajectory["steps"]),
                        config["window_size"],
                    )
                    engine.append_markdown(
                        response_path,
                        trajectory_id,
                        json.dumps(validated, indent=2, ensure_ascii=False),
                    )
                    engine.remove_markdown_section(error_path, trajectory_id)
                    successes += 1
                    last_error = None
                    print(f"Rated {condition} {trajectory_id}")
                    break
                except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
                    last_error = error
                    if attempt == 0:
                        print(f"Retrying {condition} {trajectory_id} after invalid JSON")
                        continue
                except engine.DailyQuotaExhausted as error:
                    last_error = error
                    hard_stop = True
                    break
                except Exception as error:
                    last_error = error
                    break

            if last_error is not None:
                ensure_ledger(error_path, condition, f"Experiment 2 {condition} Errors")
                error_body = (
                    f"Error: {type(last_error).__name__}: {last_error}\n\n"
                    + "\n\n--- Retry output ---\n\n".join(
                        output or "(empty output)" for output in raw_outputs
                    )
                )
                if trajectory_id not in existing_errors:
                    engine.append_markdown(error_path, trajectory_id, error_body)
                    existing_errors[trajectory_id] = error_body
                failures += 1
                print(
                    f"ERROR {condition} {trajectory_id}: "
                    f"{type(last_error).__name__}: {last_error}"
                )
            if hard_stop:
                print("Stopping cleanly on hard quota or billing exhaustion")
                break
        if hard_stop:
            break

    print(f"Model: {MODEL}")
    print(f"Successful responses this run: {successes}")
    print(f"Errors this run: {failures}")
    return 2 if hard_stop else (0 if not failures else 1)


if __name__ == "__main__":
    raise SystemExit(main())
