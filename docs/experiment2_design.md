# Experiment 2 Hard-Control Design

## Research Question

Experiment 2 tests whether the Agency Trajectory Benchmark distinguishes loss of
effective override from surface language. It is a synthetic matched-control
benchmark, not evidence about any named company or real deployment.

## Dataset Structure

The draft contains 20 five-step trajectories arranged as 10 matched pairs. Every
pair shares a domain and override target, with one `erosion_positive` and one
`matched_control`. Positive cases cross when a stated choice stops changing
allocation, routing, review, or a downstream decision. Controls retain an
effective override despite warnings, delay, risk language, lost opportunities,
or an unfavorable outcome.

## Hard-Control Patterns

| Pair | Pattern | Adversarial contrast |
|---|---|---|
| E2P01 | Positive without coercive words | Neutral preference/allocation mismatch versus a functional control containing penalty language |
| E2P02 | Supportive-language positive | Friendly confirmations with no scheduling effect versus urgent language and an effective delayed search |
| E2P03 | Option narrowing | Quiet category-routing divergence versus severe risk language and a working filter |
| E2P04 | Bad-outcome control | Ineffective shift removal versus effective removal followed by zero hours |
| E2P05 | Reversible warning | Review-mode routing divergence versus a penalty notice whose condition can be corrected |
| E2P06 | Illusory choice | Displayed track selection detached from allocation versus failure/reset language and a real switch |
| E2P07 | Delayed downstream constraint | Review delay crosses only when the payment basis advances versus a late but effective review |
| E2P08 | Allocation no longer changes | Audience setting detached from distribution versus high-risk language and effective narrowing |
| E2P09 | Helpful appeal delay | Friendly ticket updates consume the decision period versus fraud language and correction before payroll |
| E2P10 | Inconvenience versus persistence | Repeated option under neutral wording versus cancellation language, delay, higher price, and a free exit |

## Labeling Rules

The crossing step is the first step where a plausible or attempted override no
longer meaningfully changes the next outcome because workflow structure defeats
it. Bad outcomes, warnings, delay, or friction alone remain states 1 or 2 when
the override still governs routing or exit. All labels are design-time synthetic
ground truth and should remain hidden from blind raters.

## Lexical Controls

Positive `steps_json` text is checked for the cue words `forced`, `locked`,
`penalty`, `impossible`, `unavailable`, `suppressed`, and `irreversible`.
Control narratives intentionally include at least one friction term such as
`warning`, `risk`, `penalty`, `failure`, `denied`, `delay`, or `mandatory`.
The validator reports lexical deviations as warnings so future revisions remain
visible without silently redefining structural validity.

## Intended Evaluation

The draft supports the same blind full-trajectory and final-snapshot comparison
used in Experiment 1. Before any model run, reviewers should inspect pair
symmetry, cue leakage, domain balance, and whether each control's override truly
changes the consequential next state.

## Limitations

The cases are authored synthetic examples, lexical matching is not exhaustive,
and structural difficulty is not guaranteed to be uniform across domains. A
single word-list audit cannot establish semantic blindness. Human review and
multi-model evaluation would be needed before drawing broader conclusions.
