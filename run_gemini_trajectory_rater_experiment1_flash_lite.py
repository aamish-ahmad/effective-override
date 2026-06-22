"""Run the official Gemini Flash Lite trajectory ratings for Experiment 1.

This entry point reuses the validated parsing, response validation, persistence,
and retry implementation from the original runner while replacing every run-
specific path and default. It never reads the legacy mixed-model output files.
"""

from __future__ import annotations

from pathlib import Path

from scripts.env_utils import load_local_env


load_local_env()

import run_gemini_trajectory_rater_experiment1 as runner


ROOT = Path(__file__).parent
RESPONSES_PATH = (
    ROOT
    / "data"
    / "experiment1_trajectory_rater_responses_gemini_3_1_flash_lite.md"
)
ERRORS_PATH = (
    ROOT
    / "data"
    / "experiment1_trajectory_rater_errors_gemini_3_1_flash_lite.md"
)
RUBRIC_PATH = ROOT / "rubric.md"
DEFAULT_MODEL = "gemini-3.1-flash-lite"
DEFAULT_SLEEP_SECONDS = 5.0


def is_hard_quota_or_billing_error(error: Exception) -> bool:
    """Return true for quota failures that cannot succeed during this run."""
    message = str(error).lower()
    daily_quota_markers = (
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
        and any(marker in message for marker in daily_quota_markers)
    ) or any(marker in message for marker in billing_markers)


def build_prompt(template: str, trajectory: dict[str, object]) -> str:
    """Build a blind prompt from steps only, with no CSV labels or metadata."""
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


def configure_runner() -> None:
    """Apply the model-specific configuration before any files are read."""
    runner.RESPONSES_PATH = RESPONSES_PATH
    runner.ERRORS_PATH = ERRORS_PATH
    runner.DEFAULT_MODEL = DEFAULT_MODEL
    runner.DEFAULT_SLEEP_SECONDS = DEFAULT_SLEEP_SECONDS
    runner.build_prompt = build_prompt
    runner.is_daily_quota_error = is_hard_quota_or_billing_error


def main() -> int:
    configure_runner()
    return runner.main()


if __name__ == "__main__":
    raise SystemExit(main())

