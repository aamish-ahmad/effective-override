"""Compute trajectory-only metrics for Experiment 2 hard controls."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
INPUT_PATH = (
    ROOT / "data" / "experiment2_with_trajectory_rater_gemini_3_1_flash_lite.csv"
)
OUTPUT_PATH = (
    ROOT / "data" / "experiment2_trajectory_metrics_gemini_3_1_flash_lite.json"
)
MODEL = "gemini-3.1-flash-lite"


def parse_label(value: str, *, allow_uncertain: bool) -> bool | None:
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


def response_is_valid(row: dict[str, str]) -> bool:
    try:
        if row["trajectory_rater_model"] != MODEL:
            return False
        rating = row["trajectory_rater_crossing_present"].strip().lower()
        if rating not in {"yes", "no", "uncertain"}:
            return False
        states = json.loads(row["trajectory_rater_state_sequence"])
        steps = json.loads(row["steps_json"])
        if not isinstance(states, list) or len(states) != len(steps):
            return False
        if any(isinstance(state, bool) or state not in {0, 1, 2, 3} for state in states):
            return False
        crossing_step = parse_step(row["trajectory_rater_crossing_step"])
        if rating == "yes" and crossing_step is None:
            return False
        if rating != "yes" and crossing_step is not None:
            return False
        confidence = float(row["trajectory_rater_confidence"])
        if not 0 <= confidence <= 1:
            return False
        return all(
            row[field] != ""
            for field in (
                "trajectory_rater_override_attempt",
                "trajectory_rater_system_structure",
                "trajectory_rater_downstream_constraint",
                "trajectory_rater_reason",
            )
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False


def case_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    labels = Counter(row["trajectory_rater_crossing_present"].strip().lower() for row in rows)
    return {key: labels[key] for key in ("yes", "no", "uncertain")}


def evaluate_group(rows: list[dict[str, str]]) -> dict[str, object]:
    binary = []
    uncertain_ids = []
    false_positive_ids = []
    false_negative_ids = []
    for row in rows:
        truth = parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)
        rating = parse_label(row["trajectory_rater_crossing_present"], allow_uncertain=True)
        if rating is None:
            uncertain_ids.append(row["trajectory_id"])
            continue
        binary.append((truth, rating))
        if not truth and rating:
            false_positive_ids.append(row["trajectory_id"])
        elif truth and not rating:
            false_negative_ids.append(row["trajectory_id"])
    correct = sum(truth == rating for truth, rating in binary)
    failure_ids = false_positive_ids + false_negative_ids + uncertain_ids
    return {
        "total_rows": len(rows),
        "binary_denominator": len(binary),
        "binary_agreement": correct / len(binary) if binary else None,
        "false_positives": len(false_positive_ids),
        "false_positive_ids": false_positive_ids,
        "false_negatives": len(false_negative_ids),
        "false_negative_ids": false_negative_ids,
        "uncertain_count": len(uncertain_ids),
        "uncertain_ids": uncertain_ids,
        "failure_ids": failure_ids,
    }


def fmt(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.3f}"


def main() -> int:
    with INPUT_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if len(rows) != 20:
        raise ValueError(f"expected 20 integrated rows, found {len(rows)}")

    valid_responses = sum(response_is_valid(row) for row in rows)
    overall = evaluate_group(rows)
    binary_rows = []
    for row in rows:
        truth = parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)
        rating = parse_label(row["trajectory_rater_crossing_present"], allow_uncertain=True)
        if rating is not None:
            binary_rows.append((truth, rating))
    expected = [truth for truth, _ in binary_rows]
    observed = [rating for _, rating in binary_rows]

    positives = [row for row in rows if parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)]
    controls = [row for row in rows if not parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)]
    step_errors = []
    for row in rows:
        truth_step = parse_step(row["ground_truth_crossing_step"])
        rating_step = parse_step(row["trajectory_rater_crossing_step"])
        if truth_step is not None and rating_step is not None:
            step_errors.append(abs(truth_step - rating_step))

    per_type = {}
    for hard_control_type in sorted({row["hard_control_type"] for row in rows}):
        group = [row for row in rows if row["hard_control_type"] == hard_control_type]
        per_type[hard_control_type] = evaluate_group(group)

    metrics = {
        "model": MODEL,
        "total_rows": len(rows),
        "valid_responses": valid_responses,
        "binary_agreement_denominator": overall["binary_denominator"],
        "binary_agreement": overall["binary_agreement"],
        "cohens_kappa": cohen_kappa(expected, observed),
        "false_positives": overall["false_positives"],
        "false_positive_ids": overall["false_positive_ids"],
        "false_negatives": overall["false_negatives"],
        "false_negative_ids": overall["false_negative_ids"],
        "uncertain_count": overall["uncertain_count"],
        "uncertain_ids": overall["uncertain_ids"],
        "positive_cases": case_counts(positives),
        "control_cases": case_counts(controls),
        "crossing_step_comparison_count": len(step_errors),
        "mean_crossing_step_absolute_error": sum(step_errors) / len(step_errors) if step_errors else None,
        "exact_crossing_step_accuracy": sum(error == 0 for error in step_errors) / len(step_errors) if step_errors else None,
        "within_one_step_accuracy": sum(error <= 1 for error in step_errors) / len(step_errors) if step_errors else None,
        "per_hard_control_type": per_type,
    }
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    print(f"Total rows: {len(rows)}")
    print(f"Valid responses: {valid_responses}")
    print(f"Binary agreement: {fmt(metrics['binary_agreement'])} ({overall['binary_denominator']} rows)")
    print(f"Cohen's kappa: {fmt(metrics['cohens_kappa'])}")
    print(f"False positives: {overall['false_positives']} {overall['false_positive_ids']}")
    print(f"False negatives: {overall['false_negatives']} {overall['false_negative_ids']}")
    print(f"Uncertain count: {overall['uncertain_count']} {overall['uncertain_ids']}")
    print(f"Positive yes/no/uncertain: {metrics['positive_cases']['yes']}/{metrics['positive_cases']['no']}/{metrics['positive_cases']['uncertain']}")
    print(f"Control yes/no/uncertain: {metrics['control_cases']['yes']}/{metrics['control_cases']['no']}/{metrics['control_cases']['uncertain']}")
    print(f"Mean crossing-step absolute error: {fmt(metrics['mean_crossing_step_absolute_error'])}")
    print(f"Exact crossing-step accuracy: {fmt(metrics['exact_crossing_step_accuracy'])}")
    print(f"Within-one-step accuracy: {fmt(metrics['within_one_step_accuracy'])}")
    failures = {
        name: result["failure_ids"]
        for name, result in per_type.items()
        if result["failure_ids"]
    }
    print(f"Per-hard-control-type failures: {failures or 'None'}")
    print(f"Metrics output: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
