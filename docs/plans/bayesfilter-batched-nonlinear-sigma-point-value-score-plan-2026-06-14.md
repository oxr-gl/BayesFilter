# Batched Nonlinear Sigma-Point Value+Score Plan

Date: 2026-06-14

Owning root: `/home/ubuntu/python/BayesFilter`

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Can the repository's SVD cubature, SVD-UKF, and SVD-CUT4 nonlinear sigma-point filters evaluate likelihood and analytic score over a batch of independent parameter proposals/chains on GPU, like the experimental batched Kalman prototype? |
| Candidate mechanism | Lift the existing scalar SVD/eigen sigma-point value+score recursion to a leading batch axis over model/derivative tensors, keeping time sequential and sigma-point rules shared across batch rows. |
| Expected failure mode | Model callbacks are scalar-point shaped, derivative branch gates fail for some rows, batched eigensystem derivative algebra has axis mistakes, or GPU remains slower for small batches because point/state matrices are tiny. |
| Promotion criterion | Additive experimental kernels pass scalar row parity for value and score on `n>1`, `m>1`, multiple rules, and sampled rows from realistic batches. |
| Promotion veto | Any nonfinite value/score, wrong row order, scalar parity failure beyond tolerance, derivative branch failure in rows that scalar score accepts, wrong GPU/CPU placement in timing harnesses, hidden fallback to scalar Python/`tf.map_fn` loops inside the timed batched path, or UKF parameters that are not matched to the scalar authority path. |
| Continuation veto | Repeated branch-gate failures on the chosen smooth test fixture that also fail scalar score, or evidence that current scalar APIs cannot define the required derivatives for the selected fixture. |
| Repair trigger | Value parity passes but score parity fails: inspect derivative point-axis algebra; branch diagnostics fail only for some rows: select smoother parameter box or add row-level branch reporting; GPU slower at small `B`: run batch ladder before judging. |
| Explanatory diagnostics | CPU/GPU warm medians, point count, eigen-gap/floor summaries, per-filter timing, first-call tracing time, memory/capacity probes. |
| What must not be concluded | No production default, no HMC convergence, no nonlinear UKF/CUT4 scientific validity, no broad GPU speedup, no masked/time-varying/Hessian readiness. |

## Skeptical Plan Audit

The Kalman experiment is encouraging but is not a correctness baseline for
nonlinear sigma-point filters.  The nonlinear path adds sigma-point axes,
transition/observation callbacks, SVD/eigh derivative branches, deterministic
residual checks, and branch diagnostics.  A timing-only GPU run would be a wrong
baseline because it would not prove the batched algebra matches the scalar
non-batched authority path.

The fair baseline is:

- value: existing scalar `tf_svd_sigma_point_filter` for `tf_svd_cubature` and
  `tf_svd_ukf`, and existing scalar `tf_svd_cut4_filter` for CUT4;
- score: existing scalar `tf_svd_cubature_score`, `tf_svd_ukf_score`, and
  `tf_svd_cut4_score`;
- branch gates: existing scalar `nonlinear_sigma_point_score_branch_summary`
  style diagnostics, or equivalent row-level branch labels in the new harness.

The first implementation must be additive and must not change package exports
or existing runtime files until parity and review pass.

Claude plan review round 1 found material gaps and the plan was revised before
execution:

- UKF parity must freeze to the repository scalar defaults
  `alpha=1.0`, `beta=2.0`, `kappa=0.0` unless a separate scalar non-default
  value authority is added;
- the first-slice batched model/derivative containers must be mandatory local
  dataclasses because current structural contracts validate scalar ranks;
- the evidence must include an anti-loop check so a row-wise `tf.map_fn` or
  Python unstack implementation cannot pass as a native batched kernel;
- branch-gate artifacts must cover the actual batch parameter set;
- at least one moderate batch must use all-row parity, not only sampled rows.

## Existing Scalar Authority Map

Current scalar value paths:

- `bayesfilter/nonlinear/sigma_points_tf.py`
  - `tf_svd_sigma_point_filter(..., backend="tf_svd_cubature")`
  - `tf_svd_sigma_point_filter(..., backend="tf_svd_ukf")`
  - `tf_svd_sigma_point_log_likelihood_with_rule(...)`
- `bayesfilter/nonlinear/svd_cut_tf.py`
  - `tf_svd_cut4_filter(...)`
  - `tf_svd_cut4_log_likelihood(...)`

Current scalar analytic score paths:

- `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
  - `tf_svd_cubature_score(...)`
  - `tf_svd_ukf_score(...)`
  - `tf_svd_cut4_score(...)`
  - `tf_svd_sigma_point_score_with_rule(...)`

Fixture/model helpers:

- `bayesfilter/testing/nonlinear_models_tf.py`
  - Model B nonlinear accumulation and first derivatives;
  - Model C nonlinear growth and first derivatives;
  - existing callbacks accept point arrays and are vectorized over a point axis.

## Proposed Additive Files

New implementation file:

- `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py`

New tests:

- `tests/test_experimental_batched_nonlinear_sigma_point_tf.py`

New diagnostics/benchmarks:

- `docs/benchmarks/check_experimental_batched_nonlinear_sigma_point_parity.py`
- `docs/benchmarks/benchmark_experimental_batched_nonlinear_sigma_point_cpu_gpu.py`

No `bayesfilter/nonlinear/__init__.py` export in the first slice.

## API First Slice

Add experimental functions with an explicit batch-native contract:

```text
tf_batched_svd_sigma_point_value_and_score(
    observations,
    batched_model,
    batched_derivatives,
    *,
    backend: {"tf_svd_cubature", "tf_svd_ukf", "tf_svd_cut4"},
    placement_floor=0.0,
    innovation_floor=1e-12,
    rank_tolerance=1e-12,
    spectral_gap_tolerance=1e-8,
    fixed_null_tolerance=1e-10,
    jitter=0.0,
    allow_fixed_null_support=False,
) -> (log_likelihood[B], score[B, p], diagnostics)
```

The first batched model/derivative containers must be mandatory local dataclasses
rather than reusing `TFStructuralStateSpace` or `TFStructuralFirstDerivatives`.
Those public contracts intentionally validate scalar/non-batched ranks.  Required
batched tensor shapes:

```text
initial_mean:              [B, n]
initial_covariance:        [B, n, n]
innovation_covariance:     [B, q, q]
observation_covariance:    [B, m, m]
d_initial_mean:            [B, p, n]
d_initial_covariance:      [B, p, n, n]
d_innovation_covariance:   [B, p, q, q]
d_observation_covariance:  [B, p, m, m]
```

Callback contract for the first slice:

```text
transition_fn(previous_points[B, R, n], innovation_points[B, R, q]) -> [B, R, n]
observation_fn(state_points[B, R, n]) -> [B, R, m]
deterministic_residual_fn(previous[B, R, n], innovation[B, R, q], next[B, R, n]) -> [B, R, d]
transition_state_jacobian_fn(previous[B, R, n], innovation[B, R, q]) -> [B, R, n, n]
transition_innovation_jacobian_fn(previous[B, R, n], innovation[B, R, q]) -> [B, R, n, q]
d_transition_fn(previous[B, R, n], innovation[B, R, q]) -> [B, p, R, n]
observation_state_jacobian_fn(state[B, R, n]) -> [B, R, m, n]
d_observation_fn(state[B, R, n]) -> [B, p, R, m]
```

Do not silently wrap scalar callbacks with a Python loop in the timed path.  If
an adapter is needed, make it a test-only/scalar-parity helper and label it as
not GPU-timing eligible.

UKF first-slice scope:

- freeze UKF to the scalar authority defaults `alpha=1.0`, `beta=2.0`,
  `kappa=0.0`;
- do not expose non-default UKF parameters in first-slice parity artifacts;
- adding non-default UKF parameters requires adding an explicit matching scalar
  value path using `tf_svd_sigma_point_log_likelihood_with_rule` and a score
  path using `tf_svd_sigma_point_score_with_rule`.

## Algebra Lift

Lift the scalar score recursion in
`svd_sigma_point_derivatives_tf._smooth_sigma_point_score_with_rule`:

- state carries:
  - `mean[B, n]`
  - `covariance[B, n, n]`
  - `d_mean[B, p, n]`
  - `d_covariance[B, p, n, n]`
  - `log_likelihood[B]`
  - `score[B, p]`
- augmented covariance:
  - `aug_covariance[B, n+q, n+q]`
  - `d_aug_covariance[B, p, n+q, n+q]`
- placement eigensystem:
  - use `tf.linalg.eigh` on `[B, a, a]`;
  - factor `[B, a, a]`;
  - factor derivatives `[B, p, a, a]`;
  - branch diagnostics reduced per row and globally.
- sigma points:
  - `aug_points[B, R, a] = aug_mean[:, None, :] + rule.offsets[None, :, :] @ factor^T`;
  - derivative points `[B, p, R, a]`.
- moment projections:
  - weighted means over `R`;
  - weighted covariance and derivative covariance with explicit `B, p, R`
    axes.
- innovation eigensolve:
  - `tf.linalg.eigh` on `[B, m, m]`;
  - `eigh_solve` batched over `[B, m]` and `[B, m, m]`;
  - score terms `[B, p]`.
- Kalman update:
  - gain `[B, n, m]`;
  - derivative gain `[B, p, n, m]`;
  - covariance update `[B, n, n]` and derivative `[B, p, n, n]`.

Time remains sequential.  The parallel axes are batch `B`, sigma points `R`,
and parameters `p` inside each time step.

## Rule Coverage

Backend point counts with augmented dimension `a = n + q`:

- Cubature: `R = 2a`;
- UKF: `R = 2a + 1`;
- CUT4-G: `R = 2a + 2**a`, requires `a >= 3`.

For Model B, `n=2`, `q=1`, so `a=3` and CUT4-G has `R=14`.
That is a good first fixture because it is small, existing, and already used by
HMC readiness tests.

For larger DSGE models, CUT4-G may become enormous because of `2**a`; benchmark
plans must cap or explicitly skip high `a`.

## Test Ladder

1. Static shape and closed-failure tests:
   - bad batch dimension;
   - bad derivative shape;
   - backend rule mismatch;
   - CUT4-G rejects `a < 3`.

2. Tiny affine parity:
   - use Model A if derivative fixtures are available or easy to construct;
   - compare batched nonlinear sigma-point values to scalar value paths;
   - compare score to scalar analytic score where derivatives are available.

3. Model B realistic parity:
   - all rows for `B=3` and one moderate batch such as `B=20`;
   - sampled rows only for large batches such as `B=200` or above;
   - backends: cubature, UKF, CUT4;
   - compare value and score to scalar authority APIs;
   - use the existing branch-safe Model B parameter boxes from
     `tests/test_nonlinear_sigma_point_branch_diagnostics_tf.py`;
   - require finite outputs and branch gates pass for both scalar and batched
     rows.

4. Row-order test:
   - permute batch rows and verify values/scores follow the permutation.

5. Anti-loop/native-batch check:
   - inspect the traced graph or implementation source for forbidden
     batch-row constructs in the timed kernel: Python `for` over batch rows,
     `tf.map_fn` over batch rows, `tf.vectorized_map` as the primary batch
     implementation, or row-wise scalar model invocation;
   - time benchmarks must state this check passed before interpreting GPU
     throughput.

6. CPU graph parity:
   - eager vs `tf.function`;
   - XLA only after non-XLA graph passes.

7. GPU smoke:
   - trusted context only;
   - require tensor placement on GPU and finite outputs;
   - no speed claim.

8. CPU/GPU timing:
   - only after parity passes;
   - batch ladder `B=20, 200, 1024, 4096` for cubature/UKF;
   - CUT4 ladder should be smaller or point-count capped if `a` is large.

## Evidence Contract For First Execution

Question:

- Can an additive batched nonlinear sigma-point value+score implementation
  match scalar non-batched value+score for Model B on all three rules?

Baseline:

- scalar `tf_svd_cubature_score`, `tf_svd_ukf_score`, `tf_svd_cut4_score` and
  matching scalar value filters.

Primary pass/fail:

- all-row parity for `B=3` and `B=20`, with max value error under `1e-8` and
  max score error under `1e-7` for Model B, all three backends, CPU-only.

Veto:

- any nonfinite output;
- branch failure in batched path where scalar row passes;
- wrong row order;
- shape mismatch accepted instead of failing closed.
- forbidden batch-row loop constructs in the timed implementation path.

Explanatory only:

- runtime, GPU placement, first-call tracing, point count, floor/gap summaries.

Not concluded:

- speedup, production readiness, HMC convergence, default backend change.

Artifact:

- JSON parity artifact under `docs/benchmarks/`;
- branch-summary artifact over the exact batch parameter set under
  `docs/benchmarks/`;
- anti-loop/native-batch check in the result note;
- result note under `docs/plans/`.

## Implementation Sequence

1. Create `experimental_batched_svd_sigma_point_tf.py` with mandatory local dataclasses
   for batched structural model and derivatives.
2. Implement batched helper utilities:
   - batched symmetrize;
   - batched PSD eigensystem and solve;
   - batched smooth factor derivative with branch assertions;
   - batched weighted covariance and derivative covariance.
3. Implement `tf_batched_svd_sigma_point_value_and_score_with_rule`.
4. Add backend wrappers for cubature, UKF, and CUT4.
5. Add Model B batched fixture builder in tests or benchmark harness, with
   genuinely batched callbacks.
6. Add parity tests against scalar APIs, including all-row `B=20` parity.
7. Add native-batch/anti-loop check for timed implementation.
8. Only after CPU parity and anti-loop checks pass, run trusted GPU smoke and
   CPU/GPU timing.

## Risk Register

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Callback vectorization mismatch | Existing callbacks may only assume `[R, dim]`, while GPU batching needs `[B, R, dim]`. | Start with explicit batched Model B callbacks; later add an adapter contract. |
| SVD/eigh derivative branch gates | Some rows can fail spectral-gap/floor assumptions. | Preserve row-level branch diagnostics and compare against scalar branch outcomes. |
| CUT4 point explosion | `2**a` grows quickly. | First support only small `a`; add point-count guard in benchmark harness. |
| Tensor memory growth | Derivative tensors scale as `[B, p, R, dim]`. | Run capacity ladder after parity; record memory/OOM as veto, not correctness failure. |
| GPU timing misleading | Small batches and FP64 may be CPU-faster. | Use batch ladder and clear explanatory-only timing labels. |
| Hidden scalar loops | A `tf.map_fn` or Python loop over batch could pass parity but miss GPU throughput goal. | Permit only for scalar-parity reference; timed implementation must use native batch axes. |
| UKF non-default mismatch | Existing scalar dispatcher defaults do not expose non-default UKF parameters symmetrically for value and score. | First slice freezes UKF to repo defaults; non-default UKF needs a separate matching scalar authority path. |

## Next Smallest Action

Implement the first additive batched Model B path for `tf_svd_cubature` only,
with CPU all-row scalar parity for `B=3` and `B=20`, branch-safe parameter
boxes, and an anti-loop check.  Once that passes, extend the same kernel to
default UKF and CUT4 by swapping the sigma-point rule.
