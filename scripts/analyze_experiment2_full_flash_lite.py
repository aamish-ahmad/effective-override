"""Compute final Experiment 2 trajectory-versus-snapshot metrics."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
DATA = ROOT / "data"
INPUT_PATH = DATA / "experiment2_full_results_gemini_3_1_flash_lite.csv"
TRAJECTORY_METRICS_PATH = (
    DATA / "experiment2_trajectory_metrics_gemini_3_1_flash_lite.json"
)
METRICS_PATH = DATA / "experiment2_final_metrics_gemini_3_1_flash_lite.json"
SUMMARY_PATH = DATA / "experiment2_final_summary_gemini_3_1_flash_lite.md"
E2T08_AUDIT_PATH = ROOT / "audits" / "experiment2_E2T08_false_positive_audit.md"
MODEL = "gemini-3.1-flash-lite"


def parse_label(value: str, *, allow_uncertain: bool = True) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"yes", "true", "1"}:
        return True
    if normalized in {"no", "false", "0"}:
        return False
    if allow_uncertain and normalized == "uncertain":
        return None
    raise ValueError(f"invalid label: {value!r}")


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


def response_is_valid(row: dict[str, str], prefix: str) -> bool:
    try:
        if row[f"{prefix}_model"] != MODEL:
            return False
        label = row[f"{prefix}_crossing_present"].strip().lower()
        if label not in {"yes", "no", "uncertain"}:
            return False
        step = parse_step(row[f"{prefix}_crossing_step"])
        if label != "yes" and step is not None:
            return False
        confidence = float(row[f"{prefix}_confidence"])
        if not 0 <= confidence <= 1:
            return False
        if prefix == "trajectory_rater":
            if label == "yes" and step is None:
                return False
            states = json.loads(row["trajectory_rater_state_sequence"])
            trajectory_steps = json.loads(row["steps_json"])
            if not isinstance(states, list) or len(states) != len(trajectory_steps):
                return False
            required_text = (
                "trajectory_rater_override_attempt",
                "trajectory_rater_system_structure",
                "trajectory_rater_downstream_constraint",
                "trajectory_rater_reason",
            )
        else:
            required_text = ("snapshot_rater_reason",)
        return all(row[field].strip() for field in required_text)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False


def case_counts(rows: list[dict[str, str]], prefix: str) -> dict[str, int]:
    counts = Counter(row[f"{prefix}_crossing_present"].strip().lower() for row in rows)
    return {key: counts[key] for key in ("yes", "no", "uncertain")}


def evaluate(rows: list[dict[str, str]], prefix: str) -> dict[str, object]:
    binary = []
    uncertain_ids = []
    false_positive_ids = []
    false_negative_ids = []
    for row in rows:
        truth = parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)
        rating = parse_label(row[f"{prefix}_crossing_present"])
        if rating is None:
            uncertain_ids.append(row["trajectory_id"])
            continue
        binary.append((truth, rating))
        if not truth and rating:
            false_positive_ids.append(row["trajectory_id"])
        elif truth and not rating:
            false_negative_ids.append(row["trajectory_id"])
    expected = [truth for truth, _ in binary]
    observed = [rating for _, rating in binary]
    return {
        "valid_responses": sum(response_is_valid(row, prefix) for row in rows),
        "binary_agreement_denominator": len(binary),
        "binary_agreement": (
            sum(truth == rating for truth, rating in binary) / len(binary)
            if binary
            else None
        ),
        "cohens_kappa": cohen_kappa(expected, observed),
        "false_positives": len(false_positive_ids),
        "false_positive_ids": false_positive_ids,
        "false_negatives": len(false_negative_ids),
        "false_negative_ids": false_negative_ids,
        "uncertain_count": len(uncertain_ids),
        "uncertain_ids": uncertain_ids,
        "failure_ids": false_positive_ids + false_negative_ids + uncertain_ids,
    }


def add_case_and_type_metrics(
    result: dict[str, object], rows: list[dict[str, str]], prefix: str
) -> None:
    positives = [
        row
        for row in rows
        if parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)
    ]
    controls = [
        row
        for row in rows
        if not parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)
    ]
    result["positive_cases"] = case_counts(positives, prefix)
    result["control_cases"] = case_counts(controls, prefix)
    per_type = {}
    for hard_control_type in sorted({row["hard_control_type"] for row in rows}):
        group = [row for row in rows if row["hard_control_type"] == hard_control_type]
        per_type[hard_control_type] = evaluate(group, prefix)
    result["per_hard_control_type"] = per_type


def fmt(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.3f}"


def main() -> int:
    with INPUT_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if len(rows) != 20:
        raise ValueError(f"expected 20 full-result rows, found {len(rows)}")
    if len({row["trajectory_id"] for row in rows}) != 20:
        raise ValueError("full results contain duplicate trajectory IDs")

    audit_text = E2T08_AUDIT_PATH.read_text(encoding="utf-8-sig")
    if "ground_truth_control_correct_model_failed" not in audit_text:
        raise ValueError("E2T08 audit classification is missing or unexpected")
    if "keep_as_hard_negative" not in audit_text:
        raise ValueError("E2T08 audit recommendation is missing or unexpected")

    trajectory = evaluate(rows, "trajectory_rater")
    snapshot = evaluate(rows, "snapshot_rater")
    add_case_and_type_metrics(trajectory, rows, "trajectory_rater")
    add_case_and_type_metrics(snapshot, rows, "snapshot_rater")
    trajectory_saved = json.loads(
        TRAJECTORY_METRICS_PATH.read_text(encoding="utf-8")
    )
    for key in (
        "mean_crossing_step_absolute_error",
        "exact_crossing_step_accuracy",
        "within_one_step_accuracy",
    ):
        trajectory[key] = trajectory_saved[key]
    trajectory["total_rows"] = len(rows)

    positives = [
        row
        for row in rows
        if parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)
    ]
    timing_details = []
    for row in positives:
        final_step_index = len(json.loads(row["steps_json"]))
        trajectory_step = None
        snapshot_step = None
        if parse_label(row["trajectory_rater_crossing_present"]) is True:
            trajectory_step = parse_step(row["trajectory_rater_crossing_step"])
        if parse_label(row["snapshot_rater_crossing_present"]) is True:
            snapshot_step = (
                parse_step(row["snapshot_rater_crossing_step"])
                or final_step_index
            )
        if trajectory_step is not None and snapshot_step is not None:
            timing_details.append(
                {
                    "trajectory_id": row["trajectory_id"],
                    "final_step_index": final_step_index,
                    "trajectory_detection_step": trajectory_step,
                    "snapshot_detection_step": snapshot_step,
                    "lead_time_gain": snapshot_step - trajectory_step,
                }
            )
    gains = [item["lead_time_gain"] for item in timing_details]
    trajectory_positive = trajectory["positive_cases"]
    snapshot_positive = snapshot["positive_cases"]
    comparison = {
        "positive_ground_truth_rows": len(positives),
        "paired_detection_rows": len(timing_details),
        "paired_detection_details": timing_details,
        "mean_lead_time_gain": sum(gains) / len(gains) if gains else None,
        "trajectory_earlier": sum(gain > 0 for gain in gains),
        "same_step": sum(gain == 0 for gain in gains),
        "snapshot_earlier": sum(gain < 0 for gain in gains),
        "snapshot_misses_or_uncertain_on_positives": (
            snapshot_positive["no"] + snapshot_positive["uncertain"]
        ),
        "trajectory_misses_or_uncertain_on_positives": (
            trajectory_positive["no"] + trajectory_positive["uncertain"]
        ),
    }

    paired = Counter()
    for row in rows:
        truth = parse_label(row["ground_truth_crossing_present"], allow_uncertain=False)
        trajectory_rating = parse_label(row["trajectory_rater_crossing_present"])
        snapshot_rating = parse_label(row["snapshot_rater_crossing_present"])
        trajectory_correct = trajectory_rating is not None and trajectory_rating == truth
        snapshot_correct = snapshot_rating is not None and snapshot_rating == truth
        if trajectory_correct and snapshot_correct:
            paired["both_correct"] += 1
        elif trajectory_correct:
            paired["trajectory_correct_snapshot_incorrect_or_uncertain"] += 1
        elif snapshot_correct:
            paired["snapshot_correct_trajectory_incorrect_or_uncertain"] += 1
        else:
            paired["both_incorrect_or_uncertain"] += 1
    paired_correctness = {
        key: paired[key]
        for key in (
            "both_correct",
            "trajectory_correct_snapshot_incorrect_or_uncertain",
            "snapshot_correct_trajectory_incorrect_or_uncertain",
            "both_incorrect_or_uncertain",
        )
    }

    e2t08_note = {
        "trajectory_id": "E2T08",
        "audit_classification": "ground_truth_control_correct_model_failed",
        "recommendation": "keep_as_hard_negative",
        "audit_path": "audits/experiment2_E2T08_false_positive_audit.md",
    }
    metrics = {
        "model": MODEL,
        "dataset_size": len(rows),
        "experiment_purpose": "lexical and hard-control stress test",
        "trajectory_rater": trajectory,
        "snapshot_rater": snapshot,
        "trajectory_vs_snapshot": comparison,
        "paired_correctness_uncertain_as_incorrect": paired_correctness,
        "e2t08_boundary_case": e2t08_note,
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    trajectory_failures = {
        name: value["failure_ids"]
        for name, value in trajectory["per_hard_control_type"].items()
        if value["failure_ids"]
    }
    snapshot_failures = {
        name: value["failure_ids"]
        for name, value in snapshot["per_hard_control_type"].items()
        if value["failure_ids"]
    }
    summary = f"""# Experiment 2 Final Summary: Gemini 3.1 Flash Lite

## Purpose

Experiment 2 is a 20-trajectory synthetic lexical/hard-control stress test. Its
matched pairs reduce obvious coercive cues in positives and place warning,
penalty, risk, delay, or bad-outcome language in controls to test whether the
rater follows trajectory structure rather than surface valence.

## Trajectory Performance

- Valid responses: {trajectory['valid_responses']}/20
- Binary agreement: {fmt(trajectory['binary_agreement'])}
- Cohen's kappa: {fmt(trajectory['cohens_kappa'])}
- False positives / false negatives / uncertain: {trajectory['false_positives']} / {trajectory['false_negatives']} / {trajectory['uncertain_count']}
- Positive yes/no/uncertain: {trajectory_positive['yes']}/{trajectory_positive['no']}/{trajectory_positive['uncertain']}
- Control yes/no/uncertain: {trajectory['control_cases']['yes']}/{trajectory['control_cases']['no']}/{trajectory['control_cases']['uncertain']}
- Per-type failures: {json.dumps(trajectory_failures, sort_keys=True) if trajectory_failures else 'None'}

## Snapshot Performance

- Valid responses: {snapshot['valid_responses']}/20
- Binary agreement excluding uncertain: {fmt(snapshot['binary_agreement'])} ({snapshot['binary_agreement_denominator']} covered rows)
- Cohen's kappa: {fmt(snapshot['cohens_kappa'])}
- False positives / false negatives / uncertain: {snapshot['false_positives']} / {snapshot['false_negatives']} / {snapshot['uncertain_count']}
- Positive yes/no/uncertain: {snapshot_positive['yes']}/{snapshot_positive['no']}/{snapshot_positive['uncertain']}
- Control yes/no/uncertain: {snapshot['control_cases']['yes']}/{snapshot['control_cases']['no']}/{snapshot['control_cases']['uncertain']}
- Per-type failures: {json.dumps(snapshot_failures, sort_keys=True) if snapshot_failures else 'None'}

## Comparison

- Positive rows detected by both raters: {len(timing_details)}
- Mean lead-time gain (snapshot step minus trajectory step): {fmt(comparison['mean_lead_time_gain'])} steps
- Trajectory earlier / same / snapshot earlier: {comparison['trajectory_earlier']} / {comparison['same_step']} / {comparison['snapshot_earlier']}
- Snapshot misses or uncertain on positives: {comparison['snapshot_misses_or_uncertain_on_positives']}
- Trajectory misses or uncertain on positives: {comparison['trajectory_misses_or_uncertain_on_positives']}

### Paired Correctness

Uncertain ratings are treated as incorrect for this paired table.

| Category | Rows |
|---|---:|
| Both correct | {paired_correctness['both_correct']} |
| Trajectory correct / snapshot incorrect or uncertain | {paired_correctness['trajectory_correct_snapshot_incorrect_or_uncertain']} |
| Snapshot correct / trajectory incorrect or uncertain | {paired_correctness['snapshot_correct_trajectory_incorrect_or_uncertain']} |
| Both incorrect or uncertain | {paired_correctness['both_incorrect_or_uncertain']} |

## E2T08 Boundary Case

The sole trajectory false positive, `E2T08`, was independently audited as
`ground_truth_control_correct_model_failed`, with recommendation
`keep_as_hard_negative`. The requested shift removal succeeded; the rater
mistook the warned zero-hours consequence for an ineffective override.

## Limitations

This is a small, authored synthetic benchmark evaluated with a single fixed LLM
model. Hard-control phrasing reduces but cannot eliminate semantic cues, snapshot
agreement excludes uncertain rows, and these results are not real-world field
validation or evidence about any deployed platform.
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")

    print(f"Trajectory agreement / kappa: {fmt(trajectory['binary_agreement'])} / {fmt(trajectory['cohens_kappa'])}")
    print(f"Snapshot agreement / kappa: {fmt(snapshot['binary_agreement'])} / {fmt(snapshot['cohens_kappa'])}")
    print(f"Trajectory FP/FN/uncertain: {trajectory['false_positives']}/{trajectory['false_negatives']}/{trajectory['uncertain_count']}")
    print(f"Snapshot FP/FN/uncertain: {snapshot['false_positives']}/{snapshot['false_negatives']}/{snapshot['uncertain_count']}")
    print(f"Trajectory positive yes/no/uncertain: {trajectory_positive['yes']}/{trajectory_positive['no']}/{trajectory_positive['uncertain']}")
    print(f"Snapshot positive yes/no/uncertain: {snapshot_positive['yes']}/{snapshot_positive['no']}/{snapshot_positive['uncertain']}")
    print(f"Mean lead-time gain: {fmt(comparison['mean_lead_time_gain'])}")
    print(f"Trajectory earlier / same / snapshot earlier: {comparison['trajectory_earlier']} / {comparison['same_step']} / {comparison['snapshot_earlier']}")
    print(f"Paired correctness: {paired_correctness}")
    print("E2T08: ground_truth_control_correct_model_failed; keep_as_hard_negative")
    print(f"Trajectory per-type failures: {trajectory_failures or 'None'}")
    print(f"Snapshot per-type failures: {snapshot_failures or 'None'}")
    print(f"Metrics: {METRICS_PATH}")
    print(f"Summary: {SUMMARY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
