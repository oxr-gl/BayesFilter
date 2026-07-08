# Identifiable SSL-LSTM Oracle Geometry Diagnostic - 2026-07-08

## Decision

- geometry_sanity_passed: `False`
- vetoes: `['low_rank_dense_precision_mismatch']`
- next_justified_action: repair oracle geometry before any filtering-likelihood or HMC run

## Primary Comparison

- dense whitened precision min/max: `0.011079077440161046` / `70.14564858082295`
- low-rank accepted/status: `True` / `usable`
- relative Frobenius error: `0.9998145205348199`
- max absolute error: `63.51657479035691`

## Nonclaims

- complete-data oracle geometry diagnostic only
- not a filtering-likelihood validity result
- not HMC convergence evidence
- not posterior correctness evidence
- not sampler superiority evidence
- not Zhao-Cui source-faithfulness evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- low-rank quadratic geometry diagnostic only
- not a certified MAP covariance
- not posterior correctness evidence
- not HMC convergence evidence
- not sampler superiority evidence
- not default-readiness evidence
- not source-faithful Zhao-Cui evidence
