"""Integrate official Flash Lite snapshot ratings into Experiment 2."""

from pathlib import Path

import integrate_flash_lite_snapshot_rater as integrator


ROOT = Path(__file__).parent


def configure() -> None:
    integrator.SOURCE_PATH = ROOT / "data" / "experiment2_hard_controls_v1.csv"
    integrator.TRAJECTORY_RESULTS_PATH = (
        ROOT
        / "data"
        / "experiment2_with_trajectory_rater_gemini_3_1_flash_lite.csv"
    )
    integrator.RESPONSES_PATH = (
        ROOT
        / "data"
        / "experiment2_snapshot_rater_responses_gemini_3_1_flash_lite.md"
    )
    integrator.OUTPUT_PATH = (
        ROOT / "data" / "experiment2_full_results_gemini_3_1_flash_lite.csv"
    )
    integrator.EXPECTED_COUNT = 20


def main() -> int:
    configure()
    return integrator.main()


if __name__ == "__main__":
    raise SystemExit(main())
