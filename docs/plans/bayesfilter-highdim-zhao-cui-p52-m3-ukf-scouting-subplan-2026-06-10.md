# P52-M3 Subplan: UKF Scouting And Centering Protocol

metadata_date: 2026-06-10
phase: P52-M3
status: PLAN_REVIEW_CONVERGED

## Objective

Implement UKF or block/local UKF scouting for spatial SIR as a design aid for
fixed-rank Zhao-Cui filtering.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can UKF provide deterministic centers, scales, covariance diagnostics, and effective-dimension summaries for spatial SIR d=18/d=50/d=100? |
| Baseline/comparator | Existing spatial SIR model equations, lower-rung dense references where available, and P52 rank-budget protocol. |
| Primary pass criterion | UKF scout produces finite means/covariances and a manifest of grid-center, scale, covariance-spectrum, and local-correlation diagnostics for each requested dimension. |
| Veto diagnostics | UKF likelihood or moments treated as correctness oracle; UKF failure hidden by clipping; UKF gradients promoted to HMC readiness. |
| Not concluded | No Zhao-Cui filtering correctness, no exact likelihood, no HMC readiness. |

## Planned Work

1. Define full UKF for d=18 and either full or block/local UKF for d=50/d=100.
2. Use UKF outputs only to propose grid centers, state scales, local covariance
   structure, and rank expectations.
3. Record sigma-point count (`2d + 1` for full UKF), horizon, process/observation
   covariance choices, and finite/nonfinite diagnostics.
4. Add tests that UKF scout metadata labels itself as `scout_not_truth`.
5. Compare d=18 UKF diagnostics against the lower-rung spatial SIR evidence
   only as a sanity check, not a promotion criterion.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-result-2026-06-10.md`

Required token:

`PASS_P52_M3_UKF_SCOUTING` or
`BLOCK_P52_M3_UKF_SCOUTING`
