# Agency Trajectory Benchmark v0

Agency Trajectory Benchmark (`ATB-v0`) is a synthetic matched-control benchmark for detecting **effective override loss** in human-in-the-loop systems.

Human-in-the-loop is not human-in-control. A workflow can still present nominal choices while a person's override no longer meaningfully changes the next consequential state. `ATB-v0` operationalizes that failure as a trajectory-level construct and compares full-trajectory evaluation against lower-context baselines.

This repository is a public research artifact release. It does **not** claim real-world validation, does **not** establish wrongdoing by any deployed platform, and does **not** present authored labels or LLM ratings as ground truth beyond this synthetic benchmark.

## What This Repository Contains

- Two synthetic matched-control experiments for effective human override and effective override loss.
- Model-specific response ledgers, integrated result tables, metrics JSON files, audits, and paper scaffolding.
- Reproduction scripts for local post-processing, analysis, robustness checks, and the Experiment 2 baseline ladder.

## Core Construct

A trajectory crosses into **effective override loss** at the earliest step where:

1. A human override action is attempted or plausibly available.
2. That override no longer meaningfully changes the next outcome trajectory.
3. The failure is caused by system structure.
4. The loss persists or creates downstream constraint.

Bad outcomes alone do not count. The benchmark is designed to distinguish structural loss of control from inconvenience, delay, or an unfavorable but still override-sensitive result.

## Main Results

### Experiment 1: Ordinary Synthetic Matched Controls

- Dataset: 30 trajectories, 15 positives, 15 matched controls.
- Full trajectory: agreement `1.000`, Cohen's kappa `1.000`.
- Final-step snapshot: covered-case agreement `0.760`, Cohen's kappa `0.464`.
- Snapshot positive judgments: `5 yes / 5 no / 5 uncertain`.

### Experiment 2: Lexical Hard Controls

- Dataset: 20 trajectories, 10 positives, 10 matched controls.
- Full trajectory: agreement `0.950`, Cohen's kappa `0.900`.
- Final-step snapshot: covered-case agreement `0.722`, Cohen's kappa `0.444`.
- Snapshot positive judgments: `4 yes / 5 no / 1 uncertain`.

### History-Sensitivity Checks

- Experiment 2 second-model robustness check (`gemini-3.5-flash`): Cohen's kappa `0.900`.
- Experiment 2 baseline ladder kappas:
- `final_step`: `0.444`
- `last_2_steps`: `0.231`
- `last_3_steps`: `0.700`
- `full_trajectory`: `0.900`

Across Experiment 1 and Experiment 2, the final-step snapshot baseline detected `9/25` positive cases and missed or withheld judgment on `16/25` positive effective-override-loss cases.

## Repository Layout

- [data](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/data): source datasets, integrated result tables, metrics JSON files, and model response ledgers.
- [audits](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/audits): integrity, prompt-blindness, qualitative, pairwise, and statistical audit outputs.
- [robustness](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/robustness): Experiment 2 second-model robustness outputs.
- [baseline_ladder](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/baseline_ladder): Experiment 2 history-sensitivity baseline ladder outputs.
- [paper](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/paper): claim controls, paper scaffold, tables, and release-facing notes.
- [repro](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/repro): no-API local reproduction entry points.

## Reproduction

Local post-processing and analysis can be rerun without API calls:

```powershell
python integrate_flash_lite_trajectory_rater.py
python scripts/analyze_experiment1_trajectory_flash_lite.py
python integrate_flash_lite_snapshot_rater.py
python scripts/analyze_experiment1_full_flash_lite.py
python scripts/audit_experiment1_robustness.py
python integrate_experiment2_trajectory_rater.py
python scripts/analyze_experiment2_trajectory_flash_lite.py
python integrate_experiment2_snapshot_rater.py
python scripts/analyze_experiment2_full_flash_lite.py
python integrate_experiment2_robustness.py
python integrate_experiment2_baseline_ladder.py
```

Convenience wrappers are also provided:

- [repro/run_repro_no_api.sh](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/repro/run_repro_no_api.sh)
- [repro/run_repro_no_api.bat](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/repro/run_repro_no_api.bat)

API runners are included for completeness, but the public release is intended to be inspectable and reproducible from the committed local artifacts without hidden API calls in final analysis.

## Limitations

- Synthetic, author-generated trajectories only.
- One fixed primary model and one recorded run for the main reported comparison.
- No blinded human annotation study.
- Small sample sizes.
- One domain family rather than broad real-world coverage.
- Final-step snapshot is a deliberately weak low-context baseline, not a universal snapshot method.
- No real-world validation claim is supported by this repository.

## Public Release Notes

- Local workflow notes and task files are intentionally excluded from version control.
- Local environment files and secrets are intentionally excluded from version control.
- Reviewer-feedback files containing prohibited motivating wording were intentionally excluded from the public release commit.
