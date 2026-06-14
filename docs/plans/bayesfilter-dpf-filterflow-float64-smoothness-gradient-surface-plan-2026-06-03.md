# Plan: FilterFlow Float64 Smoothness Gradient Surface Comparison

## Question

Given that BayesFilter and the local float64 FilterFlow executable now agree on
the bounded `simple_linear_smoothness.py` scalar surface, do they also agree on
the diagonal GradientTape derivatives of the same scalar with respect to
`theta_1` and `theta_2` in
`A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]`?

This remains a difference audit only. The result can say whether BayesFilter
matches the local FilterFlow executable for this bounded gradient surface. It
must not assert that either gradient is mathematically correct.

## Evidence Contract

- Comparator: `.localsource/filterflow` branch
  `bayesfilter-py311-float64-reference` at
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.
- Scalar contract: FilterFlow `routine()` computes
  `tf.reduce_mean(final_state.log_likelihoods)` and differentiates that scalar
  with `resampling_correction=False`.
- Gradient contract: compare `tf.linalg.diag_part(ll_grad)` from FilterFlow
  against the BayesFilter `GradientTape` gradient with respect to the two-vector
  `theta` used to build `diag(theta)+[[0,1],[0,0]]`.
- Primary criterion: both scalar values and two-vector gradients agree within
  float64 audit tolerances on the bounded 4x4 mesh.
- Required settings: CPU-only, `T=100`, `batch_size=1`, `n_particles=50`,
  `data_seed=123`, `filter_seed=1234`, `epsilon=0.25`, `scaling=0.85`,
  `convergence_threshold=1e-6`, `max_iter=500`, `resampling_neff=0.9999`,
  `optimal_proposal=True`, and float64 data/model tensors.
- Bounded mesh: `mesh_size=4` over the same `[0.95, 1.0]^2` grid as
  `simple_linear_smoothness.py`. This is not the full default `mesh_size=20`.
- Veto diagnostics: wrong FilterFlow reference branch/commit, comparator drift,
  FilterFlow subprocess failure, non-finite scalar or gradient values,
  CPU-only invariant failure, JSON/schema failure, protected-path drift, or
  scalar-contract mismatch.
- Explanatory only: Kalman finite-difference gradients, transport residuals,
  runtime, and per-row scalar agreement if gradient agreement fails.
- Not concluded: mathematical gradient correctness, posterior correctness,
  full `mesh_size=20` smoothness agreement, production readiness, public API
  readiness, or monograph claims.

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-result-2026-06-03.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-gradient-surface-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_surface_2026-06-03.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored/student code
- `.localsource/filterflow` source

## Skeptical Pre-Execution Audit

- Wrong-baseline risk: use the float64 FilterFlow executable branch, not old
  float32 compatibility results.
- Wrong-scalar risk: use the exact smoothness scalar with
  `resampling_correction=False`; do not compare a Kalman scalar or per-time
  normalization as the primary criterion.
- Wrong-gradient risk: compare diagonal transition-matrix derivatives only,
  matching FilterFlow's `tf.linalg.diag_part(ll_grad)`.
- Proxy-risk: finite gradients alone are a smoke/veto diagnostic, not evidence
  of gradient agreement.
- Randomness risk: use FilterFlow's `pf(..., seed=1234)` path and BayesFilter's
  matching split-seed protocol without replaying proposal particles.
- Scope risk: a bounded `mesh_size=4` pass does not establish full
  `mesh_size=20` smoothness or analytic gradient correctness.

Audit result: pass.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_surface_2026-06-03.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
rg -n "^\s*(from|import)\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-gradient-surface-2026-06-03.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
git -C .localsource/filterflow status --short --branch
git status --short --branch
```

