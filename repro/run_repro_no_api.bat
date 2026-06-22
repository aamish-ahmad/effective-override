@echo off
setlocal
cd /d "%~dp0\.."
python integrate_flash_lite_trajectory_rater.py || exit /b 1
python scripts\analyze_experiment1_trajectory_flash_lite.py || exit /b 1
python integrate_flash_lite_snapshot_rater.py || exit /b 1
python scripts\analyze_experiment1_full_flash_lite.py || exit /b 1
python scripts\audit_experiment1_robustness.py || exit /b 1
