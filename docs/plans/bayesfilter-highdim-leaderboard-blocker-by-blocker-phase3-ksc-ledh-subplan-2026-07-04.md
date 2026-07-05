# Phase 3 Subplan: KSC Current LEDH Adapter Repair

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Repair the current LEDH KSC row so it has an honest same-target value route and
same-target analytical/manual score route, or preserve a precise blocker if the
row cannot be proven.

## Entry Conditions Inherited From The Previous Phase

- Phase 0 froze the leaderboard baseline and row-family order.
- Phase 2 has either passed or recorded a precise actual-SV blocker that does
  not invalidate KSC work.
- The KSC row remains blocked in the July 3 leaderboard artifact.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase3-ksc-ledh-result-2026-07-04.md`
- Any code or benchmark edits needed for the KSC LEDH adapter.
- Row-local JSON/Markdown result artifact.
- Visible execution ledger update.

## Required Checks, Tests, And Reviews

- Target freeze check: row id, target, and adapter name must match the July 3
  blocked KSC row.
- Local CPU smoke or compile check for the adapter change.
- Same-target value/score consistency check for the KSC row.
- `git diff --check` on touched files.
- Claude review of the phase result if the row is admitted or the blocker
  wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the KSC current LEDH row be repaired into a same-target value plus analytical/manual score row? |
| Baseline/comparator | The July 3 combined leaderboard KSC blocked row and any explicitly cited KSC source-row artifacts. |
| Primary criterion | Same-target KSC value and score are both finite and share the same route; otherwise the phase records a precise blocker. |
| Veto diagnostics | KSC evidence borrowed from actual-SV or generalized-SV, autodiff score provenance, or a changed target. |
| Explanatory diagnostics | FD consistency, runtime, and score norm. |
| Not concluded | Actual-SV, generalized-SV, SIR, predator-prey, UKF cleanup, or full leaderboard regeneration. |

## Forbidden Claims/Actions

- Do not promote actual-SV evidence to KSC.
- Do not call autodiff score provenance analytical/manual.
- Do not reuse a sidecar as the main row.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if Phase 3 writes either:

- admitted KSC same-target value/score; or
- a precise KSC blocker that does not require reordering later phases.

## Stop Conditions

Stop and write a blocker result if:

- the current LEDH adapter is not proven for the KSC target;
- the score route lacks theta coordinates or manual provenance;
- the phase attempts to use another family’s evidence as admission.

## Phase-End Duties

At the end of Phase 3:

1. run the required local checks;
2. write the Phase 3 result / close record;
3. draft or refresh the Phase 4 subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
