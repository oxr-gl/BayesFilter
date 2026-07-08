# Identifiable SSL-LSTM Oracle Geometry Diagnostic - 2026-07-08

## Decision

- geometry_sanity_passed: `True`
- vetoes: `[]`
- next_justified_action: try the same geometry initializer on a filtering likelihood

## Primary Comparison

- dense whitened precision min/max: `0.011079077440161046` / `70.14564858082295`
- low-rank accepted/status: `True` / `usable`
- relative Frobenius error: `0.16562858339111414`
- max absolute error: `7.017620140739954`

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
