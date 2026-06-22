"""Print read-only diagnostics for trajectory and final-step snapshot ratings."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).parent / "data" / "experiment0.csv"


def says_yes(value: object) -> bool:
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


def optional_step(value: object) -> int | None:
    if pd.isna(value) or str(value).strip() == "":
        return None
    return int(float(value))


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    rows = []

    for _, source in data.iterrows():
        final_step_number = len(json.loads(source["steps_json"]))
        trajectory_present = says_yes(source["blind_rater_crossing_present"])
        snapshot_present = says_yes(source["snapshot_crossing_present"])
        trajectory_detection_step = (
            optional_step(source["blind_rater_crossing_step"])
            if trajectory_present
            else None
        )
        snapshot_detection_step = final_step_number if snapshot_present else None
        lead_time_gain = (
            snapshot_detection_step - trajectory_detection_step
            if snapshot_detection_step is not None
            and trajectory_detection_step is not None
            else None
        )

        rows.append(
            {
                "trajectory_id": source["trajectory_id"],
                "condition": source["condition"],
                "ground_truth_crossing_present": source[
                    "ground_truth_crossing_present"
                ],
                "ground_truth_crossing_step": optional_step(
                    source["ground_truth_crossing_step"]
                ),
                "trajectory_rater_crossing_present": source[
                    "blind_rater_crossing_present"
                ],
                "trajectory_rater_crossing_step": optional_step(
                    source["blind_rater_crossing_step"]
                ),
                "snapshot_crossing_present": source["snapshot_crossing_present"],
                "snapshot_crossing_step": optional_step(
                    source["snapshot_crossing_step"]
                ),
                "final_step_number": final_step_number,
                "snapshot_detection_step": snapshot_detection_step,
                "trajectory_detection_step": trajectory_detection_step,
                "lead_time_gain": lead_time_gain,
            }
        )

    print(pd.DataFrame(rows).to_string(index=False, na_rep=""))


if __name__ == "__main__":
    main()
