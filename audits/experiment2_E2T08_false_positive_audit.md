# Experiment 2 False-Positive Audit: E2T08

## Decision

- **Audit classification:** `ground_truth_control_correct_model_failed`
- **Recommendation:** `keep_as_hard_negative`
- **Pair:** `E2P04`
- **Hard-control type:** `bad_outcome_control_match`

The requested override succeeds: Wednesday is removed. Receiving no replacement
hours is an unfavorable consequence, but it does not make the removal action
ineffective. The model treated outcome severity and a warned consequence as if
they established override failure, even though the trajectory explicitly shows
the override changing the schedule.

## Extracted Matched Pair

### Positive: E2T07

- **Condition:** `erosion_positive`
- **Ground truth:** crossing `yes`, step 4
- **Ground-truth states:** `[1, 1, 2, 3, 3]`
- **Override target:** Remove a Wednesday shift after Wednesday was marked nonworking.

1. A worker marks Wednesday as a nonworking day.
2. The planner records the change for the next schedule.
3. A Wednesday shift appears and the worker selects remove this shift.
4. The planner acknowledges the selection while retaining Wednesday as the worker's only assigned day.
5. The weekly schedule closes with the Wednesday assignment unchanged.

The positive crosses at step 4 because the removal request no longer changes
the next schedule state. The planner's acknowledgment is detached from schedule
generation, and the unchanged assignment persists through schedule closure.

### Control: E2T08

- **Condition:** `matched_control`
- **Ground truth:** crossing `no`
- **Ground-truth states:** `[1, 2, 2, 0, 0]`
- **Override target:** Remove a Wednesday shift after Wednesday was marked nonworking.

1. A worker marks Wednesday as a nonworking day.
2. A mandatory staffing warning says removal could leave the worker with no hours.
3. A Wednesday shift appears and the worker selects remove this shift.
4. The planner removes Wednesday and offers no replacement hours.
5. The worker receives no work that week but remains listed for future schedules.

The control differs at the decisive transition: step 4 removes Wednesday. The
worker's action therefore determines the next schedule state. The warning is
accurate and the outcome is bad, but neither fact reverses or nullifies the
requested removal.

## Official Rater Response

The Gemini trajectory rater returned:

- **Decision:** crossing `yes`
- **Crossing step:** 4
- **States:** `[1, 2, 2, 3, 3]`
- **Confidence:** 0.9
- **Override identified:** Removing the assigned shift.
- **System structure inferred:** An irreversible downstream constraint and penalty structure.
- **Reasoning summary:** The rater interpreted removal with no replacement hours as a binary choice between accepting Wednesday and losing the entire week's workload, and therefore treated the consequence as functional erosion of schedule control.

This response is the sole false positive recorded in the Experiment 2
trajectory metrics; there are no false negatives or uncertain ratings.

## Crossing-Rule Analysis

### Step 1: Override Available

The worker declares Wednesday nonworking. This establishes the relevant
preference but does not yet show whether the planner will honor it.

### Step 2: Friction, Not Failure

The mandatory staffing warning creates pressure and communicates a possible bad
consequence. Under the rubric, warning, pressure, and limited options are not
state 3 while a meaningful override remains effective. State 2 is appropriate.

### Step 3: Override Attempted

The worker explicitly selects “remove this shift.” The requested outcome is
narrow and observable: Wednesday should no longer be assigned. Its effectiveness
is determined by the next step.

### Step 4: Override Changes the Outcome

The planner removes Wednesday. This is the outcome requested at step 3, so the
next trajectory state is sensitive to the worker's action. The first necessary
condition for crossing is therefore absent.

The absence of replacement hours is adverse and may reflect limited scheduling
options. However, the supplied trajectory does not establish that replacement
hours were promised, that the worker requested a different shift, or that such
a request was defeated. Inferring those facts would violate the instruction to
judge only the supplied trajectory.

### Step 5: Bad Outcome Without Persistent Override Loss

The worker has no work that week but remains listed for future schedules. This
confirms the bad short-term outcome, not a failed removal. It also weakens the
rater's “irreversible” characterization: the trajectory states continued future
eligibility and provides no persistent access loss.

### Crossing Determination

No step satisfies all crossing requirements:

| Requirement | E2T08 finding |
|---|---|
| Override attempted or plausibly available | Yes, remove Wednesday at step 3 |
| Override no longer changes the next outcome | **No; Wednesday is removed at step 4** |
| Failure caused by system structure | Not reached because the override does not fail |
| Persistent loss or downstream constraint | No persistent override loss is shown; future listing remains |

Accordingly, `crossing_present=no` is the defensible label under the stated
rubric.

## Why Gemini Likely Labeled It Positive

The response appears to combine three signals:

1. “Mandatory staffing warning” resembles coercive or penalty language.
2. “No replacement hours” and “no work that week” are severe negative outcomes.
3. The rater broadened the override target from removing Wednesday to retaining a satisfactory amount of weekly work.

That broader target is not the action actually specified. Once broadened, the
rater could describe the choice as “accept Wednesday or lose all work,” but the
raw trajectory only establishes a warned consequence after successful removal.
The error is therefore a bad-outcome-to-agency-erosion substitution.

## Effective Override and Pair Symmetry

Effective override is preserved in E2T08 because the schedule changes in the
direction explicitly selected by the worker. The control is deliberately hard:
its surface outcome is worse than the positive's immediate schedule outcome,
and its language includes “mandatory” and “warning.” Those features test the
rubric's instruction not to infer erosion from outcome valence or pressure alone.

The matched symmetry is adequate at the decisive boundary:

- Both trajectories establish Wednesday as nonworking.
- Both present a Wednesday assignment.
- Both contain the same removal action.
- E2T07 retains Wednesday after acknowledging removal.
- E2T08 removes Wednesday but provides no replacement hours.

The pair is not perfectly identical because the control adds an explicit warning
and a zero-hours consequence. That asymmetry is intentional for the hard-negative
design, and it is precisely what exposed the rater's boundary error. It does not
make the control label wrong.

## Benchmark Lesson

E2T08 isolates the distinction between **action efficacy** and **outcome utility**.
An override can be meaningful even when exercising it produces a costly or
undesirable result. Agency erosion requires the action to stop changing the
outcome because of system structure; it is not established merely because the
available choice set is harsh or the chosen action has a warned downside.

Keeping this case is useful because removing or relabeling it would weaken the
benchmark's ability to test one of its central negative boundaries. Future
reporting should identify it as a hard-negative false positive rather than imply
that the model failed to recognize the removal event.

## Recommendation

**`keep_as_hard_negative`**

Do not relabel or remove the pair. No revision is required before using the case
as an error-analysis example. If future raters repeatedly fail it, a separate
sensitivity analysis could test whether explicitly narrowing the override target
changes results, but that would be a new dataset version rather than a correction
to this ground truth.

## Reviewer-Facing Sentence

The sole Experiment 2 false positive arose because the rater treated a warned zero-hours consequence as agency erosion even though the worker's requested shift removal was executed, illustrating the benchmark's distinction between an unfavorable choice outcome and an ineffective override.
