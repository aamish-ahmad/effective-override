# Data Schema

## Core Dataset Columns

The public datasets use a trajectory-oriented tabular schema built around:

- `trajectory_id`
- `pair_id`
- `condition`
- `steps_json`
- `ground_truth_crossing_present`
- `ground_truth_crossing_step`
- `ground_truth_state_sequence`
- release-specific descriptive fields such as `override_attempt`, `system_structure`, and `downstream_constraint`

## Integrated Trajectory Rater Columns

Integrated trajectory outputs add fields such as:

- `trajectory_rater_model`
- `trajectory_rater_crossing_present`
- `trajectory_rater_crossing_step`
- `trajectory_rater_state_sequence`
- `trajectory_rater_override_attempt`
- `trajectory_rater_system_structure`
- `trajectory_rater_downstream_constraint`
- `trajectory_rater_reason`
- `trajectory_rater_confidence`

## Integrated Snapshot Columns

Integrated snapshot outputs add fields such as:

- `snapshot_rater_model`
- `snapshot_rater_crossing_present`
- `snapshot_rater_crossing_step`
- `snapshot_rater_reason`
- `snapshot_rater_confidence`

## Derived Release Outputs

Derived release artifacts include integrated CSV tables, metrics JSON files, audit markdown files, robustness results, and baseline ladder summaries.
