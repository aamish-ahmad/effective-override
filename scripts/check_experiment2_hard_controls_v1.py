"""Validate the Experiment 2 hard-control v1 dataset."""

from pathlib import Path

import check_experiment2_hard_controls as validator


validator.DATA_PATH = (
    Path(__file__).parents[1] / "data" / "experiment2_hard_controls_v1.csv"
)


if __name__ == "__main__":
    raise SystemExit(validator.main())
