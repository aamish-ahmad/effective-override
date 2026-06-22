# Results

## Headline

ATB evaluates whether effective override loss is easier to detect when a rater receives the full trajectory rather than only the final visible state.

## Experiment 1

| Condition | Agreement | Cohen's kappa |
|---|---:|---:|
| Trajectory | 1.000 | 1.000 |
| Snapshot | 0.760 covered-case | 0.464 |

Trajectory evaluation achieved perfect binary agreement in Experiment 1. The final-step snapshot baseline was materially weaker and included five uncertain judgments.

## Experiment 2

| Condition | Agreement | Cohen's kappa |
|---|---:|---:|
| Trajectory | 0.950 | 0.900 |
| Snapshot | 0.722 covered-case | 0.444 |
| Robustness | 0.950 | 0.900 |

Experiment 2 preserves the main pattern under lexical hard controls: trajectory evaluation remains substantially stronger than final-step-only evaluation.

## Aggregate Snapshot Misses

Across Experiment 1 and Experiment 2, the final-step snapshot baseline detected `9/25` positives and missed or withheld judgment on `16/25` positives.

## Baseline Ladder

| Context window | Cohen's kappa |
|---|---:|
| `final_step` | 0.444 |
| `last_2_steps` | 0.231 |
| `last_3_steps` | 0.700 |
| `full_trajectory` | 0.900 |

The baseline ladder supports the release interpretation that the construct is history-sensitive in this synthetic benchmark.
