# Experiment Report

## Scope

This release contains two synthetic matched-control experiments for effective override loss.

## Experiment 1

Experiment 1 is the ordinary matched-control benchmark. It contains 30 trajectories arranged as 15 matched pairs and supports the primary trajectory-versus-snapshot comparison.

## Experiment 2

Experiment 2 is the lexical hard-control benchmark. It contains 20 trajectories arranged as 10 matched pairs and tests whether the trajectory advantage persists when surface wording is more adversarially controlled.

## Robustness and Ladder Checks

The release also includes:

- an Experiment 2 second-model robustness check with kappa `0.900`
- an Experiment 2 baseline ladder with context-window kappas `0.444`, `0.231`, `0.700`, and `0.900`

## Release Interpretation

The current artifact is best read as a public synthetic benchmark release for trajectory-sensitive evaluation of effective override loss. It is not a real-world validation package.
