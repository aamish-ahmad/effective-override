# Experiment 1 Robustness Audit

## Headline Result

In this synthetic matched-control benchmark, a single fixed LLM rater achieved higher binary accuracy and earlier detection with full trajectories than with final-step snapshots. This is evidence that trajectory-level evaluation captures effective override loss earlier than snapshot-only evaluation within this benchmark.

## Why the Trajectory Result Is Stronger

The trajectory rater had binary accuracy 1.000 and positive detection rate 1.000; the snapshot rater had covered-case accuracy 0.760, coverage 0.833, and positive detection rate 0.333. For paired positive detections, mean lead-time gain was 1.000 step.

## Data Integrity Status

**PASS**

- [x] source has 30 rows
- [x] trajectory IDs are unique
- [x] source has 15 matched pairs
- [x] each pair has one positive and one control
- [x] all steps_json values parse
- [x] all state sequences parse
- [x] all trajectories have exactly five steps
- [x] 30 official trajectory responses parse
- [x] 30 official snapshot responses parse
- [x] integrated full results has 30 rows
- [x] integrated results have no missing or extra IDs
- [x] response ledgers have no missing or extra IDs

## Prompt Blindness Status

**PASS**. Static inspection found no forbidden dataset or rater-result fields in either `build_prompt` function. See `experiment1_prompt_blindness_audit.md` for scope and limitations.

## Pairwise Error Summary

- Snapshot positive misses: 5
- Snapshot positive uncertain: 5
- Snapshot control false positives: 1
- Full per-pair decisions: `experiment1_pairwise_error_audit.md`

## Robustness Metrics

- Trajectory binary accuracy: 1.000
- Snapshot binary accuracy excluding uncertain: 0.760
- Snapshot coverage: 0.833
- Snapshot positive yes/no/uncertain: 5/5/5
- Snapshot control yes/no/uncertain: 1/14/0
- Exact / within-one-step crossing accuracy: 0.933 / 1.000
- Trajectory earlier / same / snapshot earlier: 5 / 0 / 0

## Paired Statistical Comparison

Uncertain snapshot labels are treated as incorrect for paired correctness, while their effect is separately reported through snapshot coverage.

### Paired Correctness Table

| Category | Rows |
|---|---:|
| both correct | 19 |
| trajectory correct / snapshot incorrect or uncertain | 11 |
| snapshot correct / trajectory incorrect or uncertain | 0 |
| both incorrect or uncertain | 0 |

### Exact McNemar/Binomial Fallback

- Discordant counts (`b` / `c` / `n`): 11 / 0 / 11
- Exact two-sided p-value: 0.0009765625
- Calculation: standard-library exact binomial tail; SciPy is not required.
- Interpretation: Under an exact paired sign-test/McNemar formulation over discordant pairs, the probability of observing 11 trajectory-favoring discordances and 0 snapshot-favoring discordances under the null of equal paired correctness is p = 0.0009765625.

## Reproducibility Status

**PASS**. Shell and batch scripts rerun only local integrations, analyses, and this audit. The lineage manifest records SHA256 hashes for source, ledgers, prompts, runners, integrations, analyses, and final artifacts.

## Remaining Limitations

This is a synthetic matched-control benchmark using a single fixed LLM rater, not real-world field validation. Static prompt inspection is not a captured network-payload audit, the dataset is small and constructed, and findings do not prove universal human agency erosion or validate claims about real gig platforms.
