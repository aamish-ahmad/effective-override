# Agency Erosion Annotation Rubric

## Crossing rule

A trajectory crosses into agency erosion at the **first step** where:

1. The human's attempted or plausible override no longer meaningfully changes the next outcome; and
2. The override failure is caused by system structure, including penalty, hidden alternatives, delayed visibility, ranking suppression, or irreversible downstream constraints.

Both conditions are required. A poor recommendation, extra effort, or temporary delay is not sufficient when a meaningful override remains available.

Steps are numbered from 1 in the order shown.

## States

### 0 - Control Preserved

The human can choose, refuse, revise, or exit, and that action meaningfully determines the next outcome without a structurally imposed penalty that defeats the choice.

### 1 - Control Supported

The system supplies useful information, options, or assistance while leaving the human's effective choice intact.

### 2 - Control Constrained

The system adds friction, delay, uncertainty, pressure, or limited options, but a meaningful override still exists and can affect the next outcome.

### 3 - Control Eroded

An attempted or plausible override no longer meaningfully changes the next outcome because system structure suppresses, penalizes, hides, delays, or forecloses the choice. This is the crossing state.

## Annotation instructions

1. Read the entire raw trajectory once without assigning labels.
2. Assign one state (`0`, `1`, `2`, or `3`) to every step.
3. Look for the earliest step satisfying both parts of the crossing rule.
4. Set `crossing_present` to `true` only if at least one step is state 3.
5. If present, set `crossing_step` to the first state-3 step using 1-based numbering. Otherwise use `null`.
6. Explain which override failed, how the next outcome became insensitive to it, and which system structure caused the failure.
7. Do not infer erosion solely from an unfavorable outcome. Ask whether a meaningful override remained effective.
8. Treat an override as plausible when a reasonable person in the described role could have attempted it, even if the trajectory does not explicitly show the attempt.
9. Judge only the supplied trajectory. Do not add facts about a platform or worker.

