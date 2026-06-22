# Limitations

Agency Trajectory Benchmark v0 is a seed artifact with deliberately narrow
evidence. Its results should be interpreted as measurements on two fixed
synthetic matched-control datasets, not estimates of behavior in a real-world
population.

## Synthetic Data

All 50 trajectories are authored synthetic cases. This design permits controlled
positive/control contrasts and exact crossing labels, but it does not reproduce
the noise, missing context, strategic behavior, institutional detail, or base
rates of deployed workflows. Synthetic internal validity does not establish
ecological validity.

## Author-Generated Labels

The same research process defined the construct, authored the examples, and
assigned design-time labels. Validators and qualitative audits improve internal
consistency but cannot remove confirmation bias or establish construct validity.
The labels should be described as authored benchmark ground truth, not objective
human-agency truth.

## No Human Annotators

No independent human annotators, domain experts, affected participants, or
adjudication panel evaluated the trajectories. Inter-rater reliability,
comprehension of the crossing rule, stakeholder validity, and disagreement
patterns are unknown.

## One Model

Both evaluation views use one fixed model, `gemini-3.1-flash-lite`. This controls
the model identity within each trajectory/snapshot comparison but provides no
evidence of model-family generality. The documented E2T08 false positive also
shows that high aggregate agreement can coexist with a meaningful construct
boundary error.

## One Recorded Run

The artifact contains one recorded response per model-view-item combination.
There is no estimate of stochastic variation, rerun stability, prompt-order
sensitivity, decoding sensitivity, or calibration. Results may differ under a
new run even with the same nominal model.

## No Multi-Model Robustness

No second monitor or model family was evaluated. Using the same fixed model for
both views controls model identity within each comparison, but it does not show
that the trajectory advantage, uncertainty pattern, or boundary errors persist
across model families.

## Small Sample

The benchmark contains 50 trajectories in 25 pairs. Experiment 1 has 30 rows;
Experiment 2 has 20, and each Experiment 2 hard-control type contains only one
positive/control pair. Aggregate scores and especially per-type results are
therefore fragile.

## Weak Final-Step-Only Baseline

The snapshot comparator receives only the final visible step. It is useful for
testing endpoint information loss but is not representative of all low-context
or snapshot methods. Last-k windows, selected events, structured summaries,
retrieval, state tracking, and learned temporal baselines could recover missing
context. The results support an advantage over this final-step-only baseline,
not universal trajectory superiority.

## Confidence and Investment Curves Are Not Modeled

The benchmark does not measure turn-level monitor confidence, user investment,
or workflow lock-in as rising trajectories, and it does not estimate whether an
investment curve crosses a detection-confidence curve before intervention. Its
crossing labels concern override effectiveness, not confidence-versus-investment
dynamics.

## Handoff Signature and Response Latency Are Undeveloped

No Handoff Signature, response-latency feature, handoff event, or content-
agnostic temporal detector is defined or evaluated. These may be useful future
signals, but they are not current methods or results.

## Single-Domain and Domain-Depth Concern

The benchmark is not literally single-domain: its synthetic cases span several
workflow settings. However, each domain has shallow coverage, no representative
sampling, and no domain-specific expert validation. The study is effectively a
single authored benchmark regime rather than evidence of transfer across mature
real-world domains.

## Residual Lexical and Template Cues

Experiment 2 removes several obvious coercive words from positives and introduces
friction language into controls, but semantic mismatch cues and repeated
narrative structures remain. Controls may also create a reverse shortcut because
warning language is deliberately common. No cue-only model, independent
paraphrase set, or held-out template test has been run.

## No Real-World Validation

No real platform logs, worker records, operational traces, interviews, field
experiments, or representative samples were used. The benchmark cannot establish
prevalence, causality, harm, misconduct, legal violation, policy relevance, or
behavior by any deployed system.

## Real-World Case Intake Is Future Work

The artifact has no approved real-world case-intake pipeline. Any future intake
requires consent, de-identification, provenance checks, privacy and ethics review,
independent annotation, adjudication, and domain-expert review before a case can
enter an evaluation set. A motivating observation is not validation evidence.

## Prompt-Blindness Audit Scope

Static inspection found no forbidden label fields in prompt-construction logic,
but this is not a captured network-payload audit. It cannot rule out runtime
environment changes, dependency changes, provider-side transformations, or
future code drift.

## P-Values over Synthetic Data

The Experiment 1 exact paired p-value summarizes an extreme discordance pattern
in a fixed authored dataset. It should not be interpreted as a population-level
probability, a real-world effect estimate, or evidence of policy significance.
Effect counts and transparent denominators are more important at this stage.

## Construct Breadth

Effective override loss captures one component of control in sequential systems.
It does not measure perceived autonomy, welfare, fairness, informed consent,
coercion, dignity, legal rights, or human agency as a whole. Even the term
â€œagency erosionâ€ must remain tied to the operational crossing rule.

## Consequence for Claims

The defensible conclusion is limited: in these two authored synthetic
matched-control experiments, the same fixed LLM rater agreed more often with
design-time labels when given full trajectories than when given only the final
step. Human validation, stronger baselines, multi-model repeated runs,
independently authored held-out data, and ethical real-world studies remain
necessary.



