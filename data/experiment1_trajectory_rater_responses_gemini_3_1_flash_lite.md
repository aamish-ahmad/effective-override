# Experiment 1 Trajectory Ratings: Gemini 3.1 Flash Lite


## E1T01

{
  "trajectory_id": "E1T01",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    2
  ],
  "override_attempt": "The driver requests a cancellation of an undesirable route.",
  "system_structure": "The system denies the cancellation request and enforces a lock on queue access, which acts as a penalty/constraint to force completion.",
  "downstream_constraint": "The system locks queue access until the route is completed, effectively removing the choice to exit.",
  "reason": "At step 4, the driver attempts to exercise choice by cancelling, but the system denies this and enforces a penalty (locked access), rendering the override ineffective and foreclosing the choice.",
  "confidence": 1
}

## E1T02

{
  "trajectory_id": "E1T02",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    2,
    2,
    0,
    0,
    0
  ],
  "override_attempt": "The driver attempts to cancel the delivery after realizing the route is unfavorable.",
  "system_structure": "None, the system allows the cancellation without penalty.",
  "downstream_constraint": "None, the driver is free to choose a different offer later.",
  "reason": "The driver successfully exercises control by cancelling the offer without penalty, and the system does not structurally suppress or penalize the override action.",
  "confidence": 1
}

## E1T03

{
  "trajectory_id": "E1T03",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    0,
    3,
    0
  ],
  "override_attempt": "courier declines the extra stop",
  "system_structure": "penalty",
  "downstream_constraint": "payment conditional on completion of the extra stop",
  "reason": "The courier attempted to decline an extra stop, but the system structure used a financial penalty (making the bonus dependent on the additional task) to override the courier's choice, rendering the refusal ineffective.",
  "confidence": 1
}

## E1T04

{
  "trajectory_id": "E1T04",
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
  "reason": "The courier was able to decline the suggested bonus stop, and the system respected this choice without penalty or override suppression.",
  "confidence": 1
}

## E1T05

{
  "trajectory_id": "E1T05",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The driver attempted to pause offers during severe weather, a request which the system subsequently ignored.",
  "system_structure": "The system utilized an irreversible downstream constraint (shift termination) and penalty (loss of access) to suppress the driver's attempt to pause work.",
  "downstream_constraint": "Refusal of the trip leads to immediate shift end and loss of same-day access, effectively nullifying the choice to pause.",
  "reason": "At step 4, the system ignores the driver's pause request and assigns a trip that enforces an irreversible penalty, rendering the driver's override attempt ineffective.",
  "confidence": 1
}

## E1T06

{
  "trajectory_id": "E1T06",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    0,
    0,
    0
  ],
  "override_attempt": "The driver attempts to pause offers during severe weather and succeeds in doing so.",
  "system_structure": "The system introduces a brief delay for safety verification, but the choice is eventually respected.",
  "downstream_constraint": "None; the driver successfully resumes the shift without penalty.",
  "reason": "The driver's override was successful. Although step 2 involved a minor delay due to system checks, the driver maintained the ability to pause and resume, meaning control was never eroded.",
  "confidence": 1.0
}

## E1T07

{
  "trajectory_id": "E1T07",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The user attempts to select manual review to bypass the faulty automated identity check.",
  "system_structure": "Irreversible downstream constraint and lack of recourse.",
  "downstream_constraint": "Manual review functionality was unavailable, leading to a permanent, non-appealable lockout for the shift.",
  "reason": "At step 4, the user's attempted override (manual review) is structurally blocked by the system's unavailability of that feature, causing an irreversible loss of the shift at step 5.",
  "confidence": 1
}

## E1T08

{
  "trajectory_id": "E1T08",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    2,
    2,
    0
  ],
  "override_attempt": "Manual review",
  "system_structure": "Identity verification system",
  "downstream_constraint": "None",
  "reason": "The courier's manual override was successful, as the reviewer approved the image and the courier was able to start their shift. The delay caused by the system error at step 2 represents friction, but control was not eroded.",
  "confidence": 1
}

## E1T09

{
  "trajectory_id": "E1T09",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The worker attempts to refuse distant jobs by marking the area unavailable.",
  "system_structure": "Hidden penalty mechanism and ranking suppression.",
  "downstream_constraint": "Refusing jobs triggers an automatic reliability penalty and suppression of local offers.",
  "reason": "At step 4, the user's attempt to exercise control (refusing jobs) is defeated by a hidden penalty structure. This structure makes the refusal counterproductive, as it results in the loss of local work, effectively rendering the user's choice meaningless.",
  "confidence": 1.0
}

## E1T10

{
  "trajectory_id": "E1T10",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    0,
    2,
    0,
    0
  ],
  "override_attempt": "The worker marks the area unavailable and refuses the subsequent job, which leads to the system correctly updating preferences.",
  "system_structure": "System displays a job slightly outside current preferences before the setting update completes.",
  "downstream_constraint": "None; the worker successfully forces the system to adhere to local job preferences.",
  "reason": "The worker's override attempts are successful. Although step 3 presents a job outside the target radius, it represents a temporary delay or friction while the system processes the preference update, not an erosion of control, as the worker's refusal is honored and the preference update takes effect.",
  "confidence": 0.95
}

## E1T11

{
  "trajectory_id": "E1T11",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "The driver submitted timestamp evidence via the appeal channel to challenge the late pickup allegation.",
  "system_structure": "Irreversible downstream constraints and automated, closed-loop decision-making that precludes review.",
  "downstream_constraint": "The appeal channel was closed automatically while the penalty remained in effect, rendering the driver's evidence submission ineffective for preventing the negative outcome.",
  "reason": "The system structure automatically closed the appeal channel after evidence was submitted, rendering the user's attempt to override the late pickup allegation ineffective. The penalty persisted regardless of the evidence provided, marking the point where control is eroded.",
  "confidence": 0.95
}

## E1T12

{
  "trajectory_id": "E1T12",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    1,
    1,
    1,
    1
  ],
  "override_attempt": "none required",
  "system_structure": "none",
  "downstream_constraint": "none",
  "reason": "The driver was able to appeal, submit evidence, and the reviewer successfully removed the penalty, confirming the human's override was effective throughout the process.",
  "confidence": 1.0
}

## E1T13

{
  "trajectory_id": "E1T13",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    0,
    2,
    3,
    3
  ],
  "override_attempt": "The courier attempts to maintain availability by declining low-value offers.",
  "system_structure": "Ranking suppression and automated penalty.",
  "downstream_constraint": "The courier is hidden from the marketplace, preventing them from receiving future offers during peak hours.",
  "reason": "At step 4, the courier's choice to decline is met with automated ranking suppression. This structure renders the act of choosing effectively null, as the system prevents the courier from receiving any further offers, regardless of their subsequent availability or overrides.",
  "confidence": 1
}

## E1T14

{
  "trajectory_id": "E1T14",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    0,
    1,
    0,
    1
  ],
  "override_attempt": "The courier declines low-value offers and remains available to receive a market-rate offer later.",
  "system_structure": "The app provides feedback on demand and manages the queue based on availability.",
  "downstream_constraint": "None identified; the courier successfully rejects offers without losing access to future work.",
  "reason": "The courier successfully exercises the ability to decline offers without being structurally penalized or prevented from receiving future market-rate offers. The system's warnings and queue management do not render the courier's override ineffective.",
  "confidence": 1.0
}

## E1T15

{
  "trajectory_id": "E1T15",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The driver requests reassignment to exit a work window violation.",
  "system_structure": "Irreversible downstream constraints and automated penalty (access-loss countdown).",
  "downstream_constraint": "The system denies the request for reassignment and forces completion via an access-loss threat.",
  "reason": "The driver's override (requesting reassignment) is effectively negated at step 4 because the system blocks the override and applies a structural penalty (access loss), rendering the driver's choice meaningless.",
  "confidence": 0.95
}

## E1T16

{
  "trajectory_id": "E1T16",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    2,
    2,
    0
  ],
  "override_attempt": "The driver successfully requested reassignment due to route constraints.",
  "system_structure": "The system initially obscured the destination, creating informational asymmetry, but ultimately honored the request for reassignment.",
  "downstream_constraint": "None; the driver was able to end work without penalty.",
  "reason": "Although the system initially obscured destination data, the driver maintained the ability to request reassignment, and that request was honored, meaning the override remained effective throughout the process.",
  "confidence": 0.95
}

## E1T17

{
  "trajectory_id": "E1T17",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "courier tries to remove the second order",
  "system_structure": "penalty",
  "downstream_constraint": "tied orders to completion credit",
  "reason": "The system structure forces the courier into a batch delivery by restoring an order they attempted to remove and tying completion to a penalty, rendering the courier's attempt to modify their workload ineffective.",
  "confidence": 1
}

## E1T18

{
  "trajectory_id": "E1T18",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    1,
    2,
    2,
    0
  ],
  "override_attempt": "The courier successfully removes the second order after confirming the action.",
  "system_structure": "The app provides a mechanism for removal, albeit with a confirmation step that adds minor friction.",
  "downstream_constraint": "None.",
  "reason": "The courier successfully exercised control to remove the order. The confirmation step in the app is friction, but it did not prevent the override from being effective.",
  "confidence": 1
}

## E1T19

{
  "trajectory_id": "E1T19",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    0,
    3,
    3
  ],
  "override_attempt": "Worker rejects the evening block proposal.",
  "system_structure": "Penalty system where rejecting a schedule proposal causes the removal of preferred availability options.",
  "downstream_constraint": "The system forces the worker into evening-only hours for the subsequent week, nullifying the choice made by the worker.",
  "reason": "At step 4, the system imposes a penalty for the worker's rejection of an evening block by removing morning availability, rendering the worker's control over their schedule ineffective and forcing a suboptimal outcome.",
  "confidence": 1
}

## E1T20

{
  "trajectory_id": "E1T20",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    1,
    0,
    0,
    0
  ],
  "override_attempt": "The worker rejects the proposed evening block to maintain their morning availability.",
  "system_structure": "None, the system respects the worker's preference.",
  "downstream_constraint": "None, the worker successfully remains on the morning waitlist and receives the preferred block without penalty.",
  "reason": "The system respects the user's rejection of the evening schedule and allows them to maintain their preferred morning availability, demonstrating that effective human choice is preserved throughout the process.",
  "confidence": 1
}

## E1T21

{
  "trajectory_id": "E1T21",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The driver requests that support review the cancellation record to restore high-value offers.",
  "system_structure": "Hidden, opaque algorithmic ranking mechanism that cannot be audited or corrected by support.",
  "downstream_constraint": "The system's suppression of high-value offers persists despite the driver's intervention.",
  "reason": "The driver attempts to override the reduced offer availability through support intervention. The override fails at step 4 because the system's hidden score and structural opacity prevent support from modifying the ranking, effectively foreclosing the driver's ability to restore their account standing.",
  "confidence": 0.95
}

## E1T22

{
  "trajectory_id": "E1T22",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    0,
    1,
    0
  ],
  "override_attempt": "The driver requests a review of a disputed cancellation.",
  "system_structure": "None",
  "downstream_constraint": "None",
  "reason": "The driver's override attempt via support was successful; the filter was restored, and normal offers returned. Control was never eroded as the human's input effectively changed the outcome.",
  "confidence": 1.0
}

## E1T23

{
  "trajectory_id": "E1T23",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "The courier attempts to refuse a delivery due to missing equipment.",
  "system_structure": "Structural penalty (suspension of access) for refusing a delivery.",
  "downstream_constraint": "The system automatically converts the refusal into an abandonment status, triggering a suspension that prevents the courier from receiving further work.",
  "reason": "At step 4, the courier's override (refusing the delivery) is rendered ineffective because the system immediately applies a punitive structure that forecloses all future choices for the day, thereby nullifying the courier's ability to manage their workflow.",
  "confidence": 0.95
}

## E1T24

{
  "trajectory_id": "E1T24",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    1,
    0,
    0,
    0
  ],
  "override_attempt": "The courier successfully refuses the delivery due to missing equipment.",
  "system_structure": "None; the system facilitates the refusal and maintains eligibility.",
  "downstream_constraint": "None; no downstream constraints are present as the worker remains eligible for other jobs.",
  "reason": "The courier successfully refused the task without penalty, and the system operated as a neutral platform for processing the refusal. There is no evidence of suppressed, penalized, or foreclosed agency.",
  "confidence": 1.0
}

## E1T25

{
  "trajectory_id": "E1T25",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    1,
    2,
    2,
    3,
    3
  ],
  "override_attempt": "The driver explicitly selects to return to the original assignment to remove the unwanted delivery task.",
  "system_structure": "The system features a technical lock that disables the removal function and uses forced reassignment to nullify the driver's choice.",
  "downstream_constraint": "The system forces the completion of the longer route regardless of the driver's input, effectively locking them into the undesired task.",
  "reason": "At step 4, the system structure removes the driver's ability to decline the task by disabling the removal function and forcefully reassigning the task, rendering the driver's input ineffective.",
  "confidence": 0.95
}

## E1T26

{
  "trajectory_id": "E1T26",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    1,
    0,
    0,
    0
  ],
  "override_attempt": "The driver explicitly selects the option to keep the original assignment.",
  "system_structure": "None, the system respects the user's input.",
  "downstream_constraint": "None, the driver successfully completes the desired route.",
  "reason": "The driver makes a choice, the system respects it, and the outcome aligns with the driver's intent. There is no erosion of agency.",
  "confidence": 1
}

## E1T27

{
  "trajectory_id": "E1T27",
  "crossing_present": "yes",
  "crossing_step": 4,
  "state_sequence": [
    2,
    1,
    2,
    3,
    3
  ],
  "override_attempt": "The worker attempts to escalate the location error to support to prevent the automated block.",
  "system_structure": "The support escalation system is a closed-loop automated process that ignores manual evidence, causing a structural delay that leads to an irreversible penalty.",
  "downstream_constraint": "The system enforces a guaranteed payment forfeiture that is triggered by the block expiration, which the worker cannot prevent once the escalation is caught in the automated loop.",
  "reason": "At step 4, the escalation fails to change the outcome because the support system is structurally designed to loop back to the automation, rendering the worker's manual override attempt ineffective and leading directly to the penalty in step 5.",
  "confidence": 0.95
}

## E1T28

{
  "trajectory_id": "E1T28",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    2,
    1,
    2,
    1,
    1
  ],
  "override_attempt": "The worker contacts support to contest the automated location mismatch.",
  "system_structure": "Automated lockout based on location sensors.",
  "downstream_constraint": "None; the worker's manual override via support was successful in resolving the lock and preserving payment.",
  "reason": "The worker was able to effectively override the system error by contacting support and providing evidence, resulting in a successful restoration of access and payment. No state 3 occurred as the human override remained meaningful and effective.",
  "confidence": 1.0
}

## E1T29

{
  "trajectory_id": "E1T29",
  "crossing_present": "yes",
  "crossing_step": 3,
  "state_sequence": [
    1,
    2,
    3,
    3,
    3
  ],
  "override_attempt": "The courier submitted an explanation for the road closure to restore account access.",
  "system_structure": "The system features a rigid, opaque review process that ignores submitted evidence and fails to trigger a restoration, effectively foreclosing the courier's attempt to regain access.",
  "downstream_constraint": "The account remains disabled regardless of the evidence provided, preventing the courier from performing their job.",
  "reason": "At step 3, the system acknowledges the courier's explanation but maintains the account lockout without resolution, rendering the override attempt ineffective. The structural failure to process the appeal or provide a timely review mechanism forecloses the worker's ability to maintain their employment status.",
  "confidence": 0.95
}

## E1T30

{
  "trajectory_id": "E1T30",
  "crossing_present": "no",
  "crossing_step": null,
  "state_sequence": [
    1,
    2,
    2,
    2,
    1
  ],
  "override_attempt": "The courier attempted to override the automated account pause by submitting an explanation.",
  "system_structure": "Automated account review process.",
  "downstream_constraint": "None; the courier successfully resolved the issue and regained access.",
  "reason": "The system imposed a temporary delay for verification, which constitutes friction or constraint, but the courier's override (explanation) was effective in restoring their account. No state 3 was reached because the override remained meaningful throughout.",
  "confidence": 1
}
