# P48 Scientific Decision Test Ladder

metadata_date: 2026-06-09
program: P48-source-code-discrepancy-and-rewrite
status: EXECUTED_STATIC_AUDIT

## Purpose

This ladder defines the tests needed where the P48 discrepancy ledger found
`test_required` or `split_lanes` decisions.  It is not a request to loosen
P47 tolerances.  It is a route-decision ladder: fixed-branch BayesFilter,
source-faithful clean-room filtering, and exact/classical references must be
kept distinct.

## Global Evidence Rules

- Baselines must be matched target-to-target, not merely model-family-to-model
  family.
- Small fixed-design success can nominate a route but cannot certify
  paper-scale source equivalence.
- Monte Carlo routes need multi-seed uncertainty or an explicit reason one
  seed is diagnostic only.
- Adaptive source-faithful filtering may be a strong likelihood estimator
  without being a differentiable HMC likelihood.
- HMC/gradient validation remains fixed-branch unless a separate differentiable
  adaptive-route plan exists.
- The need for analytical gradients can justify a separate gradient-bearing
  adaptation, but it cannot justify labeling an ad hoc or materially different
  route as source-faithful.
- Any source-faithful BayesFilter implementation must be clean-room and
  TensorFlow / TensorFlow Probability backed.

## Ladder 0: Claim And Route Governance

Question: are all future claims route-specific?

Baselines:

- P10/P34: source understanding only.
- P46/P47: fixed-design BayesFilter evidence and blockers only.

Promotion criterion:

- Artifacts name one of: `source_understanding`, `source_faithful_filtering`,
  `fixed_branch_gradient`, `diagnostic_smoke`, or `blocked`.

Veto diagnostics:

- Any pass token claiming adaptive MATLAB TT/SIRT reproduction from fixed-design
  grid tests.
- Any production claim from a preflight or smoke-only result.

Artifact:

- P48 result and future P49+ plan headers.

## Ladder 1: Low-Dimensional Analytic Density And Marginalization

Question: can the BayesFilter squared-density and transport machinery reproduce
known low-dimensional density normalizers, marginals, and conditionals?

Baselines:

- Analytic Gaussian and low-degree polynomial positive densities.
- Tensor-product quadrature reference for dimensions 1--3.

Primary criterion:

- Normalizer, marginal density, conditional CDF, inverse-CDF round-trip, and
  moment errors are inside predeclared tolerances with scale-aware metrics.

Veto diagnostics:

- Nonfinite normalizer.
- Negative normalized density where squared-density semantics should prevent it.
- Non-monotone conditional CDF.
- Branch identity mismatch in replay.

Not concluded:

- No SIR or predator-prey production readiness.

## Ladder 2: Source-Faithful Clean-Room One-Step Filter

Question: can a clean-room source-faithful lane reproduce the one-step
Zhao--Cui sequence: sample propagation, ESS, recentering, TT/SIRT fit,
normalizer, inverse transport sampling, and proposal correction?

Baselines:

- Exact Kalman one-step for linear-Gaussian models.
- Dense quadrature reference for scalar nonlinear models.
- Source MATLAB/Octave reduced smoke only as operational algorithm evidence,
  not bitwise target.

Primary criterion:

- Log-normalizer and posterior moments match exact/dense references within
  uncertainty-calibrated tolerances.

Veto diagnostics:

- ESS accounting inconsistent with weights.
- Jacobian or affine determinant omitted from normalizer.
- Source-like route silently falls back to all-axes pairwise grid propagation.

Not concluded:

- No adaptive-route differentiability.

## Ladder 3: SV Calibration Ladder

Question: on dimensions 1, 2, and 3, do fixed branch, CUT4, source-faithful
clean-room route, and Kalman/mixture references agree statistically where the
SV transformation gives a classical comparator?

Baselines:

- Kalman filter on mixture-Gaussian transformed SV where applicable.
- CUT4 statistical comparator.
- Dense quadrature for small dimensions and horizons.

Primary criterion:

- Value gaps and gradient directional errors are small relative to calibrated
  likelihood and score variability across simulated datasets at the same model
  parameters.

Veto diagnostics:

- Target mismatch between `y_t` and transformed `z_t = log(y_t^2)`.
- Gaussian-mixture approximation treated as exact when it is only a comparator.
- Finite-difference gradient used as a promotion criterion without regression
  or step-size stability diagnostics.

Not concluded:

- No generalized SV production claim unless target equality is separately
  checked.

## Ladder 4: Spatial SIR Source-Faithful Route

Question: can the clean-room source-faithful route avoid the all-grid pairwise
explosion and reach the source-style SIR scale ladder?

Baselines:

- J=1 and J=3 dense/reference smoke where feasible.
- J=3, J=5, J=9 preflight complexity and finite-output checks.
- Source paper configuration as a route target, not as a bitwise reference.

Primary criterion:

- No pairwise-grid explosion at J=5/J=9.
- Finite normalizers, sensible ESS, and moment diagnostics at increasing J.
- For J=1/J=3, agreement with dense/reference ladders within uncertainty.

Veto diagnostics:

- Pairwise transition count grows as `grid_points^2`.
- ESS collapses without reapproximation recovery.
- Output promoted without multi-seed or uncertainty context.

Not concluded:

- No paper reproduction or public-data claim.

## Ladder 5: Predator-Prey Preconditioned Route

Question: is the large P47 M5b gap caused by BayesFilter route mismatch/tuning,
or does it persist after implementing source-style preconditioning?

Baselines:

- Fixed-branch BayesFilter P47 candidate.
- Clean-room full solver without preconditioner.
- Clean-room preconditioned solver variants, starting with the simplest source
  option supported by the target.
- Dense or high-order reference at short horizon.

Primary criterion:

- Horizon ladder shows monotone or explainable improvement in log-likelihood
  and filtering moments versus fixed branch, with no veto failures.

Veto diagnostics:

- Normalizer/Jacobian accounting mismatch.
- Condition-number veto from fitter treated as scientific failure.
- Coordinate-map tuning chosen after looking at production target without a
  holdout or replay rule.

Not concluded:

- No evidence against the Zhao--Cui source method from the existing P47 M5b
  fixed-branch failure.

## Ladder 6: Gradient Lane Boundary

Question: what can be used safely for HMC?

Separate question: if the HMC-safe route differs from the source algorithm, is
it labeled and tested as an adaptation rather than as source-faithful
Zhao--Cui?

Baselines:

- Current deterministic fixed branch with branch replay.
- Autodiff directional derivatives.
- Carefully designed finite-difference regression diagnostics on short
  horizons only.

Primary criterion:

- Branch replay is identical.
- Directional gradients agree within scale-aware tolerances and likelihood
  variance context.
- No adaptive random branch is used unless frozen and declared fixed.
- Any departure from source mechanisms is explicitly named in the artifact and
  compared against an exact, dense, CUT4, or source-faithful filtering baseline
  before accuracy claims are made.

Veto diagnostics:

- Data-dependent rank/ESS/resampling path included in the differentiated
  function without a reviewed differentiability contract.
- Finite-difference instability interpreted as proof of bad autodiff without
  step-size sweep or regression check.
- Analytical-gradient necessity used as a rhetorical shortcut to promote an
  ad hoc route as source-faithful.

Not concluded:

- Fixed-branch HMC readiness does not imply source-faithful filtering
  equivalence.

## Recommended P49 Sequence

1. P49-M0: claim-language and pass-token cleanup.
2. P49-M1: clean-room source-faithful one-step filter skeleton.
3. P49-M2: analytic density/marginal/transport tests.
4. P49-M3: linear-Gaussian and scalar nonlinear filtering tieouts.
5. P49-M4: SV dim 1--3 value/gradient calibration.
6. P49-M5: source-faithful spatial SIR route preflight.
7. P49-M6: predator-prey preconditioned route ablation.
8. P49-M7: separate fixed-branch gradient/HMC closeout.
