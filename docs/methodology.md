# Methodology

ATB is a synthetic matched-control benchmark for effective override loss in human-in-the-loop systems.

## Construct

The benchmark uses a trajectory-level crossing rule. A crossing occurs at the earliest step where:

1. a human override is attempted or plausibly available
2. the override no longer meaningfully changes the next outcome trajectory
3. the failure is caused by system structure
4. the loss persists or creates downstream constraint

Bad outcomes alone do not satisfy the rule.

## Evaluation Design

The current release compares:

- full-trajectory evaluation
- final-step snapshot evaluation
- Experiment 2 robustness with a second model
- Experiment 2 baseline ladder windows of increasing context

## Datasets

- Experiment 1: 30 trajectories, 15 matched pairs
- Experiment 2: 20 trajectories, 10 matched pairs, with lexical hard controls

## Claim Boundary

The repository supports a synthetic benchmark claim only. It does not support a real-world validation claim.
