# Public Release Manifest

## Release Scope

This manifest describes the `v1.0.0` public release of Agency Trajectory Benchmark.

## Committed Result Datasets

- `data/experiment1.csv`
- `data/experiment1_full_results_gemini_3_1_flash_lite.csv`
- `data/experiment1_with_trajectory_rater_gemini_3_1_flash_lite.csv`
- `data/experiment2_hard_controls_draft.csv`
- `data/experiment2_hard_controls_v1.csv`
- `data/experiment2_full_results_gemini_3_1_flash_lite.csv`
- `data/experiment2_with_trajectory_rater_gemini_3_1_flash_lite.csv`

## Committed Metrics Files

- `data/experiment1_trajectory_metrics_gemini_3_1_flash_lite.json`
- `data/experiment1_final_metrics_gemini_3_1_flash_lite.json`
- `data/experiment1_statistical_audit_gemini_3_1_flash_lite.json`
- `data/experiment2_trajectory_metrics_gemini_3_1_flash_lite.json`
- `data/experiment2_final_metrics_gemini_3_1_flash_lite.json`
- `baseline_ladder/experiment2_baseline_ladder_metrics.json`
- `robustness/experiment2_robustness_metrics.json`

## Committed Response Ledgers

- `data/experiment1_snapshot_rater_responses_gemini_3_1_flash_lite.md`
- `data/experiment1_trajectory_rater_responses_gemini_3_1_flash_lite.md`
- `data/experiment2_snapshot_rater_responses_gemini_3_1_flash_lite.md`
- `data/experiment2_trajectory_rater_responses_gemini_3_1_flash_lite.md`
- `robustness/experiment2_trajectory_rater_responses_robustness.md`
- `baseline_ladder/experiment2_last2_responses_gemini_3_1_flash_lite.md`
- `baseline_ladder/experiment2_last3_responses_gemini_3_1_flash_lite.md`

## Committed Release-Facing Files

- `README.md`
- `CITATION.cff`
- `LICENSE`
- `docs/`
- `reports/`
- `release/`

## Excluded Files and Why

- `CODEX_TASK_*.md`: local process files, not release artifacts
- `.env`, `.env.local`, `.env.*`, `secrets.txt`: local secret-bearing files
- `paper/ground_truth_reviewer_feedback_digest.md`: excluded from the public release surface
- `paper/reviewer_feedback_coverage_current_paper.md`: excluded from the public release surface
- `data/experiment0.csv`: older pilot dataset not part of this release
- `data/blind_rater_responses.md`: older pilot response ledger not part of this release
- `data/blind_rater_responses_raw.md`: older pilot raw response ledger not part of this release
- `data/snapshot_rater_responses.md`: older pilot snapshot ledger not part of this release
- `data/experiment1_trajectory_rater_errors.md`: older mixed-model error ledger not part of this release
- `data/experiment1_trajectory_rater_responses.md`: older mixed-model trajectory ledger not part of this release
- `scripts/check_experiment1.py`: excluded because it contains prohibited real-world wording in validation literals
- `scripts/check_experiment2_hard_controls.py`: excluded because it contains prohibited real-world wording in validation literals
