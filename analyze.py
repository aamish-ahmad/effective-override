"""Analyze trajectory and snapshot rater labels against ground truth."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scorer import binary_agreement, cohen_kappa_binary, crossing_step_error, within_one_step


DATA_PATH = Path(__file__).parent / "data" / "experiment0.csv"


def parse_optional_bool(value: object) -> bool | None:
    if pd.isna(value) or str(value).strip().lower() in {"", "uncertain"}:
        return None
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"Invalid boolean label: {value!r}")


def format_metric(value: float) -> str:
    return "N/A" if pd.isna(value) else f"{value:.3f}"


def evaluate_rater(data: pd.DataFrame, rater: str, step_column: str) -> dict[str, object]:
    labeled = data[data[rater].notna()].copy()
    expected = labeled["ground_truth"].tolist()
    observed = labeled[rater].tolist()
    true_positive = labeled[
        (labeled["ground_truth"] == True) & (labeled[rater] == True)  # noqa: E712
    ]
    expected_steps = true_positive["ground_truth_crossing_step"].tolist()
    observed_steps = true_positive[step_column].tolist()
    false_positives = labeled[
        (labeled["ground_truth"] == False) & (labeled[rater] == True)  # noqa: E712
    ]["trajectory_id"].tolist()
    false_negatives = labeled[
        (labeled["ground_truth"] == True) & (labeled[rater] == False)  # noqa: E712
    ]["trajectory_id"].tolist()
    return {
        "count": len(labeled),
        "agreement": binary_agreement(expected, observed),
        "kappa": cohen_kappa_binary(expected, observed),
        "step_error": crossing_step_error(expected_steps, observed_steps),
        "within_one": within_one_step(expected_steps, observed_steps),
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


def print_evaluation(label: str, result: dict[str, object], total: int) -> None:
    print(f"{label}:")
    print(f"  Labeled trajectories: {result['count']}/{total}")
    print(f"  Binary agreement: {format_metric(result['agreement'])}")
    print(f"  Cohen's kappa: {format_metric(result['kappa'])}")
    print(f"  Mean crossing step error: {format_metric(result['step_error'])}")
    print(f"  Within-one-step accuracy: {format_metric(result['within_one'])}")
    print(f"  False positives: {result['false_positives'] or 'None'}")
    print(f"  False negatives: {result['false_negatives'] or 'None'}")


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    data["ground_truth"] = data["ground_truth_crossing_present"].map(parse_optional_bool)
    data["trajectory_rater"] = data["blind_rater_crossing_present"].map(parse_optional_bool)
    data["snapshot_rater"] = data["snapshot_crossing_present"].map(parse_optional_bool)

    trajectory_result = evaluate_rater(
        data, "trajectory_rater", "blind_rater_crossing_step"
    )
    snapshot_result = evaluate_rater(data, "snapshot_rater", "snapshot_crossing_step")

    paired_positive = data[
        (data["trajectory_rater"] == True) & (data["snapshot_rater"] == True)  # noqa: E712
    ]
    trajectory_snapshot_step_error = crossing_step_error(
        paired_positive["blind_rater_crossing_step"],
        paired_positive["snapshot_crossing_step"],
    )
    positive_cases = data[data["ground_truth"] == True]  # noqa: E712
    snapshot_uncertain_on_positive = int(
        positive_cases["snapshot_crossing_present"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("uncertain")
        .sum()
    )
    lead_time_gains = []
    detected_positive_cases = positive_cases[
        (positive_cases["trajectory_rater"] == True)  # noqa: E712
        & (positive_cases["snapshot_rater"] == True)  # noqa: E712
        & positive_cases["blind_rater_crossing_step"].notna()
    ]
    for _, row in detected_positive_cases.iterrows():
        final_step_number = len(json.loads(row["steps_json"]))
        trajectory_detection_step = float(row["blind_rater_crossing_step"])
        lead_time_gains.append(final_step_number - trajectory_detection_step)
    mean_lead_time_gain = (
        pd.Series(lead_time_gains, dtype="float64").mean()
        if lead_time_gains
        else float("nan")
    )

    positives_found = int(((data["ground_truth"] == True) & (data["trajectory_rater"] == True)).sum())  # noqa: E712
    controls_rejected = int(((data["ground_truth"] == False) & (data["trajectory_rater"] == False)).sum())  # noqa: E712
    true_positive = data[(data["ground_truth"] == True) & (data["trajectory_rater"] == True)]  # noqa: E712
    expected_steps = true_positive["ground_truth_crossing_step"].tolist()
    observed_steps = true_positive["blind_rater_crossing_step"].tolist()
    close_positive_steps = sum(
        abs(expected_step - observed_step) <= 1
        for expected_step, observed_step in zip(expected_steps, observed_steps)
        if not pd.isna(expected_step) and not pd.isna(observed_step)
    )
    passed = positives_found >= 2 and controls_rejected >= 2 and close_positive_steps >= 2

    print_evaluation("Ground truth vs trajectory rater", trajectory_result, len(data))
    print_evaluation("Ground truth vs snapshot rater", snapshot_result, len(data))
    print(
        "Trajectory vs snapshot mean crossing step error: "
        f"{format_metric(trajectory_snapshot_step_error)}"
    )
    print(f"Mean lead-time gain on positive cases: {format_metric(mean_lead_time_gain)}")
    print(
        "Snapshot uncertain on positive cases: "
        f"{snapshot_uncertain_on_positive}"
    )
    print(f"Trajectory rater pass/fail gate: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
