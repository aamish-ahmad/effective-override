# Experiment 1 Prompt Blindness Audit

**Status: PASS**

## Forbidden-Field Inspection

Static AST-based inspection was limited to each runner's `build_prompt` function.

| Runner | Forbidden fields in prompt construction |
|---|---|
| `run_gemini_trajectory_rater_experiment1_flash_lite.py` | None |
| `run_gemini_snapshot_rater_experiment1_flash_lite.py` | None |

## Rater Views

The trajectory rater sees the blind-rater instructions, full rubric, trajectory ID, and all five raw trajectory steps. Its prompt construction does not reference CSV condition or ground-truth columns.

The snapshot rater sees the snapshot instructions, trajectory ID, final-step index, and final visible step only. Its prompt construction does not include earlier steps, labels, or trajectory-rater output.

## Static-Inspection Limitations

This audit checks checked-in prompt-construction source, not network payload capture. It cannot rule out runtime code replacement, dependency changes, provider-side transformations, or uncommitted local modifications after hashing.
