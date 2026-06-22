"""Inspect Experiment 1 trajectory-rater completion without changing responses."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
DATA_PATH = ROOT / "data" / "experiment1.csv"
RESPONSES_PATH = ROOT / "data" / "experiment1_trajectory_rater_responses.md"
MISSING_PATH = ROOT / "data" / "experiment1_missing_trajectory_ids.txt"


def completed_ids() -> set[str]:
    if not RESPONSES_PATH.exists():
        return set()
    content = RESPONSES_PATH.read_text(encoding="utf-8-sig")
    header = re.compile(r"(?m)^##\s+([A-Za-z0-9_-]+)\s*$")
    matches = list(header.finditer(content))
    completed = set()
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        body = content[match.end():end].strip()
        try:
            response = json.loads(body)
        except json.JSONDecodeError:
            continue
        trajectory_id = match.group(1)
        if isinstance(response, dict) and response.get("trajectory_id") == trajectory_id:
            completed.add(trajectory_id)
    return completed


def main() -> None:
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        all_ids = [row["trajectory_id"] for row in csv.DictReader(source)]

    completed = completed_ids()
    missing = [trajectory_id for trajectory_id in all_ids if trajectory_id not in completed]
    MISSING_PATH.write_text(
        "".join(f"{trajectory_id}\n" for trajectory_id in missing),
        encoding="utf-8",
    )

    print(f"Total trajectories: {len(all_ids)}")
    print(f"Completed trajectories: {len(all_ids) - len(missing)}")
    print(f"Missing trajectories: {len(missing)}")
    print(f"Missing ID list: {', '.join(missing) if missing else 'None'}")


if __name__ == "__main__":
    main()
