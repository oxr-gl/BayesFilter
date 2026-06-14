# P51-M3 Subplan: Spatial SIR Production Route Architecture

metadata_date: 2026-06-09
phase: P51-M3
status: PLAN_REVIEW_CONVERGED

## Objective

Close or narrow the P50 spatial SIR production route architecture blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current spatial SIR route avoid the all-axes retained-grid architecture blocker for the same P50/P47 blocked production row while preserving deterministic differentiability and production-row criteria? |
| Baseline/comparator | P47 M4b blocker, P50 M6 manifest row `spatial_sir_production_route`, existing spatial SIR diagnostics, route preflight tests, and P50 M4 calibration rules. |
| Primary pass criterion | A route architecture preflight passes for the same blocked production target family and route criteria recorded in P47/P50 before execution, or a narrower reviewed blocker identifies the missing architecture change.  A preflight pass does not by itself claim production spatial SIR filtering readiness. |
| Veto diagnostics | Lower-rung J=1 diagnostics are promoted to J=9 production; finite score probes are treated as certified gradients; memory/route complexity is ignored. |
| Not concluded | No production spatial SIR readiness or HMC readiness unless production and HMC criteria pass. |

## Planned Work

1. Inspect current spatial SIR route architecture and blocker tests.
2. Record the exact P50/P47 blocked production row identity before execution;
   do not substitute an easier target family or lower-rung fixture.
3. Try the smallest architecture repair or preflight narrowing.
4. Run focused route/diagnostic tests.
5. Record pass or narrowed blocker and review with Claude.

## Repair Loop

Repair code/tests if the blocker is local. Stop for a new algorithmic route
decision beyond the reviewed deterministic framework.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-result-2026-06-09.md`

Required token:

`PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT` or
`BLOCK_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT`

Required manifest:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-manifest-2026-06-09.json`
