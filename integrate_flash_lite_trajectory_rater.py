"""Integrate official Flash Lite trajectory ratings into Experiment 1."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
SOURCE_PATH = ROOT / "data" / "experiment1.csv"
RESPONSES_PATH = (
    ROOT
    / "data"
    / "experiment1_trajectory_rater_responses_gemini_3_1_flash_lite.md"
)
OUTPUT_PATH = (
    ROOT
    / "data"
    / "experiment1_with_trajectory_rater_gemini_3_1_flash_lite.csv"
)
MODEL = "gemini-3.1-flash-lite"
EXPECTED_COUNT = 30

RESPONSE_FIELDS = (
    "trajectory_id",
    "crossing_present",
    "crossing_step",
    "state_sequence",
    "override_attempt",
    "system_structure",
    "downstream_constraint",
    "reason",
    "confidence",
)
OUTPUT_FIELDS = (
    "trajectory_rater_model",
    "trajectory_rater_crossing_present",
    "trajectory_rater_crossing_step",
    "trajectory_rater_state_sequence",
    "trajectory_rater_override_attempt",
    "trajectory_rater_system_structure",
    "trajectory_rater_downstream_constraint",
    "trajectory_rater_reason",
    "trajectory_rater_confidence",
)
HEADER = re.compile(r"(?m)^##\s+([A-Za-z0-9_-]+)\s*$")


def read_sections(path: Path) -> list[tuple[str, str]]:
    content = path.read_text(encoding="utf-8-sig")
    matches = list(HEADER.finditer(content))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        sections.append((match.group(1), content[match.end():end].strip()))
    return sections


def validate_response(response: object, header_id: str, step_count: int) -> dict:
    if not isinstance(response, dict):
        raise ValueError(f"{header_id}: response must be a JSON object")
    if set(response) != set(RESPONSE_FIELDS):
        missing = sorted(set(RESPONSE_FIELDS) - set(response))
        extra = sorted(set(response) - set(RESPONSE_FIELDS))
        raise ValueError(f"{header_id}: response fields mismatch; missing={missing}, extra={extra}")
    if response["trajectory_id"] != header_id:
        raise ValueError(f"{header_id}: JSON trajectory_id does not match header")

    label = response["crossing_present"]
    if label not in {"yes", "no", "uncertain"}:
        raise ValueError(f"{header_id}: invalid crossing_present {label!r}")
    crossing_step = response["crossing_step"]
    if label == "yes":
        if isinstance(crossing_step, bool) or not isinstance(crossing_step, int):
            raise ValueError(f"{header_id}: yes requires an integer crossing_step")
        if not 1 <= crossing_step <= step_count:
            raise ValueError(f"{header_id}: crossing_step is outside the trajectory")
    elif crossing_step is not None:
        raise ValueError(f"{header_id}: no/uncertain requires crossing_step=null")

    states = response["state_sequence"]
    if not isinstance(states, list) or len(states) != step_count:
        raise ValueError(f"{header_id}: state_sequence must have {step_count} entries")
    if any(isinstance(state, bool) or state not in {0, 1, 2, 3} for state in states):
        raise ValueError(f"{header_id}: state_sequence contains an invalid state")
    if label == "yes":
        if states[crossing_step - 1] != 3:
            raise ValueError(f"{header_id}: crossing_step must identify state 3")
        if states.index(3) + 1 != crossing_step:
            raise ValueError(f"{header_id}: crossing_step must be the first state 3")
    elif 3 in states:
        raise ValueError(f"{header_id}: no/uncertain response cannot contain state 3")
    for field in ("override_attempt", "system_structure", "downstream_constraint", "reason"):
        if not isinstance(response[field], str):
            raise ValueError(f"{header_id}: {field} must be a string")
    confidence = response["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError(f"{header_id}: confidence must be numeric")
    if not 0 <= confidence <= 1:
        raise ValueError(f"{header_id}: confidence must be between 0 and 1")
    return response


def serialize(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def main() -> int:
    with SOURCE_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    if len(rows) != EXPECTED_COUNT:
        raise ValueError(f"expected {EXPECTED_COUNT} source rows, found {len(rows)}")

    source_ids = [row["trajectory_id"] for row in rows]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("source CSV contains duplicate trajectory_id values")
    steps_by_id = {row["trajectory_id"]: json.loads(row["steps_json"]) for row in rows}

    sections = read_sections(RESPONSES_PATH)
    section_ids = [trajectory_id for trajectory_id, _ in sections]
    duplicates = sorted({item for item in section_ids if section_ids.count(item) > 1})
    if duplicates:
        raise ValueError(f"duplicate response trajectory_id values: {duplicates}")
    if len(sections) != EXPECTED_COUNT:
        raise ValueError(f"expected {EXPECTED_COUNT} response sections, found {len(sections)}")
    if set(section_ids) != set(source_ids):
        missing = sorted(set(source_ids) - set(section_ids))
        extra = sorted(set(section_ids) - set(source_ids))
        raise ValueError(f"response ID mismatch; missing={missing}, extra={extra}")

    responses = {}
    for trajectory_id, body in sections:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as error:
            raise ValueError(f"{trajectory_id}: invalid JSON: {error}") from error
        responses[trajectory_id] = validate_response(
            parsed, trajectory_id, len(steps_by_id[trajectory_id])
        )

    for row in rows:
        response = responses[row["trajectory_id"]]
        row["trajectory_rater_model"] = MODEL
        for response_field, output_field in zip(RESPONSE_FIELDS[1:], OUTPUT_FIELDS[1:]):
            row[output_field] = serialize(response[response_field])

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(
            destination, fieldnames=fieldnames + list(OUTPUT_FIELDS), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Source rows: {len(rows)}")
    print(f"Valid responses: {len(responses)}")
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
