# Plan: FilterFlow Float64 Smoothness Gradient Full Surface

## Question

After the bounded `mesh_size=4` surface passed, does BayesFilter still match the
local float64 FilterFlow executable on the script-default `mesh_size=20`
`simple_linear_smoothness.py` scalar and diagonal gradient surface?

This is a difference audit only: the result may say whether the two
implementations agree under this fixture. It must not assert that either
implementation is mathematically correct.

## Evidence Contract

- Comparator: `.localsource/filterflow` branch
  `bayesfilter-py311-float64-reference` at
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.
- Scalar: `tf.reduce_mean(final_state.log_likelihoods)` with
  `resampling_correction=False`.
- Gradient: FilterFlow `tf.linalg.diag_part(tape.gradient(scalar,
  transition_matrix_variable))` versus BayesFilter GradientTape gradient with
  respect to `theta` in `diag(theta)+[[0,1],[0,0]]`.
- Primary criterion: all 400 scalar/gradient rows agree within the existing
  float64 audit tolerances.
- Veto diagnostics: wrong FilterFlow branch/commit, comparator drift, FilterFlow
  subprocess failure, non-finite scalar/gradient, CPU-only invariant failure,
  JSON/schema failure, protected-path drift, or scalar-contract mismatch.
- Explanatory only: transport residuals, runtime, row order, and ESS.
- Not concluded: mathematical correctness, analytic gradient correctness,
  posterior correctness, production readiness, HMC readiness, public API
  readiness, or monograph claims.

## Exact Inputs

- `T=100`, `batch_size=1`, `n_particles=50`.
- `mesh_size=20` over `[0.95, 1.0]^2`, matching the script default.
- `data_seed=123`, `filter_seed=1234`.
- `epsilon=0.25`, `scaling=0.85`, `convergence_threshold=1e-6`,
  `max_iter=500`, `resampling_neff=0.9999`.
- `optimal_proposal=True`, float64 model/data tensors, CPU-only execution.

## Write Set

Allowed:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py`
- this plan
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-result-2026-06-03.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-gradient-full-surface-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_full_surface_2026-06-03.json`

Forbidden:

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored/student code
- `.localsource/filterflow` source

## Skeptical Pre-Execution Audit

- Baseline: use the float64 FilterFlow reference branch, not older float32 or
  compatibility results.
- Scope: only `mesh_size` changes from 4 to 20; scalar, seeds, dtype, and
  algorithm contracts stay fixed.
- Proxy risk: finite gradients and transport residuals are veto/explanatory
  diagnostics only.
- Threshold risk: use the same tolerances as the bounded pass so the run tests
  implementation agreement rather than retuning criteria.
- Artifact risk: write a separate full-surface result and JSON, leaving the
  bounded result intact.

Audit result: pass.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf --full-surface
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf --full-surface --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_full_surface_2026-06-03.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
rg -n "^\\s*(from|import)\\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
rg -n "[ \\t]$" docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-gradient-full-surface-2026-06-03.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
git -C .localsource/filterflow status --short --branch
git status --short --branch
```
