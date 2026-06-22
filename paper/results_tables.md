# Results Tables

## Table 1. Experiment 1: Trajectory versus Final-Step Snapshot

| Metric | Full trajectory | Final-step snapshot |
|---|---:|---:|
| Dataset rows | 30 | 30 |
| Valid responses | 30 | 30 |
| Binary agreement denominator | 30 | 25 |
| Binary agreement | 1.000 | 0.760 |
| Cohen's kappa | 1.000 | 0.464 |
| False positives | 0 | 1 |
| False negatives | 0 | 5 |
| Uncertain | 0 | 5 |
| Positive yes / no / uncertain | 15 / 0 / 0 | 5 / 5 / 5 |
| Control yes / no / uncertain | 0 / 15 / 0 | 1 / 14 / 0 |

**Timing:** Five positives were detected by both views. Full trajectory was one
step earlier in all five; mean snapshot-minus-trajectory lead-time gain was
`1.000` step.

**Denominator note:** Snapshot agreement and kappa exclude uncertain rows.

## Table 2. Experiment 2 Hard Controls: Trajectory versus Final-Step Snapshot

| Metric | Full trajectory | Final-step snapshot |
|---|---:|---:|
| Dataset rows | 20 | 20 |
| Valid responses | 20 | 20 |
| Binary agreement denominator | 20 | 18 |
| Binary agreement | 0.950 | 0.722 |
| Cohen's kappa | 0.900 | 0.444 |
| False positives | 1 | 0 |
| False negatives | 0 | 5 |
| Uncertain | 0 | 2 |
| Positive yes / no / uncertain | 10 / 0 / 0 | 4 / 5 / 1 |
| Control yes / no / uncertain | 1 / 9 / 0 | 0 / 9 / 1 |

**Timing:** Four positives were detected by both views. Full trajectory was
earlier in two and tied in two; mean snapshot-minus-trajectory lead-time gain was
`0.500` step.

**Boundary note:** The trajectory false positive is E2T08, audited as
`ground_truth_control_correct_model_failed` and retained as a hard negative.

## Cross-Experiment Positive Snapshot Summary

| Dataset | Positive cases | Snapshot yes | Snapshot no | Snapshot uncertain | Missed or uncertain |
|---|---:|---:|---:|---:|---:|
| Experiment 1 | 15 | 5 | 5 | 5 | 10 |
| Experiment 2 | 10 | 4 | 5 | 1 | 6 |
| **Total** | **25** | **9** | **10** | **6** | **16** |

Across both experiments, the final-step snapshot baseline missed or withheld
judgment on **16/25 positive effective-override-loss cases**. This aggregation is
a transparent count across the two fixed synthetic datasets, not a population
estimate.

## Table 3. Paired Correctness

Uncertain ratings count as incorrect in this table.

| Paired category | Experiment 1 | Experiment 2 |
|---|---:|---:|
| Both correct | 19 | 13 |
| Trajectory correct / snapshot incorrect or uncertain | 11 | 6 |
| Snapshot correct / trajectory incorrect or uncertain | 0 | 0 |
| Both incorrect or uncertain | 0 | 1 |
| Total | 30 | 20 |

For Experiment 1, the exact paired sign-test/McNemar calculation over discordant
pairs is `b=11`, `c=0`, `p=0.0009765625`. This p-value summarizes a fixed,
authored synthetic benchmark and is not a population-level or real-world effect
estimate.

## Table 4. Limitation and Claim Boundary

| Evidence supports | Evidence does not support |
|---|---|
| A proposed operational rubric for effective override loss | A complete measure of human agency |
| Fixed-model agreement with authored synthetic labels | LLM judgments as ground truth |
| Full-trajectory advantage over one final-step-only baseline in two datasets | Universal trajectory superiority or failure of all snapshot methods |
| Replication under authored lexical hard controls | Elimination of all lexical or template cues |
| A documented bad-outcome false-positive mode | Estimated prevalence of that error in deployed systems |
| A synthetic matched-control seed benchmark | Real-world platform validation, legal conclusions, or policy evidence |

## Reporting Rules

- Always pair snapshot agreement with its non-uncertain denominator and uncertain count.
- Do not average Experiment 1 and Experiment 2 into a single headline accuracy without a prespecified aggregation rationale.
- Keep timing metrics restricted to positives detected by both views.
- Identify all figures and tables as synthetic benchmark results.

