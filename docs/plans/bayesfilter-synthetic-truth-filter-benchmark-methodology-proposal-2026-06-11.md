# Synthetic-Truth Filter Benchmark Methodology Proposal

metadata_date: 2026-06-11
status: PROPOSAL_REVIEW_CONVERGED_ITERATION_4
owner: Codex
reviewer: Claude Code read-only
scope: filtering value/gradient benchmark methodology

## Purpose

The earlier full filter ladder stalled because exact nonlinear likelihood
oracles are not available for every model.  This proposal replaces the
unworkable "oracle error everywhere" requirement with a synthetic-truth
likelihood-geometry benchmark.  Exact references remain mandatory where they
exist, especially for LGSSM/Kalman rows, but nonlinear models are evaluated by
their behavior at known data-generating parameters sampled from a benchmark
truth distribution.

The goal is to close the filtering part of BayesFilter before moving to
Bayesian estimation.  The benchmark should reveal whether each available filter
produces plausible likelihood values, score behavior, curvature diagnostics,
failure rates, and Monte Carlo uncertainty across the model roster.

## Evidence Contract

Question:

- For each model and filter, does the approximate filtering likelihood have
  statistically plausible value, score, and local curvature behavior when
  evaluated at parameters that generated the data?

Baselines and comparators:

- LGSSM rows retain exact Kalman likelihood, score, and Hessian references.
- Nonlinear rows use the data-generating truth as the benchmark anchor rather
  than an unavailable exact likelihood oracle.
- Deterministic filters are compared under common synthetic data, parameter
  draws, horizon choices, and value/gradient conventions.
- Stochastic filters are compared with nested data and filter-seed replication
  so particle Monte Carlo uncertainty is separated from data-generation
  uncertainty.

Primary report objects:

- average log likelihood at the generating truth;
- average score vector at the generating truth;
- score norm, max score component, min score component, and standardized score
  diagnostics;
- Hessian or negative-Hessian curvature diagnostics where available;
- failure, NaN, degeneracy, and branch-veto rates;
- Monte Carlo standard errors for stochastic filters.

Promotion or pass/fail criteria:

- This proposal does not set a universal numerical threshold for correctness.
  It defines a measurement ladder and calibration protocol.
- A benchmark run is reportable only if the model/data/filter contracts are
  frozen before running, the horizon calibration is recorded, and diagnostic
  uncertainty is reported.
- A filter should not be ranked on likelihood level alone when its score,
  curvature, or failure diagnostics veto the interpretation.

Veto diagnostics:

- missing frozen truth-parameter distribution or synthetic data contract;
- hidden substitution of smoke/preflight data for benchmark measurements;
- treating nonlinear truth-point geometry as proof of exact likelihood
  correctness;
- missing score parameterization or sign convention;
- missing Hessian sign convention;
- missing Monte Carlo uncertainty for particle filters;
- using historical `LEDH-PFPF-OT` as current Algorithm 1 evidence;
- changing thresholds or model roster after inspecting results;
- missing canonical derivative coordinates or missing transform/Jacobian policy
  for a model row.

Explanatory diagnostics:

- per-time likelihood increment autocorrelation;
- HAC or batch-means long-run variance estimates;
- effective sample size, resampling counts, and particle degeneracy;
- resource ladders over particles, sigma-point rules, sparse-grid level, or
  tensor ranks;
- wall time and memory use.

What will not be concluded:

- The benchmark does not prove exact nonlinear likelihood correctness.
- It does not certify DPF resampling gradients as valid unless a separate
  reviewed gradient contract is present.
- It does not establish Bayesian posterior accuracy or HMC readiness by itself.
- It does not imply that one theta value validates a model; the design uses a
  batch of truth parameters precisely to avoid that failure mode.

Result artifact:

- A future benchmark run should write a manifest, raw results, summary tables,
  calibration note, and reset memo under `docs/plans` and the project benchmark
  output directory.

## Mathematical Benchmark Object

For each model row, define unconstrained benchmark coordinates
\(\phi\in\mathbb R^p\) and a frozen differentiable transform
\(\theta=\tau(\phi)\) into physical parameters.  The primary score and Hessian
tables are in the \(\phi\) coordinates.  Physical-coordinate derivatives may be
reported as explanatory diagnostics, but they are not the cross-filter
comparison coordinate unless a row explicitly declares physical coordinates as
canonical.

If a filter computes derivatives in physical coordinates, the score must be
converted by the chain rule:

```text
g_phi = J_tau(phi)^T g_theta.
```

For Hessians, the transform contribution must also be included:

```text
H_phi = J_tau^T H_theta J_tau
        + sum_k g_theta,k Hessian_phi tau_k.
```

If the Hessian-transform term is not implemented or reviewed, the Hessian cell
is `not_available_transform_gap`, not a failed curvature result.

For a model with benchmark-coordinate parameter vector \(\phi\), draw truth
parameters \(\phi_{0,b}\) from a calibrated distribution \(\Pi_{\rm bench}\)
and set \(\theta_{0,b}=\tau(\phi_{0,b})\):

```text
phi_{0,b} ~ Pi_bench,                 b = 1,...,B
y_{b,r,1:T} ~ p(. | tau(phi_{0,b})),  r = 1,...,R
```

For algorithm \(a\), evaluate at the generating benchmark-coordinate
parameter:

```text
ell_{a,b,r}(phi_{0,b}) = T^{-1} log p_a(y_{b,r,1:T} | tau(phi_{0,b}))
g_{a,b,r}(phi_{0,b})   = T^{-1} grad_phi log p_a(y_{b,r,1:T} | tau(phi_{0,b}))
H_{a,b,r}(phi_{0,b})   = T^{-1} Hessian_phi log p_a(y_{b,r,1:T} | tau(phi_{0,b}))
```

For stochastic filters, add filter-seed replication:

```text
ell_{a,b,r,s}, g_{a,b,r,s}, H_{a,b,r,s},    s = 1,...,S
```

This nested design separates:

- between-truth variation over \(\theta_{0,b}\);
- within-truth data variation over \(y_{b,r,1:T}\);
- algorithmic Monte Carlo variation over filter seed \(s\).

The benchmark manifest must include a row capability matrix:

```text
value_only
value_plus_score
value_plus_score_plus_hessian
diagnostic_derivative_only
not_available_with_reason
```

This prevents missing derivatives from being interpreted as numerical failures
and prevents diagnostic-only gradients from being promoted into the main score
ladder.

The accepted-draw manifest must bind this capability status at the row and draw
level.  For every `(model_row, truth_draw_id, algorithm)` tuple, it must record:

```text
capability_status
score_coordinate_system
score_derivative_provenance
hessian_coordinate_system_or_reason
hessian_derivative_provenance_or_gap
diagnostic_only_reason
not_available_reason
```

This crosswalk is required because a row may be value-plus-score for one
algorithm, value-only for another, or diagnostic-only after a draw-specific
branch veto.  Summary tables may aggregate these states only after preserving
the tuple-level status.  The derivative provenance fields distinguish native
canonical-coordinate derivatives, chain-rule-converted physical-coordinate
derivatives, reviewed full Hessian transforms, partial transforms, fixed-branch
diagnostics, and unreviewed transform gaps.

## Why Expected Score Is The Central Diagnostic

For the exact likelihood under standard regularity and stationarity/mixing
conditions,

```text
E_{theta0}[ grad_theta log p_theta(Y_{1:T}) |_{theta=theta0} ] = 0.
```

For dependent time-series data this does not mean one finite dataset has zero
score.  The total score is typically \(O_p(\sqrt{T})\), while the average score
is \(O_p(T^{-1/2})\).  Across \(R\) independent datasets at the same truth,

```text
SE(mean average score_j) ~= sqrt(long_run_var(score_j increment) / (R T)).
```

Therefore the benchmark should report average score and its uncertainty, not
expect the raw finite-sample score to vanish.

When the benchmark also averages over truth draws, uncertainty must be
decomposed hierarchically.  For a per-time diagnostic \(q\), write
\(\mu_b=E(q\mid \phi_{0,b})\) and \(\sigma_b^2\) for its conditional long-run
variance.  A simple balanced-design variance estimate for the across-truth mean
is:

```text
Var(mean_{b,r} qbar_{b,r})
  ~= Var_b(mu_b) / B + mean_b(sigma_b^2 / (R T)) / B.
```

Thus increasing \(B\) measures robustness across plausible truths, while
increasing \(R T\) reduces conditional data uncertainty at each truth.  The
horizon calibration below is performed conditional on fixed truth first, then
the selected \(T\) is chosen by a worst-case or high-quantile rule across a
pilot batch of truth draws.  Between-truth variation is reported separately and
is not used to pretend that a short time series is precise.

## Likelihood And Hessian Sign Conventions

The report object is the average log likelihood.  Raw likelihood is avoided
because it is a product over time and is numerically/statistically unstable.

For log likelihood:

- near a local maximum, the Hessian should be negative definite;
- equivalently, the negative Hessian should be positive definite.

For negative log likelihood:

- the Hessian should be positive definite.

Every table must state which convention it uses.  This proposal uses log
likelihood and reports eigenvalue diagnostics for \(-H\) when Hessians are
available.

## Truth-Parameter Distribution

One fixed \(\theta_0\) can accidentally land in an easy, lucky, or pathological
region.  The benchmark therefore uses a batch of truths from a calibrated
benchmark prior or design distribution.

The benchmark distribution should:

- cover plausible project-relevant parameter values;
- exclude explosive, nonstationary, unidentified, or numerically degenerate
  regions unless a separate stress test intentionally includes them;
- include boundary or difficult regimes only under an explicit stress-lane
  label;
- record the transform from unconstrained coordinates to physical parameters;
- freeze seeds and accepted draws before algorithm comparisons begin;
- record acceptance rules for stationarity, positivity, identifiability,
  finite simulated observations, finite filter initialization, and numerical
  admissibility;
- preserve a draw manifest containing proposed draws, accepted draws, rejected
  draws, rejection reasons, and random seeds.

Recommended two-lane design:

- `core_prior`: well-posed and representative parameter draws used for the main
  ladder;
- `stress_prior`: edge-case draws used to measure robustness and failure modes,
  not to rank ordinary-case accuracy.

## Horizon Calibration

There is no universal "long enough" \(T\).  The horizon should be selected from
the required precision of the average log likelihood and average score.

For per-time quantity \(q_t\), estimate its long-run variance:

```text
sigma_q^2 = gamma_0 + 2 sum_{k >= 1} gamma_k.
```

Then the standard error of the replicate mean is approximately:

```text
SE(mean qbar) ~= sqrt(sigma_q^2 / (R T)).
```

Given tolerated half-width \(\epsilon\) and multiplier \(z\), choose:

```text
T >= (z sigma_q / (epsilon sqrt(R)))^2.
```

Pilot ladder:

```text
T in {512, 1024, 2048, 4096, 8192}
R in {16, 32}
```

The final run should use the smallest horizon for which:

- conditional average log-likelihood standard errors meet the target for every
  pilot truth or for a predeclared high quantile such as 90 or 95 percent;
- conditional average score component standard errors meet the target for every
  pilot truth or for the same predeclared high quantile;
- componentwise standardized mean scores are stable when \(T\) doubles;
- replicate-level negative-Hessian eigenvalue diagnostics stabilize where
  available;
- stochastic-filter Monte Carlo uncertainty is not confounded with data
  uncertainty.

Long-run variance estimation may use HAC/Newey-West or batch-means estimates.
The chosen estimator and lag/batch rule are part of the benchmark manifest.

## Stochastic-Filter Seed Calibration

For particle filters and other stochastic filters, choose the number of filter
seeds \(S\) by a seed ladder, for example:

```text
S in {4, 8, 16, 32}
```

For each dataset and truth draw, decompose uncertainty into data and filter
Monte Carlo components.  The preferred stopping rule is:

```text
MC_SE <= kappa * data_SE
```

for average log likelihood, every canonical score coordinate, and every
reported scalar score summary such as norm or extrema.  The constant
\(\kappa\) is fixed before execution, for example \(\kappa=0.25\).  If the
maximum planned \(S\) does not meet the rule, the cell remains reportable only
with a `mc_noise_dominant` flag and should not be ranked against deterministic
filters by small differences.

## Algorithm Ladder

The intended rows are the current filters, with historical or superseded rows
kept out of the current-performance tables:

- Kalman exact or mixture enumeration, where applicable;
- UKF;
- SVD sigma-point filter;
- CUT4;
- Zhao-Cui scalar or multistate routes;
- bootstrap DPF current implementation;
- faithful LEDH-PFPF Algorithm 1 with UKF local covariance.

`LEDH-PFPF-OT` is historical-only unless a separate reviewed plan reinstates a
specific current row.

## Model Ladder

The model roster should be frozen before execution and should include:

- LGSSM rows for exact Kalman validation;
- quadratic-observation and cubic/additive Gaussian rows;
- stochastic-volatility transformed actual non-Gaussian and
  Gaussian-mixture-surrogate rows;
- generalized stochastic-volatility rows;
- predator-prey rows;
- spatial-SIR rows;
- other project-approved P30/P44/P50/P51/P53 model rows with frozen parameter
  and observation contracts.

Every model row must record:

- state dimension and observation dimension;
- parameter vector and transformations;
- truth-parameter draw distribution;
- data-generation seed contract;
- horizon calibration result;
- reference type, if any;
- applicable filters and known diagnostic-only lanes.

## Tables To Produce

Main value table:

```text
rows: algorithms
columns: models
cell: mean average loglik, SE, failure rate
```

Main score table:

```text
rows: algorithms
columns: models
cell: mean score norm, max component, min component, max standardized component
```

Curvature table:

```text
rows: algorithms
columns: models
cell: mean/median/quantiles of lambda_min(-H), positive-definite fraction,
      convention
```

The primary curvature diagnostic is replicate-level
\(\lambda_{\min}(-H_{a,b,r})\), not \(\lambda_{\min}(-\bar H)\).  Eigenvalues
of the mean Hessian may be reported as explanatory diagnostics, but they can
hide replicate-level curvature failures and must not be the main pass/fail
object.

Stochastic-filter uncertainty table:

```text
rows: DPF algorithms
columns: models
cell: data SE, particle MC SE, particle ladder trend, degeneracy diagnostics
```

Truth-robustness table:

```text
rows: algorithms
columns: models
cell: worst-theta score norm, between-theta SD, failure-rate by theta batch
```

LGSSM exact-reference table:

```text
rows: algorithms
columns: LGSSM variants
cell: exact value error, exact gradient error, Hessian error when available
```

Componentwise score artifact:

```text
rows: algorithms x models x parameter coordinates
cell: signed mean score, SE, confidence interval, standardized mean
```

The summary score table may show norms and extrema, but the componentwise
artifact is required so coordinate-specific bias cannot be hidden.

## Interpretation Rules

- A higher average log likelihood is not by itself a win if score or curvature
  diagnostics fail.
- A near-zero expected score is evidence of plausible local likelihood geometry,
  not proof of exact nonlinear filtering.
- Particle methods must report uncertainty over filter seeds; one-seed results
  are diagnostics only.
- Deterministic filters still need truth-parameter and dataset replication
  because data-generation variability remains.
- Stress-prior failures should be reported as robustness information, not
  silently merged with core-prior ranking.

## Skeptical Plan Audit

Wrong baselines:

- The plan avoids requiring exact nonlinear references where none exist.  It
  keeps exact comparisons only where exact references are valid.

Proxy metrics:

- Smoke tests, adapter tests, and preflight matrices remain engineering gates
  only.  They cannot populate benchmark cells.

Missing stop conditions:

- Stop if model truth distributions, data seeds, gradient parameterization,
  or sign conventions are not frozen.
- Stop if benchmark-coordinate transforms and derivative-chain rules are not
  frozen.
- Stop if stochastic filters lack nested seed replication.
- Stop if horizon calibration is skipped and no justified fixed \(T\) is
  recorded.
- Stop if curvature is summarized only by eigenvalues of an averaged Hessian.

Unfair comparisons:

- All filters see the same truth draws and datasets.
- Algorithm-specific resource ladders are reported, not hidden.
- Diagnostic-only gradients are labeled as such.

Hidden assumptions:

- Expected score zero is a population property, not a one-dataset equality.
- Hessian definiteness depends on the log-likelihood sign convention.
- The calibrated benchmark prior is not the full Bayesian prior unless
  explicitly declared.

Stale context:

- Historical `LEDH-PFPF-OT` rows are excluded from current evidence.
- Previous N/A cells are not filled from old smoke or preflight evidence.

Environment mismatches:

- CPU-only runs must hide GPU devices and record that choice.
- GPU runs require trusted/escalated execution and separate manifest entries.

Artifact-answer risk:

- The final artifact must answer the ladder question with measured likelihood,
  score, curvature, and uncertainty summaries, not just runnable adapters.

## Implementation Phases For A Future Runbook

P0. Freeze methodology, sign conventions, and row contract.

P1. Freeze model roster, benchmark-coordinate transforms, truth-parameter
distributions, acceptance rules, draw manifests, capability matrix, and seeds.

P2. Implement or verify synthetic data generators for every model row.

P3. Implement truth-point value, score, and Hessian evaluators for every filter.

P4. Add stochastic nested replication for DPF filters, run the seed ladder, and
record MC/data uncertainty decomposition.

P5. Run horizon calibration pilot and choose \(T\), \(R\), \(B\), and \(S\).

P6. Run full core-prior ladder.

P7. Run stress-prior robustness ladder.

P8. Produce tables, componentwise score artifacts, replicate-level curvature
artifacts, manifests, diagnostics, and reset memo.

P9. Run Claude read-only audit until convergence or max five iterations.

## Literature Anchors For The Chapter

The chapter should cite:

- state-space and HMM likelihood asymptotics for likelihood/score averaging and
  MLE behavior;
- HAC/Newey-West or equivalent long-run variance estimation for dependent
  time-series averages;
- particle score/observed-information literature for the special variance and
  degeneracy risks of particle score estimates;
- the filter-specific sources already cited by the project for Kalman,
  sigma-point, sparse-grid, particle, Li-Coates particle flow, and Zhao-Cui
  tensor-train methods.

## Claude Review Loop Contract

Claude is read-only reviewer.  Codex patches on `VERDICT: REVISE`.  Stop at the
first `VERDICT: AGREE` or after five iterations.  A Claude timeout or empty
review is not a valid rejection; probe Claude with a minimal prompt, and if the
probe works, shorten or split the review prompt.
