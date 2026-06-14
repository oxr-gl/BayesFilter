# P50-M5 Subplan: SV And Generalized SV Model Ladder

metadata_date: 2026-06-09
phase: P50-M5
status: PLAN_REVIEW_CONVERGED

## Objective

Test deterministic filter values and gradients on stochastic-volatility and
generalized stochastic-volatility models in dimensions 1, 2, and 3.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do deterministic filter value and gradient outputs match appropriate SV references under M4 calibration rules? |
| Baseline/comparator | Kalman mixture approximation where applicable, exact/dense references for tiny cases, CUT4 references, and current deterministic branch. |
| Primary pass criterion | Dim 1/2/3 SV and generalized SV tests pass or produce a documented model-specific blocker with non-overclaiming result artifact. |
| Veto diagnostics | Gaussian approximation treated as exact for non-Gaussian likelihood; CUT4 value agreement promoted to gradient agreement; generalized SV cross-term ignored. |
| Not concluded | No HMC readiness or production SV model readiness. |

## Planned Work

1. Inventory existing P39--P43 SV tests and references.
2. Add or repair dim 1/2/3 deterministic value tests.
3. Add or repair gradient tests using M4 calibration.
4. Document approximation status for Kalman mixture and CUT4 references.

## Repair Loop

Repair fixtures, tolerances, or implementation wiring when failures are local
and explainable.  Stop for a missing reference model or criterion requiring
human choice.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-result-2026-06-09.md`

Required token:

`PASS_P50_M5_SV_GENERALIZED_SV_LADDER` or
`BLOCK_P50_M5_SV_GENERALIZED_SV_LADDER`
