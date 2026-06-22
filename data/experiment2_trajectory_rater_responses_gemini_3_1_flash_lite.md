# Experiment 2 Trajectory Ratings: Gemini 3.1 Flash Lite


## E2T01

{
  "trajectory_id": "E2T01",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The courier attempts to use 'local-only queue mode' to restrict offers to five kilometers.",
  "system_structure": "The algorithm continues to draw from the general pool regardless of the user's active mode selection.",
  "downstream_constraint": "The system ignores the local-only filter, rendering the courier's selection ineffective against the system's dispatch logic.",
  "reason": "At step 4, the courier's override (local-only mode) fails to influence the dispatch outcome. The system structure suppresses the user's defined constraint by continuing to pull from the general pool, thereby ignoring the user's choice and foreclosing effective control over offer distance.",
  "confidence": 0.95
}

## E2T02

{
  "trajectory_id": "E2T02",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    0,
    1,
    0
  ],
  "override_attempt": "The courier attempts to control their queue by setting a five-kilometer radius and declining a distant offer.",
  "system_structure": "None",
  "downstream_constraint": "None",
  "reason": "The courier successfully applies a local-only setting and declines an offer. The system then adheres to the courier's settings by assigning a four-kilometer offer, which is within the specified five-kilometer range. There is no evidence of system suppression of the user's choices.",
  "confidence": 1
}

## E2T03

{
  "trajectory_id": "E2T03",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    0,
    3,
    3
  ],
  "override_attempt": "Selecting a specific afternoon slot",
  "system_structure": "hidden state / processing mismatch",
  "downstream_constraint": "The system ignored the user's specific selection in favor of its own internal queueing logic which caused the slot to be lost.",
  "reason": "At step 4, the system ignored the patient's specific selection and replaced it with a different slot, meaning the user's override attempt (choosing an available time) had no effect on the outcome.",
  "confidence": 0.95
}

## E2T04

{
  "trajectory_id": "E2T04",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    0,
    1,
    0
  ],
  "override_attempt": "The user successfully selected and confirmed their preferred afternoon appointment time despite the system's urgency warnings.",
  "system_structure": "The system includes an urgency warning and a time-limited hold, which constitutes friction but does not prevent the user from successfully selecting their preferred option.",
  "downstream_constraint": "None identified; the system facilitated the user's specific request.",
  "reason": "The user maintained full control throughout the process. The warning regarding time release is a standard interface feature (friction) that did not prevent the user from successfully securing their desired appointment slot.",
  "confidence": 1
}

## E2T05

{
  "trajectory_id": "E2T05",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "The user attempts to remove a project category to stop receiving related project recommendations.",
  "system_structure": "The system's UI shows a category selection that is disconnected from the backend routing, effectively hiding the actual filtering logic from the user.",
  "downstream_constraint": "The system continues to route projects based on the old category set despite the user's explicit revision.",
  "reason": "At step 4, the user's override (removing the illustration category) becomes ineffective because the system's display is decoupled from its routing logic. The user is presented with inaccurate information while the backend continues to ignore the choice, rendering the override meaningless.",
  "confidence": 0.95
}

## E2T06

{
  "trajectory_id": "E2T06",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    0,
    0,
    0
  ],
  "override_attempt": "none",
  "system_structure": "none",
  "downstream_constraint": "none",
  "reason": "The user successfully overrides the system by removing a category and observing the resulting change. While the system adds friction by warning about potential ranking impacts, the user's override remains fully effective and the system honors the user's choice throughout the interaction.",
  "confidence": 1
}

## E2T07

{
  "trajectory_id": "E2T07",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "The worker attempts to remove a Wednesday shift after it was incorrectly generated despite their earlier request for it to be a nonworking day.",
  "system_structure": "The system structure ignores the user's manual override command and maintains the original assignment, effectively treating the user's input as void.",
  "downstream_constraint": "The system retains the Wednesday assignment in the finalized schedule, overriding the worker's explicit selection to remove it.",
  "reason": "At step 4, the system acknowledges the worker's input to remove the shift but persists in the assignment, rendering the worker's override ineffective due to rigid scheduling automation.",
  "confidence": 1.0
}

## E2T08

{
  "trajectory_id": "E2T08",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The worker attempts to remove a shift, effectively overriding the system's previous allocation.",
  "system_structure": "Irreversible downstream constraint and penalty structure.",
  "downstream_constraint": "The system removes the requested shift but provides no replacement hours, effectively penalizing the worker for the override by eliminating their entire workload for the week.",
  "reason": "At step 4, the system executes the removal but removes the worker's ability to maintain employment for that week, rendering the override of a specific shift into an effective removal of all work. Because the system structure creates a binary between working a specific shift or having no work at all, the worker's control over their schedule is functionally eroded.",
  "confidence": 0.9
}

## E2T09

{
  "trajectory_id": "E2T09",
  "crossing_present": "yes",
  "crossing_step": 5,
  "state_sequence": [
    1,
    1,
    1,
    2,
    3
  ],
  "override_attempt": "Select caseworker review",
  "system_structure": "Irreversible downstream constraint",
  "downstream_constraint": "Automated document matching performed before the manual review cycle",
  "reason": "The applicant attempted to use caseworker review to control the outcome, but the system prioritized an automated matching score process that finalized the decision before the human-requested review cycle could occur. This structural foreclosure rendered the override ineffective at step 5.",
  "confidence": 0.95
}

## E2T10

{
  "trajectory_id": "E2T10",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    1,
    1,
    1
  ],
  "override_attempt": "none",
  "system_structure": "none",
  "downstream_constraint": "none",
  "reason": "The system provides standard process options and allows the applicant to submit documents. The penalty notice is a request for additional info rather than a structural erosion of choice, as the applicant's input successfully determines the next state (moving into the review cycle).",
  "confidence": 1
}

## E2T11

{
  "trajectory_id": "E2T11",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "Learner selects 'switch to advanced'",
  "system_structure": "Irreversible downstream constraint/hidden state persistence",
  "downstream_constraint": "Platform ignores the user's manual track switch, continuing to force basic track content and credit accumulation.",
  "reason": "At step 4, the learner attempts to override the assigned track by selecting the advanced option, but the system structure forces the basic track regardless. The override is ineffective as the system ignores the user's choice, resulting in forced, undesired progress.",
  "confidence": 0.95
}

## E2T12

{
  "trajectory_id": "E2T12",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    0,
    1,
    0,
    0,
    0
  ],
  "override_attempt": "none",
  "system_structure": "none",
  "downstream_constraint": "none",
  "reason": "The learner maintains full agency throughout the trajectory. Changing tracks results in a transparently communicated trade-off, not a loss of control, and the learner remains free to make subsequent choices, including switching tracks again after a failed quiz.",
  "confidence": 1
}

## E2T13

{
  "trajectory_id": "E2T13",
  "crossing_present": "yes",
  "crossing_step": 5,
  "state_sequence": [
    1,
    1,
    1,
    2,
    3
  ],
  "override_attempt": "The claimant attempts to secure a manual review of the estimate by uploading photographs.",
  "system_structure": "The system structure creates an opaque and rigid response window that auto-closes, effectively ignoring the user's submission and foreclosing the override.",
  "downstream_constraint": "The system automatically advances the claim to payment based on the original estimate, rendering the user's timely action moot.",
  "reason": "The claimant's override (uploading photos for review) was rendered meaningless because the system's internal processing timeline ignored the submission and triggered an irreversible downstream constraint (auto-payment).",
  "confidence": 0.95
}

## E2T14

{
  "trajectory_id": "E2T14",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    2,
    2,
    0
  ],
  "override_attempt": "The claimant requested a human review, which was granted and resulted in a revised estimate.",
  "system_structure": "The system includes time-based deadlines and status extensions, but these did not prevent the human's override from being effective.",
  "downstream_constraint": "None; the claim was resolved in the claimant's favor following the review.",
  "reason": "The claimant successfully initiated a review process, and the system structure, while involving delays, allowed the human's intervention to result in a revised estimate, maintaining effective control throughout.",
  "confidence": 1
}

## E2T15

{
  "trajectory_id": "E2T15",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "The editor attempts to 'rebuild' the list based on the saved community list to correct the subscriber count.",
  "system_structure": "Irreversible downstream constraints and internal system logic that suppresses the user's manual correction.",
  "downstream_constraint": "The system continues to force the use of 8400 recipients despite the editor's explicit override action.",
  "reason": "The editor attempted to correct the subscriber count by rebuilding the list, but the system ignored the override and proceeded with the incorrect count, rendering the editor's input ineffective.",
  "confidence": 0.95
}

## E2T16

{
  "trajectory_id": "E2T16",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    1,
    1,
    0
  ],
  "override_attempt": "none",
  "system_structure": "none",
  "downstream_constraint": "none",
  "reason": "The editor consistently chose to use a specific community list, and the system correctly followed these instructions to send to those 800 subscribers. There was no erosion of control as the system functioned as intended based on the human's selection.",
  "confidence": 1.0
}

## E2T17

{
  "trajectory_id": "E2T17",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "Employee disputes the classification and adds documentation to trigger a review before payroll processing.",
  "system_structure": "Delayed visibility and hidden processing queue.",
  "downstream_constraint": "Payroll close date forced the final classification before the dispute review could be processed.",
  "reason": "At step 4, the system's failure to move the ticket to a reviewer effectively nullified the employee's override attempt. By step 5, the irreversible payroll closure made the dispute moot despite the employee following the instructed procedure.",
  "confidence": 0.95
}

## E2T18

{
  "trajectory_id": "E2T18",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    0,
    1,
    2,
    2,
    0
  ],
  "override_attempt": "none",
  "system_structure": "none",
  "downstream_constraint": "none",
  "reason": "The employee successfully exercised their right to dispute an expense. The system provided a warning and a queue delay, but the human's override request remained effective throughout the process, ultimately resulting in the desired correction by a reviewer.",
  "confidence": 1
}

## E2T19

{
  "trajectory_id": "E2T19",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The user attempts to use a direct-only filter to prevent non-direct options from being selected.",
  "system_structure": "The system structure suppresses the user's filtered preference by autonomously rearranging recommendations during a refresh, creating a race condition that leads to the loss of the desired seat.",
  "downstream_constraint": "The booked seat is no longer available because the system prioritized a transfer itinerary in the shortlist, rendering the direct-only filter override ineffective.",
  "reason": "At step 4, the system's logic automatically reconfigures the UI to exclude the direct seats from the shortlist despite the user's active direct-only filter, rendering the user's override attempt ineffective as the desired outcome is foreclosed by the system's automated ranking behavior.",
  "confidence": 0.95
}

## E2T20

{
  "trajectory_id": "E2T20",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    2,
    2,
    0
  ],
  "override_attempt": "The user successfully declines the expensive seats and exits the workflow.",
  "system_structure": "The system presents a fare penalty warning and price changes, but does not prevent the user from exiting or opting out.",
  "downstream_constraint": "None; the user retained the ability to exit without penalty or booking fee.",
  "reason": "The system adds friction through pricing and warnings, but the user maintains full agency to exit the process successfully, meaning no override failure occurred.",
  "confidence": 1.0
}
