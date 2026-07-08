# Minimal SSL-LSTM Quadratic Initializer Mechanics - 2026-07-08

## Decision

- mechanics_smoke_passed: `True`
- vetoes: `[]`
- next_justified_action: write closeout and decide whether a separate short-chain plan is warranted

## Fixed Geometry

- step size: `0.22590050090246147`
- leapfrog steps: `7`
- covariance source: `low_rank_spd_quadratic_geometry_precision_theta_coordinates`

## Mechanics Diagnostics

- samples shape: `[4, 24]`
- finite sample count: `4`
- nonfinite sample count: `0`
- acceptance rate: `1.0`
- log accept nonfinite count: `0`
- target log prob nonfinite count: `0`
- native divergence trace present: `False`

## Boundary

- HMC runtime invoked: `True`
- HMC tuning invoked: `False`

## Nonclaims

- Phase 3 bounded mechanics smoke only
- CPU-hidden debug/reference exception only
- fixed-kernel tiny HMC runtime only
- not HMC readiness evidence
- not HMC tuning success evidence
- not posterior correctness evidence
- not sampler convergence evidence
- not sampler superiority evidence
- not default-readiness evidence
- not GPU/XLA production-readiness evidence
- not source-faithful Zhao-Cui parity evidence
- native divergence telemetry unavailable is not zero divergences
- Phase 1 target-adapter admission only
- CPU-hidden debug/reference exception only
- not an HMC sample or canary result
- not HMC convergence evidence
- not posterior correctness evidence
- not a method ranking or superiority claim
- not source-faithful SSL-LSTM Zhao-Cui parity evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not LEDH evidence
