# Packaging Gate Report

## Scope

Repository: `effective-override` local public release candidate  
Working tree base commit before packaging updates: `4ee7bf8`

## Gate P1: Public HEAD Safety

Status: `PASS`

Checks run against committed `HEAD`:

- forbidden public wording scan
- real API key assignment scan
- excluded task/env/reviewer-feedback file presence scan

Result:

- Forbidden public wording scan: clean.
- Real API key assignment scan: clean.
- Excluded task/env/secret/reviewer-feedback files: absent from committed `HEAD`.

Notes:

- Variable names such as `GEMINI_API_KEY` remain allowed where they are used as environment-variable identifiers rather than literal secrets.
- `.env.example` remains allowed as a placeholder template.

## Gate P2: README First-Screen Clarity

Status: `PASS`

Action taken:

- Rewrote `README.md` to reflect the current `ATB-v0` release rather than the earlier Experiment 0-only framing.

Verified near the top:

- `Agency Trajectory Benchmark v0` / `ATB-v0`
- `Human-in-the-loop is not human-in-control`
- `synthetic matched-control benchmark`
- `effective override loss`
- explicit no-real-world-validation disclaimer
- main results
- reproduction section

## Gate P3: Submission Artifact Present

Status: `WARN`

Result:

- `submission/apart_effective_override_submission.pdf`: missing

Action taken:

- Added `submission/README.md` with the required placement note.

Reason for warning:

- No fake PDF was created.

## Gate P4: No-API Reproduction

Status: `WARN`

Checks:

- `repro/run_repro_no_api.sh`: present
- `repro/run_repro_no_api.bat`: present
- `python -m py_compile integrate_experiment2_robustness.py`: passed
- `python -m py_compile integrate_experiment2_baseline_ladder.py`: passed
- `python -m py_compile run_experiment2_trajectory_rater_robustness.py`: passed
- `python -m py_compile run_experiment2_baseline_ladder_rater.py`: passed

Reproduction script run:

- Command: `bash repro/run_repro_no_api.sh`
- Outcome: shell/path warning rather than artifact failure
- Exact error:
- `wsl: Failed to start the systemd user session for 'root'. See journalctl for more details.`
- `repro/run_repro_no_api.sh: line 5: python: command not found`

Interpretation:

- The `.sh` wrapper is present, but this local Bash/WSL environment did not have `python` on the path. This is a packaging environment warning, not evidence that the repository artifacts are internally inconsistent.

## Gate P5: Results Consistency

Status: `PASS`

Verified committed artifact values:

- Experiment 1 trajectory kappa: `1.000`
- Experiment 1 snapshot kappa: `0.464`
- Experiment 2 trajectory kappa: `0.900`
- Experiment 2 snapshot kappa: `0.444`
- second-model robustness kappa: `0.900`
- baseline ladder `final_step`: `0.444`
- baseline ladder `last_2_steps`: `0.231`
- baseline ladder `last_3_steps`: `0.700`
- baseline ladder `full_trajectory`: `0.900`
- final-step snapshot missed or withheld judgment on `16/25` positive cases across both experiments

Action taken:

- Updated `README.md` wording to match committed metrics.

No metrics JSON or CSV artifacts were edited.

## Gate P6: Release Manifest

Status: `PASS`

Action taken:

- Added `release/public_release_manifest.md` covering committed artifacts and intentionally excluded files.

## Gate P7: Final Git Status and Commit Handling

Status: `PENDING_AT_REPORT_TIME`

Expected packaging-only staged files if committed:

- `README.md`
- `submission/README.md`
- `release/packaging_gate_report.md`
- `release/public_release_manifest.md`

The final status, staged scan, and commit hash should be recorded after staging these packaging-layer files.
