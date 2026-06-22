"""Generate final-step-only snapshot ratings with the Gemini API."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).parent
CSV_PATH = ROOT / "data" / "experiment0.csv"
PROMPT_PATH = ROOT / "prompts" / "snapshot_rater_prompt.md"
RESPONSES_PATH = ROOT / "data" / "snapshot_rater_responses.md"
ERRORS_PATH = ROOT / "data" / "snapshot_rater_errors.md"
DEFAULT_MODEL = "gemini-3.5-flash"

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
    "required": [
        "trajectory_id",
        "snapshot_crossing_present",
        "snapshot_crossing_step",
        "snapshot_reason",
        "confidence",
    ],
    "additionalProperties": False,
}


def display_id(trajectory_id: str) -> str:
    match = re.fullmatch(r"([A-Za-z]+)0*(\d+)", trajectory_id.strip())
    return f"{match.group(1).upper()}{int(match.group(2))}" if match else trajectory_id


def load_snapshots() -> list[dict[str, object]]:
    snapshots = []
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            steps = json.loads(row["steps_json"])
            if not isinstance(steps, list) or not steps:
                raise ValueError(f"{row['trajectory_id']}: steps_json must be a nonempty list")
            snapshots.append(
                {
                    "trajectory_id": row["trajectory_id"],
                    "final_step_number": len(steps),
                    "final_step": str(steps[-1]),
                }
            )
    return snapshots


def build_prompt(base_prompt: str, snapshot: dict[str, object]) -> str:
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
    missing = set(RESPONSE_SCHEMA["required"]) - value.keys()
    if missing:
        raise ValueError(f"missing required fields: {sorted(missing)}")
    if display_id(str(value["trajectory_id"])) != display_id(expected_id):
        raise ValueError(f"trajectory_id does not match requested ID {expected_id}")
    label = str(value["snapshot_crossing_present"]).lower()
    if label not in {"yes", "no", "uncertain"}:
        raise ValueError("snapshot_crossing_present must be yes, no, or uncertain")
    step = value["snapshot_crossing_step"]
    if label == "yes":
        if not isinstance(step, int) or isinstance(step, bool):
            raise ValueError("positive snapshot_crossing_step must be an integer")
        if step != final_step_number:
            raise ValueError("positive snapshot_crossing_step must equal final step number")
    elif step is not None:
        raise ValueError("no/uncertain snapshot_crossing_step must be null")
    if not isinstance(value["snapshot_reason"], str):
        raise ValueError("snapshot_reason must be a string")
    confidence = value["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("confidence must be a number")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return value


def write_markdown(path: Path, entries: list[tuple[str, str]]) -> None:
    content = "".join(f"## {display_id(identifier)}\n\n{body.strip()}\n\n" for identifier, body in entries)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="validate inputs without API calls")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    snapshots = load_snapshots()
    base_prompt = PROMPT_PATH.read_text(encoding="utf-8-sig")
    prompts = [build_prompt(base_prompt, snapshot) for snapshot in snapshots]
    api_key = os.getenv("GEMINI_API_KEY")

    if args.dry_run or not api_key:
        reason = "--dry-run requested" if args.dry_run else "GEMINI_API_KEY is not set"
        print(f"Dry run: {reason}; no API calls made.")
        print(f"Validated final-step-only prompts: {len(prompts)}")
        return 0

    from google import genai

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    client = genai.Client(api_key=api_key)
    successes: list[tuple[str, str]] = []
    errors: list[tuple[str, str]] = []

    for snapshot, prompt in zip(snapshots, prompts):
        trajectory_id = str(snapshot["trajectory_id"])
        raw_output = ""
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": RESPONSE_SCHEMA,
                },
            )
            raw_output = response.text or ""
            parsed = json.loads(raw_output)
            validated = validate_response(
                parsed, trajectory_id, int(snapshot["final_step_number"])
            )
            successes.append((trajectory_id, json.dumps(validated, indent=2)))
            print(f"Rated {trajectory_id}")
        except Exception as error:  # Continue after API, transport, and response errors.
            error_body = f"Error: {type(error).__name__}: {error}\n\nRaw output:\n{raw_output or '(none)'}"
            errors.append((trajectory_id, error_body))
            print(f"ERROR {trajectory_id}: {type(error).__name__}: {error}")

    write_markdown(RESPONSES_PATH, successes)
    if errors:
        write_markdown(ERRORS_PATH, errors)
    elif ERRORS_PATH.exists():
        ERRORS_PATH.unlink()

    print(f"Total trajectories processed: {len(snapshots)}")
    print(f"Successful JSON responses: {len(successes)}")
    print(f"Errors: {len(errors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
