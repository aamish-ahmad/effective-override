# Agency Trajectory Benchmark (ATB)

Agency Trajectory Benchmark (ATB) is a synthetic matched-control benchmark for detecting effective override loss in human-in-the-loop systems.

**Core sentence:** Human-in-the-loop is not human-in-control.

Current release: `v0.1.0`

This repository packages the current public research artifact for ATB. It focuses on a narrow operational construct, **effective override loss**, and compares full-trajectory evaluation against lower-context baselines. The repository does not make any real-world validation claim.

## At a Glance

| Item | Value |
|---|---|
| Project | Agency Trajectory Benchmark (ATB) |
| Repository | `effective-override` |
| Release | `v0.1.0` |
| Construct | Effective override loss |
| Scope | Synthetic matched-control benchmark |
| Primary comparison | Full trajectory vs final-step snapshot |
| Public claim boundary | No real-world validation claim |

## Main Results

| Evaluation setting | Agreement | Cohen's kappa | Notes |
|---|---:|---:|---|
| Experiment 1 trajectory | 1.000 | 1.000 | 30 trajectories |
| Experiment 1 snapshot | 0.760 covered-case | 0.464 | 5 positive yes, 5 no, 5 uncertain |
| Experiment 2 trajectory | 0.950 | 0.900 | 20 trajectories |
| Experiment 2 snapshot | 0.722 covered-case | 0.444 | 4 positive yes, 5 no, 1 uncertain |
| Experiment 2 robustness | 0.950 | 0.900 | second-model check |
| Experiment 2 ladder: final_step | 0.722 covered-case | 0.444 | final visible state only |
| Experiment 2 ladder: last_2_steps | 0.632 covered-case | 0.231 | partial recent history |
| Experiment 2 ladder: last_3_steps | 0.850 | 0.700 | broader recent history |
| Experiment 2 ladder: full_trajectory | 0.950 | 0.900 | full ordered context |

Across Experiment 1 and Experiment 2, the final-step snapshot baseline detected `9/25` positive cases and missed or withheld judgment on `16/25` positive cases.

## Quick Start

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run local no-API integration and analysis steps:

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

Local wrappers are also included under [repro](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/repro).

## Reproduction

Reproduction for the committed public artifact is local and file-backed:

- source datasets are committed under [data](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/data)
- model response ledgers are committed under `data/`, `robustness/`, and `baseline_ladder/`
- local post-processing scripts regenerate integrated CSV and JSON outputs without API calls
- final analysis does not depend on hidden network requests

See [docs/reproducibility.md](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/docs/reproducibility.md) for the release-facing reproducibility notes.

## Repository Map

| Path | Purpose |
|---|---|
| [data](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/data) | datasets, response ledgers, integrated results, metrics |
| [docs](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/docs) | methodology, schema, terminology, reproducibility, availability |
| [reports](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/reports) | release-facing results and limitation summaries |
| [audits](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/audits) | integrity, prompt-blindness, qualitative, and statistical audits |
| [robustness](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/robustness) | Experiment 2 second-model robustness check |
| [baseline_ladder](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/baseline_ladder) | Experiment 2 history-sensitivity ladder |
| [paper](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/paper) | manuscript scaffold and claim-control notes |
| [repro](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/repro) | local reproduction wrappers |

## Key Outputs

- Experiment 1 final metrics: [data/experiment1_final_metrics_gemini_3_1_flash_lite.json](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/data/experiment1_final_metrics_gemini_3_1_flash_lite.json)
- Experiment 2 final metrics: [data/experiment2_final_metrics_gemini_3_1_flash_lite.json](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/data/experiment2_final_metrics_gemini_3_1_flash_lite.json)
- Experiment 2 robustness metrics: [robustness/experiment2_robustness_metrics.json](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/robustness/experiment2_robustness_metrics.json)
- Experiment 2 baseline ladder metrics: [baseline_ladder/experiment2_baseline_ladder_metrics.json](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/baseline_ladder/experiment2_baseline_ladder_metrics.json)
- Packaging gate report: [release/packaging_gate_report.md](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/release/packaging_gate_report.md)

## Data Availability

All synthetic benchmark datasets, model response ledgers included in this release, integrated outputs, and public audit files are committed in the repository. See [docs/data_availability.md](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/docs/data_availability.md) for the exact release-facing scope and exclusions.

## Paper

Paper manuscript is in preparation. Paper scaffold and claim-control notes are included under [paper](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/paper).

If a public paper PDF is later added, the expected path is `paper/effective_override_v0_1.pdf`.

## Citation

If you use this software or research artifact, please cite the repository metadata in [CITATION.cff](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/CITATION.cff).

## License

This repository is released under the MIT License. See [LICENSE](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/LICENSE).

## Limitations

- Synthetic, author-generated benchmark only.
- One fixed primary model and one recorded primary run.
- No blinded human annotation study in the current release.
- Small sample sizes.
- One domain family rather than broad deployment coverage.
- Final-step snapshot is a narrow low-context baseline, not a statement about all snapshot methods.
- No real-world validation claim is supported by this repository.
