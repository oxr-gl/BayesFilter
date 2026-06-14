# P50-M1 Subplan: Deterministic Filter Loop Contract

metadata_date: 2026-06-09
phase: P50-M1
status: PLAN_REVIEW_CONVERGED

## Objective

Specify the deterministic differentiable filter loop that integrates P49 helper
contracts for retained objects, proposal correction, ESS diagnostics,
recentering, Jacobian accounting, and normalizer accumulation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact deterministic full-loop contract should implementation phases build and test? |
| Baseline/comparator | P49 helper contracts, existing deterministic fixed branch, exact/dense/Kalman/CUT4 references. |
| Primary pass criterion | A full-loop contract defines inputs, state object, per-step operations, accounting signs, differentiability boundaries, and reference tests. |
| Veto diagnostics | Stochastic/adaptive randomness enters the HMC gradient path without a reviewed deterministic contract; normalizer or Jacobian accounting is underspecified. |
| Not concluded | No implementation completion or numerical accuracy. |

## Planned Work

1. Define deterministic filter state and per-time-step operation order.
2. Specify value-path and gradient-path requirements.
3. Specify exact, dense, Kalman, and CUT4 reference ladders.
4. Identify smallest implementation surface for M2 and M3.

## Repair Loop

Patch the contract if Claude or local audit finds ambiguous accounting, missing
stop conditions, or hidden randomness.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p50-m1-deterministic-filter-loop-contract-result-2026-06-09.md`

Required token:

`PASS_P50_M1_DETERMINISTIC_FILTER_LOOP_CONTRACT` or
`BLOCK_P50_M1_DETERMINISTIC_FILTER_LOOP_CONTRACT`
