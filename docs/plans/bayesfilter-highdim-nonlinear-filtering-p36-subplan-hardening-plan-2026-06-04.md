# P36 Zhao--Cui Subplan Hardening Plan

metadata_date: 2026-06-04

parent_plans:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-subplan-2026-06-04.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-subplan-2026-06-04.md`

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
- P35 parent and phase subplans listed above.
- Local backend policy:
  `AGENTS.md` and `CLAUDE.md`.

what_is_not_concluded:
- This P36 plan does not implement Zhao--Cui, fixed-branch TT fitting, squared
  densities, transports, filtering, derivatives, benchmarks, or public APIs.
- This plan does not approve DSGE trials.
- This plan does not claim adaptive Zhao--Cui rank, pivot, cross, basis, or
  coordinate choices are differentiable.
- This plan does not claim the authors' MATLAB repository is production
  BayesFilter code.
- This plan does not permit a NumPy, JAX, PyTorch, MATLAB, or Octave production
  implementation path.
- This plan does not change the existing top-level `bayesfilter.__all__`.

## Objective

The P35 phase subplans correctly identify the implementation phases and major
guardrails, but they are not yet sufficiently implementation-ready.  P36's job
is to harden those subplans into engineering specifications that a future
implementation agent can follow without inventing unstated mathematical,
shape, serialization, testing, or failure-exit policy.

The intended P36 output is a reviewed hardening standard and phase-by-phase
patch plan.  The next implementation step after P36 should be either:

1. patch the P35 phase subplans in place using this hardening standard; or
2. create P36 phase-specific hardened specification addenda under
   `docs/plans/`.

No production code should be written until those hardened implementation specs
exist and pass review.

## Skeptical Plan Audit

Wrong baseline risk: treating the MATLAB repository or P10 Octave smoke as a
correctness oracle would be wrong.  P36 keeps exact analytic functions, Kalman
references, finite differences with identical branch hashes, and resource
budgets as the gates.  P10 is only stage-sanity evidence.

Proxy-metric risk: fit residuals, holdout residuals, ESS, wall time, memory,
and rank growth can explain failures or nominate settings.  They cannot certify
mathematical correctness unless exact references or finite-difference gates
also pass.

Hidden-assumption risk: basis normalization, reference measure, mass measure,
coordinate map, vectorization order, branch hash fields, and retained-filter
storage can each silently change the scalar.  P36 requires each one to be
explicit in the hardened phase specs.

Environment risk: GPU diagnostics require elevated/trusted execution under
`AGENTS.md`.  P36's hardening plan does not run GPU benchmarks.  Phase 6 must
state GPU/CPU status in manifests before any scaling claim.

Artifact risk: a broad plan with no exact signatures would not answer the
user's question.  Therefore each hardened phase must name write sets,
symbols, signatures, tensor shapes, tests, failure statuses, commands, and
non-claims.

Audit decision: proceed with the P36 planning artifact only.  Do not implement
production code in this turn.

## Evidence Contract

Question: can the P35 Zhao--Cui implementation subplans be hardened enough that
future agents know exactly what to implement, what to test, what to reject, and
what not to claim?

Baseline/comparator:
- P35 phase subplans as currently written;
- P30 mathematical note for equations and fixed-branch scope;
- P34 audit for reference-stage ordering and clean-room boundary;
- existing BayesFilter style: frozen dataclasses, TensorFlow `tf.float64`,
  explicit diagnostics, and stable public API tests.

Primary pass criteria:
- P36 names the missing implementation details for every P35 phase;
- every phase has required write sets, class/function surfaces, shapes, dtype
  policy, tests, failure exits, and result-ledger fields;
- Phase 5 includes explicit derivative recursions for sweep environments,
  normal matrices, right-hand sides, coefficients, normalizers, and retained
  filters;
- Phase 6 includes concrete benchmark manifests, scaling grids, resource
  budgets, and acceptance statuses;
- Phase 7 preserves top-level API deferral until reviewed evidence exists;
- Claude review returns `PASS`, or all remaining disagreements are recorded as
  unresolved blockers.

Veto diagnostics:
- plan permits production code before hardened specs;
- plan permits top-level public API exposure before Phase 7;
- plan treats adaptive Zhao--Cui derivatives as implemented or certified;
- plan omits measure-convention or branch-identity gates;
- plan omits exact small-model value/score baselines before stress models;
- plan allows finite-difference rows with branch mismatch as derivative
  evidence;
- plan allows NumPy/JAX/PyTorch as the BayesFilter-owned algorithmic backend
  without reviewed exception;
- Claude raises a blocker that Codex accepts or partially accepts and is not
  patched within the review loop.

Explanatory diagnostics:
- number and severity of Claude findings;
- Codex classifications: `ACCEPT`, `PARTIAL`, `DISPUTE`, `CLARIFY`;
- residual open risks after max review iterations.

Artifacts:
- this plan;
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md`.

## Global Hardening Standard

Every hardened P35 phase spec must include the following sections.

1. Exact file ownership.
   List production files, test files, result ledgers, and forbidden files.  If
   a phase writes no production code, say so.  Phases 0--6 must not edit
   `bayesfilter/__init__.py` or `tests/test_v1_public_api.py` except to run
   existing tests.

2. Symbol surface.
   Name each class, dataclass, enum, protocol, function, method, and status
   string.  Include constructor or function signatures with argument names,
   default values, dtype expectations, and return types.

3. Tensor contract.
   For every public-in-module method, state shape, dtype, batch convention, and
   broadcasting policy.  The default dtype is TensorFlow `tf.float64`.  NumPy is
   allowed only in independent test references, serialization/reporting, or a
   reviewed exception.

4. Measure and coordinate contract.
   State whether an object lives in physical Lebesgue coordinates,
   reference-Lebesgue coordinates, or reference-measure coordinates.  State the
   density being represented, the mass measure used by contractions, the domain
   map, and any Jacobian or reference-density factor.

5. Mathematical equations.
   Provide the exact equation the implementation computes, including index
   order and vectorization order.  If the code is an approximation, name the
   approximation and its residual diagnostic.

6. Failure exits.
   Name every deterministic status, exception, or validation result.  State
   which are vetoes and which are explanatory warnings.

7. Branch manifest.
   For any branch-bearing phase, list every field in the canonical realized
   branch manifest and how it affects the hash.  Selective hashes are forbidden.

8. Tests.
   Name pytest files, test function names, fixtures, exact inputs, expected
   outputs or tolerances, and commands.  Tests must include both successful
   examples and failure exits.

9. Result ledger.
   State the result file pattern, run manifest fields, decision table, and
   non-claims.

10. Stop condition.
    State when the phase blocks the next phase.  A phase cannot pass with
    unresolved measure mismatch, branch mismatch, nonfinite value/score,
    failed exact references, or unreviewed backend exception.

## Global Clean-Room Rule

The production implementation phases must not use third-party source code as a
coding input.  The following paths are forbidden implementation sources during
Phases 0--7:

```text
third_party/audit/tensor-ssm-paper-demo/**
third_party/audit/zhao_cui_tensor_ssm_p10/source/**
```

Those paths may be cited only as audit/reference artifacts in planning or
post-hoc stage sanity ledgers.  They must not be used as translation, porting,
class-layout, helper-name, or comment sources for BayesFilter production code.

Every phase result ledger must include:

```text
clean_room_inputs
third_party_code_consulted
clean_room_attestation
```

Accepted values:

```text
clean_room_inputs:
  P30 mathematical note
  P35/P36 implementation specs
  BayesFilter local APIs and tests
  independently derived equations

third_party_code_consulted:
  none_for_implementation
  audit_only_with_paths_and_purpose

clean_room_attestation:
  no MATLAB/Octave source translated, copied, or ported
  production code justified by equations and BayesFilter contracts
```

If a future worker consults a forbidden source while implementing, the phase
must stop and write a contamination-risk note before any code can be accepted.

## Global Status Contract

The hardened specs must use deterministic status names.  The initial status
namespace must include:

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

The hardening specs may add narrower statuses, but they may not replace these
names with ad hoc strings.  Every pytest failure-exit test must assert the
exact status.

## Phase 0 Hardening: Design Contract And Non-Public Skeleton

The hardened Phase 0 spec must turn the skeleton into exact contracts.

Required write set:

```text
bayesfilter/highdim/__init__.py
bayesfilter/highdim/diagnostics.py
bayesfilter/highdim/fixed_branch.py
bayesfilter/highdim/validation.py
tests/highdim/test_phase0_contracts.py
docs/plans/*p35-phase0*result*.md
```

Required symbols:

```text
DensityMeasure(Enum)
  PHYSICAL_LEBESGUE
  REFERENCE_LEBESGUE
  REFERENCE_MEASURE

MassMeasure(Enum)
  REFERENCE_LEBESGUE
  REFERENCE_MEASURE

HighDimStatus(Enum)
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

MeasureConvention(frozen=True)
  density_measure: DensityMeasure
  mass_measure: MassMeasure
  reference_weight_name: str
  physical_coordinate_name: str = "r"
  reference_coordinate_name: str = "z"
  dtype_name: str = "float64"

HighDimValidationResult(frozen=True)
  status: HighDimStatus
  message: str
  diagnostics: Mapping[str, object]
```

Required helper signatures:

```text
assert_density_matches_mass(convention: MeasureConvention) -> None
assert_finite_tensor(name: str, tensor: tf.Tensor) -> None
assert_shape(name: str, tensor: tf.Tensor, expected_rank: int | None) -> None
assert_tf_float64(name: str, tensor: tf.Tensor) -> None
```

`BranchManifest` must have a canonical serializer specified before code:

```text
BranchManifest(version: str, payload: Mapping[str, object])
BranchManifest.to_canonical_bytes() -> bytes
BranchManifest.sha256() -> BranchHash
BranchIdentity(manifest: BranchManifest, hash: BranchHash)
```

Canonical serialization must include sorted mapping keys, tuple/list order,
tensor dtype, tensor shape, byte order, scalar type tags, finite-float policy,
and a version tag.  Serialization may convert TensorFlow tensors at the
serialization/reporting boundary; this is not an algorithmic NumPy backend.

Required Phase 0 tests:

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

Exit: the skeleton is importable, non-public, TensorFlow-backed, and unable to
represent an unmeasured density or partial branch identity.

## Phase 1 Hardening: Basis, Mass, And TT Algebra

The hardened Phase 1 spec must remove all off-by-one and measure ambiguity.

Required write set:

```text
bayesfilter/highdim/bases.py
bayesfilter/highdim/tt.py
bayesfilter/highdim/diagnostics.py
bayesfilter/highdim/fixed_branch.py
tests/highdim/test_bases.py
tests/highdim/test_tt_algebra.py
docs/plans/*p35-phase1*result*.md
```

Required basis symbols and signatures:

```text
BoundedInterval(left: TensorLike, right: TensorLike, dtype: tf.DType = tf.float64)
UniformReferenceMeasure(domain: BoundedInterval)
LegendreBasis1D(domain: BoundedInterval, max_degree: int, normalized: bool = True)
LegendreBasis1D.basis_dim -> int  # max_degree + 1
LegendreBasis1D.evaluate(points: tf.Tensor) -> tf.Tensor
LegendreBasis1D.derivative(points: tf.Tensor) -> tf.Tensor
LegendreBasis1D.mass_matrix(measure: MassMeasure) -> tf.Tensor
LegendreBasis1D.integral_vector(measure: MassMeasure) -> tf.Tensor
ProductBasis(bases: Sequence[LegendreBasis1D], convention: MeasureConvention)
ProductBasis.evaluate_axis(axis: int, points: tf.Tensor) -> tf.Tensor
```

Pinned Legendre convention:

For \(x\in[a,b]\), \(\xi=2(x-a)/(b-a)-1\).  Under the uniform probability
reference measure \(d\nu(x)=dx/(b-a)\),

```text
psi_n(x) = sqrt(2 n + 1) P_n(xi),  n = 0,...,max_degree.
```

Then

```text
integral psi_n(x) psi_m(x) dnu(x) = delta_nm
integral psi_0(x) dnu(x) = 1
integral psi_n(x) dnu(x) = 0  for n > 0
integral psi_n(x) psi_m(x) dx = (b-a) delta_nm
d psi_n / dx = sqrt(2 n + 1) P'_n(xi) * 2/(b-a).
```

Required TT symbols and signatures:

```text
TTCore(values: tf.Tensor)  # shape [rank_left, basis_dim, rank_right]
FunctionalTT(
    cores: Sequence[TTCore],
    product_basis: ProductBasis,
    measure_convention: MeasureConvention,
    branch_identity: BranchIdentity | None = None,
)
FunctionalTT.rank_tuple() -> tuple[int, ...]
FunctionalTT.basis_dim_tuple() -> tuple[int, ...]
FunctionalTT.evaluate(points: tf.Tensor) -> tf.Tensor
FunctionalTT.integrate_all(measure: MassMeasure | None = None) -> tf.Tensor
FunctionalTT.contract_axes(integrate_axes: Sequence[int]) -> object
FunctionalTT.manifest_payload() -> Mapping[str, object]
```

Shape contract:

```text
points: [n_points, dimension]
core[k].values: [r_k, p_k, r_{k+1}]
r_0 = r_D = 1
evaluate(points): [n_points]
```

Pinned vector/matrix evaluation equation:

```text
H_k(z_{i,k})[a,b] = sum_l C_k[a,l,b] psi_{k,l}(z_{i,k})
v_{i,0} = [1]
v_{i,k+1} = v_{i,k} H_k(z_{i,k})
f(z_i) = v_{i,D}[0]
```

Complexity gate must compute estimated elements and bytes before any dense
product-basis or dense contraction allocation.

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

Exit: every basis and TT object has unambiguous degree, mass, dtype, rank, and
evaluation semantics.

## Phase 2 Hardening: Squared Density And Transport

The hardened Phase 2 spec must state exactly how a square-root TT becomes a
normalized density and how KR conditionals are computed.

Required write set:

```text
bayesfilter/highdim/squared_tt.py
bayesfilter/highdim/transport.py
bayesfilter/highdim/diagnostics.py
tests/highdim/test_squared_tt_density.py
tests/highdim/test_transport.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase2*result*.md
```

Required symbols:

```text
DefensiveDensityProtocol
TensorProductReferenceDensity
SquaredTTDensity
SquaredTTDiagnostics
KRCDFConfig
KRTransport
KRInversionResult
```

Required signatures:

```text
DefensiveDensityProtocol.log_density(points: tf.Tensor) -> tf.Tensor
DefensiveDensityProtocol.normalizer(measure: MassMeasure) -> tf.Tensor
DefensiveDensityProtocol.manifest_payload() -> Mapping[str, object]

TensorProductReferenceDensity(
    product_basis: ProductBasis,
    measure_convention: MeasureConvention,
    floor: tf.Tensor = tf.constant(0.0, dtype=tf.float64),
)

SquaredTTDiagnostics(
    status: HighDimStatus,
    normalizer: tf.Tensor,
    square_mass: tf.Tensor,
    defensive_mass: tf.Tensor,
    tau: tf.Tensor,
    floor_count: int,
    branch_hash: str,
    extra: Mapping[str, object] = MappingProxyType({}),
)

KRCDFConfig(
    grid_size: int,
    bisection_steps: int,
    monotonicity_tolerance: float,
    bracket_tolerance: float,
    denominator_floor: float,
    max_floor_count: int,
    dtype: tf.DType = tf.float64,
)

KRInversionResult(
    z_value: tf.Tensor,       # [N] for one coordinate
    cdf_value: tf.Tensor,     # [N]
    iterations: int,
    status: HighDimStatus,
    diagnostics: Mapping[str, object],
)

KRTransport(
    density: SquaredTTDensity,
    coordinate_order: tuple[int, ...],
    cdf_config: KRCDFConfig,
)
KRTransport.forward(z_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor, tuple[KRInversionResult, ...]]
KRTransport.inverse(u_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor, tuple[KRInversionResult, ...]]
KRTransport.log_jacobian(z_points: tf.Tensor) -> tf.Tensor
```

Shape contract:

```text
z_points: [N,D]
u_points: [N,D], with entries in [0,1]
forward returns (u_points, log_abs_det_dF_dz, per_axis_results)
inverse returns (z_points, log_abs_det_dz_dF, per_axis_results)
log_jacobian returns [N]
```

Required `SquaredTTDensity` signature:

```text
SquaredTTDensity(
    sqrt_tt: FunctionalTT,
    defensive_density: DefensiveDensityProtocol,
    tau: tf.Tensor,
    normalizer_floor: tf.Tensor,
    denominator_floor: tf.Tensor,
    measure_convention: MeasureConvention,
    branch_identity: BranchIdentity,
)
```

Pinned equations:

```text
q_u(z) = h(z)^2 + tau q_0(z)
Z = integral q_u(z) dM(z)
q(z) = q_u(z) / Z
```

For the square term,

```text
M_k[l,m] = integral psi_{k,l}(z_k) psi_{k,m}(z_k) dM_k(z_k)
G_k[(a,a'),(b,b')] =
  sum_{l,m} C_k[a,l,b] C_k[a',m,b'] M_k[l,m]
Z_h = contract(G_1,...,G_D)
Z = Z_h + tau Z_0.
```

Required methods and shapes:

```text
unnormalized_density(points: tf.Tensor) -> tf.Tensor  # [N,D] -> [N]
normalizer() -> tf.Tensor  # scalar
log_density(points: tf.Tensor) -> tf.Tensor  # [N]
marginal_density(keep_axes: Sequence[int]) -> object
conditional_density(axis: int, prefix: tf.Tensor, grid: tf.Tensor) -> tf.Tensor
```

KR transport equations:

```text
u_j = F_j(z_j | z_{<j})
F_j(s | z_{<j}) = integral_{lower_j}^{s} q(z_j | z_{<j}) dM_j(z_j)
z_j = F_j^{-1}(u_j | z_{<j})
log |det dF/dz| = sum_j log q(z_j | z_{<j})
```

Required CDF/inversion contract:
- bracketed bisection is the first accepted inverse method;
- Newton refinement is optional and cannot replace bisection tests;
- CDF monotonicity failure, bracket failure, and nonfinite density are vetoes;
- floor usage is recorded and becomes a veto above a declared count/size.
- exact statuses are `CDF_MONOTONICITY_FAILURE`,
  `INVERSE_BRACKET_FAILURE`, `CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED`, and
  `NONFINITE_VALUE`.

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

Exit: density, marginal, conditional, and transport routines all preserve the
measure contract and branch identity.

## Phase 3 Hardening: Fixed-Branch Fitting

The hardened Phase 3 spec must make alternating least squares executable and
auditable.

Required write set:

```text
bayesfilter/highdim/fitting.py
bayesfilter/highdim/fixed_branch.py
bayesfilter/highdim/validation.py
tests/highdim/test_fixed_branch_fit.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase3*result*.md
```

Required symbols:

```text
FixedTTFitConfig
FixedTTFitSampleBatch
FixedTTFitResult
CoreUpdateDiagnostics
SweepDiagnostics
FixedDesignBuilder
FixedTTFitter
```

Required signatures and fields:

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
    points: tf.Tensor,        # [N,D]
    target_values: tf.Tensor, # [N]
    weights: tf.Tensor,       # [N]
    holdout_points: tf.Tensor | None,
    holdout_values: tf.Tensor | None,
    holdout_weights: tf.Tensor | None,
)

FixedTTFitter.fit(
    product_basis: ProductBasis,
    samples: FixedTTFitSampleBatch,
    config: FixedTTFitConfig,
    initial_cores: Sequence[TTCore],
    branch_seed: int | str,
    measure_convention: MeasureConvention,
) -> FixedTTFitResult
```

Pinned environment equations for core \(j\):

```text
H_{i,k}[a,b] = sum_l C_k[a,l,b] psi_{k,l}(z_{i,k})
L_{i,0} = [1]
L_{i,j} = L_{i,j-1} H_{i,j-1}
R_{i,D} = [1]
R_{i,j+1} = H_{i,j+1} R_{i,j+2}
```

Pinned design-row vectorization:

```text
A_j[i, index(a,l,b)] = L_{i,j}[a] psi_{j,l}(z_{i,j}) R_{i,j+1}[b]
index(a,l,b) = ((a * p_j) + l) * r_{j+1} + b
A_j shape = [N, r_j p_j r_{j+1}]
```

Pinned solve:

```text
N_j = A_j^T W A_j + rho I
d_j = A_j^T W y
c_j = solve(N_j, d_j)
C_j = unvec(c_j, [r_j,p_j,r_{j+1}])
```

After every accepted core update, all later environment tensors must be
recomputed from the current cores before the next core update.  The hardened
spec must forbid stale environment reuse unless a test proves the cached value
is invalidated and rebuilt.

Branch manifest must include:

```text
product_basis fields
measure_convention
sample points, target values hash, weights, holdout hash
ranks, ridge, dtype, sweep_order, max_sweeps
initial core hash and initialization rule
each realized core update status
condition estimates and stabilization choices
complexity budgets and gates
solver backend and deterministic seed
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

Exit: fixed-design fitting has exact shapes, deterministic replay, branch
hashes, complexity gates, and no adaptive derivative claim.

## Phase 4 Hardening: Filtering Value Path

The hardened Phase 4 spec must state the full scalar value path and retained
filter storage policy.

Required write set:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/filtering.py
bayesfilter/highdim/validation.py
tests/highdim/test_filtering_kalman_exact.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase4*result*.md
```

Required symbols:

```text
TFHighDimStateSpaceModel(Protocol)
HighDimCoordinateMap(Protocol)
FixedBranchFilterConfig
RetainedFilter
AdjacentTargetBatch
FixedBranchFilterStepResult
FixedBranchFilterResult
FixedBranchSquaredTTFilter
```

Required signatures:

```text
HighDimCoordinateMap.forward(reference_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]
HighDimCoordinateMap.inverse(physical_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]
HighDimCoordinateMap.manifest_payload() -> Mapping[str, object]
```

`forward` returns physical points and log absolute Jacobian determinant.  The
default initial implementation should support only parameter-independent maps.

```text
FixedBranchFilterConfig(
    fit_config: FixedTTFitConfig,
    density_tau: float,
    normalizer_floor: float,
    denominator_floor: float,
    retained_storage_byte_budget: int,
    coordinate_maps: tuple[HighDimCoordinateMap, ...],
    measure_convention: MeasureConvention,
    deterministic_seed: int,
    dtype: tf.DType = tf.float64,
)

RetainedFilter(
    density: SquaredTTDensity,
    retained_axes: tuple[int, ...],
    retained_coordinate_names: tuple[str, ...],
    measure_convention: MeasureConvention,
    normalizer: tf.Tensor,
    branch_identity: BranchIdentity,
    storage_kind: Literal["squared_tt", "contracted_tt"],
    diagnostics: Mapping[str, object],
)

AdjacentTargetBatch(
    time_index: int,
    physical_points: tf.Tensor,    # [N, P + 2 d_x] or [N, P + d_x] at t=0
    reference_points: tf.Tensor,   # [N, D_t]
    log_target: tf.Tensor,         # [N]
    sqrt_target: tf.Tensor,        # [N]
    weights: tf.Tensor,            # [N]
    measure_convention: MeasureConvention,
    retained_filter_hash: str | None,
)

FixedBranchFilterStepResult(
    time_index: int,
    fit_result: FixedTTFitResult,
    density: SquaredTTDensity,
    log_normalizer: tf.Tensor,
    retained_filter: RetainedFilter,
    branch_identity: BranchIdentity,
    status: HighDimStatus,
    diagnostics: Mapping[str, object],
)

FixedBranchFilterResult(
    log_likelihood: tf.Tensor,
    retained_filter: RetainedFilter,
    steps: tuple[FixedBranchFilterStepResult, ...],
    branch_identity: BranchIdentity,
    status: HighDimStatus,
    diagnostics: Mapping[str, object],
)

FixedBranchSquaredTTFilter(config: FixedBranchFilterConfig)
FixedBranchSquaredTTFilter.log_likelihood(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observations: tf.Tensor,
    initial_branch: BranchIdentity | None = None,
) -> FixedBranchFilterResult
```

Required model protocol signatures:

```text
parameter_dim(self) -> int
state_dim(self) -> int
observation_dim(self) -> int
initial_log_density(theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor
transition_log_density(theta: tf.Tensor, x_prev: tf.Tensor, x_next: tf.Tensor, t: int) -> tf.Tensor
observation_log_density(theta: tf.Tensor, x_t: tf.Tensor, y_t: tf.Tensor, t: int) -> tf.Tensor
```

Shape convention:

```text
theta: [N,P] or [P] with documented broadcasting
x_prev, x_next: [N,d_x] or [d_x]
y_t: [d_y]
log_density returns [N]
adjacent physical block r_t = concat(theta, x_prev, x_t): [N, P + 2 d_x]
reference block z_t: [N, D_t]
```

Pinned target equations:

For \(t=0\),

```text
gamma_0(theta,x_0) = prior(theta) p_theta(x_0) g_theta(y_0 | x_0).
```

For \(t\ge 1\),

```text
gamma_t(theta,x_{t-1},x_t)
 = retained_{t-1}(theta,x_{t-1})
   f_theta(x_t | x_{t-1})
   g_theta(y_t | x_t).
```

If \(r=\Psi_t(z)\), the reference-measure target is

```text
gamma_t^nu(z) =
  gamma_t(Psi_t(z)) |det D Psi_t(z)| / omega_t(z).
```

The step normalizer is \(Z_t=\int gamma_t^nu(z)d\nu_t(z)\).  The accumulated
scalar is \(\hat ell(theta)=\sum_t \log Z_t\), plus only explicitly declared
constant offsets.

Retained-filter storage:
- retain a marginal object over \((theta,x_t)\), not a dense product-basis
  matrix by default;
- store retained coordinate indices, coordinate names, basis objects, measure
  convention, normalizer, branch identity, and contraction diagnostics;
- for multi-dimensional retained \(z_t\), store the retained marginal as a
  `SquaredTTDensity` or contracted TT representation with integrated axes
  recorded;
- refuse full dense product-basis storage if estimated bytes exceed budget;
- next-step target must assert that the retained filter's measure convention
  matches the next adjacent target contract.

Required exact fixtures:

```text
scalar one-step linear-Gaussian evidence
scalar two-step linear-Gaussian evidence and filtering mean/variance
small multivariate linear-Gaussian evidence and marginal mean/covariance
non-identity affine physical-to-reference map with non-uniform reference density
scalar nonlinear observation with dense quadrature oracle
```

Pinned Phase 4 fixture table:

```text
fixture_scalar_lgssm_one_step:
  model:
    x0 ~ N(0, 1)
    y0 | x0 ~ N(x0, 0.09)
  observations: [0.2]
  expected_log_evidence: -0.980376005178410
  expected_filter_mean: 0.183486238532110
  expected_filter_variance: 0.082568807339450
  tolerance: abs <= 2e-10 for direct fixture, abs <= 2e-6 for TT path

fixture_scalar_lgssm_two_step:
  model:
    x0 ~ N(0, 1)
    x1 = 0.7 x0 + eta1, eta1 ~ N(0, 0.25)
    yt | xt ~ N(xt, 0.09)
  observations: [0.2, -0.1]
  expected_log_evidence: -1.484707421612687
  expected_filter_mean_t1: -0.045960935616108
  expected_filter_variance_t1: 0.068709910778876
  tolerance: abs <= 2e-10 for direct fixture, abs <= 5e-6 for TT path

fixture_fd_grid_default:
  finite_difference_h: [1e-2, 3e-3, 1e-3, 3e-4]
  branch_hash_equality: exact string equality

fixture_seed_default:
  deterministic_seed: 1701
```

For multivariate Kalman and non-identity reference fixtures, the hardened Phase
4 subplan must include the exact matrices and expected evidence/moments before
implementation starts.  P36 permits those to be generated from an independent
closed-form test fixture, but the generated values must be checked into the
phase result ledger before production code can pass.

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

Exit: the value path matches exact references and carries retained filters
under the correct measure before any derivative or stress claim.

## Phase 5 Hardening: Fixed-Branch Derivatives

The hardened Phase 5 spec must be more explicit than P35.  It must
differentiate the realized fixed-branch scalar, including environment changes
inside a fixed alternating-sweep replay.  It must not differentiate adaptive
branch choices.

Required write set:

```text
bayesfilter/highdim/derivatives.py
bayesfilter/highdim/filtering.py
bayesfilter/highdim/fitting.py
bayesfilter/highdim/validation.py
tests/highdim/test_fixed_branch_derivatives.py
tests/highdim/test_failure_exits.py
docs/plans/*p35-phase5*result*.md
```

Required symbols:

```text
FixedBranchDerivativeConfig
FixedBranchReplayTape
CoreDerivativeState
SweepDerivativeDiagnostics
FixedBranchScoreResult
FiniteDifferenceRow
FiniteDifferenceTable
```

Required signatures:

```text
FixedBranchDerivativeConfig(
    parameter_indices: tuple[int, ...],
    finite_difference_h: tuple[float, ...] = (1e-2, 3e-3, 1e-3, 3e-4),
    derivative_ridge_floor: float = 1e-12,
    solve_condition_number_veto: float = 1e12,
    allow_parameter_dependent_coordinate_map: bool = False,
    allow_moving_basis: bool = False,
    dtype: tf.DType = tf.float64,
)

CoreDerivativeState(
    core_index: int,
    core: TTCore,
    dot_core: tf.Tensor,       # [r_j,p_j,r_{j+1}]
    pre_update_core_hash: str,
    post_update_core_hash: str | None,
)

SweepDerivativeDiagnostics(
    time_index: int,
    sweep_index: int,
    sweep_direction: Literal["forward", "reverse"],
    core_index: int,
    status: HighDimStatus,
    condition_number: tf.Tensor,
    normal_matrix_hash: str,
    rhs_hash: str,
    coefficient_hash: str,
    environment_provenance: Mapping[str, object],
)

FixedBranchReplayTape(
    version: str,
    branch_identity: BranchIdentity,
    entries: tuple[Mapping[str, object], ...],
)
FixedBranchReplayTape.manifest_payload() -> Mapping[str, object]
FixedBranchReplayTape.assert_matches_branch(branch_identity: BranchIdentity) -> None

FixedBranchScoreResult(
    log_likelihood: tf.Tensor,
    score: tf.Tensor,          # [P] or selected parameter shape
    branch_identity: BranchIdentity,
    replay_tape_hash: str,
    finite_difference_table: "FiniteDifferenceTable | None",
    status: HighDimStatus,
    diagnostics: Mapping[str, object],
)

FiniteDifferenceRow(
    parameter_index: int,
    h: float,
    value_plus: tf.Tensor,
    value_minus: tf.Tensor,
    branch_hash_plus: str,
    branch_hash_minus: str,
    branch_hash_base: str,
    centered_difference: tf.Tensor,
    analytic_gradient: tf.Tensor,
    abs_error: tf.Tensor,
    rel_error: tf.Tensor,
    row_status: HighDimStatus,
)

FiniteDifferenceTable(rows: tuple[FiniteDifferenceRow, ...])
FiniteDifferenceTable.valid_rows() -> tuple[FiniteDifferenceRow, ...]
FiniteDifferenceTable.max_abs_error() -> tf.Tensor
```

Same-scalar contract:

```text
ell_hat(theta; B, y_0:T)
```

where `B` is the full realized branch manifest.  The derivative evaluation may
reuse only objects fixed in `B`: sample points, ranks, basis definitions,
coordinate maps unless explicitly declared parameter-dependent, sweep order,
ridge policy, floors, defensive density, solver choices, and retained-storage
policy.  Adaptive rank, pivot, basis, coordinate-map selection, branch
failure/success decisions, and sample-set changes are outside scope.

Phase 5 branch manifest fields:

```text
manifest_version
observation_hash
time_indices
theta_shape_and_dtype
retained_filter_hashes
retained_axes_and_order
coordinate_map_identity
coordinate_map_parameter_dependent: bool
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
replay_tape_hash
replay_tape_version
```

Missing any field is a `BRANCH_HASH_MISSING` or `REPLAY_TAPE_MISMATCH` veto,
depending on whether the missing field is in the branch manifest or replay
tape.

Replay tape entry schema:

```text
time_index
initial_core_hashes
initial_dot_core_hashes
initialization_rule
initial_dot_core_policy
sweep_index
sweep_direction
core_index
pre_update_core_hash
post_update_core_hash
update_status
sample_points_hash
target_values_hash
target_derivative_values_hash
weights_hash
environment_provenance
left_environment_hash
right_environment_hash
design_matrix_hash
normal_matrix_hash
rhs_hash
coefficient_hash
derivative_coefficient_hash
```

Replay algorithm:

```text
for each time step t in realized branch order:
  load retained filter and branch objects recorded for t
  initialize current cores C from branch.initial_core_hashes and initialization_rule
  initialize derivative cores dot C from initial_dot_core_policy
  assert initialized core hashes match initial_core_hashes
  assert initialized derivative core hashes match initial_dot_core_hashes
  for each sweep s in realized sweep order:
    if sweep_direction == "forward":
      core_order = (0, 1, ..., D-1)
    else:
      core_order = (D-1, D-2, ..., 0)

    for each core index j in core_order:
      assert current C_j hash == replay.pre_update_core_hash
      rebuild L and dot L from current cores left of j
      rebuild R and dot R from current cores right of j
      build A_j, dot A_j, N_j, dot N_j, d_j, dot d_j
      solve for c_j and dot c_j
      assert c_j hash == replay.coefficient_hash
      update C_j and dot C_j
      assert updated C_j hash == replay.post_update_core_hash
      invalidate cached environments touching any axis >= j in forward sweeps
      invalidate cached environments touching any axis <= j in reverse sweeps
```

Pre-update/post-update semantics:
- \(L_{i,j}\), \(R_{i,j+1}\), \(A_j\), \(N_j\), and \(d_j\) are built from the
  current core list immediately before the core \(j\) update;
- the current core list includes all accepted prior updates in the same sweep;
- in a reverse sweep, right environments therefore use post-update right-side
  cores from earlier reverse-sweep updates;
- rejected updates must leave both \(C_j\) and \(\dot C_j\) unchanged and must
  record `update_status`;
- stale environment cache use is a `REPLAY_ENVIRONMENT_STALE` veto.
- initial derivative cores must be zero when the initialization rule is
  parameter-independent, must be differentiated when the initializer is
  declared parameter-dependent, and otherwise must raise
  `UNSUPPORTED_MOVING_BASIS_DERIVATIVE` or `REPLAY_TAPE_MISMATCH` before the
  first core update.

Pinned sweep derivative equations:

Let \(C_k\) be the current core and \(\dot C_k=\partial C_k/\partial\theta_m\)
for one parameter component.  With fixed basis points,

```text
H_{i,k}[a,b] = sum_l C_k[a,l,b] psi_{k,l}(z_{i,k})
dot H_{i,k}[a,b] = sum_l dot C_k[a,l,b] psi_{k,l}(z_{i,k})
```

If a reviewed future branch allows parameter-dependent fixed coordinate maps,
then the hardened spec must add the basis term

```text
sum_l C_k[a,l,b] dot psi_{k,l}(z_{i,k})
```

and must test \(\dot A\) with moving basis values.  The initial implementation
should set this path to unsupported.

Environment derivatives:

```text
L_{i,0} = [1],       dot L_{i,0} = [0]
L_{i,j} = L_{i,j-1} H_{i,j-1}
dot L_{i,j} = dot L_{i,j-1} H_{i,j-1} + L_{i,j-1} dot H_{i,j-1}

R_{i,D} = [1],       dot R_{i,D} = [0]
R_{i,j} = H_{i,j} R_{i,j+1}
dot R_{i,j} = dot H_{i,j} R_{i,j+1} + H_{i,j} dot R_{i,j+1}
```

Design-row derivative for core \(j\):

```text
A_j[i,index(a,l,b)] = L_{i,j}[a] psi_{j,l}(z_{i,j}) R_{i,j+1}[b]

dot A_j[i,index(a,l,b)] =
  dot L_{i,j}[a] psi_{j,l}(z_{i,j}) R_{i,j+1}[b]
  + L_{i,j}[a] psi_{j,l}(z_{i,j}) dot R_{i,j+1}[b]
```

Add the \(\dot\psi\) term only for a separately reviewed moving-basis branch.

Normal equation derivative:

```text
N_j = A_j^T W A_j + rho I
d_j = A_j^T W y
c_j = solve(N_j, d_j)

dot N_j =
  dot A_j^T W A_j + A_j^T W dot A_j
  + A_j^T dot W A_j + dot rho I

dot d_j =
  dot A_j^T W y + A_j^T W dot y + A_j^T dot W y

dot c_j = solve(N_j, dot d_j - dot N_j c_j)
```

Initial fixed-branch default: \(W\) and \(\rho\) are fixed, so
\(\dot W=0\) and \(\dot\rho=0\).  The equations must still appear in the spec
so future implementation does not confuse "fixed branch" with "fixed design
matrix after earlier cores have changed."

TT evaluation derivative:

```text
dot f(z_i) = sum_j L_{i,j} dot H_{i,j} R_{i,j+1}
```

Squared-density normalizer:

```text
Z = integral h(z)^2 dM(z) + tau Z_0
dot Z = 2 integral h(z) dot h(z) dM(z) + dot tau Z_0 + tau dot Z_0
dot log Z = dot Z / Z
```

Initial default: \(\dot\tau=0\), \(\dot Z_0=0\), unless explicitly declared in
the branch.

Retained-filter quotient derivative:

```text
m_t(a) = integral q_t(a,b) dM_b
retained_t(a) = m_t(a) / Z_t
dot retained_t(a) =
  dot m_t(a) / Z_t - m_t(a) dot Z_t / Z_t^2.
```

The next target derivative must include both the primitive model derivative and
the derivative of the carried retained filter:

```text
dot gamma_t =
  dot retained_{t-1} f g
  + retained_{t-1} dot f g
  + retained_{t-1} f dot g.
```

Finite-difference table schema:

```text
parameter_index
h
branch_hash_plus
branch_hash_minus
branch_hash_base
D(h) = [ell(theta+h e_m; B_plus) - ell(theta-h e_m; B_minus)]/(2h)
G_m = analytic fixed-branch derivative
abs_error
rel_error
row_status
```

Rows with nonidentical branch hashes are
`FINITE_DIFFERENCE_BRANCH_MISMATCH`; they are not derivative successes and not
derivative failures.

Pinned Phase 5 fixture and tolerance table:

```text
fixture_scalar_lgssm_transition_score:
  same model as fixture_scalar_lgssm_two_step
  differentiated parameter: transition coefficient A
  A_base: 0.7
  observations: [0.2, -0.1]
  expected_score_dell_dA: -0.241250978551728
  direct_reference_tolerance: abs <= 2e-10
  fixed_branch_tt_tolerance: abs <= 2e-5

fixture_scalar_lgssm_one_step_prior_mean_score:
  model:
    x0 ~ N(mu0, 1)
    y0 | x0 ~ N(x0, 0.09)
  mu0_base: 0.0
  observation: [0.2]
  expected_log_evidence: -0.980376005178410
  expected_score_dell_dmu0: 0.183486238532110
  derivation: (y0 - mu0) / (1 + 0.09)
  direct_reference_tolerance: abs <= 2e-10
  fixed_branch_tt_tolerance: abs <= 2e-5

fixture_scalar_nonlinear_dense_quadrature_score:
  model:
    x0 ~ N(0, 1)
    y0 | x0, theta ~ N(theta sin(x0), 0.25)
  theta_base: 0.4
  observation: [0.1]
  dense_oracle: Gauss-Hermite quadrature with at least 120 nodes
  expected_log_evidence: -0.373000101795619
  expected_score_dell_dtheta: -0.608378439103854
  oracle_stability_check: 80, 120, and 160 node values agree within 1e-9
  direct_reference_tolerance: abs <= 5e-10
  fixed_branch_tt_tolerance: abs <= 5e-5

fixture_fixed_ls_derivative:
  points: [[-1.0], [0.0], [1.0]]
  weights: [1.0, 1.0, 1.0]
  basis: normalized Legendre max_degree 1 on [-1,1]
  target(theta, x): theta * (1 + 0.5 x)
  theta_base: 2.0
  ridge: 1e-10
  finite_difference_h: [1e-2, 3e-3, 1e-3, 3e-4]
  expected_branch_hash_rule: exact equality for base/plus/minus
  coefficient_derivative_tolerance: abs <= 2e-8

fixture_normalizer_derivative:
  h_theta(z) = 1 + theta z on z in [-0.5,0.5]
  theta_base: 0.2
  reference_measure: uniform probability
  Z(theta) = 1 + theta^2 / 12
  dlogZ(theta) = (theta / 6) / Z(theta)
  tolerance: abs <= 2e-10 for analytic contraction, abs <= 2e-6 for TT path

fixture_fd_rows:
  h_grid: [1e-2, 3e-3, 1e-3, 3e-4]
  valid_row_abs_error: <= 2e-5 for scalar LGSSM score
  valid_row_rel_error: <= 2e-4 unless |G| < 1e-8
  branch_hash_equality: exact string equality
  branch_mismatch_status: FINITE_DIFFERENCE_BRANCH_MISMATCH
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

Exit: value and score are for the same fixed branch, exact score baselines pass,
and finite-difference evidence is invalid unless branch hashes agree.

## Phase 6 Hardening: Stress Models And Performance Ladder

The hardened Phase 6 spec must be an experiment-ready benchmark plan, not a
list of aspirations.

Required write set:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/validation.py
tests/highdim/test_scaling_smoke.py
docs/plans/*p35-phase6*stress-plan*.md
docs/plans/*p35-phase6*result*.md
```

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

Linear-Gaussian:

```text
x_0 ~ N(m0,P0)
x_t = A_theta x_{t-1} + b_theta + eta_t,  eta_t ~ N(0,Q_theta)
y_t = H_theta x_t + c_theta + eps_t,      eps_t ~ N(0,R_theta)
```

Stochastic volatility:

```text
x_0 ~ N(mu, sigma^2/(1-phi^2))
x_t = mu + phi (x_{t-1}-mu) + sigma eta_t
y_t | x_t ~ N(0, beta^2 exp(x_t))
```

SIR in log or constrained coordinates must specify whether the state is
physical constrained \((S,I,R)\), log-transformed, or simplex-transformed, and
must state the transition and observation distributions before execution.

Predator-prey is blocked until the positive-state coordinate policy and
observation likelihood are specified.

Required manifest fields:

```text
git commit
command
conda/env name
CPU/GPU status and whether GPU command was escalated
random seed list
dtype
model name and equations
dimension/rank/degree/horizon grid
row/column/normal-matrix budgets
expected memory model and measured peak memory if available
wall time
exact-reference error when available
fit and holdout residuals
normalizer and CDF diagnostics
branch hash and deterministic replay status
decision status
what is not concluded
```

Required scaling grids:

```text
LGSSM exact ladder:
  state_dim: 1, 2, 4, 8
  parameter_dim: 0, 1, 2
  horizon: 1, 2, 5, 10
  rank: 1, 2, 4, 8
  max_degree: 1, 2, 4

SV tiny-reference ladder:
  horizon: 1, 2, 5
  rank: 1, 2, 4
  max_degree: 2, 4
```

GPU commands must follow `AGENTS.md`: detection, initialization, benchmarks, or
GPU TensorFlow runs require escalated/trusted execution.  Deliberate CPU-only
runs must hide GPUs before framework import and record that choice.

Required tests and artifacts:

```text
test_scaling_smoke_lgssm_runs_tiny_grid_with_finite_diagnostics
test_scaling_smoke_blocks_when_phase0_to_phase5_regression_flag_is_set
test_scaling_manifest_requires_resource_and_replay_fields
test_stress_status_separates_tuning_approximation_resource_failures
```

Exit: no stress claim can override failed Phase 0--5 exact gates.  DSGE trials
remain blocked until a Phase 6 result ledger records a defensible operating
envelope.

## Phase 7 Hardening: Public API Decision

The hardened Phase 7 spec must make API exposure a reviewed decision, not a
side effect of implementation.

Required write set only if Phase 7 explicitly approves API exposure:

```text
bayesfilter/__init__.py
bayesfilter/highdim/__init__.py
tests/test_v1_public_api.py
tests/highdim/test_public_api_highdim.py
docs/plans/*p35-phase7*result*.md
```

Required API decision statuses:

```text
KEEP_INTERNAL
EXPERIMENTAL_SUBPACKAGE_ONLY
STABLE_TOP_LEVEL_API
BLOCKED_UNRESOLVED_VALIDATION
BLOCKED_UNSTABLE_BRANCH_CONTRACT
```

Candidate public symbols, if and only if stable exposure is approved:

```text
TFFixedBranchSquaredTTFilterConfig
TFFixedBranchSquaredTTFilterResult
TFFixedBranchSquaredTTScoreResult
tf_fixed_branch_squared_tt_log_likelihood
tf_fixed_branch_squared_tt_score
```

Names must contain `fixed_branch` or equivalent scope language.  Documentation
must state:

```text
measure convention
fixed-branch scalar definition
branch manifest and hash role
exact small-model validation status
stress-model validation status
failure exits
non-claims about adaptive derivatives and exact nonlinear likelihood
```

Required API tests:

```text
test_existing_v1_public_api_symbols_preserved
test_no_highdim_top_level_symbols_before_phase7_option_c
test_experimental_subpackage_import_is_explicit_only
test_stable_public_symbols_include_fixed_branch_scope_language
test_public_docs_do_not_claim_adaptive_derivative
```

Exit: API exposure is blocked unless prior result ledgers pass with no
unresolved blocker and the public surface accurately communicates fixed-branch
scope.

## Claude Review Protocol

Run Claude as a bounded hostile reviewer with this command pattern:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p36-subplan-hardening-review-iter<N> \
  --model sonnet \
  --effort high \
  "<prompt>"
```

Maximum iterations: 5.

Claude must check:
- whether P36 actually hardens P35 or remains broad;
- whether each phase has implementation-ready details;
- whether Phase 5 derivative equations correctly cover alternating-sweep
  environment derivatives;
- whether exact tests and failure exits are specific enough to prevent
  ambiguous implementation;
- whether any backend, branch, measure, API, clean-room, or DSGE guardrail is
  weakened.

For every Claude finding, Codex must record one classification:

```text
ACCEPT
PARTIAL
DISPUTE
CLARIFY
```

Accepted or partially accepted findings must be patched in this P36 plan.
Disputed findings must receive a concise rebuttal in the ledger and, if another
Claude round is run, in the next prompt.  If unresolved disagreements remain
after five iterations, final acceptance is blocked.

## Validation For This P36 Artifact

Required commands:

```bash
git diff --check -- \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md

rg -n "metadata_date|seed_papers|what_is_not_concluded" \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md

git status --short -- \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-plan-2026-06-04.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-p36-subplan-hardening-claude-review-ledger-2026-06-04.md
```

Pass condition: only the two P36 files are created or modified by this task,
Claude review passes or no unresolved accepted blocker remains, metadata fields
exist, and whitespace validation passes.
