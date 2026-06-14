# P50-M3 Subplan: Sequential Likelihood Path

metadata_date: 2026-06-09
phase: P50-M3
status: PLAN_REVIEW_CONVERGED

## Objective

Extend the deterministic one-step value path into a multi-step sequential
likelihood path with stable accumulation and explicit accounting.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the deterministic sequential likelihood path accumulate step values and accounting terms correctly? |
| Baseline/comparator | M2 one-step path, exact/Kalman references for low-dimensional linear or transformed models, existing deterministic branch. |
| Primary pass criterion | Multi-step tests pass for reproducibility, accumulation identity, shape/dtype, and low-dimensional reference agreement. |
| Veto diagnostics | Sequential pass relies on per-step tests only; log-likelihood signs drift; hidden state mutation breaks autodiff; stochastic randomness enters the HMC path. |
| Not concluded | No model-suite completion, gradient accuracy, or HMC readiness. |

## Planned Work

1. Add or repair sequential loop wiring.
2. Add multi-step low-dimensional reference tests.
3. Record limitations and model coverage.

## Repair Loop

Repair deterministic loop and test fixtures.  Stop only for human-required
backend, dependency, or mathematical-specification changes.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p50-m3-sequential-likelihood-path-result-2026-06-09.md`

Required token:

`PASS_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH` or
`BLOCK_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH`
