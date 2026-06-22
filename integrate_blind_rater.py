import csv
import json
import re
from pathlib import Path


RESPONSES_PATH = Path("data/blind_rater_responses.md")
CSV_PATH = Path("data/experiment0.csv")

FIELD_MAP = {
    "crossing_present": "blind_rater_crossing_present",
    "crossing_step": "blind_rater_crossing_step",
    "reason": "blind_rater_reason",
    "state_sequence": "blind_rater_state_sequence",
    "confidence": "blind_rater_confidence",
    "override_attempt": "blind_rater_override_attempt",
    "system_structure": "blind_rater_system_structure",
    "downstream_constraint": "blind_rater_downstream_constraint",
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

    in_string = False
    escaped = False
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise ValueError("unterminated JSON object")


def parse_response(text):
    # Gemini's rendered Markdown escaped JSON punctuation in this export.
    cleaned = re.sub(r"\\([_\[\]])", r"\1", json_object(text))
    return json.loads(cleaned)


def normalized_id(value):
    match = re.fullmatch(r"([A-Za-z]+)0*(\d+)", value.strip())
    if not match:
        return None
    return match.group(1).upper(), int(match.group(2))


def serialize(value):
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def main():
    markdown = RESPONSES_PATH.read_text(encoding="utf-8-sig")
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = reader.fieldnames

    by_id = {row["trajectory_id"]: row for row in rows}
    by_normalized = {}
    for trajectory_id in by_id:
        key = normalized_id(trajectory_id)
        if key is not None:
            by_normalized.setdefault(key, []).append(trajectory_id)

    updated = []
    malformed = []
    unmatched = []
    found_sections = list(sections(markdown))
    for header_id, body in found_sections:
        try:
            response = parse_response(body)
        except (ValueError, json.JSONDecodeError) as error:
            malformed.append((header_id, str(error)))
            print(f"WARNING malformed response under {header_id}: {error}")
            continue

        # The header is authoritative. Normalization only bridges T1 to CSV ID T01.
        candidates = by_normalized.get(normalized_id(header_id), [])
        if header_id in by_id:
            trajectory_id = header_id
        elif len(candidates) == 1:
            trajectory_id = candidates[0]
        else:
            unmatched.append(header_id)
            print(f"WARNING unmatched header trajectory ID: {header_id}")
            continue

        reason = response.get("reason")
        if isinstance(reason, str):
            response["reason"] = re.sub(r"\\?\[cite:\s*\d+\]", "", reason)

        row = by_id[trajectory_id]
        for response_field, csv_field in FIELD_MAP.items():
            if csv_field in fieldnames and response_field in response:
                row[csv_field] = serialize(response[response_field])
        updated.append(trajectory_id)
        print(f"Updated {trajectory_id} from header {header_id}")

    with CSV_PATH.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Integrated: {len(updated)}")
    print(f"Malformed: {len(malformed)}")
    print(f"Unmatched: {len(unmatched)}")
    if not found_sections:
        print("WARNING no response sections found")


if __name__ == "__main__":
    main()
