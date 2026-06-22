# Agency Trajectory Benchmark

Agency Trajectory Benchmark is a synthetic benchmark for testing whether evaluators can detect when a human's apparent override stops changing the outcome of an AI-mediated workflow.

The project studies a narrow failure mode: effective override loss. A system may still offer choices, appeals, confirmations, or other human-in-the-loop actions, while the actual trajectory has already become insensitive to those actions. In that case, the human remains present in the workflow but no longer has effective control over the next consequential state.

This release contains two matched-control experiments, model response ledgers, integrated metrics, robustness checks, a baseline ladder, audit notes, and no-API reproduction scripts.

The main result is simple: final-state evaluation misses many positive cases that are visible from the ordered trajectory. Across both experiments, the final-step snapshot baseline detected 9/25 positive cases and missed or withheld judgment on 16/25 positive effective-override-loss cases.

This is a synthetic benchmark and research artifact. It is not a real-world validation study and does not make claims about deployed platforms.

Version: `v1.0.0`

## Overview

| Item | Value |
|---|---|
| Project | Agency Trajectory Benchmark |
| Repository | `effective-override` |
| Release | `v1.0.0` |
| Construct | effective override loss |
| Scope | synthetic matched-control benchmark |
| Comparison | full trajectory vs final-step snapshot |

## Main Results

| Evaluation setting | Agreement | Cohen's kappa |
|---|---:|---:|
| Experiment 1 trajectory | 1.000 | 1.000 |
| Experiment 1 snapshot | 0.760 covered-case | 0.464 |
| Experiment 2 trajectory | 0.950 | 0.900 |
| Experiment 2 snapshot | 0.722 covered-case | 0.444 |
| Experiment 2 robustness | 0.950 | 0.900 |
| Experiment 2 ladder: final_step | 0.722 covered-case | 0.444 |
| Experiment 2 ladder: last_2_steps | 0.632 covered-case | 0.231 |
| Experiment 2 ladder: last_3_steps | 0.850 | 0.700 |
| Experiment 2 ladder: full_trajectory | 0.950 | 0.900 |

## Quick Start

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the local no-API integration and analysis steps:

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

Additional wrappers are available under `repro/`.

## Reproduction

The repository includes committed datasets, response ledgers, integrated outputs, audits, and release-facing summaries. Local post-processing can be rerun without API calls. See [docs/reproducibility.md](docs/reproducibility.md).

## Repository Map

- [data/](data/): datasets, response ledgers, integrated outputs, and metrics
- [docs/](docs/): terminology, methodology, schema, reproducibility, and data availability notes
- [reports/](reports/): release-facing summaries of results, statistical framing, and limitations
- [audits/](audits/): integrity, prompt-blindness, qualitative, and statistical audits
- [robustness/](robustness/): Experiment 2 second-model robustness outputs
- [baseline_ladder/](baseline_ladder/): Experiment 2 context-window ladder outputs
- [paper/](paper/): manuscript scaffold and claim-control notes
- [release/public_release_manifest.md](release/public_release_manifest.md): committed release inventory

## Key Outputs

- [reports/results.md](reports/results.md)
- [data/experiment1_final_metrics_gemini_3_1_flash_lite.json](data/experiment1_final_metrics_gemini_3_1_flash_lite.json)
- [data/experiment2_final_metrics_gemini_3_1_flash_lite.json](data/experiment2_final_metrics_gemini_3_1_flash_lite.json)
- [robustness/experiment2_robustness_metrics.json](robustness/experiment2_robustness_metrics.json)
- [baseline_ladder/experiment2_baseline_ladder_metrics.json](baseline_ladder/experiment2_baseline_ladder_metrics.json)

## Data Availability

The committed public release includes the synthetic benchmark datasets, committed response ledgers used in the release, integrated outputs, audit files, and release-facing reports. See [docs/data_availability.md](docs/data_availability.md).

## Paper

Paper manuscript is in preparation. Paper scaffold and claim-control notes are included under `paper/`.

If a public paper PDF is later added, the expected path is `paper/effective_override_v1_0.pdf`.

## Citation

If you use this repository, cite the software and research artifact metadata in [CITATION.cff](CITATION.cff).

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Limitations

- synthetic, author-generated benchmark only
- one fixed primary model and one recorded primary run
- no blinded human annotation study in the current release
- small sample sizes
- one domain family rather than broad deployment coverage
- final-step snapshot is a narrow low-context baseline, not a statement about all snapshot methods
- no real-world validation claim is supported by this repository
