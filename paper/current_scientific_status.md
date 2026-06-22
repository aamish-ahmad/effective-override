# Current Scientific Status

## Artifact Scope

Agency Trajectory Benchmark v0 currently contains two authored synthetic
matched-control experiments evaluated with one fixed LLM model under two views:
full trajectory and isolated final step. It operationalizes **effective override
loss**, not human agency in its entirety.

## What Is Complete

- A four-state rubric with an explicit first-crossing rule.
- Experiment 1: 30 trajectories, 15 matched pairs, trajectory and final-snapshot ratings, integration, metrics, summary, prompt-blindness audit, robustness audit, lineage manifest, and local repro scripts.
- Experiment 2: 20 trajectories, 10 lexical hard-control pairs, qualitative pre-audit, five-pair revision, trajectory and final-snapshot ratings, final metrics, and summary.
- One fixed model (`gemini-3.1-flash-lite`) used for both views in both experiments.
- Strict ledger validation and model-specific derived outputs.
- Focused error analysis for `E2T08`, preserving it as a hard negative.
- Explicit limitations and a claim boundary in the current paper-scoping files.

## What Is Strong

### 1. Internal operational clarity

The rubric separates override effectiveness from outcome quality. A crossing
requires both action ineffectiveness and a structural cause. E2T08 demonstrates
that this boundary is nontrivial and empirically useful for error analysis.

### 2. Replicated within-benchmark trajectory advantage

- Experiment 1: trajectory agreement/kappa `1.000/1.000`; snapshot covered-case agreement/kappa `0.760/0.464`.
- Experiment 2: trajectory agreement/kappa `0.950/0.900`; snapshot covered-case agreement/kappa `0.722/0.444`.
- Across positive cases, the final-step baseline missed or was uncertain on 16/25; the trajectory rater missed or was uncertain on 0/25.
- Where both detected a positive, trajectory detection was never later: Experiment 1 had five earlier cases; Experiment 2 had two earlier and two tied.

This is the strongest current result, provided it is described as a result on
two synthetic matched-control datasets with a final-step-only baseline.

### 3. Adversarial hard-control design

Experiment 2 reduces obvious coercive vocabulary in positives and introduces
warning, risk, penalty, delay, and bad-outcome language in controls. Five pairs
were revised before rating to improve causal clarity and symmetry. The trajectory
rater still achieved `0.950` agreement, with one interpretable hard-negative
false positive.

### 4. Auditability

The project validates data and response ledgers, records model-specific outputs,
checks prompt-construction blindness statically, documents lineage, and preserves
known errors rather than relabeling them away.

## What Is Weak

1. **Labels are authored, not independently adjudicated.** The benchmark tests agreement with its own designed construct labels.
2. **One model and one recorded run.** There is no multi-model replication, stochastic stability estimate, or prompt-sensitivity study.
3. **The baseline ladder is incomplete.** Final-step-only is informative but weak; no last-k, summary, structured-state, retrieval, or learned temporal baseline exists.
4. **The sample is small.** Fifty trajectories and 25 pairs cannot support broad generalization; Experiment 2 per-type cells contain two rows each.
5. **Lexical and template leakage remain possible.** Experiment 2 reduces obvious cues but retains semantic mismatches and authored narrative regularity.
6. **No human validity evidence exists.** There is no inter-rater reliability, expert review panel, worker review, or construct-validity study.

## What Is Not Yet Known

- Whether independent humans can apply the crossing rule reliably.
- Whether affected workers and domain experts consider the construct meaningful.
- Whether other LLM families reproduce the trajectory advantage.
- Whether results are stable across reruns, temperatures, prompt variants, and ordering.
- Whether stronger low-context baselines close the gap.
- Whether the rubric transfers to naturally occurring, incomplete, or noisy workflow records.
- The prevalence or consequences of effective override loss in any real system.
- Whether the construct predicts downstream harm, dissatisfaction, compliance risk, or behavior.
- Whether a reliable automated detector can be calibrated for operational use.
- Whether monitor confidence crosses user investment or workflow lock-in before an actionable intervention point.
- Whether handoff events or response latency provide a content-agnostic signal beyond trajectory text.

## What Experiment 3 Could Test

Experiment 3 should be an **independent-label and baseline-ladder validation**:

1. Recruit independent case authors who do not see the current examples or model outputs.
2. Create a preregistered held-out set with balanced positives, controls, bad-outcome controls, delayed crossings, and lexical counterfactuals.
3. Obtain blinded labels from multiple human annotators, including domain experts or affected-workflow participants where feasible.
4. Report inter-rater reliability, disagreement categories, adjudicated labels, and rubric revisions made without viewing model performance.
5. Compare final step, last two steps, last three steps, structured summary, sliding window, and full trajectory.
6. Evaluate multiple model families and repeated runs, reporting variance, calibration, and failure consistency.
7. Keep development and held-out test sets separate and preregister primary metrics.
8. Add preregistered confidence-versus-investment/lock-in trajectories without conflating them with the current override-effectiveness crossing.
9. Evaluate Handoff Signature and response latency as separate content-agnostic baselines.

This experiment would test whether the observed advantage is attributable to
temporal information rather than author templates, a weak endpoint baseline, or
one model's prompt behavior.

## Ride-Hailing Case

The ride-hailing toll case should **not enter the current scientific evidence
chain** because none of the supplied evidence files documents its provenance,
consent, factual verification, or representativeness. If retained at all, it may
appear as a short, de-identified motivating anecdote clearly labeled as
motivation rather than evidence, after privacy and factual review. A generic
synthetic vignette is safer for the current seed-benchmark report.

It must not be used to imply wrongdoing by a named company, validate gig-platform
behavior, establish prevalence, or support legal and policy conclusions.

## Publication Posture

An arXiv-style release is defensible only as a transparent **seed benchmark**:

- Put â€œsynthetic matched-controlâ€ and â€œseed benchmarkâ€ in the abstract and conclusion.
- Report exact dataset sizes and one-model scope.
- Name the comparator â€œfinal-step-only baseline.â€
- Report uncertainty and coverage beside snapshot accuracy.
- Include E2T08 and the author-label limitation prominently.
- Present inferential statistics as fixed-benchmark summaries, not population evidence.
- Make future human, multi-model, and real-world validation explicit.

## Conclusion

The current artifact is strongest as a synthetic matched-control benchmark seed for effective override loss, not as real-world validation.


