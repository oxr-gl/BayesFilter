# P37-M2.6a Subplan: Fixed-Design TT Fitting For A Scalar SV Adjacent Target

metadata_date: 2026-06-05
phase: P37-M2.6a

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-remaining-phases-gated-execution-master-plan-2026-06-05.md`

## Purpose

Build the smallest source-governed bridge from the M2.5 scalar dense nonlinear
value path to actual functional TT approximation.  M2.6a fits square-root
functional TT approximations to fixed stochastic-volatility adjacent targets
and checks those approximations against independent dense oracle values.

This phase does not build the full sequential TT/SIRT filter.  It validates the
target-construction and fixed-design TT fitting piece that later phases will
compose into squared densities and retained filters.

## Source-Governance Status

- P30 anchors identified:
  - stochastic-volatility equations `eq:p27-sv1`--`eq:p27-sv10`;
  - adjacent-state target and retained normalization:
    `eq:p25-bridge-1`--`eq:p25-bridge-3`;
  - scalar fixed-branch adjacent target and target vector:
    `eq:p24-p22-o3`--`eq:p24-p22-o5`;
  - physical-to-reference pullback and reference-measure correction:
    `eq:p25-bridge-8`, `eq:p33-pullback-leb`,
    `eq:p33-pullback-nu`;
  - square-root fitting and squared-density reconstruction:
    `eq:p24-p22-o6`--`eq:p24-p22-o8`,
    `eq:p33-density-with-floor`, `eq:p33-full-normalizer`;
  - validation ladder near `Large-Scale Validation Models And Test Protocol`.
  M2.6a uses these exact labels for target fitting only and does not claim full
  Algorithm 5.
- Zhao--Cui paper anchors identified: stochastic-volatility benchmark section,
  functional TT approximation and squared-density/SIRT construction sections.
- MATLAB behavioral anchors identified: `eg2_sv/mainscript.m`;
  `deep-tensor.dev/src/@TTFun/TTFun.m`;
  `deep-tensor.dev/src/@TTFun/cross.m`;
  `deep-tensor.dev/src/SIRT.m`;
  `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/models.py`,
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/fitting.py`,
  `bayesfilter/highdim/bases.py`,
  planned `tests/highdim/test_p30_sv_fixed_design_tt_target.py`.
- Deviations listed: yes.  M2.6a is a `BAYESFILTER_EXTENSION` fixed-design
  clean-room fitting gate, not MATLAB adaptive cross reproduction.  The
  max-log scaling in `build_adjacent_target_batch`, branch-hash replay
  manifests, fixed fixture IDs, and heldout reconstruction checks are
  BayesFilter engineering extensions with BayesFilter code/test anchors.
- Clean-room boundary respected: yes.  MATLAB paths are behavioral anchors
  only; implementation will use existing BayesFilter fixed-design fitter.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Mathematical Target

Use the P30 synthetic transformed SV convention:

```text
theta' = (Phi^{-1}(gamma), log beta),      X'_t = X_t,
gamma in (0,1), beta > 0, sigma fixed.
```

The scalar model is:

```text
X_0 | theta ~ N(0, sigma^2 / (1-gamma^2)),
X_t | X_{t-1}, theta ~ N(gamma X_{t-1}, sigma^2),
Y_t | X_t, theta ~ N(0, beta^2 exp(X_t)).
```

M2.6a uses two fixed adjacent targets.

Initial target:

```text
g_0(x_0) = p_theta(x_0) p_theta(y_0 | x_0).
```

Transition target with a retained dense filter from M2.5:

```text
g_t(x_t) =
  p_theta(y_t | x_t)
  int p_theta(x_t | x_{t-1}) pi_{t-1}(x_{t-1}) dx_{t-1}.
```

The implementation target for fitting is the square-root function on a bounded
reference interval:

```text
h_t(z) = sqrt(g_t(T(z)) |det DT(z)| / omega(z))
```

where `T` is the declared scalar coordinate map and `omega` is the uniform
reference density used by the Legendre product basis.  The maximum-log scaling
used by `build_adjacent_target_batch` is allowed, but tests must compare the
same scaled target and record that scaling in diagnostics.

Traceability of this fitting target:

- `g_t` is the P30/paper adjacent filtering target specialized to the scalar SV
  equations.  General anchor: `eq:p25-bridge-1`; scalar fixed-branch anchor:
  `eq:p24-p22-o3`; retained/evidence anchor: `eq:p25-bridge-3`.
- `|det DT| / omega` is the reference-space density conversion required by the
  P30/P35 measure convention.  Lebesgue pullback anchor:
  `eq:p25-bridge-8` and `eq:p33-pullback-leb`; reference-measure correction
  anchor: `eq:p33-pullback-nu`.
- the square-root target is the squared-density/SIRT construction specialized
  to the fixed-design BayesFilter fitting lane.  Fitted value anchors:
  `eq:p24-p22-o5`, `eq:p24-p22-o6`, `eq:p24-p22-o8`; squared-density
  reconstruction anchors: `eq:p24-p22-o7`, `eq:p33-density-with-floor`, and
  `eq:p33-full-normalizer`.
- max-log scaling is not a Zhao--Cui mathematical claim; it is a
  `BAYESFILTER_EXTENSION` numerical stabilization.  Reconstruction tests must
  compare quantities under the same scale and record the shift.

## Fixed Fixtures

M2.6a uses the following deterministic fixtures.  Any change must be recorded
in the result ledger as a new fixture version, not silently substituted.

Common model fixture:

```text
fixture_id = p37.m2p6a.sv.scalar.fixed-target.v1
model = StochasticVolatilitySSM(sigma=1.0)
gamma = 0.6
beta = 0.4
theta = model.unconstrained_from_physical(gamma=0.6, beta=0.4)
observations = (0.12, -0.08, 0.05)
coordinate map = AffineCoordinateMap(offset=[0.0], matrix=[[8.0]])
reference domain = [-1,1], physical window approximately [-8,8]
fit quadrature order = 321 for retained dense filter construction
```

Initial target fixture:

```text
target_id = p37.m2p6a.sv.initial.t0.v1
time_index = 0
target = p_theta(x_0) p_theta(y_0 | x_0)
training nodes = Gauss-Legendre order 161 on reference [-1,1]
holdout nodes = Gauss-Legendre order 121 on reference [-1,1]
```

Transition target fixture:

```text
target_id = p37.m2p6a.sv.transition.t1.v1
time_index = 1
retained filter = M2.5 scalar dense retained filter after y_0
retained filter construction = FixedBranchSquaredTTFilter with the common
  model fixture, observations=(0.12,), coordinate map radius 8.0, order 321,
  seed="p37-m2p6a-retained-t0"
target = p_theta(y_1 | x_1) int p_theta(x_1 | x_0) pi_0(x_0) dx_0
training nodes = Gauss-Legendre order 161 on reference [-1,1]
holdout nodes = Gauss-Legendre order 121 on reference [-1,1]
```

Fitting fixture:

```text
fitting_fixture_id = p37.m2p6a.sv.fixed-design-fit.degree64.v2
failed_original_fitting_fixture_id = p37.m2p6a.sv.fixed-design-fit.degree12.v1
basis = normalized LegendreBasis1D(BoundedInterval(-1.0, 1.0), max_degree=64)
ranks = (1,1)
ridge = 1e-12
max_sweeps = 2
sweep_order = (0,)
row_budget >= 161
column_budget >= 65
condition_number_warning = 1e10
condition_number_veto = 1e14
holdout_tolerance = 2e-5
branch_seed prefix = p37-m2p6a
```

Promotion holdout fixture:

```text
tuning_holdout = Gauss-Legendre order 121 on reference [-1,1]
audit_holdout = deterministic midpoint-shifted uniform grid with 149 points
  z_i = -1 + 2(i+0.5)/149, i=0,...,148
promotion metrics use audit_holdout only
tuning_holdout metrics are explanatory after degree selection
```

Metric definitions:

```text
train_rms = sqrt(sum_i w_i (h_hat(z_i)-h(z_i))^2 / sum_i w_i)
audit_rms = sqrt(sum_i w_i (h_hat(z_i)-h(z_i))^2 / sum_i w_i)
audit_relative_target_error =
  max_i |h_hat(z_i)^2 - h(z_i)^2| / max(1e-12, |h(z_i)^2|)
```

Training weights are Gauss-Legendre probability weights on the reference
interval.  Audit weights are uniform probability weights on the midpoint grid.
RMS metrics are normalized by `sum_i w_i`.

## Evidence Contract

Question: can BayesFilter build a fixed-design functional TT approximation of
the P30 scalar SV adjacent target whose evaluations match dense oracle target
values on independent holdout points?

Baseline/comparator:

- independent dense formulas for `g_0` and `g_t` using the M2.5 scalar dense
  retained filter;
- existing `FixedTTFitter` direct weighted least-squares diagnostics;
- existing M2/M2.5 SV dense reference tests as guardrails.

Primary pass criteria:

- fitted TT status is `OK`;
- train weighted RMS residual for the scaled square-root target is `<= 2e-5`;
- audit weighted RMS residual for the scaled square-root target is `<= 2e-5`;
- audit reconstructed unnormalized target values agree with dense oracle
  values with maximum relative target error `<= 2e-3`;
- deterministic branch hashes replay under identical inputs;
- complexity, condition-number, and nonfinite veto diagnostics are finite and
  recorded.

Veto diagnostics:

- nonfinite target, sqrt target, TT evaluation, residual, condition number, or
  branch hash;
- shape or measure convention mismatch;
- fitting against physical points instead of the declared reference basis;
- target construction that drops the coordinate Jacobian or reference density;
- residual-only pass with poor dense heldout target reconstruction;
- accidental claim of full sequential TT/SIRT filtering.
- regression in the existing LGSSM exact-reference guardrails;
- regression in the M2/M2.5 SV dense-reference or scalar dense value-path
  guardrails.

Explanatory-only diagnostics:

- basis degree, rank, number of sweeps, ridge, train residual, holdout
  residual, condition numbers, wall time, row count, target window, and branch
  hashes.

What will not be concluded:

- no squared-density normalizer or marginalization correctness;
- no sequential filtering log evidence;
- no adaptive TT-cross or MATLAB behavior reproduction;
- no Zhao--Cui paper-scale `T=1000` result;
- no derivative, HMC, DSGE, GPU, or large-scale scalability claim.

Artifact preserving result:

- result ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_FIXTURE_REVISION`.

The wrong baseline would be comparing M2.6a only to `FixedTTFitter` residuals.
That would test an algebraic least-squares solver, not whether the SV adjacent
target is correctly constructed.  The subplan therefore requires heldout dense
oracle reconstruction in addition to fitter residuals.

The main proxy risk is treating a successful 1D TT fit as full Zhao--Cui
filtering.  M2.6a prevents this by fitting one adjacent target and explicitly
deferring squared-density normalizer, retained marginalization, and sequential
recursion to M2.6b/M2.6c.

The main hidden assumption is that one-dimensional SV can be represented by a
functional TT.  In 1D the TT is just a polynomial expansion, so this phase is a
minimal target-construction and fitting gate rather than evidence of high-rank
or high-dimensional behavior.  That is acceptable because M2.6a is a bridge,
not a scalability phase.

Stop conditions are explicit: if dense oracle reconstruction fails, if branch
replay fails, if the fixed fixtures drift without a new fixture ID, or if broad
LGSSM/M2/M2.5 guardrails regress, this phase does not promote.

Fixture revision note after first implementation attempt:

- The originally reviewed degree-12 fixture failed the predeclared train RMS
  gate at about `6e-3` on both initial and transition targets.
- A bounded tuning diagnostic over the same fixed target, dense oracle,
  scaling, and original tuning holdout showed degree 64 gives train/tuning
  RMS below `1e-11` for the initial target and below `5e-13` for the
  transition target, with tuning relative target error below `2.1e-5`.
- The fixture revision changes only approximation capacity
  (`max_degree=64`, corresponding column budget); it does not change target,
  observations, coordinate map, scaling, metric definitions, or tolerances.
- Claude review blocked using the tuning holdout for promotion.  The final
  promotion gate therefore uses a fresh untouched audit holdout fixture with a
  deterministic midpoint grid of 149 points, and the result ledger must report
  both the failed original fitting fixture and the revised promotion fixture.
- This is a plan correction before promotion, not a post-hoc pass by relaxing
  tolerances or reusing tuned holdout evidence.

## Planned Implementation Tasks

1. Add clean-room helper functions for SV adjacent target batches:
   - initial target batch from `p(x_0)p(y_0|x_0)`;
   - transition target batch from a scalar dense retained filter and
     `p(x_t|x_{t-1})p(y_t|x_t)`.
2. Ensure helper diagnostics record:
   - target kind;
   - fixture ID and target ID;
   - dense retained filter hash when applicable;
   - coordinate map payload;
   - reference density convention;
   - max-log scaling inherited from `build_adjacent_target_batch`.
3. Add tests that fit the initial and transition targets with a bounded
   Legendre product basis and fixed ranks.
4. Add tests that reconstruct heldout unnormalized target values from fitted
   TT evaluations and compare to dense oracle values.
5. Add deterministic replay tests for fit branch hashes.
6. Add governance/result ledger and update traceability only to say SV has
   fixed-design target-fitting evidence, not full TT/SIRT filtering evidence.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/filtering.py
bayesfilter/highdim/__init__.py
tests/highdim/test_p30_sv_fixed_design_tt_target.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6a-fixed-design-tt-sv-target-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

No top-level `bayesfilter` exports are allowed.

## Planned Commands

Focused:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_model_suite_contracts.py
```

Broad highdim guardrail:

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
  tests/highdim/test_p30_sv_fixed_design_tt_target.py
```

Compile/whitespace:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
git diff --check
```

All runs are deliberate CPU-only tests with `CUDA_VISIBLE_DEVICES=-1`.

## Exit Criteria

- Claude plan review returns `PASS_M2P6A_PLAN` or equivalent.
- Focused tests pass.
- Broad highdim guardrail passes.
- Compile and whitespace checks pass.
- Claude implementation/governance review returns `PASS_M2P6A_CODE` and
  `PASS_M2P6A_GOVERNANCE` or equivalent.
- Result ledger records a decision table and non-claims.
