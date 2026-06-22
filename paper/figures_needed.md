# Figures Needed

These are proposed figures, not completed figures. Every caption must state that
the data are synthetic and the results use one fixed LLM rater.

## Figure 1. Benchmark Pipeline Diagram

**Purpose:** Show the controlled workflow from authored matched pair to blind
trajectory/snapshot prompts, raw ledgers, strict integration, metrics, and audits.

**Elements:**

- Synthetic positive/control pair.
- Hidden design labels.
- Full-trajectory branch and final-step-only branch.
- Same fixed model on both branches.
- Response validation and deterministic local analysis.
- Claim-boundary and failure audits.

**Avoid:** Any implication that model outputs create ground truth.

## Figure 2. Trajectory versus Snapshot Comparison

**Purpose:** Compare agreement, positive detection, and uncertainty across both
experiments.

**Preferred form:** Two experiment panels with point/bar estimates and explicit
denominators. Show uncertain as its own category rather than silently excluding
it.

**Avoid:** A single pooled score that obscures dataset differences.

## Figure 3. State Transition and Crossing Diagram

**Purpose:** Explain states 0-3 and the first transition to state 3.

**Elements:**

- State 0 control preserved.
- State 1 control supported.
- State 2 control constrained.
- State 3 control eroded.
- Override attempt, system response, and first ineffective next-state transition.
- Explicit annotation: bad outcome alone does not create state 3.

## Figure 4. E2T08 Boundary Case Schematic

**Purpose:** Visualize why the hard negative is a model error rather than a label
correction.

**Two lanes:**

- Requested action: remove Wednesday -> Wednesday removed (effective override).
- Outcome utility: no replacement hours -> bad outcome.

Mark the rater's mistaken inference from outcome utility to action inefficacy.

## Figure 5. Claim-Evidence Map

**Purpose:** Separate supported benchmark claims from unsupported real-world
claims.

**Layers:**

1. Strong within-benchmark results.
2. Moderate construct and seed-benchmark claims.
3. Future validation targets.
4. Prohibited real-world, legal, universal, and named-actor conclusions.

## Production Checklist

- Source all numbers directly from final metrics JSON files.
- Add dataset sizes and uncertainty denominators in captions.
- Use accessible colors and non-color encodings.
- Do not use real company branding, screenshots, or interface replicas.
- Store figure-generation code separately from empirical source artifacts.
