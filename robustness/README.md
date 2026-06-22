# Experiment 2 Robustness Check

This directory contains an isolated science-gate run over the fixed Experiment
2 hard-control v1 dataset.

## Configuration

- `GEMINI_API_KEY`: required; loaded from the shell or ignored local env files.
- `GEMINI_ROBUSTNESS_MODEL`: defaults to `gemini-3.5-flash`.
- `GEMINI_REQUEST_SLEEP_SECONDS`: defaults to `5`.

If the robustness model is `gemini-3.1-flash-lite`, the run type is
`repeated_run_stability`. Any other model is `second_model_robustness`.

## Prompt Protocol

The runner prefers `prompts/trajectory_rater_prompt.md`. That file is not in the
current workspace, so it falls back explicitly to the official Experiment 2
protocol: `prompts/blind_rater_prompt.md` plus `rubric.md`. Only trajectory ID
and raw steps are added; labels, condition, hard-control type, and prior outputs
are never sent.

## Commands

```powershell
python run_experiment2_trajectory_rater_robustness.py
python integrate_experiment2_robustness.py
```

The ledger stores model and run-type metadata. The runner refuses to append if
the current environment does not match existing metadata. Responses are appended
immediately, so quota or model-availability failures preserve completed work.

## Science Gate

- `PASS_STRONG`: 20 valid responses, kappa at least 0.80, at most two total false positives plus false negatives, and at most two uncertain ratings.
- `PASS_PARTIAL`: at least 15 valid responses and broad support for trajectory evaluation, operationalized as agreement at least 0.70 and kappa at least 0.50, but the strong criteria are not met.
- `FAIL`: fewer than 15 valid responses, unreliable parsing, or agreement/kappa below the partial-support thresholds.

These thresholds describe this fixed synthetic science gate. They are not
real-world validation criteria.
