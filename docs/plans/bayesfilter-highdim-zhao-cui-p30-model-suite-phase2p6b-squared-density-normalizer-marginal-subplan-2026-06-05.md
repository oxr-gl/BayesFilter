# P37-M2.6b Subplan: Squared-Density Normalizer And Retained Marginal For Scalar SV Adjacent Targets

metadata_date: 2026-06-05
phase: P37-M2.6b

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md`

overnight_runbook:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-2026-06-05.md`

depends_on:
- P37-M2.5 scalar dense nonlinear value path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p5-nonlinear-value-path-result-2026-06-05.md`
- P37-M2.6a fixed-design TT SV adjacent target fitting:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md`

## Purpose

Convert the M2.6a fitted square-root functional TT into the squared-density
objects needed by the Zhao--Cui/P30 filtering construction, and validate the
normalizer and retained marginal against dense quadrature or exact one-axis
contractions on the same fixed scalar SV adjacent targets.

This phase tests the density-construction layer only.  It does not run a
sequential SV filter.

## Source-Governance Status

- P30 anchors identified:
  - square-mass contraction: `eq:p33-square-mass`;
  - mass matrix: `eq:p33-mass-matrix`;
  - mass recursion: `eq:p33-mass-recursion`;
  - mass finalization: `eq:p33-mass-final`;
  - density with floor: `eq:p33-density-with-floor`;
  - full normalizer: `eq:p33-full-normalizer`;
  - retained marginal: `eq:p33-retained-marginal`;
  - retained normalized density: `eq:p33-retained-normalized`.
- Zhao--Cui paper anchors identified: Eq. (13) and Lemma 1 for squared-TT
  defensive density and its normalizer; Proposition 2 and Eq. (14) for
  marginal density; Algorithm 1(c) and normalizing constant \(c_t\) for the
  filtering normalizer.  These anchors are cross-checked against
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md`.
- MATLAB behavioral anchors identified: `deep-tensor.dev/src/SIRT.m`;
  `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`;
  `deep-tensor.dev/src/@TTSIRT/marginalise.m`;
  `deep-tensor.dev/src/@TTIRT/marginalise.m`.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/squared_tt.py`,
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/fitting.py`,
  planned `tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`.
- Deviations listed: yes.  This is a BayesFilter fixed-design scalar density
  check, not MATLAB adaptive cross or full SIRT reproduction.
  Current `SquaredTTDensity.marginal_density` is metadata-only for marginal
  values and is insufficient for the M2.6b retained-density claim.  M2.6b must
  add a narrow BayesFilter-owned scalar retained-density evaluator or helper
  with direct tests against dense oracle values before it can promote retained
  marginal evidence.
- Clean-room boundary respected: yes.  MATLAB files are behavioral anchors
  only.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Fixed M2.6b Fixtures

M2.6b must reuse the exact passed M2.6a lineage:

```text
source_fixture_id = p37.m2p6a.sv.scalar.fixed-target.v1
source_fit_fixture_id = p37.m2p6a.sv.fixed-design-fit.degree64.v2
initial_target_id = p37.m2p6a.sv.initial.t0.v1
transition_target_id = p37.m2p6a.sv.transition.t1.v1
coordinate_map = AffineCoordinateMap(offset=[0.0], matrix=[[8.0]])
basis = normalized LegendreBasis1D(BoundedInterval(-1.0, 1.0), max_degree=64)
ranks = (1, 1)
scale_shift_convention = M2.6a target log_scale_shift, unchanged per target
retained_filter_for_transition = M2.6a retained dense filter after y_0,
  hash recorded in the M2.6b result ledger
```

M2.6b promotion fixtures:

```text
m2p6b_normalizer_audit_fixture_id =
  p37.m2p6b.sv.normalizer-audit.gl257.v1
normalizer_audit_grid = Gauss-Legendre order 257 on reference [-1,1]
normalizer_audit_weights = Gauss-Legendre probability weights

m2p6b_retained_density_audit_fixture_id =
  p37.m2p6b.sv.retained-density-audit.mid173.v1
retained_density_audit_grid =
  z_i = -1 + 2(i+0.25)/173, i=0,...,172
retained_density_audit_weights = uniform probability weights

tuning_only_grids =
  M2.6a Gauss-Legendre order 121 tuning holdout,
  M2.6a midpoint 149 promotion audit grid
```

The M2.6b promotion grids are intentionally distinct from the M2.6a training,
tuning, and audit grids.  Reusing M2.6a audit points is allowed only as an
explanatory replay check, not as M2.6b promotion evidence.

Defensive density fixture:

```text
defensive_density = TensorProductReferenceDensity(product_basis, convention)
tau_primary = 0.0
tau_auxiliary = 1e-12
floor_normalizer_under_reference_measure = 1.0
primary scientific promotion uses tau_primary
positive-tau behavior is auxiliary code-path evidence only
```

## Evidence Contract

Question: after M2.6a target fitting, can BayesFilter compute the squared-TT
normalizer and retained marginal for the fixed scalar SV adjacent targets in a
way that agrees with dense oracle integration?

Baseline/comparator:

- dense quadrature of the scaled square-root target from M2.6a;
- dense quadrature of reconstructed unnormalized target values;
- existing `SquaredTTDensity.sqrt_square_normalizer`,
  `SquaredTTDensity.normalizer`, and marginal/conditional diagnostics;
- M2.5 dense scalar retained filter for the transition target.

Primary pass criteria:

- square-mass normalizer from TT contraction agrees with dense quadrature on
  initial and transition M2.6a targets within predeclared absolute and relative
  tolerances;
- full defensive-floor normalizer agrees with dense formula
  `sqrt_square_normalizer + tau * floor_normalizer` for pinned `tau_primary=0`
  and auxiliary `tau_auxiliary=1e-12`;
- normalized retained density on the single retained axis agrees with dense
  normalized density values on the M2.6b retained-density audit grid;
- if the unnormalized retained marginal \(a_S(z)\) is reported, it is checked
  separately as \(a_S(z)=\widehat Z\,\widehat p_S(z)\) on the same grid;
- branch identity and density manifest replay under identical fixtures;
- broad M2.6a and highdim guardrails remain green.

Retained-density definition:

```text
promoted retained object = normalized retained density
  p_hat_S(z) from P30 eq:p33-retained-normalized
scalar 1D case = all axes retained, so p_hat_S(z) is the normalized
  squared-density over the reference coordinate
unnormalized retained marginal a_S(z) from eq:p33-retained-marginal is an
  explicit secondary check if reported
forbidden substitute = conditional_density(), pointwise normalized slice, or
  SquaredTTDensity.marginal_density metadata alone
```

Primary comparators:

```text
normalizer comparator =
  dense oracle integration of reconstructed scaled target values on
  p37.m2p6b.sv.normalizer-audit.gl257.v1
retained-density comparator =
  dense oracle normalized density values on
  p37.m2p6b.sv.retained-density-audit.mid173.v1, normalized by the dense
  normalizer comparator
TT one-axis contraction =
  explanatory cross-check only in scalar 1D unless separately reviewed
```

Initial tolerance policy:

```text
normalizer_abs_tol = 5e-5
normalizer_rel_tol = 5e-4
retained_density_linf_tol = 5e-3
retained_density_integral_abs_tol = 5e-4
```

These tolerances are planning values.  Claude may require tightening or a
fresh fixture before implementation.

Veto diagnostics:

- nonfinite square-root TT evaluation, squared density, normalizer, marginal,
  branch hash, or dense oracle value;
- density floor used to hide a poor fitted target without being declared;
- TT contraction and dense quadrature compare different measures or scales;
- retained marginal is normalized by a tuned or stale normalizer;
- retained-density evidence is supplied only by `conditional_density`,
  pointwise slice normalization, or metadata-only `marginal_density`;
- M2.6b changes M2.6a fixture IDs, target IDs, retained-filter hash,
  coordinate map, basis family/degree, rank, or log-scale-shift convention
  without a reviewed fixture-lineage amendment;
- M2.6b uses M2.6a tuning or audit grids as primary M2.6b promotion evidence;
- `tau`, defensive-density family, or floor normalizer differs from the pinned
  M2.6b fixture without reviewed amendment;
- M2.6a fixed target fit or replay guardrail regresses;
- any claim of sequential TT/SIRT filtering.

Explanatory-only diagnostics:

- fitted target residual, degree, rank, mass-matrix conditioning, audit-grid
  size, dense quadrature order, wall time, and memory.

What will not be concluded:

- no sequential SV log evidence;
- no adaptive TT-cross/MATLAB reproduction;
- no paper-scale `T=1000`;
- no derivative/HMC/DSGE/GPU readiness;
- no high-dimensional scalability claim.

Artifacts preserving result:

- result ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-result-2026-06-05.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-claude-review-ledger-2026-06-05.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW`.

The wrong baseline would be checking only `SquaredTTDensity.normalizer()` on a
toy constant TT, because that is already covered by existing unit tests and
does not validate the M2.6a SV target.  M2.6b must compare the fitted SV target
normalizer and retained density against dense oracle integration on fresh audit
points.

The main proxy risk is treating normalizer agreement for one adjacent target as
sequential evidence.  The phase blocks that claim explicitly and defers
evidence recursion to M2.6c.

The main hidden assumption is measure consistency: the TT contraction must use
the same reference measure, scaling, and coordinate-map convention as the dense
oracle.  Any mismatch is a veto rather than a tuning issue.

## Planned Implementation Tasks

1. Reuse the M2.6a fixed target-building fixtures and fitted TT outputs.
2. Construct `SquaredTTDensity` objects from the fitted square-root TT.
3. Compute square-mass normalizers by TT contraction.
4. Compute dense quadrature normalizers on an independent audit grid under the
   same scaled reference measure.
5. Add a narrow scalar retained-density evaluator or helper that evaluates
   the normalized retained density from the squared TT on all-retained scalar
   reference points; this helper may not delegate the promoted claim to
   `conditional_density` or metadata-only `marginal_density`.
6. Validate retained scalar density values and integral normalization on the
   M2.6b retained-density audit grid.
7. Add branch replay and manifest checks for the density construction.
8. Write the result ledger, Claude review ledger, and traceability update.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/filtering.py
bayesfilter/highdim/squared_tt.py
tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

Do not modify top-level public API exports.

## Planned Commands

Focused:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_squared_tt_density.py
```

Guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py
```

Compile:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
```
