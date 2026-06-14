# Plan: FilterFlow Float64 Smoothness Scalar Surface Comparison

## Question

After the float64 reference branch cleared the full 2D no-replay comparison,
does BayesFilter match the local float64 FilterFlow executable on the actual
`simple_linear_smoothness.py` scalar surface?

This is a difference audit only. The question is whether BayesFilter and the
local FilterFlow executable produce the same scalar values for the same
bounded smoothness mesh, not whether either implementation is mathematically
correct.

## Evidence Contract

- Comparator: `.localsource/filterflow` branch
  `bayesfilter-py311-float64-reference` at
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.
- Scalar contract: FilterFlow `routine()` returns
  `tf.reduce_mean(final_state.log_likelihoods)`; with `batch_size=1`, this is
  also the single-batch total particle-filter log likelihood. BayesFilter must
  compute the same scalar definition.
- Primary criterion: BayesFilter scalar surface values agree with the
  executable FilterFlow scalar surface within float64 audit tolerance on the
  bounded mesh.
- Required settings: CPU-only, `T=100`, `batch_size=1`, `n_particles=50`,
  `data_seed=123`, `filter_seed=1234`, `epsilon=0.25`, `scaling=0.85`,
  `convergence_threshold=1e-6`, `max_iter=500`, `resampling_neff=0.9999`,
  `optimal_proposal=True`, and float64 data/model tensors.
- Bounded mesh: use `mesh_size=4` over the same `[0.95, 1.0]^2` grid as
  `simple_linear_smoothness.py`. This is a bounded debug surface, not the full
  script default `mesh_size=20`.
- Baseline gate: a non-mutating external FilterFlow extraction must run under
  CPU-only settings and report the reference branch/commit before comparison.
- Veto diagnostics: wrong FilterFlow reference branch/commit, comparator drift,
  FilterFlow subprocess failure, non-finite scalar values, CPU-only invariant
  failure, JSON/schema failure, protected-path drift, or missing scalar
  contract.
- Explanatory only: transport row/column residuals, Kalman log likelihoods,
  gradients, runtime, and per-row deltas below the primary tolerance.
- Not concluded: mathematical correctness of either implementation, posterior
  correctness, gradient correctness, full `mesh_size=20` smoothness surface
  agreement, production readiness, public API readiness, or monograph claims.

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_scalar_surface_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-result-2026-06-03.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-scalar-surface-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_scalar_surface_2026-06-03.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored/student code
- `.localsource/filterflow` source

## Skeptical Pre-Execution Audit

- Wrong-baseline risk: compare against the local float64 FilterFlow executable,
  not old float32 or compatibility evidence.
- Wrong-scalar risk: use `tf.reduce_mean(final_state.log_likelihoods)` from
  `simple_linear_smoothness.py`, not a Kalman scalar or per-time normalization.
- Wrong-promotion risk: transport residual magnitude is not a pass/fail
  criterion for this debug stage. Residuals explain numerical behavior only.
- Randomness risk: use FilterFlow's own `pf(..., seed=1234)` extraction and
  BayesFilter's matching split-seed protocol without replaying proposal
  particles.
- Hidden-drift risk: fingerprint FilterFlow before and after the run and
  verify protected path status.
- Scope risk: a bounded `mesh_size=4` pass does not establish full
  `mesh_size=20` smoothness or gradient agreement.

Audit result: pass.

## Phase Order

1. Extract bounded scalar-surface settings, observations, initial particles,
   FilterFlow scalar values, and CPU/reference status from the executable
   FilterFlow branch.
2. Run the BayesFilter TF/TFP float64 reproduction for the same mesh values,
   observations, initial particles, resampling policy, and optimal proposal.
3. Compare scalar values row by row; record per-row deltas and explanatory
   transport diagnostics.
4. Write JSON, report, and result artifacts.
5. Run targeted verification.

## Stop Conditions

- Stop as blocked if the exact FilterFlow branch/commit marker is not present.
- Stop as blocked if the FilterFlow subprocess cannot execute.
- Stop as veto if either implementation emits non-finite scalar values.
- Stop as mismatch if scalar values exceed tolerance; localize the first row.
- Stop as blocked if comparator fingerprints drift during execution.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_scalar_surface_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_scalar_surface_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_scalar_surface_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_scalar_surface_2026-06-03.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_scalar_surface_tf.py
rg -n "^\s*(from|import)\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_scalar_surface_tf.py
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-scalar-surface-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_scalar_surface_tf.py experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-scalar-surface-2026-06-03.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
git -C .localsource/filterflow status --short --branch
git status --short --branch
```

