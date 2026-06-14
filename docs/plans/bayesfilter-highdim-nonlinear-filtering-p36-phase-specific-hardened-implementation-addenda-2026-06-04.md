# P36 Zhao--Cui Phase-Specific Hardened Implementation Addenda

metadata_date: 2026-06-04

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- Gorodetsky, Karaman, and Marzouk, "A Continuous Analogue of the Tensor-Train
  Decomposition," Computer Methods in Applied Mechanics and Engineering, 2019.

source_artifacts:
- P30 mathematical note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- P34 reference implementation audit:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md`
- P35 phase subplans:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase*-subplan-2026-06-04.md`
- P36 hardening plan and review ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md`
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md`

what_is_not_concluded:
- This addendum does not implement any production code.
- This addendum does not approve DSGE trials.
- This addendum does not expose a top-level public API.
- This addendum does not claim the adaptive Zhao--Cui algorithm is
  differentiable.
- This addendum does not authorize NumPy, JAX, PyTorch, MATLAB, or Octave as a
  BayesFilter-owned production algorithmic backend.

## How To Use This Addendum

This file is the implementation-readiness layer missing from the original P35
phase subplans.  For each phase, the implementation worker must use:

1. the corresponding P35 phase subplan for motivation and sequence;
2. the P36 hardening plan for global governance;
3. this addendum for the exact implementation contract.

When P35 and this addendum differ, this addendum is the stricter contract.
Production code must not begin for a phase until that phase's checklist below
is accepted in the phase result ledger.

## Global Contract Shared By All Phases

Backend:
- BayesFilter-owned algorithmic code is TensorFlow/TensorFlow Probability
  backed and defaults to `tf.float64`.
- NumPy is allowed only in test reference fixtures, serialization/reporting, or
  an explicitly reviewed exception.
- JAX/PyTorch require a reviewed backend-exception plan.

Clean-room boundary:
- Forbidden implementation-source paths:
  `third_party/audit/tensor-ssm-paper-demo/**` and
  `third_party/audit/zhao_cui_tensor_ssm_p10/source/**`.
- Those paths may be cited only for audit-stage sanity and may not be ported,
  copied, translated, or used for class layouts, helper names, or comments.

Every phase result ledger must include:

```text
metadata_date
phase
git_commit
files_changed
commands_run
tests_run
fixtures_checked
tolerances_used
clean_room_inputs
third_party_code_consulted
clean_room_attestation
backend_status
measure_convention_status
branch_manifest_status
manifest_version
branch_hash
replay_tape_hash_when_applicable
exact_reference_status
exact_reference_metrics
primary_pass_criterion_status
veto_diagnostics_status
failure_exit_status
termination_reason
stop_condition_triggered
what_is_not_concluded
decision
```

Repository-wide statuses:

```text
OK
MEASURE_MISMATCH
REFERENCE_WEIGHT_MISSING
NONFINITE_VALUE
INVALID_SHAPE
COMPLEXITY_GATE
BRANCH_HASH_MISSING
INVALID_BRANCH_MISMATCH
SELECTIVE_BRANCH_HASH_REJECTED
CDF_MONOTONICITY_FAILURE
INVERSE_BRACKET_FAILURE
CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED
NORMALIZER_FLOOR_EXCEEDED
RETAINED_STORAGE_BUDGET_EXCEEDED
RETAINED_MEASURE_MISMATCH
RETAINED_AXES_MISMATCH
UNSUPPORTED_MOVING_BASIS_DERIVATIVE
REPLAY_TAPE_MISMATCH
REPLAY_CORE_HASH_MISMATCH
REPLAY_ENVIRONMENT_STALE
NONFINITE_RETAINED_DERIVATIVE
DERIVATIVE_SOLVE_FAILURE
FINITE_DIFFERENCE_BRANCH_MISMATCH
EXACT_REFERENCE_MISMATCH
STAGE_SANITY_ONLY
UNSUPPORTED_BACKEND
```

Phase-wide validation commands:

```bash
git diff --check
pytest -q tests/test_v1_public_api.py
```

The public API test is a guardrail in Phases 0--6.  It should pass without
changing `bayesfilter/__init__.py`.

## Phase 0 Addendum: Design Contract And Non-Public Skeleton

Allowed writes:

```text
bayesfilter/highdim/__init__.py
bayesfilter/highdim/diagnostics.py
bayesfilter/highdim/fixed_branch.py
bayesfilter/highdim/validation.py
tests/highdim/test_phase0_contracts.py
docs/plans/*p35-phase0*result*.md
```

Forbidden writes:

```text
bayesfilter/__init__.py
bayesfilter/nonlinear/**
docs/chapters/**
third_party/audit/**
```

Required symbols:

```text
DensityMeasure(Enum):
  PHYSICAL_LEBESGUE
  REFERENCE_LEBESGUE
  REFERENCE_MEASURE

MassMeasure(Enum):
  REFERENCE_LEBESGUE
  REFERENCE_MEASURE

HighDimStatus(Enum):
  exactly the repository-wide statuses listed above

MeasureConvention(frozen=True):
  density_measure: DensityMeasure
  mass_measure: MassMeasure
  reference_weight_name: str
  physical_coordinate_name: str = "r"
  reference_coordinate_name: str = "z"
  dtype_name: str = "float64"

HighDimValidationResult(frozen=True):
  status: HighDimStatus
  message: str
  diagnostics: Mapping[str, object]

BranchManifest(frozen=True):
  version: str
  payload: Mapping[str, object]
  to_canonical_bytes() -> bytes
  sha256() -> BranchHash

BranchIdentity(frozen=True):
  manifest: BranchManifest
  hash: BranchHash
```

Canonical branch serialization:
- sorted mapping keys;
- tuple/list order preserved;
- tensor dtype and shape included;
- numeric values serialized in stable byte order;
- scalar type tags included;
- finite-float policy explicit;
- version tag included.

Helper functions:

```text
assert_density_matches_mass(convention: MeasureConvention) -> None
assert_finite_tensor(name: str, tensor: tf.Tensor) -> None
assert_shape(name: str, tensor: tf.Tensor, expected_rank: int | None) -> None
assert_tf_float64(name: str, tensor: tf.Tensor) -> None
```

Required tests:

```text
test_highdim_import_does_not_touch_top_level_all
test_measure_convention_rejects_missing_density_measure
test_measure_convention_rejects_density_mass_mismatch
test_assert_finite_tensor_rejects_nan_and_inf
test_branch_hash_is_identical_for_identical_manifest
test_branch_hash_changes_for_each_manifest_field
test_branch_hash_records_tensor_dtype_shape_and_values
test_selective_hash_cannot_construct_branch_identity
test_numpy_not_used_as_highdim_algorithmic_backend
```

Phase 0 exit:
- imports pass;
- no top-level public API changes;
- branch hashing cannot be selective;
- missing or mismatched measure conventions fail deterministically.

## Phase 1 Addendum: Basis, Mass, And TT Algebra

Allowed writes:

```text
bayesfilter/highdim/bases.py
bayesfilter/highdim/tt.py
bayesfilter/highdim/diagnostics.py
bayesfilter/highdim/fixed_branch.py
tests/highdim/test_bases.py
tests/highdim/test_tt_algebra.py
docs/plans/*p35-phase1*result*.md
```

Required symbols and signatures:

```text
BoundedInterval(left: TensorLike, right: TensorLike, dtype: tf.DType = tf.float64)
UniformReferenceMeasure(domain: BoundedInterval)
LegendreBasis1D(domain: BoundedInterval, max_degree: int, normalized: bool = True)
LegendreBasis1D.basis_dim -> int
LegendreBasis1D.evaluate(points: tf.Tensor) -> tf.Tensor
LegendreBasis1D.derivative(points: tf.Tensor) -> tf.Tensor
LegendreBasis1D.mass_matrix(measure: MassMeasure) -> tf.Tensor
LegendreBasis1D.integral_vector(measure: MassMeasure) -> tf.Tensor
ProductBasis(bases: Sequence[LegendreBasis1D], convention: MeasureConvention)
ProductBasis.evaluate_axis(axis: int, points: tf.Tensor) -> tf.Tensor

TTCore(values: tf.Tensor)  # [rank_left, basis_dim, rank_right]
FunctionalTT(cores, product_basis, measure_convention, branch_identity=None)
FunctionalTT.rank_tuple() -> tuple[int, ...]
FunctionalTT.basis_dim_tuple() -> tuple[int, ...]
FunctionalTT.evaluate(points: tf.Tensor) -> tf.Tensor
FunctionalTT.integrate_all(measure: MassMeasure | None = None) -> tf.Tensor
TTContractedRepresentation(kept_axes, integrated_axes, cores,
                            measure_convention, branch_identity, diagnostics)
FunctionalTT.contract_axes(integrate_axes: Sequence[int]) -> TTContractedRepresentation
FunctionalTT.manifest_payload() -> Mapping[str, object]
```

`TTContractedRepresentation` field contract:

```text
kept_axes: tuple[int, ...]
integrated_axes: tuple[int, ...]
cores: tuple[TTCore, ...]
measure_convention: MeasureConvention
branch_identity: BranchIdentity
diagnostics: Mapping[str, object]
```

Pinned Legendre convention:

```text
xi = 2 (x-a)/(b-a) - 1
psi_n(x) = sqrt(2 n + 1) P_n(xi), n = 0,...,max_degree
integral psi_n psi_m dnu = delta_nm, dnu = dx/(b-a)
integral psi_0 dnu = 1
integral psi_n dnu = 0 for n > 0
integral psi_n psi_m dx = (b-a) delta_nm
d psi_n / dx = sqrt(2 n + 1) P'_n(xi) 2/(b-a)
```

TT evaluation contract:

```text
points: [N,D]
core[k].values: [r_k,p_k,r_{k+1}]
r_0 = r_D = 1
H_k(z_i,k)[a,b] = sum_l C_k[a,l,b] psi_k,l(z_i,k)
v_i,0 = [1]
v_i,k+1 = v_i,k H_k(z_i,k)
f(z_i) = v_i,D[0]
evaluate(points): [N]
```

Complexity gate:
- estimate dense elements and bytes before product-basis materialization;
- return `COMPLEXITY_GATE` before allocation if budgets are exceeded.

Required tests:

```text
test_legendre_basis_dim_is_max_degree_plus_one
test_normalized_legendre_reference_mass_identity_degrees_0_to_5
test_legendre_lebesgue_mass_has_interval_length_factor
test_integral_vector_is_unit_constant_under_reference_measure
test_basis_derivative_matches_finite_difference
test_product_basis_rejects_mixed_measure_conventions
test_rank_one_tt_product_evaluates_exactly
test_low_rank_bivariate_polynomial_evaluates_exactly
test_trivariate_coupled_function_has_expected_rank_shape_and_integral
test_integrate_all_uses_declared_mass_measure
test_complexity_gate_fires_before_dense_allocation
```

Phase 1 exit:
- Phase 0 and Phase 1 tests pass;
- degree convention and mass convention are recorded in the result ledger;
- no dense tensor allocation can bypass the complexity gate.

## Phase 2 Addendum: Squared Density And KR Transport

Allowed writes:

```text
bayesfilter/highdim/squared_tt.py
bayesfilter/highdim/transport.py
bayesfilter/highdim/diagnostics.py
tests/highdim/test_squared_tt_density.py
tests/highdim/test_transport.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase2*result*.md
```

Required signatures:

```text
DefensiveDensityProtocol.log_density(points: tf.Tensor) -> tf.Tensor
DefensiveDensityProtocol.normalizer(measure: MassMeasure) -> tf.Tensor
DefensiveDensityProtocol.manifest_payload() -> Mapping[str, object]

TensorProductReferenceDensity(product_basis, measure_convention, floor=0.0)

SquaredTTDensity(
    sqrt_tt: FunctionalTT,
    defensive_density: DefensiveDensityProtocol,
    tau: tf.Tensor,
    normalizer_floor: tf.Tensor,
    denominator_floor: tf.Tensor,
    measure_convention: MeasureConvention,
    branch_identity: BranchIdentity,
)
SquaredTTDensity.unnormalized_density(points: tf.Tensor) -> tf.Tensor
SquaredTTDensity.normalizer() -> tf.Tensor
SquaredTTDensity.log_density(points: tf.Tensor) -> tf.Tensor
SquaredTTMarginal(keep_axes, contracted_density, normalizer,
                  measure_convention, branch_identity, diagnostics)
SquaredTTDensity.marginal_density(keep_axes: Sequence[int]) -> SquaredTTMarginal
SquaredTTDensity.conditional_density(axis: int, prefix: tf.Tensor, grid: tf.Tensor) -> tf.Tensor

KRCDFConfig(grid_size, bisection_steps, monotonicity_tolerance,
            bracket_tolerance, denominator_floor, max_floor_count,
            dtype=tf.float64)
KRInversionResult(z_value, cdf_value, iterations, status, diagnostics)
KRTransport(density, coordinate_order, cdf_config)
KRTransport.forward(z_points) -> (u_points, log_abs_det_dF_dz, per_axis_results)
KRTransport.inverse(u_points) -> (z_points, log_abs_det_dz_dF, per_axis_results)
KRTransport.log_jacobian(z_points) -> tf.Tensor
```

`SquaredTTMarginal` field contract:

```text
keep_axes: tuple[int, ...]
contracted_density: SquaredTTDensity | TTContractedRepresentation
normalizer: tf.Tensor scalar, tf.float64
measure_convention: MeasureConvention
branch_identity: BranchIdentity
diagnostics: Mapping[str, object]
```

Pinned equations:

```text
q_u(z) = h(z)^2 + tau q_0(z)
Z = integral q_u(z) dM(z)
q(z) = q_u(z) / Z
M_k[l,m] = integral psi_k,l(z_k) psi_k,m(z_k) dM_k(z_k)
G_k[(a,a'),(b,b')] =
  sum_{l,m} C_k[a,l,b] C_k[a',m,b'] M_k[l,m]
Z_h = contract(G_1,...,G_D)
Z = Z_h + tau Z_0
u_j = F_j(z_j | z_<j)
z_j = F_j^{-1}(u_j | z_<j)
log |det dF/dz| = sum_j log q(z_j | z_<j)
```

Shape contract:

```text
points, z_points, u_points: [N,D]
density outputs: [N]
normalizer: scalar
one-axis inversion result z_value and cdf_value: [N]
```

Deterministic veto statuses:

```text
MEASURE_MISMATCH
NORMALIZER_FLOOR_EXCEEDED
CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED
CDF_MONOTONICITY_FAILURE
INVERSE_BRACKET_FAILURE
NONFINITE_VALUE
```

Required tests:

```text
test_constant_sqrt_tt_normalizes_to_one
test_pair_core_square_contraction_matches_dense_quadrature
test_nonuniform_reference_missing_weight_trap_fails
test_defensive_density_rescues_declared_zero_corner
test_marginal_contraction_matches_dense_2d_reference
test_conditional_density_integrates_to_one_on_grid
test_one_dimensional_cdf_inverse_round_trip
test_separable_density_gives_independent_kr_maps
test_kr_jacobian_identity_matches_log_conditional_sum
test_bracket_failure_returns_veto_status
```

Phase 2 exit:
- every density and transport object carries measure convention and branch hash;
- all normalizers, conditionals, CDFs, and inverse-CDFs pass exact or dense
  low-dimensional checks;
- floor usage is diagnostic until it exceeds the declared threshold, then it is
  a veto.

## Phase 3 Addendum: Fixed-Branch Fitting

Allowed writes:

```text
bayesfilter/highdim/fitting.py
bayesfilter/highdim/fixed_branch.py
bayesfilter/highdim/validation.py
tests/highdim/test_fixed_branch_fit.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase3*result*.md
```

Required signatures:

```text
FixedTTFitConfig(
    ranks: tuple[int, ...],
    ridge: float,
    max_sweeps: int,
    sweep_order: tuple[int, ...],
    row_budget: int,
    column_budget: int,
    dense_matrix_byte_budget: int,
    normal_matrix_byte_budget: int,
    condition_number_warning: float,
    condition_number_veto: float,
    holdout_tolerance: float,
    dtype: tf.DType = tf.float64,
)

FixedTTFitSampleBatch(
    points: tf.Tensor,         # [N,D], tf.float64
    target_values: tf.Tensor,  # [N], tf.float64
    weights: tf.Tensor,        # [N], tf.float64, nonnegative
    holdout_points: tf.Tensor | None = None,   # [N_hold,D], tf.float64
    holdout_values: tf.Tensor | None = None,   # [N_hold], tf.float64
    holdout_weights: tf.Tensor | None = None,  # [N_hold], tf.float64
)

FixedTTFitter.fit(product_basis, samples, config, initial_cores,
                  branch_seed, measure_convention) -> FixedTTFitResult
```

Core-update equations:

```text
H_i,k[a,b] = sum_l C_k[a,l,b] psi_k,l(z_i,k)
L_i,0 = [1]
L_i,j = L_i,j-1 H_i,j-1
R_i,D = [1]
R_i,j+1 = H_i,j+1 R_i,j+2
A_j[i,index(a,l,b)] = L_i,j[a] psi_j,l(z_i,j) R_i,j+1[b]
index(a,l,b) = ((a * p_j) + l) * r_{j+1} + b
N_j = A_j^T W A_j + rho I
d_j = A_j^T W y
c_j = solve(N_j, d_j)
C_j = unvec(c_j, [r_j,p_j,r_{j+1}])
```

Environment rule:
- after every accepted core update, rebuild environments from the current core
  list before the next update;
- stale environment reuse is forbidden unless invalidation and rebuild are
  tested explicitly.

Branch manifest fields:

```text
product_basis fields
measure_convention
sample points hash
target values hash
weights hash
holdout hash
ranks
ridge
dtype
sweep_order
max_sweeps
initial core hash
initialization rule
per-core update statuses
condition estimates
stabilization choices
complexity budgets
solver backend
deterministic seed
```

Required tests:

```text
test_fixed_fit_rank_one_separable_target_exact
test_fixed_fit_known_rank_two_bivariate_target
test_environment_recomputed_after_each_core_update
test_design_matrix_shape_and_vectorization_order
test_normal_equation_solution_matches_direct_dense_reference
test_deterministic_replay_same_manifest_same_values
test_branch_hash_changes_for_samples_ridge_ranks_sweep_order
test_holdout_residual_veto_for_under_ranked_target
test_row_column_and_normal_matrix_budgets_fail_before_allocation
test_condition_number_veto_status_is_deterministic
```

Phase 3 exit:
- exact fixed-rank examples fit within tolerance;
- deterministic replay reproduces values and branch hash;
- under-ranked and over-budget cases fail with deterministic statuses;
- no adaptive derivative claim is made.

Phase 3 termination rules:
- each core update records `OK`, `COMPLEXITY_GATE`, `NONFINITE_VALUE`, or a
  deterministic condition-number veto in diagnostics;
- `holdout_residual > holdout_tolerance` after a completed sweep is an
  acceptance veto, not an explanatory warning;
- fitting stops with `termination_reason=max_sweeps_exhausted` if no earlier
  veto fires and `max_sweeps` is reached;
- early convergence is allowed only if the hardened implementation adds a
  reviewed `sweep_delta_tolerance` field and a test for
  `termination_reason=relative_sweep_delta_below_tolerance`;
- the result ledger records `termination_reason` and
  `stop_condition_triggered`.

## Phase 4 Addendum: Filtering Value Path

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/filtering.py
bayesfilter/highdim/validation.py
tests/highdim/test_filtering_kalman_exact.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase4*result*.md
```

Required signatures:

```text
TFHighDimStateSpaceModel.parameter_dim() -> int
TFHighDimStateSpaceModel.state_dim() -> int
TFHighDimStateSpaceModel.observation_dim() -> int
TFHighDimStateSpaceModel.initial_log_density(theta, x0) -> tf.Tensor
TFHighDimStateSpaceModel.transition_log_density(theta, x_prev, x_next, t) -> tf.Tensor
TFHighDimStateSpaceModel.observation_log_density(theta, x_t, y_t, t) -> tf.Tensor

HighDimCoordinateMap.forward(reference_points) -> (physical_points, log_abs_det)
HighDimCoordinateMap.inverse(physical_points) -> (reference_points, log_abs_det)
HighDimCoordinateMap.manifest_payload() -> Mapping[str, object]

FixedBranchFilterConfig(fit_config, density_tau, normalizer_floor,
                        denominator_floor, retained_storage_byte_budget,
                        coordinate_maps, measure_convention,
                        deterministic_seed, dtype=tf.float64)
RetainedFilter(density, retained_axes, retained_coordinate_names,
               measure_convention, normalizer, branch_identity,
               storage_kind, diagnostics)
AdjacentTargetBatch(time_index, physical_points, reference_points, log_target,
                    sqrt_target, weights, measure_convention,
                    retained_filter_hash)
FixedBranchFilterStepResult(time_index, fit_result, density, log_normalizer,
                            retained_filter, branch_identity, status,
                            diagnostics)
FixedBranchFilterResult(log_likelihood, retained_filter, steps,
                        branch_identity, status, diagnostics)
FixedBranchSquaredTTFilter(config).log_likelihood(model, theta, observations,
                                                  initial_branch=None)
  -> FixedBranchFilterResult
```

Shape contract:

```text
theta: [N,P] or [P]
x_prev, x_next: [N,d_x] or [d_x]
y_t: [d_y]
log_density outputs: [N]
adjacent physical block at t>=1: [N, P + 2 d_x]
adjacent physical block at t=0: [N, P + d_x]
reference block: [N,D_t]
```

Filtering equations:

```text
gamma_0(theta,x0) = prior(theta) p_theta(x0) g_theta(y0 | x0)
gamma_t(theta,x_{t-1},x_t) =
  retained_{t-1}(theta,x_{t-1})
  f_theta(x_t | x_{t-1})
  g_theta(y_t | x_t)
gamma_t^nu(z) = gamma_t(Psi_t(z)) |det D Psi_t(z)| / omega_t(z)
Z_t = integral gamma_t^nu(z) dnu_t(z)
ell_hat(theta) = sum_t log Z_t + declared_constant_offsets
```

Retained-filter rule:
- retain a marginal object over \((theta,x_t)\);
- store retained axes/order, coordinate names, basis, measure convention,
  normalizer, branch identity, and contraction diagnostics;
- for multi-dimensional retained coordinates, store `SquaredTTDensity` or a
  contracted TT representation, never a dense product basis by default;
- if dense storage exceeds the byte budget, return
  `RETAINED_STORAGE_BUDGET_EXCEEDED`;
- next-step targets must reject retained filters with
  `RETAINED_MEASURE_MISMATCH` or `RETAINED_AXES_MISMATCH`.

Pinned scalar fixtures:

```text
fixture_scalar_lgssm_one_step:
  x0 ~ N(0,1)
  y0 | x0 ~ N(x0,0.09)
  observations: [0.2]
  expected_log_evidence: -0.980376005178410
  expected_filter_mean: 0.183486238532110
  expected_filter_variance: 0.082568807339450
  tolerance: 2e-10 direct, 2e-6 TT path

fixture_scalar_lgssm_two_step:
  x0 ~ N(0,1)
  x1 = 0.7 x0 + eta1, eta1 ~ N(0,0.25)
  y_t | x_t ~ N(x_t,0.09)
  observations: [0.2,-0.1]
  expected_log_evidence: -1.484707421612687
  expected_filter_mean_t1: -0.045960935616108
  expected_filter_variance_t1: 0.068709910778876
  tolerance: 2e-10 direct, 5e-6 TT path

fixture_multivariate_lgssm_two_step:
  m0: [0.1, -0.2]
  P0: [[1.0, 0.2], [0.2, 0.7]]
  A: [[0.8, 0.1], [-0.05, 0.6]]
  Q: [[0.12, 0.02], [0.02, 0.10]]
  H: [[1.0, 0.3]]
  R: [[0.16]]
  observations: [[0.15], [-0.05]]
  expected_log_evidence_t0: -1.070896331885871
  expected_log_evidence_t0_t1: -1.550790276990481
  expected_filter_mean_t1: [0.05354198, -0.14118922]
  expected_filter_covariance_t1:
    [[0.10101319, -0.05495946],
     [-0.05495946, 0.29692253]]
  tolerance: 2e-10 direct, 1e-5 TT path

fixture_affine_nonuniform_reference_one_step:
  physical_model:
    x0 ~ N(0,1)
    y0 | x0 ~ N(x0,0.09)
    observation: [0.2]
  coordinate_map:
    r = 0.5 + 2 z
    z in [-1,1]
    log_abs_det: log(2)
  reference_measure:
    dnu(z) = omega(z) dz
    omega(z) = (1 + 0.25 z) / 2
  reference_target:
    gamma_nu(z) = gamma_r(0.5 + 2z) * 2 / omega(z)
  expected_log_evidence_truncated_to_r_in_[-1.5,2.5]: -0.980376007510876
  expected_filter_mean_truncated: 0.183486242567321
  expected_filter_variance_truncated: 0.082568800546224
  tolerance: 5e-10 dense/reference fixture, 5e-6 TT path
```

Additional fixture obligation:
- the Phase 4 result ledger records these fixed fixtures, commands used to
  verify them, and tolerances actually applied; it must not define replacement
  fixtures after seeing implementation output.

Required tests:

```text
test_model_protocol_shapes_and_broadcasting
test_one_step_scalar_kalman_evidence
test_two_step_scalar_kalman_evidence_and_retained_marginal
test_multivariate_kalman_evidence_and_marginal
test_affine_map_nonuniform_reference_recursive_fixture
test_retained_filter_storage_rejects_dense_product_when_over_budget
test_next_step_target_rejects_measure_mismatch
test_deterministic_replay_same_seed_observations_branch_value_retained
test_p10_stage_sanity_is_labeled_stage_sanity_only
```

Phase 4 exit:
- exact scalar and multivariate small-model gates pass;
- non-identity coordinate/reference-measure fixture passes;
- P10 comparison is labeled `STAGE_SANITY_ONLY`;
- retained filter storage is measure-safe and budget-safe.

## Phase 5 Addendum: Fixed-Branch Derivatives

Allowed writes:

```text
bayesfilter/highdim/derivatives.py
bayesfilter/highdim/filtering.py
bayesfilter/highdim/fitting.py
bayesfilter/highdim/validation.py
tests/highdim/test_fixed_branch_derivatives.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase5*result*.md
```

Required signatures:

```text
FixedBranchDerivativeConfig(parameter_indices,
                            finite_difference_h=(1e-2,3e-3,1e-3,3e-4),
                            derivative_ridge_floor=1e-12,
                            solve_condition_number_veto=1e12,
                            allow_parameter_dependent_coordinate_map=False,
                            allow_moving_basis=False,
                            dtype=tf.float64)
CoreDerivativeState(core_index, core, dot_core, pre_update_core_hash,
                    post_update_core_hash)
SweepDerivativeDiagnostics(time_index, sweep_index, sweep_direction,
                           core_index, status, condition_number,
                           normal_matrix_hash, rhs_hash, coefficient_hash,
                           environment_provenance)
FixedBranchReplayTape(version, branch_identity, entries)
FixedBranchReplayTape.manifest_payload() -> Mapping[str, object]
FixedBranchReplayTape.assert_matches_branch(branch_identity) -> None
FixedBranchScoreResult(log_likelihood, score, branch_identity,
                       replay_tape_hash, finite_difference_table, status,
                       diagnostics)
FiniteDifferenceRow(parameter_index, h, value_plus, value_minus,
                    branch_hash_plus, branch_hash_minus, branch_hash_base,
                    centered_difference, analytic_gradient, abs_error,
                    rel_error, row_status)
FiniteDifferenceTable(rows).valid_rows()
FiniteDifferenceTable(rows).max_abs_error()
```

Branch manifest and replay tape must include:

```text
manifest_version
observation_hash
time_indices
theta_shape_and_dtype
retained_filter_hashes
retained_axes_and_order
coordinate_map_identity
coordinate_map_parameter_dependent
moving_basis_supported: false
fixed_sample_set_hashes
target_value_hashes
target_derivative_value_hashes
sample_weight_hashes
initial_core_hashes
initialization_rule
initial_dot_core_policy
initial_dot_core_hashes
per_step_fit_config_hashes
per_sweep_per_core_update_statuses
floor_policy_and_counts
defensive_density_identifier
solver_backend
deterministic_seed
pre_replay_branch_hash
replay_tape_version
```

The pre-replay branch identity excludes `replay_tape_hash`.  The replay tape is
materialized after the pre-replay branch is fixed, then hashed and stored in the
score result and result ledger.  This avoids a cyclic contract in which a
branch identity would need to contain the hash of the tape that contains the
branch identity.

Replay semantics:
- initialize cores and derivative cores from the manifest before any update;
- verify initialized hashes before the first core update;
- build \(L,R,A,N,d,c\) from the current pre-update core list;
- current core list includes all prior accepted updates in the same sweep;
- reverse sweeps use post-update right-side cores from earlier reverse updates;
- rejected updates leave both \(C_j\) and \(\dot C_j\) unchanged;
- stale environments are `REPLAY_ENVIRONMENT_STALE` vetoes.

Derivative equations:

```text
H_i,k[a,b] = sum_l C_k[a,l,b] psi_k,l(z_i,k)
dot H_i,k[a,b] = sum_l dot C_k[a,l,b] psi_k,l(z_i,k)
dot L_i,j = dot L_i,j-1 H_i,j-1 + L_i,j-1 dot H_i,j-1
dot R_i,j = dot H_i,j R_i,j+1 + H_i,j dot R_i,j+1
dot A_j[i,index(a,l,b)] =
  dot L_i,j[a] psi_j,l(z_i,j) R_i,j+1[b]
  + L_i,j[a] psi_j,l(z_i,j) dot R_i,j+1[b]
N_j = A_j^T W A_j + rho I
d_j = A_j^T W y
dot N_j = dot A_j^T W A_j + A_j^T W dot A_j
          + A_j^T dot W A_j + dot rho I
dot d_j = dot A_j^T W y + A_j^T W dot y + A_j^T dot W y
dot c_j = solve(N_j, dot d_j - dot N_j c_j)
dot Z = 2 integral h dot h dM + dot tau Z_0 + tau dot Z_0
dot log Z = dot Z / Z
dot retained = dot m / Z - m dot Z / Z^2
```

Initial implementation:
- fixed branch has \(\dot W=0\), \(\dot\rho=0\), \(\dot\tau=0\), and
  \(\dot Z_0=0\) unless the branch explicitly declares otherwise;
- moving-basis derivatives are unsupported and must return
  `UNSUPPORTED_MOVING_BASIS_DERIVATIVE`.

Finite-difference rule:
- valid rows require exact equality of base, plus, and minus
  `fd_compatibility_hash` values;
- `fd_compatibility_hash` excludes parameter-perturbed target values and target
  derivative values because those change by construction under
  \(\theta+h e_m\) and \(\theta-h e_m\);
- `fd_compatibility_hash` includes sample set, basis, retained axes/order,
  coordinate-map identity, sweep order, ranks, ridge, solver backend, floor
  policy, deterministic seed, and pre-replay branch structure;
- mismatch rows are `FINITE_DIFFERENCE_BRANCH_MISMATCH`;
- mismatch rows are invalid evidence, not derivative successes or failures.

Pinned fixtures:

```text
scalar two-step LGSSM transition coefficient score:
  A_base: 0.7
  observations: [0.2,-0.1]
  expected_score_dell_dA: -0.241250978551728
  tolerance: 2e-10 direct, 2e-5 TT path

one-step LGSSM prior mean score:
  mu0_base: 0.0
  observation: [0.2]
  expected_score_dell_dmu0: 0.183486238532110
  tolerance: 2e-10 direct, 2e-5 TT path

nonlinear dense quadrature score:
  x0 ~ N(0,1)
  y0 | x0,theta ~ N(theta sin(x0),0.25)
  theta_base: 0.4
  observation: [0.1]
  expected_log_evidence: -0.373000101795619
  expected_score_dell_dtheta: -0.608378439103854
  oracle: Gauss-Hermite with at least 120 nodes
  tolerance: 5e-10 direct, 5e-5 TT path
```

Required tests:

```text
test_target_derivative_matches_finite_difference
test_environment_derivatives_match_finite_difference
test_design_matrix_dotA_matches_finite_difference
test_normal_equation_dotN_dotd_dotc_matches_finite_difference
test_tt_evaluation_derivative_matches_finite_difference
test_log_normalizer_derivative_matches_finite_difference
test_retained_filter_quotient_derivative_matches_finite_difference
test_replay_tape_reconstructs_pre_and_post_update_core_states
test_reverse_sweep_uses_post_update_right_environment
test_replay_environment_cache_invalidation_is_enforced
test_one_step_scalar_kalman_score_exact
test_two_step_scalar_kalman_score_exact
test_scalar_nonlinear_dense_quadrature_score
test_branch_mismatch_invalidates_fd_row
test_derivative_replay_rejects_adaptive_branch_change
test_unsupported_moving_basis_derivative_status
test_derivative_solve_failure_status
```

Phase 5 exit:
- exact score baselines pass;
- finite-difference rows with branch mismatch are invalidated;
- replay tape reproduces pre/post core states;
- diagnostics state fixed-branch-only scope without claiming adaptive
  differentiability.

## Phase 6 Addendum: Stress Models And Performance Ladder

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/validation.py
tests/highdim/test_scaling_smoke.py
docs/plans/*p35-phase6*stress-plan*.md
docs/plans/*p35-phase6*result*.md
```

No stress run may start unless Phase 0--5 tests remain green.

Required stress statuses:

```text
PASS_EXACT_REFERENCE
PASS_DIAGNOSTIC_ONLY
FAIL_IMPLEMENTATION
FAIL_TUNING
FAIL_APPROXIMATION
FAIL_RESOURCE
FAIL_NUMERICAL_VETO
BLOCKED_BY_PHASE_REGRESSION
```

Required model equations:

```text
LGSSM:
  x0 ~ N(m0,P0)
  x_t = A_theta x_{t-1} + b_theta + eta_t, eta_t ~ N(0,Q_theta)
  y_t = H_theta x_t + c_theta + eps_t, eps_t ~ N(0,R_theta)

SV:
  x0 ~ N(mu, sigma^2/(1-phi^2))
  x_t = mu + phi (x_{t-1}-mu) + sigma eta_t
  y_t | x_t ~ N(0, beta^2 exp(x_t))
```

SIR and predator-prey are blocked until the constrained-state coordinate policy
and observation likelihood are written explicitly.

Required run manifest:

```text
git commit
command
environment
CPU/GPU status
random seeds
dtype
model equations
dimension/rank/degree/horizon grid
row/column/normal-matrix budgets
expected memory model
measured peak memory when available
wall time
exact-reference error when available
fit and holdout residuals
normalizer and CDF diagnostics
branch hash
deterministic replay status
decision status
what is not concluded
```

Required grids:

```text
LGSSM exact ladder:
  state_dim: 1,2,4,8
  parameter_dim: 0,1,2
  horizon: 1,2,5,10
  rank: 1,2,4,8
  max_degree: 1,2,4

SV tiny-reference ladder:
  horizon: 1,2,5
  rank: 1,2,4
  max_degree: 2,4
```

GPU rule:
- any GPU detection, TensorFlow GPU initialization, or benchmark command
  requires escalated/trusted execution under `AGENTS.md`;
- deliberate CPU-only runs must hide GPUs before framework import and record
  that choice.

Required tests:

```text
test_scaling_smoke_lgssm_runs_tiny_grid_with_finite_diagnostics
test_scaling_smoke_blocks_when_phase0_to_phase5_regression_flag_is_set
test_scaling_manifest_requires_resource_and_replay_fields
test_stress_status_separates_tuning_approximation_resource_failures
```

Phase 6 ladder termination rules:
- `BLOCKED_BY_PHASE_REGRESSION` halts the entire ladder immediately;
- `FAIL_NUMERICAL_VETO` halts the current model/rank/degree/horizon branch and
  requires a result-ledger explanation before any larger configuration of the
  same model is attempted;
- `FAIL_RESOURCE` halts larger configurations along the offending dimension,
  rank, degree, or horizon axis unless the resource budget is explicitly
  revised in a new reviewed plan;
- `FAIL_IMPLEMENTATION` halts all stress claims until the exact Phase 0--5
  gates are rerun;
- `FAIL_TUNING` may continue only to smaller or explicitly predeclared
  neighboring configurations;
- every ladder result records `termination_reason` and
  `stop_condition_triggered`.

Phase 6 exit:
- exact Phase 0--5 gates still pass;
- at least one LGSSM scaling result ledger reports exact reference errors;
- stress failures are classified as implementation, tuning, approximation,
  resource, or numerical-veto failures;
- DSGE trials remain blocked until a defensible operating envelope is recorded.

## Phase 7 Addendum: Public API Decision

Allowed writes only after explicit Phase 7 approval:

```text
bayesfilter/__init__.py
bayesfilter/highdim/__init__.py
tests/test_v1_public_api.py
tests/highdim/test_public_api_highdim.py
docs/plans/*p35-phase7*result*.md
```

Decision statuses:

```text
KEEP_INTERNAL
EXPERIMENTAL_SUBPACKAGE_ONLY
STABLE_TOP_LEVEL_API
BLOCKED_UNRESOLVED_VALIDATION
BLOCKED_UNSTABLE_BRANCH_CONTRACT
```

Candidate stable symbols, only if approved:

```text
TFFixedBranchSquaredTTFilterConfig
TFFixedBranchSquaredTTFilterResult
TFFixedBranchSquaredTTScoreResult
tf_fixed_branch_squared_tt_log_likelihood
tf_fixed_branch_squared_tt_score
```

API naming rule:
- stable public names must include `fixed_branch` or equivalent scope language;
- docs must state the fixed-branch scalar, measure convention, branch hash,
  exact validation status, stress validation status, failure exits, and
  non-claims about adaptive derivatives.

Required tests:

```text
test_existing_v1_public_api_symbols_preserved
test_no_highdim_top_level_symbols_before_phase7_option_c
test_experimental_subpackage_import_is_explicit_only
test_stable_public_symbols_include_fixed_branch_scope_language
test_public_docs_do_not_claim_adaptive_derivative
```

Phase 7 exit:
- no unresolved blocker remains in Phase 0--6 result ledgers;
- public API surface does not expose unstable branch internals;
- docs do not imply adaptive differentiability or exact nonlinear likelihood;
- existing v1 public API tests pass.

## Validation For This Addendum

Required local validation:

```bash
git diff --check -- \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-addenda-claude-review-ledger-2026-06-04.md

rg -n "metadata_date|seed_papers|what_is_not_concluded" \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-addenda-claude-review-ledger-2026-06-04.md

git status --short -- \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-implementation-addenda-2026-06-04.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-phase-specific-hardened-addenda-claude-review-ledger-2026-06-04.md
```

Pass condition:
- Claude review passes or no accepted blocker remains;
- metadata fields exist in both addendum and ledger;
- whitespace validation passes;
- only docs/plans P36 addendum artifacts are created by this task.
