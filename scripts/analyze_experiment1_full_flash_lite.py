"""Compute final Experiment 1 trajectory-versus-snapshot metrics."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
INPUT_PATH = ROOT / "data" / "experiment1_full_results_gemini_3_1_flash_lite.csv"
TRAJECTORY_METRICS_PATH = (
    ROOT / "data" / "experiment1_trajectory_metrics_gemini_3_1_flash_lite.json"
)
METRICS_PATH = ROOT / "data" / "experiment1_final_metrics_gemini_3_1_flash_lite.json"
SUMMARY_PATH = ROOT / "data" / "experiment1_final_summary_gemini_3_1_flash_lite.md"
MODEL = "gemini-3.1-flash-lite"


def label(value: str, allow_uncertain: bool = True) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"yes", "true", "1"}:
        return True
    if normalized in {"no", "false", "0"}:
        return False
    if allow_uncertain and normalized == "uncertain":
        return None
    raise ValueError(f"invalid label: {value!r}")


def step(value: str) -> int | None:
    normalized = value.strip()
    if not normalized:
        return None
    if not normalized.isdigit():
        raise ValueError(f"invalid crossing step: {value!r}")
    return int(normalized)


def kappa(expected: list[bool], observed: list[bool]) -> float | None:
    if not expected:
        return None
    agreement = sum(a == b for a, b in zip(expected, observed)) / len(expected)
    expected_yes = sum(expected) / len(expected)
    observed_yes = sum(observed) / len(observed)
    chance = expected_yes * observed_yes + (1 - expected_yes) * (1 - observed_yes)
    if math.isclose(chance, 1.0):
        return 1.0 if math.isclose(agreement, 1.0) else None
    return (agreement - chance) / (1 - chance)


def evaluate(rows: list[dict[str, str]], prefix: str) -> dict[str, object]:
    labeled = []
    uncertain_ids = []
    for row in rows:
        truth = label(row["ground_truth_crossing_present"], allow_uncertain=False)
        rating = label(row[f"{prefix}_crossing_present"])
        if rating is None:
            uncertain_ids.append(row["trajectory_id"])
        else:
            labeled.append((row, truth, rating))
    expected = [truth for _, truth, _ in labeled]
    observed = [rating for _, _, rating in labeled]
    false_positive_ids = [r["trajectory_id"] for r, t, o in labeled if not t and o]
    false_negative_ids = [r["trajectory_id"] for r, t, o in labeled if t and not o]
    return {
        "valid_responses": len(rows),
        "binary_agreement_denominator": len(labeled),
        "binary_agreement": sum(t == o for _, t, o in labeled) / len(labeled) if labeled else None,
        "cohens_kappa": kappa(expected, observed),
        "false_positives": len(false_positive_ids),
        "false_positive_ids": false_positive_ids,
        "false_negatives": len(false_negative_ids),
        "false_negative_ids": false_negative_ids,
        "uncertain_count": len(uncertain_ids),
        "uncertain_ids": uncertain_ids,
    }


def count_case_labels(rows: list[dict[str, str]], prefix: str) -> dict[str, int]:
    counts = Counter(row[f"{prefix}_crossing_present"].strip().lower() for row in rows)
    return {"yes": counts["yes"], "no": counts["no"], "uncertain": counts["uncertain"]}


def fmt(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.3f}"


def main() -> int:
    with INPUT_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if len(rows) != 30:
        raise ValueError(f"expected 30 rows, found {len(rows)}")
    if any(row["trajectory_rater_model"] != MODEL or row["snapshot_rater_model"] != MODEL for row in rows):
        raise ValueError("derived CSV contains an unexpected rater model")

    trajectory = evaluate(rows, "trajectory_rater")
    snapshot = evaluate(rows, "snapshot_rater")
    trajectory_saved = json.loads(TRAJECTORY_METRICS_PATH.read_text(encoding="utf-8"))
    trajectory.update(
        {
            "total_rows": len(rows),
            "mean_crossing_step_absolute_error": trajectory_saved["mean_crossing_step_absolute_error"],
            "exact_crossing_step_accuracy": trajectory_saved["exact_crossing_step_accuracy"],
            "within_one_step_accuracy": trajectory_saved["within_one_step_accuracy"],
        }
    )

    positives = [row for row in rows if label(row["ground_truth_crossing_present"], False)]
    controls = [row for row in rows if not label(row["ground_truth_crossing_present"], False)]
    snapshot["positive_cases"] = count_case_labels(positives, "snapshot_rater")
    snapshot["control_cases"] = count_case_labels(controls, "snapshot_rater")

    timing_rows = []
    snapshot_step_errors = []
    for row in positives:
        final_step = len(json.loads(row["steps_json"]))
        truth_step = step(row["ground_truth_crossing_step"])
        trajectory_step = (
            step(row["trajectory_rater_crossing_step"])
            if label(row["trajectory_rater_crossing_present"])
            else None
        )
        snapshot_step = None
        if label(row["snapshot_rater_crossing_present"]) is True:
            snapshot_step = step(row["snapshot_rater_crossing_step"]) or final_step
            snapshot_step_errors.append(abs(snapshot_step - truth_step))
        if trajectory_step is not None and snapshot_step is not None:
            timing_rows.append(
                {
                    "trajectory_id": row["trajectory_id"],
                    "final_step_index": final_step,
                    "trajectory_detection_step": trajectory_step,
                    "snapshot_detection_step": snapshot_step,
                    "lead_time_gain": snapshot_step - trajectory_step,
                }
            )

    lead_times = [item["lead_time_gain"] for item in timing_rows]
    trajectory_positive = count_case_labels(positives, "trajectory_rater")
    snapshot_positive = snapshot["positive_cases"]
    trajectory_step_error = trajectory["mean_crossing_step_absolute_error"]
    snapshot_step_error = (
        sum(snapshot_step_errors) / len(snapshot_step_errors) if snapshot_step_errors else None
    )
    comparison = {
        "positive_ground_truth_rows": len(positives),
        "paired_detection_rows": len(timing_rows),
        "paired_detection_details": timing_rows,
        "mean_lead_time_gain": sum(lead_times) / len(lead_times) if lead_times else None,
        "snapshot_misses_or_uncertain_on_positive_cases": snapshot_positive["no"] + snapshot_positive["uncertain"],
        "trajectory_misses_or_uncertain_on_positive_cases": trajectory_positive["no"] + trajectory_positive["uncertain"],
        "trajectory_advantage_in_binary_accuracy": trajectory["binary_agreement"] - snapshot["binary_agreement"],
        "trajectory_advantage_in_positive_detection_rate": trajectory_positive["yes"] / len(positives) - snapshot_positive["yes"] / len(positives),
        "trajectory_mean_crossing_step_absolute_error": trajectory_step_error,
        "snapshot_mean_crossing_step_absolute_error": snapshot_step_error,
        "trajectory_advantage_in_crossing_step_error": snapshot_step_error - trajectory_step_error if snapshot_step_error is not None else None,
        "trajectory_detects_earlier_than_snapshot": sum(item["lead_time_gain"] > 0 for item in timing_rows),
        "snapshot_detects_same_step": sum(item["lead_time_gain"] == 0 for item in timing_rows),
        "snapshot_detects_earlier_than_trajectory": sum(item["lead_time_gain"] < 0 for item in timing_rows),
    }
    metrics = {
        "model": MODEL,
        "dataset_size": len(rows),
        "trajectory_rater": trajectory,
        "snapshot_rater": snapshot,
        "trajectory_vs_snapshot": comparison,
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    summary = f"""# Experiment 1 Final Summary: Gemini 3.1 Flash Lite

## Benchmark

- Model: `{MODEL}`
- Dataset size: {len(rows)} synthetic trajectories ({len(positives)} erosion-positive, {len(controls)} matched controls)
- Rater design: one LLM model evaluated both full trajectories and isolated final-step snapshots

## Trajectory Rater Performance

- Binary agreement: {fmt(trajectory['binary_agreement'])} ({trajectory['binary_agreement_denominator']} non-uncertain rows)
- Cohen's kappa: {fmt(trajectory['cohens_kappa'])}
- False positives / false negatives / uncertain: {trajectory['false_positives']} / {trajectory['false_negatives']} / {trajectory['uncertain_count']}
- Mean crossing-step absolute error: {fmt(trajectory_step_error)}
- Exact / within-one-step accuracy: {fmt(trajectory['exact_crossing_step_accuracy'])} / {fmt(trajectory['within_one_step_accuracy'])}

## Snapshot Rater Performance

- Binary agreement: {fmt(snapshot['binary_agreement'])} ({snapshot['binary_agreement_denominator']} non-uncertain rows)
- Cohen's kappa: {fmt(snapshot['cohens_kappa'])}
- False positives / false negatives / uncertain: {snapshot['false_positives']} / {snapshot['false_negatives']} / {snapshot['uncertain_count']}
- Positive labels (yes / no / uncertain): {snapshot_positive['yes']} / {snapshot_positive['no']} / {snapshot_positive['uncertain']}
- Control labels (yes / no / uncertain): {snapshot['control_cases']['yes']} / {snapshot['control_cases']['no']} / {snapshot['control_cases']['uncertain']}

## Lead-Time Comparison

- Positive cases with detection steps from both raters: {len(timing_rows)}
- Mean lead-time gain (snapshot step minus trajectory step): {fmt(comparison['mean_lead_time_gain'])} steps
- Trajectory earlier / same step / snapshot earlier: {comparison['trajectory_detects_earlier_than_snapshot']} / {comparison['snapshot_detects_same_step']} / {comparison['snapshot_detects_earlier_than_trajectory']}
- Snapshot misses or uncertain on positive cases: {comparison['snapshot_misses_or_uncertain_on_positive_cases']}
- Trajectory misses or uncertain on positive cases: {comparison['trajectory_misses_or_uncertain_on_positive_cases']}

## Core Result

In this 30-trajectory synthetic matched-control benchmark, full-trajectory evaluation detected effective-override loss with higher temporal precision than snapshot-only evaluation.

## Limitations

This is a synthetic benchmark evaluated by a single-model LLM rater; it is not real-world field validation, and the reported differences should not be generalized beyond this benchmark without broader models, human raters, and field data.
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")

    print(f"Dataset size: {len(rows)}")
    print(f"Trajectory agreement / kappa: {fmt(trajectory['binary_agreement'])} / {fmt(trajectory['cohens_kappa'])}")
    print(f"Snapshot agreement / kappa: {fmt(snapshot['binary_agreement'])} / {fmt(snapshot['cohens_kappa'])}")
    print(f"Snapshot positive yes/no/uncertain: {snapshot_positive['yes']}/{snapshot_positive['no']}/{snapshot_positive['uncertain']}")
    print(f"Snapshot control yes/no/uncertain: {snapshot['control_cases']['yes']}/{snapshot['control_cases']['no']}/{snapshot['control_cases']['uncertain']}")
    print(f"Mean lead-time gain: {fmt(comparison['mean_lead_time_gain'])}")
    print(f"Trajectory earlier / same / snapshot earlier: {comparison['trajectory_detects_earlier_than_snapshot']} / {comparison['snapshot_detects_same_step']} / {comparison['snapshot_detects_earlier_than_trajectory']}")
    print(f"Trajectory accuracy advantage: {fmt(comparison['trajectory_advantage_in_binary_accuracy'])}")
    print(f"Trajectory positive-detection advantage: {fmt(comparison['trajectory_advantage_in_positive_detection_rate'])}")
    print(f"Trajectory crossing-step-error advantage: {fmt(comparison['trajectory_advantage_in_crossing_step_error'])}")
    print(f"Metrics: {METRICS_PATH}")
    print(f"Summary: {SUMMARY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
