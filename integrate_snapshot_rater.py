import csv
import json
import re
from pathlib import Path


RESPONSES_PATH = Path("data/snapshot_rater_responses.md")
CSV_PATH = Path("data/experiment0.csv")
FIELD_MAP = {
    "snapshot_crossing_present": "snapshot_crossing_present",
    "snapshot_crossing_step": "snapshot_crossing_step",
    "snapshot_reason": "snapshot_reason",
}


def sections(markdown):
    header = re.compile(r"(?m)^\\?##\s*([A-Za-z]+\d+)\s*$")
    matches = list(header.finditer(markdown))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        yield match.group(1), markdown[match.end():end]


def json_object(text):
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object found")
    decoder = json.JSONDecoder()
    cleaned = re.sub(r"\\([_\[\]])", r"\1", text[start:])
    value, _ = decoder.raw_decode(cleaned)
    return value


def normalized_id(value):
    match = re.fullmatch(r"([A-Za-z]+)0*(\d+)", value.strip())
    return (match.group(1).upper(), int(match.group(2))) if match else None


def serialize(value):
    if value is None:
        return ""
    return str(value)


def parse_bool(value):
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"invalid crossing_present value: {value!r}")


def parse_snapshot_label(value):
    if str(value).strip().lower() == "uncertain":
        return None
    return parse_bool(value)


def main():
    if not RESPONSES_PATH.exists():
        print(f"WARNING response file not found: {RESPONSES_PATH}")
        return

    markdown = RESPONSES_PATH.read_text(encoding="utf-8-sig")
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = reader.fieldnames

    by_id = {row["trajectory_id"]: row for row in rows}
    by_normalized = {}
    for trajectory_id in by_id:
        by_normalized.setdefault(normalized_id(trajectory_id), []).append(trajectory_id)

    updated = []
    malformed = []
    unmatched = []
    for header_id, body in sections(markdown):
        try:
            response = json_object(body)
            snapshot_present = parse_snapshot_label(
                response["snapshot_crossing_present"]
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            malformed.append(header_id)
            print(f"WARNING malformed response under {header_id}: {error}")
            continue

        candidates = by_normalized.get(normalized_id(header_id), [])
        if header_id in by_id:
            trajectory_id = header_id
        elif len(candidates) == 1:
            trajectory_id = candidates[0]
        else:
            unmatched.append(header_id)
            print(f"WARNING unmatched header trajectory ID: {header_id}")
            continue

        reason = response.get("snapshot_reason")
        if isinstance(reason, str):
            response["snapshot_reason"] = re.sub(
                r"\\?\[cite:\s*\d+\]", "", reason
            )

        row = by_id[trajectory_id]
        for response_field, csv_field in FIELD_MAP.items():
            if response_field in response:
                row[csv_field] = serialize(response[response_field])

        ground_truth_positive = parse_bool(row["ground_truth_crossing_present"])
        snapshot_step = response.get("snapshot_crossing_step")
        if ground_truth_positive and snapshot_present and snapshot_step is not None:
            row["lead_time_gain"] = serialize(
                float(row["ground_truth_crossing_step"]) - float(snapshot_step)
            )
        else:
            row["lead_time_gain"] = ""
        updated.append(trajectory_id)
        print(f"Updated {trajectory_id} from header {header_id}")

    with CSV_PATH.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Integrated: {len(updated)}")
    print(f"Malformed: {len(malformed)}")
    print(f"Unmatched: {len(unmatched)}")


if __name__ == "__main__":
    main()
