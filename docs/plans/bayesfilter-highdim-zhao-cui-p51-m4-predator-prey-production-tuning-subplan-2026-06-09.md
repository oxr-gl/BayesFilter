# P51-M4 Subplan: Predator-Prey Production Accuracy Tuning

metadata_date: 2026-06-09
phase: P51-M4
status: PLAN_REVIEW_CONVERGED

## Objective

Close or narrow the P50 predator-prey horizon-25 production accuracy/tuning
blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can tuning or a small deterministic-route repair make the same P50/P47 predator-prey horizon-25 production candidate meet the preserved reference/tolerance criteria? |
| Baseline/comparator | P47 M5b blocker, P50 M6 manifest row `predator_prey_production_route`, the same blocked horizon-25 target family, a declared dense horizon-25 reference, lower-rung predator-prey diagnostics for explanation only, and P50 M4 calibration rules. |
| Primary pass criterion | Predeclared production accuracy/tuning criteria pass against the declared horizon-25 reference for the same blocked P50/P47 production row, or a narrowed blocker records the limiting failure mode.  If the production reference is unavailable, the phase must block rather than pass on internal diagnostics. |
| Veto diagnostics | Post-hoc threshold loosening; lower-rung pass promoted to production; unavailable production reference hidden by internal diagnostics; unstable dynamics blamed without invariant/reference checks; finite scores promoted to certified gradients. |
| Not concluded | No production predator-prey readiness, HMC readiness, or nonlinear preconditioning usefulness unless explicitly passed. |

## Planned Work

1. Inspect current predator-prey production blocker and fixtures.
2. Record the exact P50/P47 blocked production row identity and preserved
   tolerance criteria before execution; do not substitute an easier target.
3. Define a bounded tuning ladder before running it.
4. Run the smallest discriminating diagnostic.
5. Record pass or narrowed blocker and review with Claude.

## Repair Loop

Repair local tuning/configuration bugs. Stop if passing requires changing
production criteria after seeing results.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-result-2026-06-09.md`

Required token:

`PASS_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING` or
`BLOCK_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING`

Required manifest:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-manifest-2026-06-09.json`
