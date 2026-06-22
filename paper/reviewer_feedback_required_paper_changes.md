# Required Paper Changes from Ground-Truth Reviewer Feedback

## Change Policy

These are proposed edits to the current scaffold. They add framing,
qualifications, and future-work commitments; they do not add new empirical
results.

## Must Add

### 1. Reviewer-Motivated Observability Framing

**Target:** Introduction, immediately after “human-in-the-loop does not imply
human-in-control.”

Add a narrow version of the feedback's strongest insight:

> A detector may fail before the relevant evidence is observable in its input,
> not merely because its classifier is weak. In our benchmark, the isolated
> final state often omits the earlier override attempt and system response needed
> to determine whether control was lost.

Qualify that the current experiments test final-state context omission, not
early-turn adversarial conversations.

### 2. Architecture Framing

**Target:** Introduction and Discussion.

Describe the trajectory/snapshot contrast as an **observability and evaluation-
interface problem**. State that final-step input structurally withholds temporal
relations needed by the rubric. Do not claim that classifier quality is
irrelevant: only one model and one final-step interface were tested.

### 3. Limitation: One Model and One Run

**Target:** Abstract qualifier and Limitations.

Retain and emphasize:

- one fixed LLM model;
- one recorded response per item/view;
- no stochastic stability estimate;
- no second monitor or model family;
- no prompt-intervention study.

### 4. Limitation: Synthetic, Author-Generated Examples

**Target:** Benchmark Design, Limitations, and Conclusion.

State that cases and labels were authored under the proposed construct. Audits
improve consistency but do not establish independent construct validity or
ecological validity.

### 5. Limitation: No Confidence/Investment Crossing Curves

**Target:** Limitations.

Add:

> The current benchmark does not model turn-level monitor confidence, user
> investment or lock-in, or the point at which those trajectories cross. Its
> crossing labels describe override effectiveness, not confidence-versus-
> investment dynamics.

### 6. Future Work: Multi-Model Robustness

**Target:** Future Work.

Evaluate multiple monitor/rater models, repeated runs, prompt variants,
calibration, abstention, and failure consistency. Report whether the
trajectory/snapshot gap persists across model families.

### 7. Future Work: Confidence versus Lock-In/Investment Trajectories

**Target:** Future Work.

Define turn-level confidence and investment/lock-in variables, preregister their
measurement, and test whether investment becomes consequential before monitor
confidence reaches an intervention threshold.

### 8. Future Work: Handoff Signature and Response Latency

**Target:** Future Work, clearly outside current results.

Test whether handoff events and response latency provide content-agnostic signals
that complement text-based trajectory evaluation. Do not claim deployment value
until latency data and baselines exist.

### 9. Future Work: Real-World Case Intake

**Target:** Future Work and Reproducibility/Ethics note.

Specify consent, de-identification, provenance, privacy review, annotation,
adjudication, and domain-expert review before real cases enter a future
Experiment 3. Real observations may motivate the work but cannot validate the
current synthetic experiments.

### 10. Future Work: Human Annotation

**Target:** Future Work.

Although not solved by the current reviewer evidence, the current paper's own
validation gap requires blinded independent human annotators, inter-rater
reliability, adjudication, and stakeholder/domain-expert review.

## Must Preserve from Current Scaffold

- Exact Experiment 1 and Experiment 2 dataset sizes.
- “Final-step-only baseline” terminology.
- Snapshot uncertainty and covered-case denominators.
- The E2T08 bad-outcome boundary case.
- Synthetic seed-benchmark framing and no-real-world-validation conclusion.

## Must Not Add

1. **Generated-code invariant extraction** into this paper.
2. **Property-based testing comparisons** into this paper.
3. **Formal verification claims** into this paper.
4. **Claims about named ride-hailing companies** or their conduct.
5. **Real-world validation claims** based on motivation or synthetic results.
6. TrajectoryCheck stability scoring, passed-gate arithmetic, or authentication examples.
7. Handoff Signature, response latency, confidence curves, or investment curves as if they were current measured results.

## Suggested Revision Order

1. Add the observability/architecture paragraph to the Introduction.
2. Add the confidence/investment non-coverage statement to Limitations.
3. Expand Future Work with multi-model, human, curve, latency, and real-case studies.
4. Recheck Abstract and Conclusion for one-model, synthetic, and no-real-world qualifiers.
5. Run the claim-evidence and do-not-claim audit after prose revision.

## Final Conclusion

The current Agency Trajectory Benchmark paper directly addresses the strongest Trajectory Blindness feedback about invisible early signals and architectural blindspots, but it does not yet address confidence/investment crossing curves, Handoff Signature development, multi-model robustness, or human annotation. TrajectoryCheck-specific critiques should remain out of scope for this paper.
