"""Compute trajectory-only metrics for Experiment 1 Flash Lite ratings."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
INPUT_PATH = (
    ROOT / "data" / "experiment1_with_trajectory_rater_gemini_3_1_flash_lite.csv"
)
OUTPUT_PATH = (
    ROOT / "data" / "experiment1_trajectory_metrics_gemini_3_1_flash_lite.json"
)
MODEL = "gemini-3.1-flash-lite"


def parse_binary(value: str, *, allow_uncertain: bool) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"yes", "true", "1"}:
        return True
    if normalized in {"no", "false", "0"}:
        return False
    if allow_uncertain and normalized == "uncertain":
        return None
    raise ValueError(f"invalid binary label: {value!r}")


def parse_step(value: str) -> int | None:
    normalized = value.strip()
    if not normalized:
        return None
    if not normalized.isdigit():
        raise ValueError(f"invalid crossing step: {value!r}")
    return int(normalized)


def cohen_kappa(expected: list[bool], observed: list[bool]) -> float | None:
    if not expected:
        return None
    agreement = sum(left == right for left, right in zip(expected, observed)) / len(expected)
    expected_yes = sum(expected) / len(expected)
    observed_yes = sum(observed) / len(observed)
    chance = expected_yes * observed_yes + (1 - expected_yes) * (1 - observed_yes)
    if math.isclose(chance, 1.0):
        return 1.0 if math.isclose(agreement, 1.0) else None
    return (agreement - chance) / (1 - chance)


def main() -> int:
    with INPUT_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))

    valid_responses = sum(
        row.get("trajectory_rater_model") == MODEL
        and row.get("trajectory_rater_crossing_present", "").strip().lower()
        in {"yes", "no", "uncertain"}
        for row in rows
    )
    binary_rows = []
    uncertain_ids = []
    for row in rows:
        truth = parse_binary(row["ground_truth_crossing_present"], allow_uncertain=False)
        rating = parse_binary(row["trajectory_rater_crossing_present"], allow_uncertain=True)
        if rating is None:
            uncertain_ids.append(row["trajectory_id"])
        else:
            binary_rows.append((row, truth, rating))

    expected = [truth for _, truth, _ in binary_rows]
    observed = [rating for _, _, rating in binary_rows]
    agreement = (
        sum(truth == rating for _, truth, rating in binary_rows) / len(binary_rows)
        if binary_rows
        else None
    )
    false_positive_ids = [
        row["trajectory_id"] for row, truth, rating in binary_rows if not truth and rating
    ]
    false_negative_ids = [
        row["trajectory_id"] for row, truth, rating in binary_rows if truth and not rating
    ]

    step_pairs = []
    for row in rows:
        truth_step = parse_step(row["ground_truth_crossing_step"])
        rating_step = parse_step(row["trajectory_rater_crossing_step"])
        if truth_step is not None and rating_step is not None:
            step_pairs.append((truth_step, rating_step))
    errors = [abs(truth - rating) for truth, rating in step_pairs]

    per_condition = {}
    for condition in sorted({row["condition"] for row in rows}):
        condition_rows = [row for row in rows if row["condition"] == condition]
        labels = Counter(row["trajectory_rater_crossing_present"].strip().lower() for row in condition_rows)
        per_condition[condition] = {
            "total": len(condition_rows),
            "yes": labels["yes"],
            "no": labels["no"],
            "uncertain": labels["uncertain"],
        }

    metrics = {
        "model": MODEL,
        "total_rows": len(rows),
        "valid_trajectory_rater_responses": valid_responses,
        "binary_agreement_denominator": len(binary_rows),
        "binary_agreement": agreement,
        "cohens_kappa": cohen_kappa(expected, observed),
        "false_positives": len(false_positive_ids),
        "false_positive_ids": false_positive_ids,
        "false_negatives": len(false_negative_ids),
        "false_negative_ids": false_negative_ids,
        "uncertain_count": len(uncertain_ids),
        "uncertain_ids": uncertain_ids,
        "crossing_step_comparison_count": len(step_pairs),
        "mean_crossing_step_absolute_error": sum(errors) / len(errors) if errors else None,
        "within_one_step_accuracy": sum(error <= 1 for error in errors) / len(errors) if errors else None,
        "exact_crossing_step_accuracy": sum(error == 0 for error in errors) / len(errors) if errors else None,
        "per_condition_counts": per_condition,
    }
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    print(f"Total rows: {metrics['total_rows']}")
    print(f"Valid trajectory rater responses: {valid_responses}")
    print(f"Binary agreement: {agreement:.3f} ({len(binary_rows)} rows)" if agreement is not None else "Binary agreement: N/A")
    kappa = metrics["cohens_kappa"]
    print(f"Cohen's kappa: {kappa:.3f}" if kappa is not None else "Cohen's kappa: N/A")
    print(f"False positives: {len(false_positive_ids)} {false_positive_ids}")
    print(f"False negatives: {len(false_negative_ids)} {false_negative_ids}")
    print(f"Uncertain count: {len(uncertain_ids)}")
    mean_error = metrics["mean_crossing_step_absolute_error"]
    print(f"Mean crossing step absolute error: {mean_error:.3f}" if mean_error is not None else "Mean crossing step absolute error: N/A")
    within_one = metrics["within_one_step_accuracy"]
    print(f"Within-one-step accuracy: {within_one:.3f}" if within_one is not None else "Within-one-step accuracy: N/A")
    exact = metrics["exact_crossing_step_accuracy"]
    print(f"Exact crossing-step accuracy: {exact:.3f}" if exact is not None else "Exact crossing-step accuracy: N/A")
    print(f"Per-condition counts: {json.dumps(per_condition, sort_keys=True)}")
    print(f"Metrics output: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
