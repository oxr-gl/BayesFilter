# Phase 6 Subplan: Predator-Prey T20 Source-Scope Adapter

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Repair the predator-prey T20 source-scope adapter so the row is either admitted
with same-target value and analytical/manual score or preserved as a precise
blocker, without using P47 lower-rung diagnostic evidence as the target row.

## Entry Conditions Inherited From The Previous Phase

- Phase 0 froze the leaderboard baseline and row-family order.
- Phase 5 has either passed or recorded a precise spatial SIR blocker that does
  not invalidate predator-prey work.
- The July 3 artifact still marks predator-prey as blocked by a missing
  source-scope adapter.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase6-predator-prey-result-2026-07-04.md`
- Any code or benchmark edits needed for the source-scope adapter.
- Row-local JSON/Markdown result artifact.
- Visible execution ledger update.

## Required Checks, Tests, And Reviews

- Target freeze check: distinguish the T20 source-scope row from the P47 lower-
  rung diagnostic fixture.
- Same-target value/score consistency check for the predator-prey row.
- Source-anchor audit if any source-faithful wording is used.
- `git diff --check` on touched files.
- Claude review of the phase result if the row is admitted or the blocker
  wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the predator-prey T20 source-scope row be repaired into same-target value plus analytical/manual score? |
| Baseline/comparator | The July 3 combined leaderboard predator-prey blocked row and any explicitly cited predator-prey source-row artifacts. |
| Primary criterion | Same-target predator-prey value and score are both finite and share the same route; otherwise the phase records a precise blocker. |
| Veto diagnostics | P47 lower-rung diagnostic promoted to T20 row; autodiff score provenance; target drift; source-faithful wording without anchors. |
| Explanatory diagnostics | FD consistency, runtime, score norm, and source-anchor audit. |
| Not concluded | UKF cleanup or full leaderboard regeneration. |

## Forbidden Claims/Actions

- Do not promote P47 diagnostic evidence to the T20 row.
- Do not call autodiff score provenance analytical/manual.
- Do not use source-faithful wording without anchors.

## Exact Next-Phase Handoff Conditions

Advance to Phase 7 only if Phase 6 writes either:

- admitted predator-prey same-target value/score; or
- a precise predator-prey blocker that does not require reordering later phases.

## Stop Conditions

Stop and write a blocker result if:

- the source-scope adapter is not proven for the T20 row;
- the phase tries to use P47 lower-rung evidence as admission;
- the score route lacks theta coordinates or manual provenance.

## Phase-End Duties

At the end of Phase 6:

1. run the required local checks;
2. write the Phase 6 result / close record;
3. draft or refresh the Phase 7 subplan;
4. review the Phase 7 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
