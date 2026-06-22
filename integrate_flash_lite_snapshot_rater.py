"""Integrate official Flash Lite snapshot ratings into Experiment 1 results."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
SOURCE_PATH = ROOT / "data" / "experiment1.csv"
TRAJECTORY_RESULTS_PATH = (
    ROOT / "data" / "experiment1_with_trajectory_rater_gemini_3_1_flash_lite.csv"
)
RESPONSES_PATH = (
    ROOT / "data" / "experiment1_snapshot_rater_responses_gemini_3_1_flash_lite.md"
)
OUTPUT_PATH = ROOT / "data" / "experiment1_full_results_gemini_3_1_flash_lite.csv"
MODEL = "gemini-3.1-flash-lite"
EXPECTED_COUNT = 30
RESPONSE_FIELDS = {
    "trajectory_id",
    "snapshot_crossing_present",
    "snapshot_crossing_step",
    "snapshot_reason",
    "confidence",
}
OUTPUT_FIELDS = (
    "snapshot_rater_model",
    "snapshot_rater_crossing_present",
    "snapshot_rater_crossing_step",
    "snapshot_rater_reason",
    "snapshot_rater_confidence",
)
HEADER = re.compile(r"(?m)^##\s+([A-Za-z0-9_-]+)\s*$")


def read_sections() -> list[tuple[str, str]]:
    content = RESPONSES_PATH.read_text(encoding="utf-8-sig")
    matches = list(HEADER.finditer(content))
    return [
        (
            match.group(1),
            content[
                match.end() : matches[index + 1].start()
                if index + 1 < len(matches)
                else len(content)
            ].strip(),
        )
        for index, match in enumerate(matches)
    ]


def validate_response(value: object, trajectory_id: str, final_step: int) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{trajectory_id}: response is not an object")
    if set(value) != RESPONSE_FIELDS:
        missing = sorted(RESPONSE_FIELDS - set(value))
        extra = sorted(set(value) - RESPONSE_FIELDS)
        raise ValueError(f"{trajectory_id}: field mismatch; missing={missing}, extra={extra}")
    if value["trajectory_id"] != trajectory_id:
        raise ValueError(f"{trajectory_id}: JSON trajectory_id differs from header")
    label = value["snapshot_crossing_present"]
    if label not in {"yes", "no", "uncertain"}:
        raise ValueError(f"{trajectory_id}: invalid snapshot label {label!r}")
    step = value["snapshot_crossing_step"]
    if label == "yes":
        if step is not None and (isinstance(step, bool) or not isinstance(step, int)):
            raise ValueError(f"{trajectory_id}: snapshot step must be integer or null")
        if isinstance(step, int) and step != final_step:
            raise ValueError(f"{trajectory_id}: snapshot step must equal final step {final_step}")
    elif step is not None:
        raise ValueError(f"{trajectory_id}: no/uncertain requires null snapshot step")
    if not isinstance(value["snapshot_reason"], str):
        raise ValueError(f"{trajectory_id}: snapshot_reason must be a string")
    confidence = value["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError(f"{trajectory_id}: confidence must be numeric")
    if not 0 <= confidence <= 1:
        raise ValueError(f"{trajectory_id}: confidence must be between 0 and 1")
    return value


def serialize(value: object) -> str:
    return "" if value is None else str(value)


def main() -> int:
    with SOURCE_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        source_rows = list(csv.DictReader(source))
    with TRAJECTORY_RESULTS_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    if len(source_rows) != EXPECTED_COUNT or len(rows) != EXPECTED_COUNT:
        raise ValueError(
            f"expected {EXPECTED_COUNT} source/trajectory rows; "
            f"found {len(source_rows)}/{len(rows)}"
        )
    source_ids = [row["trajectory_id"] for row in source_rows]
    result_ids = [row["trajectory_id"] for row in rows]
    if len(source_ids) != len(set(source_ids)) or len(result_ids) != len(set(result_ids)):
        raise ValueError("source or trajectory results contain duplicate trajectory IDs")
    if set(source_ids) != set(result_ids):
        raise ValueError("trajectory result IDs do not match experiment1.csv")
    step_counts = {
        row["trajectory_id"]: len(json.loads(row["steps_json"])) for row in source_rows
    }

    sections = read_sections()
    section_ids = [trajectory_id for trajectory_id, _ in sections]
    duplicates = sorted({item for item in section_ids if section_ids.count(item) > 1})
    if duplicates:
        raise ValueError(f"duplicate snapshot responses: {duplicates}")
    if len(sections) != EXPECTED_COUNT:
        raise ValueError(f"expected {EXPECTED_COUNT} snapshot responses, found {len(sections)}")
    if set(section_ids) != set(source_ids):
        missing = sorted(set(source_ids) - set(section_ids))
        extra = sorted(set(section_ids) - set(source_ids))
        raise ValueError(f"snapshot ID mismatch; missing={missing}, extra={extra}")

    responses = {}
    for trajectory_id, body in sections:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as error:
            raise ValueError(f"{trajectory_id}: invalid JSON: {error}") from error
        responses[trajectory_id] = validate_response(
            parsed, trajectory_id, step_counts[trajectory_id]
        )

    if any(field in fieldnames for field in OUTPUT_FIELDS):
        raise ValueError("trajectory results already contain snapshot output columns")
    for row in rows:
        response = responses[row["trajectory_id"]]
        row["snapshot_rater_model"] = MODEL
        row["snapshot_rater_crossing_present"] = response["snapshot_crossing_present"]
        row["snapshot_rater_crossing_step"] = serialize(response["snapshot_crossing_step"])
        row["snapshot_rater_reason"] = response["snapshot_reason"]
        row["snapshot_rater_confidence"] = serialize(response["confidence"])

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(
            destination, fieldnames=fieldnames + list(OUTPUT_FIELDS), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Source rows: {len(source_rows)}")
    print(f"Valid snapshot responses: {len(responses)}")
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
