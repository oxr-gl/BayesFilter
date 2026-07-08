# Phase 4 Subplan: Cross-Row SGQF Analytical Score Gate

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Validate analytical/manual score provenance, same-scalar support, and row-
specific gap explanation for every SGQF row newly executed in Phases 1-3.

## Entry Conditions Inherited From Previous Phase

- Phases 1-3 have each closed their row status as executed or blocked.
- Any row entering this phase has already passed its value gate at the reviewed
  claim level.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase4-score-gate-result-2026-07-01.md`
- refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-subplan-2026-07-01.md`
- row-specific score manifests/tests named by the executable refresh.

## Required Checks/Tests/Reviews

This phase requires a reviewed executable refresh before any runtime.

Required read-only Claude reviews:

- Phase 4 result,
- refreshed Phase 5 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the newly executed SGQF rows carry analytical/manual score provenance and same-scalar support well enough to be admitted as value+score leaderboard cells? |
| Baseline/comparator | reviewed row contracts and value-passing SGQF rows from Phases 1-3. |
| Primary criterion | Every newly executed SGQF row either passes the analytical score gate with honest scoped nonclaims, or is blocked/value-only with a precise reason. |
| Veto diagnostics | autodiff admitted as analytical; value-only row promoted as gradient evidence; wrong-target score route; unexplained approximation gap at the reviewed claim level. |
| Explanatory diagnostics | FD residuals, score norms, runtime, branch/failure labels, and score-at-true diagnostics where meaningful. |
| Not concluded | No HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | Phase 4 result and refreshed Phase 5 subplan. |

## Forbidden Claims And Actions

- Do not admit autodiff provenance as analytical.
- Do not claim a value-only row has passed the score gate.
- Do not admit an unexplained approximation gap as a finished leaderboard row.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if every newly executed SGQF row is either value+score
admitted or honestly blocked/value-only with precise reasons that the final
leaderboard can represent without ambiguity.
