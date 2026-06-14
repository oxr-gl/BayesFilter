# P50-M2 Subplan: One-Step Value Path Implementation

metadata_date: 2026-06-09
phase: P50-M2
status: PLAN_REVIEW_CONVERGED

## Objective

Implement or repair the smallest deterministic one-step filter value path that
wires retained-state, proposal correction, recentering, Jacobian, and
normalizer accounting together.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the deterministic one-step value path satisfy the M1 contract on small controlled references? |
| Baseline/comparator | M1 contract, exact/dense one-step references, Kalman/CUT4 where applicable. |
| Primary pass criterion | Focused one-step tests pass for accounting identity, shape, dtype, and reference value agreement under declared tolerances. |
| Veto diagnostics | Value agreement obtained by dropping Jacobian/proposal/normalizer terms; NumPy promoted into BayesFilter implementation; nondifferentiable randomness in the value path. |
| Not concluded | No sequential likelihood completion, gradient accuracy, or HMC readiness. |

## Planned Work

1. Inspect current deterministic fixed-branch and P49 helper APIs.
2. Implement the minimal one-step integration or document a blocker.
3. Add focused tests against exact/dense references.
4. Preserve CPU-only validation artifacts.

## Repair Loop

Fix local implementation/test failures with clear scope.  Stop for package
installation, backend-policy change, or missing mathematical specification.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p50-m2-one-step-value-path-result-2026-06-09.md`

Required token:

`PASS_P50_M2_ONE_STEP_VALUE_PATH` or
`BLOCK_P50_M2_ONE_STEP_VALUE_PATH`
