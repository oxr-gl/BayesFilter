# P44-M1 Subplan: Linear Gaussian Same-Target Baseline

metadata_date: 2026-06-07
phase: P44-M1

## Decision Target

Test LGSSM dimensions 1, 2, and 3 for CUT4 and Zhao--Cui/fixed-design TT value
and gradient agreement against exact Kalman.

## Evidence Contract

Baseline: exact Kalman value and score in the declared unconstrained parameter
vector.

Score parameterization:

- M1 uses a deterministic four-coordinate unconstrained vector
  `(rho_raw, log_q, log_r, mu_raw)`.
- The fixture maps `rho_raw` through a bounded `tanh` stability transform,
  exponentiates `log_q` and `log_r` into diagonal transition and observation
  variances, and maps `mu_raw` into the initial mean.
- Kalman, CUT4, and the fixed-design TT artifact lane must rebuild the same
  physical LGSSM from this vector before differentiating the same scalar
  log-likelihood with TensorFlow autodiff.

Zhao--Cui lane boundary:

- M1 tests fixed-design TT artifact construction on the exact LGSSM filtering
  densities as the current Zhao--Cui-style retained-density lane.
- The primary M1 likelihood/score comparison for this lane is therefore the
  exact highdim LGSSM value path with TT artifacts enabled versus the same exact
  Kalman path without TT artifacts.
- M1 must not claim that the separate scalar nonlinear fixed-design TT
  propagation helper is an exact LGSSM likelihood evaluator; that helper remains
  outside the M1 promotion target unless a later reviewed repair makes it
  same-target exact.

Primary criteria:

- CUT4 value and diagnostic score match Kalman within linear-Gaussian
  tolerances.
- Zhao--Cui/fixed-design TT value and diagnostic score match exact Kalman
  within declared tolerances.
- Dense exact references, if used, are explanatory-only for LGSSM and cannot
  replace exact Kalman as the governing baseline.
- At least five deterministic directional score checks pass per dimension.

Veto diagnostics:

- likelihood convention mismatch;
- covariance or parameter transform mismatch;
- treating TT fit residual alone as likelihood correctness;
- nonfinite value, score, covariance, or normalizer.

## Implementation Sketch

1. Reuse existing `LinearGaussianSSM` fixtures where possible.
2. Add dims 1--3 deterministic observations and parameter vectors.
3. Compute Kalman reference value/score.
4. Compute CUT4 value/score on the same structural target.
5. Compute the fixed-design TT retained-density artifact lane value/score on
   the same exact highdim LGSSM value path and assert TT artifacts are built.
6. Run local focused tests plus P43/P30 public API guardrails.

## Claim Boundary

This phase can support exact same-target Tier-1 local correctness for LGSSM. It
does not support HMC readiness, paper-scale Zhao--Cui reproduction, or an
independent TT-propagated LGSSM likelihood claim.
