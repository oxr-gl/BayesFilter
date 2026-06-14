# P42 Draft Rules: Likelihood and Gradient Validation for HMC Readiness

metadata_date: 2026-06-07
phase: P42-governance
status: `PASS_P42_RULES_GOVERNANCE_AFTER_CLAUDE_REVIEW_ITER3`

## Motivation and Worry

The central worry is that for long data records and high-dimensional latent or
parameter spaces, neither autodiff nor finite differences are automatically a
trustworthy ground truth:

- autodiff can propagate numerical error through quadrature, log-sum-exp
  recursions, eigensystems, SVD/CUT rules, TT fits, clipping/floors, and
  branch-dependent algorithms;
- naive coordinate finite differences can be dominated by subtractive
  cancellation, step-size choice, quadrature noise, basis-fit noise, solver
  tolerances, and high-dimensional anisotropy;
- long horizons can amplify tiny per-step discrepancies into large likelihood
  or score differences;
- high dimension makes coordinatewise finite-difference sweeps expensive and
  potentially misleading.

Therefore no single method should be promoted as "the gradient truth" for
serious HMC decisions unless the validation plan explains why it is stable for
the target, dimension, horizon, and implementation path under test.

## Core Target Discipline

1. Always compare the same mathematical target.
   - Native SV, exact transformed SV, KSC Gaussian-mixture transformed SV, and
     generalized SV are distinct targets.
   - Raw native SV can be compared to exact transformed SV only after applying
     the observation-only Jacobian relation.
   - Approximation targets, such as KSC mixture SV, must remain labeled as
     approximation targets even when they are useful HMC surrogates.

2. Always compare gradients in the same parameterization.
   - Gradients for physical parameters and unconstrained HMC parameters are not
     interchangeable without the chain rule.
   - Reports must state the parameter vector, transform, and ordering.

3. Do not promote value agreement to gradient correctness.
   - A value-path pass can authorize a gradient investigation.
   - It does not imply score correctness or HMC readiness.

## Claim Classes

Every result must declare exactly which class it supports.

Class A: exact same-target numerical correctness.

- Claim: the candidate computes the same mathematical likelihood or score as a
  named reference route on fixed data and fixed parameters.
- Required evidence: Tier 1 same-target value and gradient checks plus
  reference-route stability.
- Not allowed: using data-law variability or HMC acceptance as an excuse for a
  same-target numerical mismatch.

Class B: statistical smallness relative to the data-generating law.

- Claim: candidate errors are small relative to the variation in likelihoods or
  scores induced by repeated datasets from a declared data-generating law.
- Required evidence: Tier 2 simulation with separate data-law variability and
  evaluator variability.
- Not allowed: calling the candidate exact or HMC-ready solely because
  `rmse/sd_L` is small.

Class C: approximate surrogate HMC usefulness.

- Claim: the candidate defines a useful approximate target or approximate
  gradient for HMC-like computation.
- Required evidence: Tier 2 statistical-scale evidence plus Tier 3
  Hamiltonian/leapfrog probes.
- Not allowed: promoting surrogate usefulness into exact-target HMC readiness.

Class D: explanatory diagnostic only.

- Claim: the result is useful for debugging, scale setting, or hypothesis
  formation.
- Required evidence: finite values and clear non-claims.
- Not allowed: any production, exactness, or HMC-readiness claim.

## Evidence Tiers

### Tier 1: Local Numerical Correctness

Purpose:

- Establish that two implementations compute the same target on the same fixed
  data and same parameters, within numerical approximation error.

Allowed reference routes:

- exact Kalman or Kalman-mixture gradients when the target is linear Gaussian
  or conditionally linear Gaussian;
- dense quadrature with refinement when dimension/horizon permit;
- autodiff through a fixed, smooth computation graph, if branch/floor decisions
  are frozen and audited;
- regression finite-difference directional derivatives, not single-step naive
  finite differences.

Typical value tolerances:

- CUT4 versus Kalman on linear-Gaussian or KSC mixture target: `1e-10` to
  `1e-8` log likelihood;
- dense refinement, e.g. order 401 versus 801: `1e-8` to `1e-6`;
- fixed-design TT versus dense exact transformed SV: `1e-8` to `1e-5`,
  depending on basis/rank/quadrature;
- raw native SV versus exact transformed SV after Jacobian: `1e-8` to `1e-6`.

Typical gradient tolerances for small fixtures:

- vector relative score error
  `||g_method - g_ref|| / max(1, ||g_ref||)`:
  - excellent: `< 1e-4`;
  - diagnostic pass: `< 1e-3`;
  - suspicious: `1e-2`;
  - not HMC-ready: `> 1e-2`.

Near-stationary-point rule:

- A near-stationary trigger must be declared in the active HMC
  parameterization.  Do not use an unqualified Euclidean threshold.
- Default trigger:

```text
score_scale = sqrt(trace(S_ref) / p)
near_stationary if ||g_ref|| / max(sqrt(p) * score_scale, floor) < 0.1
```

  where `S_ref` is a declared reference score covariance or diagonal/block
  score-scale estimate, `p` is parameter dimension, and `floor` is a declared
  small positive constant.
- If no score-scale estimate exists, the fixture is treated as
  potentially near-stationary and vector relative score error is not sufficient.
- Reports must also include:
  - absolute vector error `||g_method - g_ref||`;
  - coordinatewise absolute errors;
  - blockwise absolute errors for declared parameter blocks;
  - at least five directional derivative checks, including random directions
    and any known stiff/sensitive directions.
- A near-stationary fixture can pass only if both absolute and directional
  errors satisfy the declared tolerances.

Horizon scaling:

- Report total value error and value error per observation:

```text
total_value_error = L_method - L_ref
per_observation_value_error = total_value_error / (T * observation_dim)
```

- Report total gradient error and a normalized score error per observation or
  per time block when the score decomposes naturally.
- Run at least a two-point horizon check, e.g. `T_short` and `T_long`, before
  claiming that a tolerance is stable for longer records.
- A small per-step error that accumulates into a large total score error is a
  veto for exact-target HMC readiness.

Veto conditions:

- reference route has not itself passed a refinement or stability check;
- finite-difference estimate depends materially on one chosen step size;
- autodiff route crosses non-smooth branch changes, floors, clipping events, or
  adaptive fitting changes that are not frozen and recorded;
- parameterization mismatch is detected;
- value target mismatch is detected.

### Tier 2: Statistical Scale of Value and Score Errors

Purpose:

- Determine whether observed numerical or approximation errors are large
  relative to the natural variability of the model-generated data.

For fixed data-generating parameters `theta0`, simulate
`Y_r ~ p(. | theta0)` and compute:

```text
L_ref,r    = log p_ref(Y_r | theta0)
L_method,r = log p_method(Y_r | theta0)
e_r        = L_method,r - L_ref,r
sd_L       = sd_r(L_ref,r)
bias       = mean_r(e_r)
sd_error   = sd_r(e_r)
rmse       = sqrt(mean_r(e_r^2))
rel_rmse   = rmse / max(sd_L, floor)
max_error  = max_r |e_r|
```

This `sd_L` is data-law variability only.  It does not measure evaluator
randomness or numerical nondeterminism.

If either evaluator is stochastic, randomized, adaptive, or may be
nondeterministic, run repeated same-dataset evaluations:

```text
L_method,r,k = kth evaluation of method on dataset r
within_sd_method,r = sd_k(L_method,r,k)
within_sd_ref,r    = sd_k(L_ref,r,k)
```

Reports must include:

- median and maximum `within_sd_method,r`;
- median and maximum `within_sd_ref,r`;
- ratio of within-dataset evaluator standard deviation to `sd_L`;
- whether paired errors use common random numbers or fixed branch seeds.

Tier 2 scaling is invalid until within-dataset evaluator variability is either:

- shown negligible relative to both `sd_L` and `rmse`; or
- included explicitly in the uncertainty report.

Suggested value-error interpretation:

- `rel_rmse < 0.001`: excellent;
- `rel_rmse < 0.01`: likely acceptable for a surrogate or approximation lane;
- `0.01 <= rel_rmse < 0.05`: concerning and needs HMC probe before promotion;
- `rel_rmse >= 0.05`: too large for default HMC use without strong additional
  justification.

For gradients, estimate score covariance:

```text
g_ref,r       = grad_theta log p_ref(Y_r | theta0)
delta_g_r     = g_method,r - g_ref,r
I_hat         = Cov_r(g_ref,r)
whitened_err  = sqrt(delta_g_r' (I_hat + ridge I)^(-1) delta_g_r)
```

If either score evaluator is stochastic, randomized, adaptive, or may be
nondeterministic, run repeated same-dataset score evaluations:

```text
g_method,r,k = kth score evaluation of method on dataset r
g_ref,r,k    = kth score evaluation of reference on dataset r
within_cov_method,r = Cov_k(g_method,r,k)
within_cov_ref,r    = Cov_k(g_ref,r,k)
directional_noise_method,r,v = sd_k(v' g_method,r,k)
directional_noise_ref,r,v    = sd_k(v' g_ref,r,k)
```

Reports must include:

- median and maximum coordinatewise within-dataset score standard deviation;
- median and maximum directional score noise over the validation directions;
- ratio of within-dataset score noise to data-law score scale;
- whether common random numbers, fixed branch seeds, or fixed fitted artifacts
  are used.

Tier 2 gradient scaling is invalid until within-dataset score-evaluator
variability is either:

- shown negligible relative to data-law score scale and candidate-reference
  score RMSE; or
- included explicitly in score-error uncertainty.

High-dimensional score-scale rule:

- Let `R` be the number of independent simulated datasets and `p` be parameter
  dimension.
- Full `I_hat` whitening is allowed only when all of the following hold:
  - `R >= 10 * p`;
  - `p <= 1000`, unless a sparse/structured covariance plan is separately
    reviewed;
  - `condition_number(I_hat + ridge I) <= 1e8`;
  - a factor-of-10 perturbation of `ridge` changes median whitened error by
    less than 10%.
- If any full-whitening condition fails, full whitening is explanatory only and
  the governing metric must use at least one mandatory fallback:
  - diagonal scaling by coordinate score variances;
  - block-diagonal scaling by declared parameter blocks;
  - shrinkage covariance, with shrinkage intensity reported;
  - directional score scaling along random and problem-informed directions.
- Minimum fallback requirements:
  - diagonal scaling requires `R >= 30` and finite positive variance for every
    scored coordinate after ridge/floor handling;
  - block scaling requires `R >= max(30, 5 * block_size)` for every block;
  - shrinkage scaling requires reporting shrinkage intensity and condition
    number after shrinkage;
  - directional scaling requires at least `max(20, 2 * p)` random directions
    when feasible, or a reviewed reduced-direction plan for very high `p`.
- Ridge must be declared as a rule, not chosen after seeing the result.  A
  default acceptable rule is:

```text
ridge = max(1e-8 * median(diag(I_hat)), 1e-12)
```

- If whitening changes materially under a factor-of-10 ridge perturbation, the
  whitened score result is explanatory only.

Gradient reports must include:

- coordinatewise absolute and relative errors;
- vector relative score error;
- cosine similarity;
- Fisher- or score-covariance-whitened error;
- bias and RMSE of directional score errors across random directions.

Veto conditions:

- the simulated-data reference is itself unstable;
- sample size is too small to estimate `sd_L` or `I_hat`;
- error is dominated by a small number of outlier datasets that are not
  explained;
- statistical scale is used to excuse a Tier-1 same-target numerical failure.
- score covariance or whitening matrix is ill-conditioned and no diagonal,
  block, shrinkage, or directional alternative is reported.

### Tier 3: HMC-Relevant Dynamics

Purpose:

- Test whether gradient error matters for Hamiltonian behavior.

Required probes before HMC-readiness claims:

- short leapfrog trajectories from common initial states and momenta;
- Hamiltonian error comparison between reference and candidate gradients;
- reversibility error;
- volume-preservation or symplectic sanity diagnostics where applicable;
- acceptance-probability degradation under matched step sizes;
- energy error as a function of trajectory length and step size.

Interpretation:

- A method can be value-accurate but HMC-bad if gradient errors align with
  stiff directions.
- A method can have visible value approximation error but still be useful as a
  deliberately approximate inference target if gradient behavior is stable and
  the target is clearly labeled.
- HMC readiness requires Tier 1, Tier 2, and Tier 3 evidence, not just one
  favorable metric.

## Finite Difference Rules

Naive single-step finite differences are not a gold standard for serious
gradient decisions.  Finite differences are corroborative evidence by default,
not truth by default.

Required directional finite-difference protocol:

1. Prefer directional derivatives over coordinate sweeps:

```text
D_v L(theta) = v' grad L(theta)
```

2. Use normalized directions:

- random Gaussian directions normalized to unit norm;
- coordinate directions only for localized debugging;
- problem-informed directions such as stiff eigenvectors when available.

3. Use a step-size ladder:

```text
h in {h_max, h_max/2, h_max/4, ..., h_min}
```

Minimum ladder:

- at least 9 step sizes for a serious gradient decision;
- at least 5 retained step sizes in the accepted stable window;
- repeat with a shifted ladder, e.g. multiply every `h` by `sqrt(2)`, before
  using the derivative estimate as Tier 1 evidence.

4. Fit a regression/Richardson model:

```text
[L(theta+h v) - L(theta-h v)] / (2h)
  = D_v L(theta) + c2 h^2 + c4 h^4 + roundoff/h + residual
```

Stable-window criterion:

- the fitted derivative over the accepted window must change by less than the
  declared tolerance when either endpoint of the window is removed;
- the shifted ladder derivative must agree with the original ladder derivative
  within the larger of the reported derivative uncertainty and the declared
  tolerance;
- residuals must not show monotone curvature or roundoff patterns left in the
  accepted window.

Regression acceptance:

- report the fitted derivative and a standard error or robust spread estimate;
- reject the finite-difference result if the uncertainty exceeds one third of
  the candidate-vs-reference discrepancy being adjudicated;
- reject the finite-difference result if the fitted derivative changes
  materially when the `roundoff/h` term is included or excluded, unless the
  accepted window is explicitly roundoff-free.

5. Report:

- accepted stable step-size window;
- fitted directional derivative;
- uncertainty or spread across the stable window;
- rejected step sizes and rejection reason;
- comparison to candidate `v' g_method`.

Veto conditions:

- no stable step-size window;
- regression residuals show systematic curvature or roundoff not captured by
  the model;
- function evaluations use adaptive branches that differ across `theta +/- h v`;
- the inferred derivative changes materially when the step ladder is shifted.
- fewer than 9 step sizes are tried or fewer than 5 are retained for a serious
  gradient decision.

## Autodiff Rules

Autodiff is a powerful route, but not automatically a reference.

Autodiff can be a primary local reference only when:

- the computation graph is fixed for the whole perturbation neighborhood used
  in directional checks, not just at the base point;
- floors, jitter, clipping, rank decisions, solver iteration counts,
  quadrature choices, basis choices, and branch choices are recorded and remain
  unchanged over that neighborhood;
- values and directional derivatives pass refinement checks under tighter
  solver tolerances, quadrature orders, basis/rank choices, or integration
  settings relevant to the route;
- the same route passes independent directional checks;
- known non-smooth operations are absent or treated as fixed-subgradient
  diagnostics.

Autodiff is explanatory only when:

- it differentiates through fitted/adaptive artifacts without a fixed-branch
  contract;
- it crosses eigensystem or SVD degeneracies without eigen-gap diagnostics;
- it differentiates through branch-dependent TT fitting or adaptive
  approximation choices;
- it relies on silent framework behavior for non-smooth operations.
- branch/floor/rank/solver/quadrature decisions have been checked only at the
  base point and not over a perturbation neighborhood.

## Reporting Requirements

Every serious likelihood or gradient comparison must state:

- target and parameterization;
- data fixture or simulation law;
- dimension, horizon, and random seed policy;
- baseline/reference route and its stability evidence;
- candidate route;
- value error metrics;
- gradient error metrics;
- statistical scale metrics when simulated datasets are used;
- HMC probe metrics if HMC readiness is discussed;
- veto diagnostics and whether any fired;
- what is not being concluded.

## Promotion Rules

Do not claim HMC readiness unless:

- value target and parameterization are correct;
- gradients pass Tier 1 local correctness on small fixtures;
- gradient errors are small relative to score covariance or Fisher scale in
  Tier 2;
- leapfrog/Hamiltonian probes are stable in Tier 3;
- all non-smooth/adaptive branch decisions are either absent, frozen, or
  explicitly handled.

Do not claim exactness for:

- KSC mixture approximations to exact log-chi-square SV;
- factorized independent-panel lanes as coupled multivariate TT;
- Monte Carlo estimates without standard errors;
- finite differences without a stable step-size/regression window;
- autodiff through adaptive branches without fixed-branch governance.
