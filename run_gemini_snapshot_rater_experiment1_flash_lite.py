"""Run final-step-only Flash Lite snapshot ratings for Experiment 1."""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from scripts.env_utils import load_local_env


load_local_env()

import run_gemini_trajectory_rater_experiment1 as robust_runner


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "experiment1.csv"
PROMPT_PATH = ROOT / "prompts" / "snapshot_rater_prompt.md"
RESPONSES_PATH = (
    ROOT / "data" / "experiment1_snapshot_rater_responses_gemini_3_1_flash_lite.md"
)
ERRORS_PATH = (
    ROOT / "data" / "experiment1_snapshot_rater_errors_gemini_3_1_flash_lite.md"
)
DEFAULT_MODEL = "gemini-3.1-flash-lite"
DEFAULT_SLEEP_SECONDS = 5.0
EXPECTED_COUNT = 30

REQUIRED_FIELDS = {
    "trajectory_id",
    "snapshot_crossing_present",
    "snapshot_crossing_step",
    "snapshot_reason",
    "confidence",
}
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "trajectory_id": {"type": "string"},
        "snapshot_crossing_present": {
            "type": "string",
            "enum": ["yes", "no", "uncertain"],
        },
        "snapshot_crossing_step": {
            "anyOf": [{"type": "integer"}, {"type": "null"}]
        },
        "snapshot_reason": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "required": sorted(REQUIRED_FIELDS),
    "additionalProperties": False,
}
JSON_ONLY_RETRY = """

Your previous response was not valid against the required JSON format. Return exactly
one JSON object and nothing else. Do not use Markdown fences or explanatory text.
Include every required field with the requested types.
"""


def load_snapshots() -> list[dict[str, object]]:
    snapshots = []
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            steps = json.loads(row["steps_json"])
            if not isinstance(steps, list) or not steps:
                raise ValueError(f"{row['trajectory_id']}: steps_json must be nonempty")
            snapshots.append(
                {
                    "trajectory_id": row["trajectory_id"],
                    "final_step_number": len(steps),
                    "final_step": str(steps[-1]),
                }
            )
    if len(snapshots) != EXPECTED_COUNT:
        raise ValueError(f"expected {EXPECTED_COUNT} trajectories, found {len(snapshots)}")
    ids = [str(item["trajectory_id"]) for item in snapshots]
    if len(ids) != len(set(ids)):
        raise ValueError("experiment1.csv contains duplicate trajectory_id values")
    return snapshots


def build_prompt(base_prompt: str, snapshot: dict[str, object]) -> str:
    """Construct a prompt containing no trajectory context before the final step."""
    return (
        f"{base_prompt.rstrip()}\n\n"
        "## Snapshot Input\n\n"
        f"trajectory_id: {snapshot['trajectory_id']}\n"
        f"final_step_number: {snapshot['final_step_number']}\n"
        f"final_step: {snapshot['final_step']}\n"
    )


def validate_response(value: object, expected_id: str, final_step_number: int) -> dict:
    if not isinstance(value, dict):
        raise ValueError("response is not a JSON object")
    if set(value) != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - set(value))
        extra = sorted(set(value) - REQUIRED_FIELDS)
        raise ValueError(f"response fields mismatch; missing={missing}, extra={extra}")
    if value["trajectory_id"] != expected_id:
        raise ValueError(f"trajectory_id must equal {expected_id}")

    label = value["snapshot_crossing_present"]
    if label not in {"yes", "no", "uncertain"}:
        raise ValueError("snapshot_crossing_present must be yes, no, or uncertain")
    step = value["snapshot_crossing_step"]
    if label == "yes":
        if isinstance(step, bool) or not isinstance(step, int):
            raise ValueError("yes requires an integer snapshot_crossing_step")
        if step != final_step_number:
            raise ValueError("positive snapshot_crossing_step must equal final step number")
    elif step is not None:
        raise ValueError("no/uncertain requires snapshot_crossing_step=null")
    if not isinstance(value["snapshot_reason"], str):
        raise ValueError("snapshot_reason must be a string")
    confidence = value["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("confidence must be numeric")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return value


def load_completed_ids(snapshots: list[dict[str, object]]) -> set[str]:
    by_id = {str(item["trajectory_id"]): item for item in snapshots}
    completed = set()
    for trajectory_id, body in robust_runner.read_markdown_sections(RESPONSES_PATH).items():
        snapshot = by_id.get(trajectory_id)
        if snapshot is None:
            print(f"WARNING: ignoring response for unknown ID {trajectory_id}")
            continue
        try:
            validate_response(
                json.loads(body), trajectory_id, int(snapshot["final_step_number"])
            )
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            print(f"WARNING: existing response for {trajectory_id} is invalid: {error}")
            continue
        completed.add(trajectory_id)
    return completed


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
        robust_runner.is_rate_limit_error(error)
        and any(marker in message for marker in daily_markers)
    ) or any(marker in message for marker in billing_markers)


def main() -> int:
    snapshots = load_snapshots()
    base_prompt = PROMPT_PATH.read_text(encoding="utf-8-sig")
    load_dotenv(ROOT / ".env")
    completed_ids = load_completed_ids(snapshots)
    remaining = [
        item for item in snapshots if str(item["trajectory_id"]) not in completed_ids
    ]
    robust_runner.DEFAULT_SLEEP_SECONDS = DEFAULT_SLEEP_SECONDS
    sleep_seconds = robust_runner.request_sleep_seconds()
    print(f"Already completed: {len(completed_ids)}")
    print(f"Remaining: {len(remaining)}")
    print(f"API request sleep delay: {sleep_seconds:.1f} seconds")
    if not remaining:
        print("All snapshots are already complete; no API calls were made.")
        return 0

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set; no API calls were made.")
        return 2

    from google import genai

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    robust_runner.RESPONSE_SCHEMA = RESPONSE_SCHEMA
    robust_runner.is_daily_quota_error = is_hard_quota_or_billing_error
    generator = robust_runner.PacedGenerator(
        genai.Client(api_key=api_key), model, sleep_seconds
    )
    successes = 0
    failures = 0
    hard_quota_exhausted = False
    existing_errors = robust_runner.read_markdown_sections(ERRORS_PATH)

    for snapshot in remaining:
        trajectory_id = str(snapshot["trajectory_id"])
        prompt = build_prompt(base_prompt, snapshot)
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
                    json.loads(raw), trajectory_id, int(snapshot["final_step_number"])
                )
                robust_runner.append_markdown(
                    RESPONSES_PATH,
                    trajectory_id,
                    json.dumps(validated, indent=2, ensure_ascii=False),
                )
                robust_runner.remove_markdown_section(ERRORS_PATH, trajectory_id)
                successes += 1
                last_error = None
                print(f"Rated {trajectory_id}")
                break
            except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
                last_error = error
                if attempt == 0:
                    print(f"Retrying {trajectory_id} after invalid JSON response")
                    continue
            except robust_runner.DailyQuotaExhausted as error:
                last_error = error
                hard_quota_exhausted = True
                break
            except Exception as error:
                last_error = error
                break

        if last_error is not None:
            error_body = (
                f"Error: {type(last_error).__name__}: {last_error}\n\n"
                + "\n\n--- Retry output ---\n\n".join(
                    output or "(empty output)" for output in raw_outputs
                )
            )
            if trajectory_id not in existing_errors:
                robust_runner.append_markdown(ERRORS_PATH, trajectory_id, error_body)
                existing_errors[trajectory_id] = error_body
            failures += 1
            print(f"ERROR {trajectory_id}: {type(last_error).__name__}: {last_error}")
        if hard_quota_exhausted:
            print("Daily quota or billing exhausted; stopping cleanly.")
            break

    processed = successes + failures
    print(f"Rows processed this run: {processed}")
    print(f"Successful JSON responses this run: {successes}")
    print(f"Errors this run: {failures}")
    print(f"Output path: {RESPONSES_PATH}")
    return 2 if hard_quota_exhausted else (0 if not failures else 1)


if __name__ == "__main__":
    raise SystemExit(main())


