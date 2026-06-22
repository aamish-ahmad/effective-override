# Experiment 2 Robustness Summary

## Configuration

- Model: `gemini-3.5-flash`
- Run type: `second_model_robustness`
- Science gate: **PASS_STRONG**

## Coverage and Ground-Truth Agreement

- Dataset rows: 20
- Rows attempted: 20
- Valid responses: 20
- Binary agreement: 0.950 over 20 non-uncertain responses
- Cohen's kappa: 0.900
- False positives / false negatives / uncertain: 1 / 0 / 0

## Primary-Rater Comparison

- Agreement with primary trajectory rater: 1.000 over 20 non-uncertain robustness responses
- Disagreement IDs: None

## E2T08 Boundary Case

- Robustness result: `yes`
- Audit classification: `ground_truth_control_correct_model_failed`
- Recommendation: `keep_as_hard_negative`

## Per-Hard-Control-Type Failures

```json
{
  "bad_outcome_control_match": [
    "E2T08"
  ]
}
```

## Interpretation

This is a robustness check on a fixed 20-row synthetic, author-labeled dataset.
It does not provide human annotation or real-world validation. A second-model run
tests judge sensitivity; a repeated run of the primary model tests only run
stability.
