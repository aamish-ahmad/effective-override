"""Run official Flash Lite full-trajectory ratings for Experiment 2."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.env_utils import load_local_env


load_local_env()

import run_gemini_trajectory_rater_experiment1 as runner


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "experiment2_hard_controls_v1.csv"
PROMPT_PATH = ROOT / "prompts" / "blind_rater_prompt.md"
RUBRIC_PATH = ROOT / "rubric.md"
VALIDATOR_PATH = ROOT / "scripts" / "check_experiment2_hard_controls_v1.py"
RESPONSES_PATH = (
    ROOT / "data" / "experiment2_trajectory_rater_responses_gemini_3_1_flash_lite.md"
)
ERRORS_PATH = (
    ROOT / "data" / "experiment2_trajectory_rater_errors_gemini_3_1_flash_lite.md"
)
DEFAULT_MODEL = "gemini-3.1-flash-lite"
DEFAULT_SLEEP_SECONDS = 5.0


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


def build_prompt(template: str, trajectory: dict[str, object]) -> str:
    """Build the blind prompt from raw steps and ID only."""
    numbered_steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(trajectory["steps"], start=1)
    )
    blind_prompt = template.replace("{{TRAJECTORY_STEPS}}", numbered_steps).rstrip()
    rubric = RUBRIC_PATH.read_text(encoding="utf-8-sig").rstrip()
    return (
        f"{blind_prompt}\n\n"
        f"## Full project rubric\n\n{rubric}\n\n"
        f"trajectory_id: {trajectory['trajectory_id']}\n"
    )


def is_hard_quota_or_billing_error(error: Exception) -> bool:
    message = str(error).lower()
    daily_markers = (
        "generaterequestsperdayperprojectpermodel-freetier",
        "daily quota",
        "per day",
        "perday",
    )
    billing_markers = (
        "billing",
        "payment required",
        "insufficient credits",
        "credit balance",
        "quota has been exhausted",
    )
    return (
        runner.is_rate_limit_error(error)
        and any(marker in message for marker in daily_markers)
    ) or any(marker in message for marker in billing_markers)


def configure_runner() -> None:
    """Set every dataset- and run-specific dependency before runner.main()."""
    runner.DATA_PATH = DATA_PATH
    runner.PROMPT_PATH = PROMPT_PATH
    runner.RESPONSES_PATH = RESPONSES_PATH
    runner.ERRORS_PATH = ERRORS_PATH
    runner.VALIDATOR_PATH = VALIDATOR_PATH
    runner.DEFAULT_MODEL = DEFAULT_MODEL
    runner.DEFAULT_SLEEP_SECONDS = DEFAULT_SLEEP_SECONDS
    runner.validate_dataset = validate_dataset
    runner.build_prompt = build_prompt
    runner.is_daily_quota_error = is_hard_quota_or_billing_error


def main() -> int:
    configure_runner()
    return runner.main()


if __name__ == "__main__":
    raise SystemExit(main())

