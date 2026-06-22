# Claims That Must Not Be Made

These restrictions apply to titles, abstracts, figures, captions, talks,
repositories, social posts, and reviewer responses. Each alternative preserves
what the current artifact actually supports.

| Do not claim | Why it is unsafe | Safer alternative wording |
|---|---|---|
| **â€œWe prove human agency erosion.â€** | The artifact proposes and tests an operational construct on authored synthetic data. It has no external construct validation or field evidence. | â€œWe propose a synthetic benchmark for effective override loss and report initial fixed-model results.â€ |
| **â€œWe prove a named ride-hailing company did anything wrong.â€** | No evaluated data from either company exists here, and the benchmark cannot establish facts, fault, or misconduct by a named entity. | â€œThe work makes no finding about any named platform; its workflows are synthetic.â€ |
| **â€œWe validate real-world gig platform behavior.â€** | There are no platform logs, worker samples, observational records, or field outcomes. | â€œThe benchmark uses synthetic allocation and workflow scenarios; real-world validation remains future work.â€ |
| **â€œWe solve human agency measurement.â€** | The rubric covers one narrow construct: whether an override stops changing a trajectory because of system structure. Human agency is broader and multidimensional. | â€œWe operationalize one testable component of agency: loss of effective override in sequential workflows.â€ |
| **â€œWe show LLM judges are ground truth.â€** | The LLM is evaluated against author-generated benchmark labels and makes a documented boundary error on E2T08. | â€œA fixed LLM rater closely matched the authored trajectory labels in these two synthetic experiments.â€ |
| **â€œWe show all snapshot methods fail.â€** | Only an isolated final-step prompt was tested. Multi-snapshot, windowed, summarized, stateful, and feature-rich methods were not evaluated. | â€œThe final-step-only baseline underperformed full-trajectory evaluation on both synthetic experiments.â€ |
| **â€œWe show universal trajectory superiority.â€** | The result uses one model, two small authored datasets, and one trajectory prompt/baseline design. | â€œA trajectory advantage appeared in both current synthetic experiments for the same fixed rater.â€ |
| **â€œWe show legal or regulatory violation.â€** | The benchmark provides no legal analysis, jurisdiction-specific facts, real actor evidence, or adjudication. | â€œThe benchmark is a technical measurement artifact and makes no legal or regulatory determination.â€ |

## Additional Guardrails

- Do not call authored labels â€œobjective truthâ€ without the modifier â€œbenchmarkâ€ or â€œdesign-time synthetic.â€
- Do not present covered-case snapshot accuracy as accuracy over all rows without also reporting uncertainty and coverage.
- Do not convert the Experiment 1 exact paired p-value into a claim about a real-world population; it describes discordance in a fixed synthetic set.
- Do not hide E2T08. Report it as the trajectory rater's hard-negative false positive and explain the action-efficacy versus outcome-utility boundary.
- Do not describe the 50 trajectories as representative of workers, platforms, industries, or deployment frequencies.
- Do not use â€œcausal,â€ â€œvalidated,â€ â€œhuman-level,â€ or â€œproduction-readyâ€ without a narrowly qualified object and evidence.

- Do not claim that classifier quality is irrelevant; one model and one prompt family cannot separate architecture from classifier effects.
- Do not state or imply that confidence/investment crossing curves, Handoff Signature, or response latency were measured.
- Do not import generated-code invariants, verification baselines, or automatic trace generation as contributions of this paper.

## Approved One-Sentence Positioning

â€œAgency Trajectory Benchmark v0 is a synthetic matched-control seed benchmark
for testing whether evaluators detect when a human override stops changing a
sequential workflow outcome.â€


