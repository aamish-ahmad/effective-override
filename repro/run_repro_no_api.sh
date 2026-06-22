#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")/.."
python integrate_flash_lite_trajectory_rater.py
python scripts/analyze_experiment1_trajectory_flash_lite.py
python integrate_flash_lite_snapshot_rater.py
python scripts/analyze_experiment1_full_flash_lite.py
python scripts/audit_experiment1_robustness.py
