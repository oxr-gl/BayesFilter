# Phase 5 Subplan: Spatial SIR Full Observed-Data/Filtering Route

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Repair the spatial SIR observed-data/filtering route so the full `j9_T20` row
is either admitted with same-target value and manual score or preserved as a
precise blocker separate from the scoped P91 local component route.

## Entry Conditions Inherited From The Previous Phase

- Phase 0 froze the leaderboard baseline and row-family order.
- Phase 4 has either passed or recorded a precise generalized-SV blocker that
  does not invalidate spatial SIR work.
- The July 3 artifact still marks the full spatial SIR row as blocked because
  the full observed-data/filtering evaluator is missing.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase5-spatial-sir-result-2026-07-04.md`
- Any code or benchmark edits needed for the full observed-data/filtering
  route.
- Row-local JSON/Markdown result artifact.
- Visible execution ledger update.

## Required Checks, Tests, And Reviews

- Target freeze check: distinguish the full observed-data/filtering row from
  the P91 local complete-data sidecar.
- Same-target value/score consistency check for the full spatial SIR row.
- Local CPU smoke or compile check for any adapter change.
- `git diff --check` on touched files.
- Claude review of the phase result if the row is admitted or the blocker
  wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the full spatial SIR observed-data/filtering row be repaired into same-target value plus analytical/manual score? |
| Baseline/comparator | The July 3 combined leaderboard spatial SIR blocked row and the P91 local component artifacts only as explicitly labeled sidecar evidence. |
| Primary criterion | Full spatial SIR observed-data/filtering value and score are both finite and share the same route; otherwise the phase records a precise blocker. |
| Veto diagnostics | P91 local component promoted to full row; target drift; autodiff score provenance; missing observed-data/filtering evaluator. |
| Explanatory diagnostics | FD consistency, runtime, and score norm. |
| Not concluded | Actual-SV, KSC, generalized-SV, predator-prey, UKF cleanup, or full leaderboard regeneration. |

## Forbidden Claims/Actions

- Do not promote P91 local component evidence to the full row.
- Do not call autodiff score provenance analytical/manual.
- Do not use a sidecar as the main row.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if Phase 5 writes either:

- admitted full spatial SIR same-target value/score; or
- a precise spatial SIR blocker that does not require reordering later phases.

## Stop Conditions

Stop and write a blocker result if:

- the full observed-data/filtering evaluator remains missing;
- the phase tries to use P91 local component evidence as admission;
- the score route lacks theta coordinates or manual provenance.

## Phase-End Duties

At the end of Phase 5:

1. run the required local checks;
2. write the Phase 5 result / close record;
3. draft or refresh the Phase 6 subplan;
4. review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
