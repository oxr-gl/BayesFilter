# Phase 2 Subplan: Actual-SV Current LEDH Adapter Repair

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Repair the current LEDH actual-SV row so it has an honest same-target value
route and same-target analytical/manual score route, or preserve a precise
blocker if the reviewed adapter cannot be proven.

## Entry Conditions Inherited From The Previous Phase

- Phase 0 froze the leaderboard baseline and row-family order.
- Phase 1 has either passed or recorded a precise LGSSM blocker that does not
  invalidate actual-SV work.
- The actual-SV row remains blocked in the July 3 leaderboard artifact.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase2-actual-sv-ledh-result-2026-07-04.md`
- Any code or benchmark edits needed for the actual-SV LEDH adapter.
- Row-local JSON/Markdown result artifact.
- Visible execution ledger update.

## Required Checks, Tests, And Reviews

- Target freeze check: row id, target, and adapter name must match the July 3
  blocked row.
- Local CPU smoke or compile check for the adapter change.
- Same-target value/score consistency check for the actual-SV row.
- `git diff --check` on touched files.
- Claude review of the phase result if the row is admitted or the blocker
  wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the actual-SV current LEDH row be repaired into a same-target value plus analytical/manual score row? |
| Baseline/comparator | The July 3 combined leaderboard actual-SV blocked row and any explicitly cited actual-SV source-row artifacts. |
| Primary criterion | Same-target actual-SV value and score are both finite and share the same route; otherwise the phase records a precise blocker. |
| Veto diagnostics | Actual-SV evidence borrowed from KSC or generalized-SV, autodiff score provenance, or a changed target. |
| Explanatory diagnostics | FD consistency, runtime, and score norm. |
| Not concluded | KSC, generalized-SV, SIR, predator-prey, UKF cleanup, or full leaderboard regeneration. |

## Forbidden Claims/Actions

- Do not promote actual-SV evidence to KSC or generalized-SV.
- Do not call autodiff score provenance analytical/manual.
- Do not reuse a sidecar as the main row.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if Phase 2 writes either:

- admitted actual-SV same-target value/score; or
- a precise actual-SV blocker that does not require reordering later phases.

## Stop Conditions

Stop and write a blocker result if:

- the current LEDH adapter is not proven for the actual-SV target;
- the score route lacks theta coordinates or manual provenance;
- the phase attempts to use another family’s evidence as admission.

## Phase-End Duties

At the end of Phase 2:

1. run the required local checks;
2. write the Phase 2 result / close record;
3. draft or refresh the Phase 3 subplan;
4. review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
