"""Run official final-step-only Flash Lite ratings for Experiment 2."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.env_utils import load_local_env


load_local_env()

import run_gemini_snapshot_rater_experiment1_flash_lite as snapshot_runner


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "experiment2_hard_controls_v1.csv"
PROMPT_PATH = ROOT / "prompts" / "snapshot_rater_prompt.md"
VALIDATOR_PATH = ROOT / "scripts" / "check_experiment2_hard_controls_v1.py"
RESPONSES_PATH = (
    ROOT / "data" / "experiment2_snapshot_rater_responses_gemini_3_1_flash_lite.md"
)
ERRORS_PATH = (
    ROOT / "data" / "experiment2_snapshot_rater_errors_gemini_3_1_flash_lite.md"
)
DEFAULT_MODEL = "gemini-3.1-flash-lite"
DEFAULT_SLEEP_SECONDS = 5.0
EXPECTED_COUNT = 20


def validate_dataset() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode:
        raise RuntimeError("Experiment 2 validation failed; no API calls were made")


def configure_runner() -> None:
    snapshot_runner.DATA_PATH = DATA_PATH
    snapshot_runner.PROMPT_PATH = PROMPT_PATH
    snapshot_runner.RESPONSES_PATH = RESPONSES_PATH
    snapshot_runner.ERRORS_PATH = ERRORS_PATH
    snapshot_runner.DEFAULT_MODEL = DEFAULT_MODEL
    snapshot_runner.DEFAULT_SLEEP_SECONDS = DEFAULT_SLEEP_SECONDS
    snapshot_runner.EXPECTED_COUNT = EXPECTED_COUNT


def main() -> int:
    validate_dataset()
    configure_runner()
    return snapshot_runner.main()


if __name__ == "__main__":
    raise SystemExit(main())
