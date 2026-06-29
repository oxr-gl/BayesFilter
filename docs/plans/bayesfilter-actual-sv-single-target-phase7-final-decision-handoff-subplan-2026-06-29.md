# Phase 7 Subplan: Final Decision And Documentation Handoff

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Write the durable final route-status decision and stop/handoff state so future
agents cannot misread partial evidence as settlement of the actual-SV target
question.

## Entry Conditions Inherited From Previous Phase

- Phase 6 gradient result exists, or the program has stopped earlier with a
  reviewed blocker that still requires a final decision artifact.
- All prior reviewed artifacts remain accessible.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase6-same-target-gradient-validation-result-2026-06-29.md`
- Phase 7 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase7-final-decision-handoff-result-2026-06-29.md`
- Updated stop handoff if blocked:
  `docs/plans/bayesfilter-actual-sv-single-target-visible-stop-handoff-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
rg -n "same-target retained|implementation variant|diagnostic-only|surrogate|blocked pending new derivation|not concluded" docs/plans/bayesfilter-actual-sv-single-target-phase7-final-decision-handoff-result-2026-06-29.md
git diff --check -- docs/plans/bayesfilter-actual-sv-single-target-phase7-*.md docs/plans/bayesfilter-actual-sv-single-target-visible-stop-handoff-2026-06-29.md
```

Claude review is required for the final decision artifact and any stop handoff
written at this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the final status of each actual-SV route and what exactly remains unresolved for future work? |
| Baseline/comparator | all reviewed phase results in this program. |
| Primary criterion | Final result lists each route status exactly, preserves non-claims, preserves blocked statuses, and writes an exact next action or stop state. |
| Veto diagnostics | silent promotion of blocked/diagnostic evidence; missing route status; missing non-claims; ambiguous next action; omitted review trail. |
| Explanatory diagnostics | review disagreements, implementation complexity, and deferred future-work notes. |
| Not concluded | Anything not established by the completed phases must remain explicit. |
| Artifact | Phase 7 final decision artifact and updated stop handoff if needed. |

## Forbidden Claims/Actions

- Do not imply a completed implementation or validation phase if it did not occur.
- Do not erase blocked or diagnostic statuses to simplify the narrative.
- Do not make a production/default/HMC claim unless a later reviewed program adds those gates.

## Exact Program Close Conditions

The program closes only if:

- every route is assigned one of the allowed final statuses;
- unresolved items are explicit;
- review trail is linked;
- exact next human/reviewed action is named.

## Stop Conditions

- Final status of at least one route cannot be written without another reset memo.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run the local final-artifact checks.
2. Write the Phase 7 final decision artifact.
3. Update the stop handoff if blocked.
4. Review the final artifact and stop state.
