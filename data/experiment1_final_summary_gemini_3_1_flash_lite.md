# Experiment 1 Final Summary: Gemini 3.1 Flash Lite

## Benchmark

- Model: `gemini-3.1-flash-lite`
- Dataset size: 30 synthetic trajectories (15 erosion-positive, 15 matched controls)
- Rater design: one LLM model evaluated both full trajectories and isolated final-step snapshots

## Trajectory Rater Performance

- Binary agreement: 1.000 (30 non-uncertain rows)
- Cohen's kappa: 1.000
- False positives / false negatives / uncertain: 0 / 0 / 0
- Mean crossing-step absolute error: 0.067
- Exact / within-one-step accuracy: 0.933 / 1.000

## Snapshot Rater Performance

- Binary agreement: 0.760 (25 non-uncertain rows)
- Cohen's kappa: 0.464
- False positives / false negatives / uncertain: 1 / 5 / 5
- Positive labels (yes / no / uncertain): 5 / 5 / 5
- Control labels (yes / no / uncertain): 1 / 14 / 0

## Lead-Time Comparison

- Positive cases with detection steps from both raters: 5
- Mean lead-time gain (snapshot step minus trajectory step): 1.000 steps
- Trajectory earlier / same step / snapshot earlier: 5 / 0 / 0
- Snapshot misses or uncertain on positive cases: 10
- Trajectory misses or uncertain on positive cases: 0

## Core Result

In this 30-trajectory synthetic matched-control benchmark, full-trajectory evaluation detected effective-override loss with higher temporal precision than snapshot-only evaluation.

## Limitations

This is a synthetic benchmark evaluated by a single-model LLM rater; it is not real-world field validation, and the reported differences should not be generalized beyond this benchmark without broader models, human raters, and field data.
