# P50-M6 Subplan: Spatial SIR And Predator-Prey Ladder

metadata_date: 2026-06-09
phase: P50-M6
status: PLAN_REVIEW_CONVERGED

## Objective

Test deterministic filter values and gradients on spatial SIR and predator-prey
models without promoting diagnostic ladders to production readiness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do deterministic filter value and gradient outputs behave correctly on nonlinear multistate models under M4 calibration rules? |
| Baseline/comparator | Existing P44--P49 diagnostic targets, exact/dense tiny references, model-specific invariants, and current deterministic branch. |
| Primary pass criterion | Spatial SIR and predator-prey ladders pass declared value/gradient diagnostics or produce scoped blockers with next smallest discriminating tests. |
| Veto diagnostics | Diagnostic smoke treated as production readiness; unstable model dynamics blamed on algorithm without invariant/reference checks; gradient path hidden by clipping or nondifferentiable guards. |
| Not concluded | No production spatial SIR or predator-prey readiness. |

## Planned Work

1. Inventory existing spatial SIR and predator-prey tests.
2. Add deterministic value and gradient diagnostics under M4 rules.
3. Add invariant checks that distinguish model instability from filter bugs.
4. Record production non-claims explicitly.

## Repair Loop

Repair local implementation/test issues.  Stop for missing model specification,
backend changes, or new scientific criteria.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-result-2026-06-09.md`

Required token:

`PASS_P50_M6_SPATIAL_SIR_PREDATOR_PREY_LADDER` or
`BLOCK_P50_M6_SPATIAL_SIR_PREDATOR_PREY_LADDER`
