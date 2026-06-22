# Experiment 2 v1 Qualitative Audit

## Scope

This re-audit reviews the complete v1 dataset against the crossing rubric, with
focused attention to the five revised pairs. It does not create new labels or
change the CSV.

## Pair Decisions

| Pair | Decision | Qualitative basis |
|---|---|---|
| E2P01 | Keep | The local-only mode is explicitly binding, an already queued offer is handled symmetrically, and refreshed allocation diverges only in the positive. The control retains scary penalty language. |
| E2P02 | Keep | Known afternoon capacity eliminates scarcity as the explanation. The positive returns the selected slot to general allocation; the control holds the same slot. |
| E2P03 | Keep | Category removal changes neither ranking nor accessible work in the positive but functions under severe warning language in the control. |
| E2P04 | Keep | Shift removal fails in the positive and succeeds in the control even though success produces the worse surface outcome of zero hours. |
| E2P05 | Keep | Identical packet-completion events lead to different routing: matching reaches decision first in the positive, while current-cycle caseworker review precedes decision in the control. |
| E2P06 | Keep | The positive's displayed advanced choice remains detached from module allocation; the control incurs reset and quiz failure while the switch works. |
| E2P07 | Keep | The pair cleanly distinguishes delay that passes the payment boundary from delay that still changes the estimate before payment. |
| E2P08 | Keep | Numeric reconstruction makes the boundary precise without a self-contained final-step contradiction: 8400 persists in the positive, while the saved 800-person list governs the control. |
| E2P09 | Keep | Review delay defeats the appeal only when payroll closes in the positive; the control corrects the amount before issuance. |
| E2P10 | Keep | Known direct inventory and a binding shortlist remove scarcity and advisory-preference ambiguity; only the positive routes direct seats outside selectable results. |

## Counts

- **Keep:** 10
- **Revise:** 0
- **Remove:** 0

## Remaining Risks

1. The dataset remains authored and synthetic; causal clarity does not establish real-world prevalence.
2. Several positives still use relational mismatch signals such as persistent counts or divergent routing, so semantic cue leakage is reduced rather than eliminated.
3. Controls intentionally contain conspicuous warning language, which may create a reverse lexical shortcut if the pattern is too regular.
4. Domain and override semantics remain heterogeneous, and binding settings may feel more natural in some domains than others.
5. Ten pairs are sufficient for a hard-control probe but too small for broad statistical generalization.

## Readiness

**Ready for API rating: Yes.** All ten pairs now have a defensible structural
crossing or preserved-control distinction, acceptable within-pair symmetry, and
no unresolved revision-level ambiguity. Readiness here means suitable for the
planned synthetic benchmark run, not validated for real-world inference.
