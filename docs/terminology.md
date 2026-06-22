# Terminology

## Agency Trajectory Benchmark (ATB)

ATB is the project name for this repository and benchmark family.

## Effective Override Loss

Effective override loss is the earliest point in a trajectory where a human override action is attempted or plausibly available, but no longer meaningfully changes the next consequential state because of system structure, with persistence or downstream constraint.

## Matched Control

A matched control is a superficially similar trajectory in which friction, delay, warnings, or adverse outcomes may occur, but the human override still changes the next consequential transition.

## Trajectory Evaluation

Trajectory evaluation gives the rater the full ordered sequence of steps.

## Final-Step Snapshot

Final-step snapshot gives the rater only the last visible state. It is a deliberately low-context baseline used to test whether the construct is history-sensitive.

## Baseline Ladder

The baseline ladder compares final-step, last-two-step, last-three-step, and full-trajectory context windows on Experiment 2.
