# Public Release Manifest

## Release Scope

This manifest describes the public-release contents committed in `4ee7bf8` for `ATB-v0`.

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

## Committed Robustness Files

- `run_experiment2_trajectory_rater_robustness.py`
- `integrate_experiment2_robustness.py`
- `robustness/README.md`
- `robustness/experiment2_robustness_results.csv`
- `robustness/experiment2_robustness_metrics.json`
- `robustness/experiment2_robustness_summary.md`
- `paper/science_gate_robustness_note.md`

## Committed Baseline Ladder Files

- `prompts/baseline_ladder_rater_prompt.md`
- `run_experiment2_baseline_ladder_rater.py`
- `integrate_experiment2_baseline_ladder.py`
- `baseline_ladder/README.md`
- `baseline_ladder/experiment2_baseline_ladder_results.csv`
- `baseline_ladder/experiment2_baseline_ladder_metrics.json`
- `baseline_ladder/experiment2_baseline_ladder_summary.md`
- `paper/baseline_ladder_note.md`

## Committed Audit Files

- `audits/experiment1_data_lineage_manifest.md`
- `audits/experiment1_pairwise_error_audit.md`
- `audits/experiment1_prompt_blindness_audit.md`
- `audits/experiment1_robustness_audit.md`
- `audits/experiment2_E2T08_false_positive_audit.md`
- `audits/experiment2_qualitative_audit.md`
- `audits/experiment2_qualitative_audit_v1.md`
- `scripts/audit_experiment1_robustness.py`

## Committed Paper and Report Files

- `paper/abstract_draft.md`
- `paper/claim_evidence_matrix.md`
- `paper/current_scientific_status.md`
- `paper/do_not_claim.md`
- `paper/figures_needed.md`
- `paper/limitations_section_draft.md`
- `paper/main_scaffold.md`
- `paper/related_work_todo.md`
- `paper/results_tables.md`
- `paper/reviewer_attack_response_table.md`
- `paper/reviewer_feedback_out_of_scope.md`
- `paper/reviewer_feedback_required_paper_changes.md`
- `paper/title_options.md`
- `README.md`
- `submission/README.md`

## Committed Reproduction Scripts

- `repro/run_repro_no_api.sh`
- `repro/run_repro_no_api.bat`
- `integrate_flash_lite_trajectory_rater.py`
- `integrate_flash_lite_snapshot_rater.py`
- `integrate_experiment2_trajectory_rater.py`
- `integrate_experiment2_snapshot_rater.py`
- `integrate_experiment2_robustness.py`
- `integrate_experiment2_baseline_ladder.py`
- `scripts/analyze_experiment1_trajectory_flash_lite.py`
- `scripts/analyze_experiment1_full_flash_lite.py`
- `scripts/analyze_experiment2_trajectory_flash_lite.py`
- `scripts/analyze_experiment2_full_flash_lite.py`

## Excluded Files and Why

- `CODEX_TASK_*.md`: local process/task files, not public release artifacts.
- `.env`, `.env.local`, `.env.*`, `secrets.txt`: secret-bearing local environment files.
- `paper/ground_truth_reviewer_feedback_digest.md`: excluded because it contains prohibited motivating wording unsuitable for the public release surface.
- `paper/reviewer_feedback_coverage_current_paper.md`: excluded because it contains prohibited motivating wording unsuitable for the public release surface.
- `data/experiment0.csv`: old pilot dataset not part of the current public release.
- `data/blind_rater_responses.md`: old pilot response ledger not part of the current public release.
- `data/blind_rater_responses_raw.md`: old pilot raw response ledger not part of the current public release.
- `data/snapshot_rater_responses.md`: old pilot snapshot ledger not part of the current public release.
- `data/experiment1_trajectory_rater_errors.md`: old mixed-model error ledger not part of the official public release.
- `data/experiment1_trajectory_rater_responses.md`: old mixed-model trajectory ledger not part of the official public release.
- `scripts/check_experiment1.py`: excluded from the public release commit because it contained prohibited real-world wording in validation literals.
- `scripts/check_experiment2_hard_controls.py`: excluded from the public release commit because it contained prohibited real-world wording in validation literals.
