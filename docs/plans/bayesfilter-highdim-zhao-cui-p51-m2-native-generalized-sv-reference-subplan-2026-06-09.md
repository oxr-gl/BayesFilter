# P51-M2 Subplan: Native Generalized SV Reference

metadata_date: 2026-06-09
phase: P51-M2
status: PLAN_REVIEW_CONVERGED

## Objective

Close or narrow the native generalized SV same-target value/gradient reference
gap from P50-M5.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we construct a defensible same-target reference for native generalized SV with observation `y_t = beta s_t + exp(h_t/2) epsilon_t` and state `(s_t, h_t)`? |
| Baseline/comparator | P50-M5 blocker, P44/P45 generalized SV diagnostics, dense low-dimensional quadrature, exact likelihood identities where feasible, and P50 M4 calibration rules. |
| Primary pass criterion | Same-target value and gradient checks pass for a declared low-dimensional native generalized SV fixture, or a precise blocker explains why the reference cannot be built now. |
| Veto diagnostics | Moment-matched Kalman or transformed-residual CUT4 is treated as exact native same-target evidence; Jacobian/residual terms are hidden; value-only evidence is promoted to gradient correctness. |
| Not concluded | No production generalized SV readiness or HMC readiness unless later phases pass. |

## Planned Work

1. Inspect current generalized SV target/tests.
2. Design the smallest dense same-target fixture and gradient reference.
3. Implement or document blocker with exact missing ingredient.
4. Test under P50-M4 comparison classes and review with Claude.

## Repair Loop

Repair reference math, target identity, Jacobian, or gradient checks if Claude
finds a concrete flaw. Stop if the same-target reference requires a new
research decision not covered by P50/P51.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md`

Required token:

`PASS_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE` or
`BLOCK_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE`

Required manifest:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-manifest-2026-06-09.json`
