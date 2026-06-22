# Experiment 2 Baseline Ladder

## Conditions

1. `final_step`: existing final-step-only result.
2. `last_2_steps`: original steps 4 and 5 only.
3. `last_3_steps`: original steps 3, 4, and 5 only.
4. `full_trajectory`: existing full-trajectory result.

All conditions use `gemini-3.1-flash-lite`. The two new ledgers are isolated and
resumable. The runner refuses to mix model or condition metadata.

## Commands

```powershell
python run_experiment2_baseline_ladder_rater.py
python integrate_experiment2_baseline_ladder.py
```

## Interpretation

Covered-case agreement excludes uncertain responses. The ladder comparison also
reports correctness with uncertain treated as incorrect. Performance is
`monotonic` only when positive detection and correctness are both non-decreasing
as context grows. Mixed improvement is `partial`; no improvement is `not`.

This is a fixed synthetic benchmark check, not external validation.
