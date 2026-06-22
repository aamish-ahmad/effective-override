# Experiment 2 Final Summary: Gemini 3.1 Flash Lite

## Purpose

Experiment 2 is a 20-trajectory synthetic lexical/hard-control stress test. Its
matched pairs reduce obvious coercive cues in positives and place warning,
penalty, risk, delay, or bad-outcome language in controls to test whether the
rater follows trajectory structure rather than surface valence.

## Trajectory Performance

- Valid responses: 20/20
- Binary agreement: 0.950
- Cohen's kappa: 0.900
- False positives / false negatives / uncertain: 1 / 0 / 0
- Positive yes/no/uncertain: 10/0/0
- Control yes/no/uncertain: 1/9/0
- Per-type failures: {"bad_outcome_control_match": ["E2T08"]}

## Snapshot Performance

- Valid responses: 20/20
- Binary agreement excluding uncertain: 0.722 (18 covered rows)
- Cohen's kappa: 0.444
- False positives / false negatives / uncertain: 0 / 5 / 2
- Positive yes/no/uncertain: 4/5/1
- Control yes/no/uncertain: 0/9/1
- Per-type failures: {"allocation_no_longer_changes": ["E2T15"], "bad_outcome_control_match": ["E2T07", "E2T08"], "helpful_appeal_delay": ["E2T17"], "inconvenience_vs_persistent_constraint": ["E2T19"], "positive_without_coercive_words": ["E2T01"], "supportive_language_positive": ["E2T03"]}

## Comparison

- Positive rows detected by both raters: 4
- Mean lead-time gain (snapshot step minus trajectory step): 0.500 steps
- Trajectory earlier / same / snapshot earlier: 2 / 2 / 0
- Snapshot misses or uncertain on positives: 6
- Trajectory misses or uncertain on positives: 0

### Paired Correctness

Uncertain ratings are treated as incorrect for this paired table.

| Category | Rows |
|---|---:|
| Both correct | 13 |
| Trajectory correct / snapshot incorrect or uncertain | 6 |
| Snapshot correct / trajectory incorrect or uncertain | 0 |
| Both incorrect or uncertain | 1 |

## E2T08 Boundary Case

The sole trajectory false positive, `E2T08`, was independently audited as
`ground_truth_control_correct_model_failed`, with recommendation
`keep_as_hard_negative`. The requested shift removal succeeded; the rater
mistook the warned zero-hours consequence for an ineffective override.

## Limitations

This is a small, authored synthetic benchmark evaluated with a single fixed LLM
model. Hard-control phrasing reduces but cannot eliminate semantic cues, snapshot
agreement excludes uncertain rows, and these results are not real-world field
validation or evidence about any deployed platform.
