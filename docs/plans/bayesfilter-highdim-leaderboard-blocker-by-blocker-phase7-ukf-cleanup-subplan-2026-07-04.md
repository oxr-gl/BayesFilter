# Phase 7 Subplan: UKF Analytical-Score Cleanup

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Clean up remaining UKF rows so their score provenance is honest. Final
regeneration and closeout are deferred to Phase 8.

## Entry Conditions Inherited From The Previous Phase

- Phase 0 froze the leaderboard baseline and row-family order.
- Phases 1-6 have each either passed or recorded precise blockers for the row
  family they targeted.
- The combined leaderboard still contains value-only UKF rows with autodiff
  score provenance blocked from admission.
- Phase 8 exists as the separate final regeneration and closeout step.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase7-ukf-cleanup-result-2026-07-04.md`
- Visible execution ledger update.
- A refreshed Phase 8 subplan.

## Required Checks, Tests, And Reviews

- Confirm that no row silently changes target or family.
- Confirm that any admitted UKF score has the same target as its value route
  and no autodiff provenance.
- Run `git diff --check` on touched files.
- Claude review of the phase result if any row admission status changes or the
  blocker wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining UKF rows be cleaned up honestly before final regeneration? |
| Baseline/comparator | The July 3 combined leaderboard JSON/Markdown and the phase-local results from phases 0-6. |
| Primary criterion | UKF score provenance is honest and a Phase 8 regeneration can proceed without silent target drift. |
| Veto diagnostics | Silent row promotion, autodiff score admitted as analytical/manual, target drift, or missing blocker reason. |
| Explanatory diagnostics | Final row counts, residual blocker list, and any remaining runtime notes. |
| Not concluded | Final leaderboard regeneration, posterior correctness, HMC readiness, or GPU superiority. |

## Forbidden Claims/Actions

- Do not silently drop blocked rows.
- Do not admit autodiff scores as analytical/manual scores.
- Do not rename a row target to make it pass.

## Exact Next-Phase Handoff Conditions

Advance to Phase 8 only if:

- UKF score provenance is honest and explicit;
- the remaining blockers are still explicit;
- the phase result explains any row that stays blocked.

## Stop Conditions

Stop if:

- any row changes target without a result artifact explaining it;
- a score is admitted without same-target provenance;
- the phase tries to regenerate the leaderboard before Phase 8.

## Phase-End Duties

At the end of Phase 7:

1. run the required local checks;
2. write the Phase 7 result / close record;
3. draft or refresh the Phase 8 subplan;
4. review the Phase 8 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
