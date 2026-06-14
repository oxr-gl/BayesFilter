# P37-M2.6c Subplan: Short Sequential SV TT Value Path

metadata_date: 2026-06-05
phase: P37-M2.6c

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md`

depends_on:
- P37-M2.6b squared-density normalizer and retained marginal result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-result-2026-06-05.md`

## Purpose

Compose the M2.6a fixed-design adjacent target fitting and M2.6b
squared-density normalizer/marginalization into a short-horizon scalar
stochastic-volatility TT/SIRT-like value path, and compare the log evidence and
retained moments against the M2/M2.5 dense scalar oracle.

This remains a scalar fixed-design BayesFilter bridge.  It is not paper-scale
Zhao--Cui adaptive TT-cross reproduction.

## Source-Governance Status

- P30 anchors identified: SV equations `eq:p27-sv1`--`eq:p27-sv10`,
  adjacent target recursion `eq:p25-bridge-1`--`eq:p25-bridge-3`,
  square-mass and retained-density anchors `eq:p33-square-mass`,
  `eq:p33-full-normalizer`, `eq:p33-retained-marginal`, and
  `eq:p33-retained-normalized`.
- Zhao--Cui paper anchors identified: SSM equations (1)--(3), filtering and
  posterior marginals (5)--(8), recursive posterior update (9)--(11),
  Algorithm 1(a) and Eq. (12) for the nonseparable target approximation,
  Algorithm 1(b) for separable TT approximation, Algorithm 1(c) for
  integration/normalizer \(c_t\), Eq. (13) and Lemma 1 for squared-TT density,
  Proposition 2 and Eq. (14) for the retained marginal, and Algorithm 2 for
  squared-TT sequential estimation.  These anchors are cross-checked against
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md`.
- MATLAB behavioral anchors identified: `eg2_sv/mainscript.m`,
  `deep-tensor.dev/src/SIRT.m`, `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`, and
  `deep-tensor.dev/src/@TTFun/cross.m`.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/fitting.py`,
  `bayesfilter/highdim/squared_tt.py`,
  planned `tests/highdim/test_p30_sv_short_sequential_tt_value_path.py`.
- Deviations listed: yes.  This is a fixed-design scalar BayesFilter extension,
  not MATLAB adaptive cross.
- Clean-room boundary respected: yes.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M2P6C_PLAN`.

## Fixed M2.6c Fixtures

M2.6c is promoted only for the pinned two-observation scalar SV horizon below.
The third M2/M2.5 observation is carried as a source fixture value but is not
part of the promoted M2.6c horizon.

```text
m2p6c_fixture_id = p37.m2p6c.sv.short-sequential-tt-value-path.v1
source_m2p6a_fixture_id = p37.m2p6a.sv.scalar.fixed-target.v1
source_m2p6a_fit_fixture_id = p37.m2p6a.sv.fixed-design-fit.degree64.v2
source_m2p6b_normalizer_fixture_id =
  p37.m2p6b.sv.normalizer-audit.gl257.v1
source_m2p6b_retained_density_fixture_id =
  p37.m2p6b.sv.retained-density-audit.mid173.v1

model = StochasticVolatilitySSM(sigma=1.0)
physical_parameters = gamma=0.6, beta=0.4, sigma=1.0
theta = model.unconstrained_from_physical(gamma=0.6, beta=0.4)
source_observations = (0.12, -0.08, 0.05)
promoted_observations = (0.12, -0.08)
promoted_time_indices = (0, 1)
promoted_horizon = two observations only, x_0 and x_1 filtering states

coordinate_map = AffineCoordinateMap(offset=[0.0], matrix=[[8.0]])
measure_convention = REFERENCE_MEASURE density and mass with
  reference_weight_name = omega
product_basis = normalized LegendreBasis1D(BoundedInterval(-1.0, 1.0),
  max_degree=64)
ranks = (1, 1)
fit_config = M2.6a degree-64 fixed-design configuration:
  ridge=1e-12, max_sweeps=2, sweep_order=(0,), row_budget=256,
  column_budget=80, dense_matrix_byte_budget=100000,
  normal_matrix_byte_budget=50000, condition_number_warning=1e10,
  condition_number_veto=1e14, holdout_tolerance=2e-5
fit_quadrature_order = 161
density_tau = 0.0
normalizer_floor = 1e-12
denominator_floor = 1e-12
```

M2.6c-owned fixture IDs:

```text
initial_target_id = p37.m2p6c.sv.initial.t0.v1
transition_target_id = p37.m2p6c.sv.transition.t1.tt-retained.v1
initial_fit_fixture_id = p37.m2p6c.sv.initial-fit.degree64.v1
transition_fit_fixture_id = p37.m2p6c.sv.transition-fit.degree64.v1
dense_comparator_fixture_id =
  p37.m2p6c.sv.dense-sequential-comparator.gl321.v1
tt_retained_propagation_fixture_id =
  p37.m2p6c.sv.tt-retained-propagation.gl321.v1
tt_retained_moment_fixture_id =
  p37.m2p6c.sv.tt-retained-moment.gl257.v1
branch_seed_prefix = p37-m2p6c-sv-short-tt
```

Dense comparator:

```text
implementation = M2/M2.5 dense scalar sequential oracle
reference_test_anchor =
  tests/highdim/test_p30_stochastic_volatility.py::_sequential_dense_grid_reference
order = 321
physical_radius = 8.0
observations = promoted_observations
outputs = per-step log_normalizers, total log_evidence, mean_path,
  variance_path
```

The dense comparator is a baseline only.  It may not be called from the
promoted TT value path except inside tests/result code that builds the
comparator object.

## Evidence Contract

Question: can the fitted scalar SV square-root TT density path produce the same
short-horizon log evidence and retained scalar moments as the dense M2/M2.5
oracle?

Baseline/comparator:

- M2/M2.5 dense scalar SV oracle for the same theta, observations, coordinate
  map, and quadrature window;
- M2.6b normalizer and retained-density checks;
- branch replay and fixed fixture manifests.

Primary pass criteria:

- per-step log normalizers agree with dense oracle within predeclared
  tolerance;
- total log evidence agrees with dense oracle within predeclared tolerance;
- retained mean and variance agree at every step within predeclared tolerance;
- every promoted step records non-null fitted-TT and squared-density branch
  hashes;
- every promoted retained filter records `storage_kind = scalar_tt_grid` and
  the squared-density branch hash used to generate the retained grid;
- branch replay is deterministic for the fixed fixtures;
- broad guardrails remain green.

Executable tolerance policy:

```text
per_step_log_normalizer_abs_tol = 5e-3
per_step_log_normalizer_rel_tol = 5e-3
total_log_evidence_abs_tol = 1e-2
total_log_evidence_rel_tol = 5e-3
retained_mean_abs_tol = 5e-2
retained_variance_abs_tol = 2e-1
retained_moment_integral_abs_tol = 5e-4
```

These tolerances are intentionally wider than the M2.6b pointwise
retained-density tolerance because M2.6c composes retained-density
approximation into the next transition target.  They are absolute promotion
criteria for this scalar bridge only; relative log-normalizer tolerances are
reported and veto only if the corresponding absolute tolerance also fails.
Failure does not authorize tolerance relaxation without a reviewed amendment.

Promoted TT per-step normalizer route:

```text
for each promoted time t:
  build scalar adjacent target under the pinned coordinate map and reference
    measure;
  fit the square-root target with the M2.6a degree-64 fixed-design fit config;
  build SquaredTTDensity with tau=0;
  scaled_normalizer = density.normalizer();
  log_normalizer_t = log(scaled_normalizer) + target.log_scale_shift;
```

For `t=0`, the adjacent target is the initial target.  For `t=1`, the adjacent
target must be built from the TT-retained grid produced at `t=0`, not from the
M2.5 dense retained filter used for M2.6a/M2.6b transition-target validation.

Promoted TT retained-moment route:

```text
moment_grid = Gauss-Legendre order 257 on reference [-1,1]
moment_weights = 0.5 * Gauss-Legendre weights
reference_density_values =
  density.normalized_retained_density_values((0,), moment_grid)
physical_points = coordinate_map.forward(moment_grid).points
mass_check = sum(moment_weights * reference_density_values)
mean = sum(moment_weights * physical_points[:,0] * reference_density_values)
second = sum(moment_weights * physical_points[:,0]^2 *
  reference_density_values)
variance = second - mean^2
```

The promoted retained object is the normalized retained density from M2.6b.
Metadata-only `marginal_density`, `conditional_density`, pointwise
renormalized slices, and dense retained summaries are forbidden as promotion
evidence.

TT retained propagation route for the next step:

```text
propagation_grid = Gauss-Legendre order 321 on reference [-1,1]
propagation_weights = Gauss-Legendre weights on [-1,1] (Lebesgue weights,
  matching the existing scalar transition helper)
reference_density_values =
  density.normalized_retained_density_values((0,), propagation_grid)
physical_density_log =
  log(reference_density_values) - log_abs_det_jacobian +
  log_uniform_reference_weight_density
retained_filter = scalar_tt_grid_retained_filter(..., density_hash=...)
```

The propagation retained filter may carry the same physical grid fields as the
existing scalar dense retained filter, but it must have
`storage_kind = scalar_tt_grid`, must record the density hash, and must be
rejected if the density hash is missing.

Veto diagnostics:

- M2.6b unresolved veto;
- nonfinite normalizer, retained moment, density, branch hash, or evidence;
- branch replay mismatch;
- comparing against a dense oracle with different observations, theta, map, or
  scale;
- hidden fallback to dense filtering as the promoted TT path;
- any promoted M2.6c step with `value_path =
  scalar_nonlinear_dense_quadrature_value_path`;
- any promoted M2.6c step with `fit_result is None`, `density is None`, or
  missing fit/density branch hash;
- routing M2.6c through `FixedBranchSquaredTTFilter.log_likelihood()` when the
  nonlinear scalar branch would call `_scalar_nonlinear_dense_value_path`;
- accepting `fit_config is None` and `product_basis is None` for the promoted
  TT path, because that is the dense-lane trigger in
  `FixedBranchSquaredTTFilter`;
- using the M2.5 dense retained filter as the promoted transition retained
  input at `t=1`;
- changing M2.6a/M2.6b basis, rank, fit config, coordinate map, tau, floor, or
  scale convention without reviewed amendment;
- extending the promoted horizon beyond `(0.12, -0.08)` without reviewed
  amendment;
- treating scalar short-horizon success as paper-scale or high-dimensional
  evidence.

Explanatory-only diagnostics:

- fit residuals, rank, basis degree, wall time, memory, target evaluations,
  condition numbers, and retained density plots.

What will not be concluded:

- no Zhao--Cui paper-scale `T=1000`;
- no adaptive TT-cross/MATLAB reproduction;
- no SMC or real-data validation;
- no derivative/HMC/DSGE/GPU readiness;
- no high-dimensional scalability claim.

Artifacts preserving result:

- result ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-result-2026-06-05.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-claude-review-ledger-2026-06-05.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_PATCH`.

M2.6b has passed local evidence and Claude code/governance review.  M2.6c may
therefore start plan review, but implementation remains blocked until this
patched M2.6c plan receives explicit `PASS_M2P6C_PLAN`.

The largest proxy risk is accidentally running the existing dense M2.5 path and
claiming TT evidence.  Tests must assert that the value path uses the fitted
TT/density artifacts and records their branch identities.

The largest baseline risk is comparing TT moments against a dense oracle built
from a different horizon, coordinate map, quadrature radius, or scaling
convention.  The fixed fixture section above pins those fields and treats drift
as a veto.

The largest hidden-assumption risk is measure conversion.  Moment computations
must use normalized retained density under the reference probability measure,
while transition propagation must reconstruct physical density from that
reference density before using the existing scalar transition formula.

## Planned Implementation Tasks

1. Add an explicit TT-only scalar sequential entry point, for example
   `scalar_nonlinear_fixed_design_tt_value_path`, instead of changing the
   current dense nonlinear route in `FixedBranchSquaredTTFilter.log_likelihood`.
2. Add or extend a retained-filter constructor for TT-generated scalar grids
   with `storage_kind = scalar_tt_grid`, physical/reference grid diagnostics,
   raw propagation weights, reconstructed `log_density_physical`, and required
   `density_hash`.
3. Permit scalar transition adjacent-target construction from
   `scalar_tt_grid` retained filters only after validating the required grid
   diagnostics, measure convention, coordinate-map replay, and density hash.
4. For `t=0`, build the pinned initial adjacent target, fit the degree-64
   square-root TT, build the squared density, compute the scaled and unscaled
   log normalizer, compute retained moments on the GL257 moment grid, and build
   the TT retained propagation grid on GL321.
5. For `t=1`, build the transition adjacent target using the TT retained grid
   from `t=0`, fit the degree-64 square-root TT, build the squared density,
   compute the log normalizer, and compute retained moments on the GL257
   moment grid.
6. Build a result object compatible with `FixedBranchFilterResult`, but with
   diagnostics `value_path = scalar_nonlinear_fixed_design_tt_value_path` and
   `tt_artifacts_present = True`.
7. Record per-step branch manifests containing target hash, fit hash, density
   hash, retained-filter hash, previous-step hash, fixture IDs, branch seeds,
   and non-claims.
8. Add focused tests in
   `tests/highdim/test_p30_sv_short_sequential_tt_value_path.py` that compare
   per-step log normalizers, total log evidence, retained means, and retained
   variances against the pinned dense comparator.
9. Add negative tests that fail if the promoted path routes through
   `scalar_nonlinear_dense_quadrature_value_path`, has missing TT artifacts,
   accepts a dense retained filter as the promoted transition input, or omits
   density hashes.
10. Rerun the M2.6b focused tests and broad highdim guardrails after the M2.6c
    implementation.
11. Write the M2.6c result ledger, update the Claude review ledger, and update
    traceability without promoting longer-horizon, paper-scale, derivative,
    HMC, DSGE, GPU, or high-dimensional claims.

## Planned File Ownership

Allowed writes after M2.6b passes:

```text
bayesfilter/highdim/filtering.py
tests/highdim/test_p30_sv_short_sequential_tt_value_path.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6c-short-sequential-sv-tt-value-path-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Planned Commands

Focused command to refine after M2.6b:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_stochastic_volatility.py
```

Broad highdim guardrail follows the overnight runbook.
