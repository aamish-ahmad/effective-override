# Agency Trajectory Benchmark v0: Main Paper Scaffold

## Paper Contract

This scaffold supports one core claim:

> Full-trajectory evaluation outperformed final-step-only snapshot evaluation in two synthetic matched-control experiments, including lexical hard controls.

Every section must preserve the following qualifiers: synthetic, authored labels,
one fixed model, one recorded run, final-step-only baseline, and no real-world
validation.

## 1. Introduction

### 1.1 Problem

- Human-in-the-loop does not necessarily mean human-in-control.
- A system may display choices or accept an override request while subsequent allocation, routing, review, or scheduling no longer responds to that choice.
- Endpoint quality alone cannot distinguish a bad outcome after an effective choice from an outcome produced after the choice stopped mattering.

Effective override loss is an observability problem: in many trajectories, the
relevant control-loss signal is not available in the final visible state. This
makes the failure architectural rather than merely a classifier weakness. An
early action can lose causal influence before that loss becomes legible in the
current text or output presented to a detector.

The full trajectory matters because control loss is a process, not a point. It
links the human action, the system response, and the downstream transition;
final-state evaluation can omit those relations even when the endpoint itself is
accurately classified.

### 1.2 Construct

- Introduce **effective override loss** as a narrow, testable construct.
- State that it is not a complete theory or measure of human agency.
- Motivate trajectory-level evaluation: the failed action and structural mechanism may appear before, and disappear from, the final visible state.

### 1.3 Contribution Summary

1. A four-state trajectory rubric with an explicit first-crossing rule.
2. Two synthetic matched-control experiments totaling 50 trajectories and 25 pairs.
3. A controlled comparison between full trajectories and isolated final-step snapshots using one fixed model.
4. A lexical hard-control experiment and a preserved hard-negative failure analysis.
5. Data-integrity, prompt-blindness, reproducibility, and claim-boundary audits.

### 1.4 Optional Motivation

An anonymized motivating example may be used only to explain the research
question. It must be de-identified, fact-checked, privacy-reviewed, and labeled
as motivation rather than evidence. If those conditions are not met, omit it
and use a generic synthetic vignette.

## 2. Construct: Effective Override Loss

### 2.1 Attempted or Plausible Override

Define an override as a human action that could reasonably refuse, revise,
redirect, appeal, or exit the current workflow. An explicit attempt is strongest;
a plausible override is permitted only when supported by the supplied trajectory.

### 2.2 Reduced Causal Influence

The core test is counterfactual sensitivity at the next transition: does the
human action meaningfully change the next-state outcome trajectory? A crossing
requires that the override no longer does so.

### 2.3 System-Structured Constraint

The loss must arise from workflow structure, such as penalties, hidden
alternatives, delayed visibility, ranking effects, decoupled settings, or
downstream constraints. Friction alone is insufficient.

### 2.4 Persistence and Downstream Lock-In

Persistent effects or downstream closure strengthen evidence that the override
has ceased to matter. Examples include schedule closure, decision issuance,
allocation carry-forward, or a review arriving after the consequential event.
Do not infer persistence when the trajectory shows continued future access.

### 2.5 Bad Outcome versus Agency Erosion

- Bad outcome plus effective override: no crossing.
- Good-looking interface plus ineffective override: possible crossing.
- Warning, delay, pressure, or fewer options: state 2 while a meaningful action still changes the next outcome.
- Structurally ineffective action: state 3 at the first such step.

## 3. Benchmark Design

### 3.1 Matched Controls

Each pair contains one `erosion_positive` and one `matched_control` with a shared
domain and override target. The decisive difference is whether the override
changes the consequential transition.

### 3.2 State Labels

| State | Name | Operational meaning |
|---:|---|---|
| 0 | Control Preserved | Human action meaningfully determines the next outcome. |
| 1 | Control Supported | Assistance or information preserves effective choice. |
| 2 | Control Constrained | Friction or pressure exists, but override remains effective. |
| 3 | Control Eroded | System structure makes the override ineffective. |

Describe the canonical crossing from state 2, control constrained, to state 3,
control eroded. Note that the first state 3 defines the crossing even if the
previous state is 0 or 1.

### 3.3 Two Evaluation Views

- **Trajectory evaluation:** complete ordered steps plus blind rubric.
- **Final-step snapshot baseline:** final visible state and its index only.
- Use â€œfinal-step-only baseline,â€ not â€œall snapshot methods.â€

### 3.4 Prompt Blindness

Rater prompts exclude condition, positive/control identity, ground-truth crossing,
ground-truth states, and the other rater's output. Cite the static
prompt-construction audit and state that it is not a captured network-payload
audit.

### 3.5 Evaluation Metrics

- Binary agreement and Cohen's kappa; exclude uncertain rows from snapshot binary denominators and report coverage separately.
- False positives, false negatives, and uncertainty.
- Crossing-step absolute error for valid paired integer steps.
- Positive detection and lead-time comparison.
- Paired correctness with uncertain treated as incorrect.

## 4. Experiment 1: Ordinary Synthetic Matched Controls

### 4.1 Dataset

- 30 five-step trajectories.
- 15 erosion positives and 15 matched controls.
- Ordinary synthetic workflow contrasts without the systematic lexical adversary used in Experiment 2.

### 4.2 Trajectory Result

- Agreement: `1.000`; kappa: `1.000`.
- False positives/false negatives/uncertain: `0/0/0`.
- Crossing-step mean absolute error: `0.067`; exact accuracy: `0.933`; within-one-step accuracy: `1.000`.

### 4.3 Snapshot Result

- Covered-case agreement: `0.760` over 25 non-uncertain rows; kappa: `0.464`.
- False positives/false negatives/uncertain: `1/5/5`.
- Positive yes/no/uncertain: `5/5/5`.

### 4.4 Comparison

- Snapshot missed or was uncertain on `10/15` positives.
- Both views detected five positives; trajectory detection was one step earlier in all five, for mean lead-time gain `1.000`.
- Paired correctness: `19` both correct, `11` trajectory-only correct, `0` snapshot-only correct, `0` both incorrect/uncertain.
- If reporting the exact paired p-value (`0.0009765625`), describe it only as a fixed synthetic-benchmark discordance summary.

## 5. Experiment 2: Lexical Hard Controls

### 5.1 Dataset and Purpose

- 20 five-step trajectories.
- 10 erosion positives and 10 matched controls.
- Positives minimize obvious coercive words.
- Controls deliberately include warning, risk, penalty, delay, or bad-outcome language while preserving an effective override.
- Five pairs were revised after qualitative audit to reduce ambiguity and improve symmetry.

### 5.2 Trajectory Result

- Agreement: `0.950`; kappa: `0.900`.
- False positives/false negatives/uncertain: `1/0/0`.
- Positive yes/no/uncertain: `10/0/0`.

### 5.3 Snapshot Result

- Covered-case agreement: `0.722` over 18 non-uncertain rows; kappa: `0.444`.
- False positives/false negatives/uncertain: `0/5/2`.
- Positive yes/no/uncertain: `4/5/1`.

### 5.4 Comparison

- Snapshot missed or was uncertain on `6/10` positives; trajectory missed or was uncertain on `0/10`.
- Both views detected four positives; trajectory was earlier in two and tied in two, with mean lead-time gain `0.500`.
- Paired correctness: `13` both correct, `6` trajectory-only correct, `0` snapshot-only correct, `1` both incorrect/uncertain.

### 5.5 E2T08

Introduce E2T08 as the sole trajectory false positive and defer detailed analysis
to Section 7. Preserve its audit classification:
`ground_truth_control_correct_model_failed`; recommendation:
`keep_as_hard_negative`.

## 6. Results

Use the tables in `paper/results_tables.md`. The results narrative should:

1. Lead with dataset-specific estimates, not a universal average.
2. Report snapshot uncertainty and denominator beside agreement.
3. Separate binary detection from crossing-step timing.
4. State that both views use the same fixed model, reducing one comparison confound but not establishing model independence.
5. Avoid causal language about real systems.

### 6.1 Aggregate Snapshot Miss Result

Across Experiment 1 and Experiment 2, the final-step snapshot baseline missed or
withheld judgment on **16/25 positive effective-override-loss cases**.

- Experiment 1 positive yes/no/uncertain: `5/5/5`.
- Experiment 2 positive yes/no/uncertain: `4/5/1`.
- Combined positives: `25`.
- Combined snapshot detections: `9 yes`.
- Combined snapshot misses or uncertainties: `10 no + 6 uncertain = 16`.

This is a result for an isolated final-step input, not evidence that all snapshot
or low-context methods fail.

## 7. Boundary Case: Bad Outcome versus Effective Override Loss

### 7.1 Case

In E2T08, a worker requests removal of a Wednesday shift. The planner removes
Wednesday and provides no replacement hours. The worker has no work that week
but remains listed for future schedules.

### 7.2 Why Ground Truth Remains Control

- The requested override was executed.
- The next schedule state changed in the requested direction.
- No replacement hours is an adverse outcome, not evidence that removal failed.
- Continued future listing contradicts the rater's inferred irreversible lock-in.

### 7.3 Model Error

The model broadened the override target from â€œremove Wednesdayâ€ to â€œretain a
satisfactory amount of work,â€ then treated the warned zero-hours consequence as
a structural penalty defeating choice. This is an action-efficacy versus
outcome-utility error.

### 7.4 Benchmark Value

Keep E2T08 as a hard negative. It demonstrates that the construct is learnable
but boundary-sensitive and prevents accuracy from being improved by relabeling a
diagnostic failure.

## 8. Discussion

### 8.1 Trajectory Information Matters in This Benchmark

The full sequence exposes the override attempt, the system response, and the
consequential transition. The final state often omits one or more of these.

Accordingly, the current comparison is best understood as an observability
contrast: the final-step interface can withhold the evidence required by the
crossing rule. One model and one prompt family cannot establish that classifier
quality is irrelevant.

### 8.2 Snapshot Misses

The final-step baseline missed or withheld judgment on 16 of 25 positives across
the two experiments. Frame this as an information-context result for this
baseline, not a rejection of all snapshot methods.

### 8.3 Learnable but Boundary-Sensitive

High trajectory agreement across ordinary and hard-control sets suggests that
the operational rule can be followed by this fixed rater on authored synthetic
data. E2T08 shows sensitivity to adverse-outcome language and override-target
scope.

### 8.4 Relevance

Potential relevance includes AI safety evaluation, workflow automation,
algorithmic allocation, review systems, and platform-mediated decisions where
nominal controls may diverge from consequential behavior. These are research
directions, not findings about deployed systems.

## 9. Limitations

Use `paper/limitations_section_draft.md` substantially as written. Do not shorten
away author labels, one-model scope, baseline weakness, small sample, lack of
human annotators, or absence of real-world validation.

The final paper must also state that it does not model monitor-confidence versus
user-investment/lock-in crossing curves, does not develop a Handoff Signature or
response-latency detector, and has no privacy-reviewed real-world case intake.

## 10. Reproducibility

- Fixed CSV datasets and design-time labels are preserved.
- Raw model response ledgers are model-specific and retained.
- Integration and analysis scripts regenerate derived CSV and JSON artifacts.
- Audits cover integrity, prompt blindness, lineage, qualitative revisions, statistical framing, and E2T08.
- Final analysis is local and deterministic; it makes no hidden API calls.
- API generation is separate, environment-configured, rate-limited, and resumable.
- Report exact model name and distinguish recorded outputs from reproducible local post-processing.

## 11. Future Work

1. Human annotation with blinded independent raters and adjudication.
2. Multi-model evaluation with repeated runs, prompt variants, and uncertainty calibration.
3. A stronger baseline ladder: final step, last two/three steps, structured summary, sliding window, and full trajectory.
4. An independently authored, preregistered held-out dataset with development/test separation.
5. Future Experiment 3 real-world case intake only after consent, privacy, ethics, provenance, and domain-review procedures are defined.
6. Turn-level monitor-confidence versus user-investment or lock-in trajectories, with preregistered variables and intervention thresholds.
7. Handoff Signature and response latency as possible content-agnostic signals, evaluated separately rather than described as current results.

### 11.1 Out-of-Scope Research Line

Generated-code trajectory validation, invariant extraction, severity-weighted
invariants, program verification comparisons, and automatic trace generation
belong to the separate TrajectoryCheck line of work and are outside the scope of
this Agency Trajectory Benchmark paper.

## Conclusion Placeholder

Agency Trajectory Benchmark v0 provides a synthetic matched-control seed for
studying effective override loss. In two current experiments, the same fixed LLM
rater performed better with full trajectories than with isolated final steps,
including under lexical hard controls. This result motivates independent human,
multi-model, stronger-baseline, and real-world validation; it does not itself
provide that validation.





