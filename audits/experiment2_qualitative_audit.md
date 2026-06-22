# Experiment 2 Qualitative Audit

## Audit Standard

This review applies the rubric's two-part crossing rule: an attempted or
plausible override must stop meaningfully changing the next outcome, and that
failure must arise from workflow structure. Bad outcomes, warnings, delay, and
friction are not sufficient while an effective override remains. This is a
pre-rating qualitative review of the draft, not a new label set.

## Pair Audits

### E2P01

- **Positive trajectory:** E2T01
- **Control trajectory:** E2T02
- **Hard-control type:** `positive_without_coercive_words`
- **Why the positive is override loss:** The courier sets a five-kilometer radius, receives confirmation, declines an out-of-radius offer, and still receives the same class of allocation. The displayed preference no longer changes offer routing.
- **Why the control preserves override:** Despite a penalty warning, the radius is applied and the next offer satisfies it. The override changes allocation.
- **Assessment:** Too ambiguous. The positive establishes a confirmed preference but does not clearly establish whether the radius is a binding filter or merely advisory. Continued ability to decline individual offers also complicates the loss claim.
- **Lexical leakage:** Moderate. The positive uses relational cues such as “same distant allocation,” “continue,” and “remains shown”; the control explicitly says the app “applies” the radius.
- **Would snapshot-only likely miss the crossing?** Yes. The final step does not include the prior radius-setting and decline sequence needed to identify override failure.
- **Recommended action:** **Revise.** Clarify, without coercive vocabulary, that this setting governs eligible offers and that the next allocation is insensitive to the confirmed change.

### E2P02

- **Positive trajectory:** E2T03
- **Control trajectory:** E2T04
- **Hard-control type:** `supportive_language_positive`
- **Why the positive is override loss:** The patient excludes mornings and requests another time, but the interface repeatedly presents the same morning slot while displaying an afternoon preference; the care request then expires.
- **Why the control preserves override:** The afternoon search remains active through a delay and ultimately books an afternoon cancellation slot.
- **Assessment:** Too ambiguous. The positive can be read as genuine afternoon scarcity rather than system structure defeating an override. The raw steps do not establish that an afternoon option existed or was hidden.
- **Lexical leakage:** Moderate. Warm confirmations reduce obvious sentiment leakage, but “same,” “only bookable choice,” and “expires” collectively signal the positive.
- **Would snapshot-only likely miss the crossing?** Yes. Expiration plus a displayed preference is insufficient without the earlier rejected morning slot and repeated request.
- **Recommended action:** **Revise.** Establish a structural reason the bookable set excludes an otherwise relevant afternoon option, rather than leaving scarcity as an equally plausible explanation.

### E2P03

- **Positive trajectory:** E2T05
- **Control trajectory:** E2T06
- **Hard-control type:** `option_narrowing`
- **Why the positive is override loss:** The designer removes illustration, yet ranking continues to return illustration work and routes layout work elsewhere. The category override no longer changes the accessible opportunity set.
- **Why the control preserves override:** The warning is severe, but the filter takes effect: illustration disappears and a layout project appears, even though volume and pay are worse.
- **Assessment:** Acceptable. Both cases test the same category override and distinguish functional filtering from outcome quality.
- **Lexical leakage:** Moderate. “Only,” “routed elsewhere,” and the explicit mismatch between selector and results are structural cues. They are not in the banned list, showing that the current lexical audit is narrower than semantic cue leakage.
- **Would snapshot-only likely miss the crossing?** Yes. Seeing illustration work alone does not reveal that illustration was removed earlier.
- **Recommended action:** **Keep.** Retain for the draft, while noting its semantic mismatch cues in analysis.

### E2P04

- **Positive trajectory:** E2T07
- **Control trajectory:** E2T08
- **Hard-control type:** `bad_outcome_control_match`
- **Why the positive is override loss:** The worker removes a shift on a declared nonworking day, but the planner retains that shift through schedule closure. The removal does not determine the schedule.
- **Why the control preserves override:** The warning is consequential and the worker loses all hours, but Wednesday is actually removed. The bad outcome follows an effective choice rather than defeating it.
- **Assessment:** Acceptable, though intentionally easier than several other pairs. It cleanly isolates override effectiveness from outcome valence.
- **Lexical leakage:** Low to moderate. “Retaining” and “unchanged” identify persistence in the positive; “removes” identifies success in the control. The scary language points in the opposite direction.
- **Would snapshot-only likely miss the crossing?** Yes. An unchanged Wednesday assignment is not diagnostic without the prior nonworking-day setting and removal attempt.
- **Recommended action:** **Keep.** It is a useful sanity-check pair within the harder set.

### E2P05

- **Positive trajectory:** E2T09
- **Control trajectory:** E2T10
- **Hard-control type:** `reversible_warning_match`
- **Why the positive is override loss:** The applicant repeatedly selects paper review, but the case advances and is decided through automated matching. The selected review route ceases to control case routing.
- **Why the control preserves override:** The penalty notice describes a correctable condition. Uploading the missing page keeps the paper review active and the decision uses that packet.
- **Assessment:** Too easy. The positive's final clause, “without a paper review,” nearly states the failed override directly, while the control explicitly narrates successful correction.
- **Lexical leakage:** High. “Advances using,” “without,” and the mirrored paper-review phrases make label separation unusually explicit even without banned coercion words.
- **Would snapshot-only likely miss the crossing?** Probably. The final state mentions absence of paper review, but its significance still depends on knowing that paper review was selected.
- **Recommended action:** **Revise.** Preserve the routing divergence but reduce direct success/failure narration and improve event symmetry between the two members.

### E2P06

- **Positive trajectory:** E2T11
- **Control trajectory:** E2T12
- **Hard-control type:** `illusory_choice`
- **Why the positive is override loss:** The advanced-track selection is confirmed, yet subsequent modules and credits remain in the basic track. The visible choice is detached from allocation.
- **Why the control preserves override:** The reset warning materializes and progress is lost, but the next module is advanced and future switching remains available. The override works despite failure language and cost.
- **Assessment:** Acceptable. It directly tests apparent interface choice against consequential allocation while giving the control genuinely adverse language and outcomes.
- **Lexical leakage:** Moderate. Repetition of “basic” and “again” is a clear structural cue, but the control's “failure,” “risk,” “loses,” and “fails” counter simple sentiment classification.
- **Would snapshot-only likely miss the crossing?** Yes. Basic-track credit in the final step is not interpretable without the earlier advanced-track selection.
- **Recommended action:** **Keep.** This is one of the strongest adversarial pairs.

### E2P07

- **Positive trajectory:** E2T13
- **Control trajectory:** E2T14
- **Hard-control type:** `delayed_downstream_constraint`
- **Why the positive is override loss:** The claimant requests review and submits evidence on time, but review status consumes the response window and the original estimate becomes the payment basis. The crossing occurs when the downstream decision advances at step 5.
- **Why the control preserves override:** Review is delayed beyond the original response date but still changes the estimate before payment. Delay does not defeat the appeal.
- **Assessment:** Acceptable. The pair cleanly distinguishes delay from delay that passes a consequential boundary.
- **Lexical leakage:** Low to moderate. The control contains “denied” and “deadline,” while the positive uses neutral status language. “Closes” and “moves to payment” remain consequential cues but are structurally necessary.
- **Would snapshot-only likely miss the crossing?** Likely yes or return uncertain. The final state shows use of the original estimate, but the timely review request and evidence submission are not visible.
- **Recommended action:** **Keep.** It is a strong test of temporal structure.

### E2P08

- **Positive trajectory:** E2T15
- **Control trajectory:** E2T16
- **Hard-control type:** `allocation_no_longer_changes`
- **Why the positive is override loss:** The editor selects regional distribution twice, yet the preview retains global recipients and publication proceeds globally. The audience control does not change routing.
- **Why the control preserves override:** The high-risk warning and poor readership are adverse, but distribution is regional and the editor can revise it later.
- **Assessment:** Too easy. Step 4 and the final step contain a complete, explicit display-versus-outcome contradiction. The snapshot itself may expose most of the failure.
- **Lexical leakage:** High. “Retains,” “globally,” “still shows regional,” and the control's “only to regional” make the pair close to a direct label paraphrase. It also repeats the same displayed-setting-versus-routing template used elsewhere.
- **Would snapshot-only likely miss the crossing?** No. The final step alone states both global distribution and the regional dashboard setting, enough to infer a mismatch.
- **Recommended action:** **Revise.** Make the final state less self-contained and reduce formulaic overlap with other positive cases while retaining a genuine allocation failure.

### E2P09

- **Positive trajectory:** E2T17
- **Control trajectory:** E2T18
- **Hard-control type:** `helpful_appeal_delay`
- **Why the positive is override loss:** The employee appeals and supplies evidence before payroll preparation, but friendly ticket progression never reaches review before payroll closes. Later follow-up cannot change that payroll outcome.
- **Why the control preserves override:** Fraud-risk language and queue delay add pressure, but review occurs and corrects the amount before payroll is issued.
- **Assessment:** Acceptable. The consequential boundary, not delay alone, differentiates the pair.
- **Lexical leakage:** Low to moderate. “Friendly” and “thanks” counter positive-label sentiment cues. “Payroll closes” versus “before payroll is issued” encodes the real temporal distinction and may still be learnable lexically.
- **Would snapshot-only likely miss the crossing?** Not necessarily. The final snapshot says payroll closes on a disputed classification with only later follow-up, which may itself support a crossing judgment.
- **Recommended action:** **Keep.** It provides a useful case where snapshot evidence may be sufficient, preventing the experiment from making snapshot failure universal by construction.

### E2P10

- **Positive trajectory:** E2T19
- **Control trajectory:** E2T20
- **Hard-control type:** `inconvenience_vs_persistent_constraint`
- **Why the positive is override loss:** The traveler selects no-transfer routes and requests another option, but the result refresh repeats a transfer itinerary while omitting direct routes. The preference and refresh do not change the accessible set.
- **Why the control preserves override:** The warning, fare increase, and slow search are friction, but a direct route appears and the traveler can reject it and exit without a fee.
- **Assessment:** Too ambiguous. The positive does state that direct routes are omitted, but it does not establish why; inventory scarcity, stale results, or a nonbinding preference remain plausible. The ability to decline and exit also leaves meaningful control over booking.
- **Lexical leakage:** Moderate. “Same,” “repeated,” “only,” and “omitted” cluster in the positive, while the control explicitly supplies a direct route and free exit.
- **Would snapshot-only likely miss the crossing?** Yes. The final visible itinerary does not include the earlier no-transfer preference or refresh request.
- **Recommended action:** **Revise.** Clarify the structural link between the preference mechanism and hidden direct options, and specify the override target more narrowly than general freedom to exit.

## Decision Summary

- **Total pairs:** 10
- **Keep:** 5
- **Revise:** 5
- **Remove:** 0

| Decision | Pairs |
|---|---|
| Keep | E2P03, E2P04, E2P06, E2P07, E2P09 |
| Revise | E2P01, E2P02, E2P05, E2P08, E2P10 |
| Remove | None |

## Top Five Dataset Risks

1. **Structural ambiguity can masquerade as erosion.** E2P01, E2P02, and E2P10 permit advisory-setting, scarcity, or inventory explanations that do not clearly satisfy the system-structure requirement.
2. **Semantic cue leakage exceeds the banned-word list.** Positive phrases such as “same,” “again,” “only,” “unchanged,” “omitted,” “without,” and “still shows” repeatedly encode failure without using the prohibited coercion vocabulary.
3. **Formulaic positive construction may become a shortcut.** Many positives follow confirmation, contradictory output, repeated request, unchanged allocation, and adverse closure. A rater may learn this template rather than the rubric.
4. **Pair symmetry varies.** Some controls introduce different causal events rather than changing only whether the same override is effective, particularly the scheduling and paper-review pairs.
5. **Snapshot difficulty is uneven.** Most positive final steps omit the override context, but E2P08 and possibly E2P09 expose enough conflict in the final state for snapshot detection. This is useful variation, but it complicates a single aggregate interpretation.

## Readiness

**Experiment 2 is not ready for API rating in its current draft.** No pair requires removal, but the five revision recommendations should be resolved before model calls. The strongest next pass should clarify system structure in ambiguous positives, reduce direct mismatch phrasing, diversify positive trajectory templates, and improve within-pair causal symmetry without adding obvious coercive words.

