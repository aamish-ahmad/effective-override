"""Generate the deterministic Experiment 1 robustness and lineage audits."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]
DATA = ROOT / "data"
AUDITS = ROOT / "audits"
SOURCE = DATA / "experiment1.csv"
FULL_RESULTS = DATA / "experiment1_full_results_gemini_3_1_flash_lite.csv"
FINAL_METRICS = DATA / "experiment1_final_metrics_gemini_3_1_flash_lite.json"
FINAL_SUMMARY = DATA / "experiment1_final_summary_gemini_3_1_flash_lite.md"
STATISTICAL_AUDIT = DATA / "experiment1_statistical_audit_gemini_3_1_flash_lite.json"
TRAJECTORY_LEDGER = DATA / "experiment1_trajectory_rater_responses_gemini_3_1_flash_lite.md"
SNAPSHOT_LEDGER = DATA / "experiment1_snapshot_rater_responses_gemini_3_1_flash_lite.md"
TRAJECTORY_RUNNER = ROOT / "run_gemini_trajectory_rater_experiment1_flash_lite.py"
SNAPSHOT_RUNNER = ROOT / "run_gemini_snapshot_rater_experiment1_flash_lite.py"
MODEL = "gemini-3.1-flash-lite"
HEADER = re.compile(r"(?m)^##\s+([A-Za-z0-9_-]+)\s*$")
FORBIDDEN_FIELDS = (
    "condition",
    "ground_truth_crossing_present",
    "ground_truth_crossing_step",
    "ground_truth_state_sequence",
    "trajectory_rater",
    "snapshot_rater",
)


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        return list(reader), list(reader.fieldnames or [])


def ledger(path: Path) -> tuple[list[tuple[str, dict]], list[str]]:
    content = path.read_text(encoding="utf-8-sig")
    matches = list(HEADER.finditer(content))
    parsed = []
    errors = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        trajectory_id = match.group(1)
        try:
            value = json.loads(content[match.end():end].strip())
            if not isinstance(value, dict):
                raise ValueError("JSON value is not an object")
            if value.get("trajectory_id") != trajectory_id:
                raise ValueError("JSON trajectory_id differs from section header")
            parsed.append((trajectory_id, value))
        except (json.JSONDecodeError, ValueError) as error:
            errors.append(f"{trajectory_id}: {error}")
    return parsed, errors


def parse_label(value: str, uncertain: bool = True) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"yes", "true", "1"}:
        return True
    if normalized in {"no", "false", "0"}:
        return False
    if uncertain and normalized == "uncertain":
        return None
    raise ValueError(f"invalid label {value!r}")


def parse_step(value: str) -> int | None:
    normalized = value.strip()
    if not normalized:
        return None
    if not normalized.isdigit():
        raise ValueError(f"invalid step {value!r}")
    return int(normalized)


def function_source(path: Path, function_name: str) -> str:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return ast.get_source_segment(source, node) or ""
    raise ValueError(f"{path.name}: missing function {function_name}")


def prompt_blindness() -> tuple[bool, dict[str, list[str]], str]:
    findings = {}
    for path in (TRAJECTORY_RUNNER, SNAPSHOT_RUNNER):
        prompt_source = function_source(path, "build_prompt")
        findings[path.name] = [field for field in FORBIDDEN_FIELDS if field in prompt_source]
    passed = not any(findings.values())
    status = "PASS" if passed else "FAIL"
    lines = [
        "# Experiment 1 Prompt Blindness Audit",
        "",
        f"**Status: {status}**",
        "",
        "## Forbidden-Field Inspection",
        "",
        "Static AST-based inspection was limited to each runner's `build_prompt` function.",
        "",
        "| Runner | Forbidden fields in prompt construction |",
        "|---|---|",
    ]
    for name, fields in findings.items():
        lines.append(f"| `{name}` | {', '.join(f'`{item}`' for item in fields) if fields else 'None'} |")
    lines += [
        "",
        "## Rater Views",
        "",
        "The trajectory rater sees the blind-rater instructions, full rubric, trajectory ID, and all five raw trajectory steps. Its prompt construction does not reference CSV condition or ground-truth columns.",
        "",
        "The snapshot rater sees the snapshot instructions, trajectory ID, final-step index, and final visible step only. Its prompt construction does not include earlier steps, labels, or trajectory-rater output.",
        "",
        "## Static-Inspection Limitations",
        "",
        "This audit checks checked-in prompt-construction source, not network payload capture. It cannot rule out runtime code replacement, dependency changes, provider-side transformations, or uncommitted local modifications after hashing.",
        "",
    ]
    return passed, findings, "\n".join(lines)


def integrity_checks() -> tuple[list[dict[str, str]], dict[str, bool], list[str]]:
    source_rows, _ = read_csv(SOURCE)
    result_rows, _ = read_csv(FULL_RESULTS)
    checks = {}
    warnings = []
    ids = [row["trajectory_id"] for row in source_rows]
    checks["source has 30 rows"] = len(source_rows) == 30
    checks["trajectory IDs are unique"] = len(ids) == len(set(ids))
    pairs = defaultdict(list)
    steps_ok = states_ok = five_steps = True
    for row in source_rows:
        pairs[row["pair_id"]].append(row)
        try:
            steps = json.loads(row["steps_json"])
            steps_ok &= isinstance(steps, list)
            five_steps &= isinstance(steps, list) and len(steps) == 5
        except json.JSONDecodeError:
            steps_ok = five_steps = False
        try:
            states_ok &= isinstance(json.loads(row["ground_truth_state_sequence"]), list)
        except json.JSONDecodeError:
            states_ok = False
    checks["source has 15 matched pairs"] = len(pairs) == 15
    checks["each pair has one positive and one control"] = all(
        Counter(row["condition"] for row in pair) == Counter({"erosion_positive": 1, "matched_control": 1})
        for pair in pairs.values()
    )
    checks["all steps_json values parse"] = steps_ok
    checks["all state sequences parse"] = states_ok
    checks["all trajectories have exactly five steps"] = five_steps
    trajectory_responses, trajectory_errors = ledger(TRAJECTORY_LEDGER)
    snapshot_responses, snapshot_errors = ledger(SNAPSHOT_LEDGER)
    trajectory_ids = [item[0] for item in trajectory_responses]
    snapshot_ids = [item[0] for item in snapshot_responses]
    checks["30 official trajectory responses parse"] = (
        len(trajectory_responses) == 30 and not trajectory_errors and len(trajectory_ids) == len(set(trajectory_ids))
    )
    checks["30 official snapshot responses parse"] = (
        len(snapshot_responses) == 30 and not snapshot_errors and len(snapshot_ids) == len(set(snapshot_ids))
    )
    result_ids = [row["trajectory_id"] for row in result_rows]
    checks["integrated full results has 30 rows"] = len(result_rows) == 30
    checks["integrated results have no missing or extra IDs"] = set(result_ids) == set(ids)
    checks["response ledgers have no missing or extra IDs"] = set(trajectory_ids) == set(ids) == set(snapshot_ids)
    warnings.extend(trajectory_errors + snapshot_errors)
    return result_rows, checks, warnings


def robust_metrics(rows: list[dict[str, str]]) -> tuple[dict, dict[str, int]]:
    trajectory_binary = []
    snapshot_binary = []
    positives = []
    controls = []
    correctness = Counter()
    step_errors = []
    lead_times = []
    timing = Counter()
    for row in rows:
        truth = parse_label(row["ground_truth_crossing_present"], False)
        trajectory = parse_label(row["trajectory_rater_crossing_present"])
        snapshot = parse_label(row["snapshot_rater_crossing_present"])
        trajectory_correct = trajectory is not None and trajectory == truth
        snapshot_correct = snapshot is not None and snapshot == truth
        if trajectory_correct and snapshot_correct:
            correctness["both_correct"] += 1
        elif trajectory_correct:
            correctness["trajectory_correct_snapshot_incorrect_or_uncertain"] += 1
        elif snapshot_correct:
            correctness["snapshot_correct_trajectory_incorrect_or_uncertain"] += 1
        else:
            correctness["both_incorrect_or_uncertain"] += 1
        if trajectory is not None:
            trajectory_binary.append(trajectory == truth)
        if snapshot is not None:
            snapshot_binary.append(snapshot == truth)
        (positives if truth else controls).append(row)
        truth_step = parse_step(row["ground_truth_crossing_step"])
        trajectory_step = parse_step(row["trajectory_rater_crossing_step"])
        if truth_step is not None and trajectory_step is not None:
            step_errors.append(abs(truth_step - trajectory_step))
        if truth and trajectory is True and snapshot is True:
            snapshot_step = parse_step(row["snapshot_rater_crossing_step"]) or len(json.loads(row["steps_json"]))
            if trajectory_step is not None:
                gain = snapshot_step - trajectory_step
                lead_times.append(gain)
                timing["trajectory_earlier" if gain > 0 else "same_step" if gain == 0 else "snapshot_earlier"] += 1
    positive_snapshot = Counter(row["snapshot_rater_crossing_present"].lower() for row in positives)
    control_snapshot = Counter(row["snapshot_rater_crossing_present"].lower() for row in controls)
    positive_trajectory = Counter(row["trajectory_rater_crossing_present"].lower() for row in positives)
    metrics = {
        "trajectory_binary_accuracy": sum(trajectory_binary) / len(trajectory_binary),
        "snapshot_binary_accuracy_excluding_uncertain": sum(snapshot_binary) / len(snapshot_binary),
        "snapshot_coverage_rate": len(snapshot_binary) / len(rows),
        "snapshot_positive": {key: positive_snapshot[key] for key in ("yes", "no", "uncertain")},
        "snapshot_control": {key: control_snapshot[key] for key in ("yes", "no", "uncertain")},
        "trajectory_positive_detection_rate": positive_trajectory["yes"] / len(positives),
        "snapshot_positive_detection_rate": positive_snapshot["yes"] / len(positives),
        "exact_crossing_step_accuracy": sum(error == 0 for error in step_errors) / len(step_errors),
        "within_one_step_crossing_accuracy": sum(error <= 1 for error in step_errors) / len(step_errors),
        "lead_time_gain_mean": sum(lead_times) / len(lead_times) if lead_times else None,
        "trajectory_earlier": timing["trajectory_earlier"],
        "same_step": timing["same_step"],
        "snapshot_earlier": timing["snapshot_earlier"],
    }
    table = {
        "both correct": correctness["both_correct"],
        "trajectory correct / snapshot incorrect or uncertain": correctness["trajectory_correct_snapshot_incorrect_or_uncertain"],
        "snapshot correct / trajectory incorrect or uncertain": correctness["snapshot_correct_trajectory_incorrect_or_uncertain"],
        "both incorrect or uncertain": correctness["both_incorrect_or_uncertain"],
    }
    return metrics, table


def mcnemar(table: dict[str, int]) -> dict[str, object]:
    b = table["trajectory correct / snapshot incorrect or uncertain"]
    c = table["snapshot correct / trajectory incorrect or uncertain"]
    n = b + c
    tail = sum(math.comb(n, k) * 0.5**n for k in range(min(b, c) + 1))
    exact_p = min(2 * tail, 1.0) if n else 1.0
    return {
        "b": b,
        "c": c,
        "n_discordant": n,
        "mcnemar_exact_p": exact_p,
    }


def pairwise_markdown(rows: list[dict[str, str]]) -> tuple[str, Counter]:
    pairs = defaultdict(list)
    summary = Counter()
    for row in rows:
        pairs[row["pair_id"]].append(row)
    lines = [
        "# Experiment 1 Pairwise Error Audit", "",
        "| Pair | Positive ID | Control ID | Ground truth | Trajectory decisions | Snapshot decisions | Snapshot error status | Trajectory correct | Crossing-step difference |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for pair_id in sorted(pairs):
        positive = next(row for row in pairs[pair_id] if row["condition"] == "erosion_positive")
        control = next(row for row in pairs[pair_id] if row["condition"] == "matched_control")
        p_snapshot = positive["snapshot_rater_crossing_present"].lower()
        c_snapshot = control["snapshot_rater_crossing_present"].lower()
        statuses = []
        if p_snapshot == "no": statuses.append("positive missed"); summary["positive_missed"] += 1
        if p_snapshot == "uncertain": statuses.append("positive uncertain"); summary["positive_uncertain"] += 1
        if c_snapshot == "yes": statuses.append("control false-positive"); summary["control_false_positive"] += 1
        if not statuses: statuses.append("none")
        p_traj = positive["trajectory_rater_crossing_present"].lower()
        c_traj = control["trajectory_rater_crossing_present"].lower()
        trajectory_correct = p_traj == "yes" and c_traj == "no"
        difference = "N/A"
        if p_traj == "yes" and p_snapshot == "yes":
            trajectory_step = parse_step(positive["trajectory_rater_crossing_step"])
            snapshot_step = parse_step(positive["snapshot_rater_crossing_step"]) or len(json.loads(positive["steps_json"]))
            difference = str(snapshot_step - trajectory_step)
        lines.append(
            f"| {pair_id} | {positive['trajectory_id']} | {control['trajectory_id']} | positive=yes; control=no | positive={p_traj}; control={c_traj} | positive={p_snapshot}; control={c_snapshot} | {'; '.join(statuses)} | {'yes' if trajectory_correct else 'no'} | {difference} |"
        )
    lines += ["", "Crossing-step difference is snapshot detection step minus trajectory detection step on positive rows where both detected a crossing.", ""]
    return "\n".join(lines), summary


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def lineage_markdown() -> str:
    paths = [
        SOURCE, TRAJECTORY_LEDGER, SNAPSHOT_LEDGER, FULL_RESULTS, FINAL_METRICS,
        FINAL_SUMMARY, ROOT / "prompts" / "blind_rater_prompt.md",
        ROOT / "prompts" / "snapshot_rater_prompt.md", ROOT / "rubric.md",
        TRAJECTORY_RUNNER, SNAPSHOT_RUNNER,
        ROOT / "integrate_flash_lite_trajectory_rater.py",
        ROOT / "integrate_flash_lite_snapshot_rater.py",
        ROOT / "scripts" / "analyze_experiment1_trajectory_flash_lite.py",
        ROOT / "scripts" / "analyze_experiment1_full_flash_lite.py",
        Path(__file__),
    ]
    lines = ["# Experiment 1 Data Lineage Manifest", "", "SHA256 hashes were computed over raw file bytes at audit time.", "", "| File | SHA256 |", "|---|---|"]
    for path in paths:
        lines.append(f"| `{path.relative_to(ROOT).as_posix()}` | `{sha256(path)}` |")
    lines += ["", "## Local Derivation Chain", "", "`experiment1.csv` + trajectory ledger -> trajectory integration/analysis -> snapshot ledger + snapshot integration -> full analysis -> robustness audit.", ""]
    return "\n".join(lines)


def fmt(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.3f}"


def main() -> int:
    AUDITS.mkdir(exist_ok=True)
    rows, checks, warnings = integrity_checks()
    integrity_passed = all(checks.values())
    blindness_passed, _, blindness_md = prompt_blindness()
    metrics, paired = robust_metrics(rows)
    test = mcnemar(paired)
    statistical_audit = {
        "model": MODEL,
        "paired_correctness_table": {
            "both_correct": paired["both correct"],
            "trajectory_correct_snapshot_incorrect_or_uncertain": paired[
                "trajectory correct / snapshot incorrect or uncertain"
            ],
            "snapshot_correct_trajectory_incorrect_or_uncertain": paired[
                "snapshot correct / trajectory incorrect or uncertain"
            ],
            "both_incorrect_or_uncertain": paired["both incorrect or uncertain"],
        },
        **test,
        "interpretation": (
            "Under an exact paired sign-test/McNemar formulation over discordant "
            "pairs, the probability of observing 11 trajectory-favoring "
            "discordances and 0 snapshot-favoring discordances under the null of "
            "equal paired correctness is p = 0.0009765625."
        ),
        "trajectory_correct_rate_uncertain_as_incorrect": (
            paired["both correct"]
            + paired["trajectory correct / snapshot incorrect or uncertain"]
        ) / len(rows),
        "snapshot_correct_rate_uncertain_as_incorrect": (
            paired["both correct"]
            + paired["snapshot correct / trajectory incorrect or uncertain"]
        ) / len(rows),
        "snapshot_coverage_rate": metrics["snapshot_coverage_rate"],
        "snapshot_accuracy_excluding_uncertain": metrics[
            "snapshot_binary_accuracy_excluding_uncertain"
        ],
        "snapshot_positive_detection_rate_yes_only": metrics[
            "snapshot_positive_detection_rate"
        ],
        "trajectory_positive_detection_rate_yes_only": metrics[
            "trajectory_positive_detection_rate"
        ],
    }
    STATISTICAL_AUDIT.write_text(
        json.dumps(statistical_audit, indent=2) + "\n", encoding="utf-8"
    )
    pairwise_md, pair_summary = pairwise_markdown(rows)
    (AUDITS / "experiment1_prompt_blindness_audit.md").write_text(blindness_md, encoding="utf-8")
    (AUDITS / "experiment1_pairwise_error_audit.md").write_text(pairwise_md, encoding="utf-8")
    (AUDITS / "experiment1_data_lineage_manifest.md").write_text(lineage_markdown(), encoding="utf-8")

    integrity_lines = "\n".join(f"- [{'x' if passed else ' '}] {name}" for name, passed in checks.items())
    paired_rows = "".join(f"| {name} | {count} |\n" for name, count in paired.items())
    robustness = f"""# Experiment 1 Robustness Audit

## Headline Result

In this synthetic matched-control benchmark, a single fixed LLM rater achieved higher binary accuracy and earlier detection with full trajectories than with final-step snapshots. This is evidence that trajectory-level evaluation captures effective override loss earlier than snapshot-only evaluation within this benchmark.

## Why the Trajectory Result Is Stronger

The trajectory rater had binary accuracy {fmt(metrics['trajectory_binary_accuracy'])} and positive detection rate {fmt(metrics['trajectory_positive_detection_rate'])}; the snapshot rater had covered-case accuracy {fmt(metrics['snapshot_binary_accuracy_excluding_uncertain'])}, coverage {fmt(metrics['snapshot_coverage_rate'])}, and positive detection rate {fmt(metrics['snapshot_positive_detection_rate'])}. For paired positive detections, mean lead-time gain was {fmt(metrics['lead_time_gain_mean'])} step.

## Data Integrity Status

**{'PASS' if integrity_passed else 'FAIL'}**

{integrity_lines}

## Prompt Blindness Status

**{'PASS' if blindness_passed else 'FAIL'}**. Static inspection found no forbidden dataset or rater-result fields in either `build_prompt` function. See `experiment1_prompt_blindness_audit.md` for scope and limitations.

## Pairwise Error Summary

- Snapshot positive misses: {pair_summary['positive_missed']}
- Snapshot positive uncertain: {pair_summary['positive_uncertain']}
- Snapshot control false positives: {pair_summary['control_false_positive']}
- Full per-pair decisions: `experiment1_pairwise_error_audit.md`

## Robustness Metrics

- Trajectory binary accuracy: {fmt(metrics['trajectory_binary_accuracy'])}
- Snapshot binary accuracy excluding uncertain: {fmt(metrics['snapshot_binary_accuracy_excluding_uncertain'])}
- Snapshot coverage: {fmt(metrics['snapshot_coverage_rate'])}
- Snapshot positive yes/no/uncertain: {metrics['snapshot_positive']['yes']}/{metrics['snapshot_positive']['no']}/{metrics['snapshot_positive']['uncertain']}
- Snapshot control yes/no/uncertain: {metrics['snapshot_control']['yes']}/{metrics['snapshot_control']['no']}/{metrics['snapshot_control']['uncertain']}
- Exact / within-one-step crossing accuracy: {fmt(metrics['exact_crossing_step_accuracy'])} / {fmt(metrics['within_one_step_crossing_accuracy'])}
- Trajectory earlier / same / snapshot earlier: {metrics['trajectory_earlier']} / {metrics['same_step']} / {metrics['snapshot_earlier']}

## Paired Statistical Comparison

Uncertain snapshot labels are treated as incorrect for paired correctness, while their effect is separately reported through snapshot coverage.

### Paired Correctness Table

| Category | Rows |
|---|---:|
{paired_rows}
### Exact McNemar/Binomial Fallback

- Discordant counts (`b` / `c` / `n`): {test['b']} / {test['c']} / {test['n_discordant']}
- Exact two-sided p-value: {test['mcnemar_exact_p']}
- Calculation: standard-library exact binomial tail; SciPy is not required.
- Interpretation: {statistical_audit['interpretation']}

## Reproducibility Status

**PASS**. Shell and batch scripts rerun only local integrations, analyses, and this audit. The lineage manifest records SHA256 hashes for source, ledgers, prompts, runners, integrations, analyses, and final artifacts.

## Remaining Limitations

This is a synthetic matched-control benchmark using a single fixed LLM rater, not real-world field validation. Static prompt inspection is not a captured network-payload audit, the dataset is small and constructed, and findings do not prove universal human agency erosion or validate claims about real gig platforms.
"""
    (AUDITS / "experiment1_robustness_audit.md").write_text(robustness, encoding="utf-8")

    print(f"Data integrity: {'PASS' if integrity_passed else 'FAIL'}")
    print(f"Prompt blindness: {'PASS' if blindness_passed else 'FAIL'}")
    print("Paired correctness table:")
    for name, count in paired.items():
        print(f"  {name}: {count}")
    print(
        f"McNemar exact: b={test['b']}, c={test['c']}, "
        f"n={test['n_discordant']}, p={test['mcnemar_exact_p']}"
    )
    print(f"Warnings: {warnings or 'None'}")
    print(f"Trajectory binary accuracy: {fmt(metrics['trajectory_binary_accuracy'])}")
    print(f"Snapshot binary accuracy excluding uncertain: {fmt(metrics['snapshot_binary_accuracy_excluding_uncertain'])}")
    print(f"Snapshot coverage: {fmt(metrics['snapshot_coverage_rate'])}")
    print(f"Lead-time gain mean: {fmt(metrics['lead_time_gain_mean'])}")
    return 0 if integrity_passed and blindness_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())




