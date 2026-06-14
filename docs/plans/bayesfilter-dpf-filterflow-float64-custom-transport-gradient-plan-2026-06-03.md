# FilterFlow Float64 Custom Transport Gradient Patch Plan

## Question

Can the experimental BayesFilter TF/TFP annealed transport component match the
local float64 FilterFlow executable on the smoothness gradient surface after
mirroring FilterFlow's `RegularisedTransform` custom backward rule?

This is a cross-implementation difference audit only. It does not assert that
either implementation is mathematically correct.

## Evidence Contract

- Comparator: local executable FilterFlow checkout on branch
  `bayesfilter-py311-float64-reference`.
- BayesFilter backend: TensorFlow / TensorFlow Probability only.
- Primary patch: add a FilterFlow-compatible custom-gradient transport matrix
  mode that clips upstream `d_transport` to `[-1, 1]`.
- Primary pass criterion: the bounded float64 smoothness gradient surface runner
  changes from gradient mismatch to implementation agreement.
- Veto diagnostics: scalar mismatch, non-finite scalar/gradient, FilterFlow
  reference drift, protected-path mutation, GPU visibility in deliberate
  CPU-only runs, or NumPy import in the BayesFilter implementation file.
- Explanatory diagnostics: raw transport-gradient mode remains available and
  labelled for future difference audits.
- Not concluded: correctness of either implementation, analytic-gradient
  correctness, posterior correctness, production readiness, public API
  readiness, HMC readiness, nonlinear-SSM validity, DSGE/NAWM validation, or
  monograph claims.

## Inputs

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-result-2026-06-03.md`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`

## Outputs

- Updated experimental component:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- Diagnostic-preservation patch:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py`
- Updated smoothness gradient surface artifacts from rerunning:
  `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-result-2026-06-03.md`
  and matching report/JSON under `experiments/dpf_implementation/reports/`.
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-result-2026-06-03.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-result-2026-06-03.md`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py`
- Smoothness gradient surface result/report/JSON artifacts under
  `docs/plans/` and `experiments/dpf_implementation/reports/`.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored student code
- `.localsource/filterflow`
- DSGE/NAWM-specific models or artifacts

## Skeptical Pre-Execution Audit

- Wrong baseline: compare only against the local float64 FilterFlow executable.
- Wrong objective: match FilterFlow executable behavior, not mathematical
  correctness.
- Hidden scalar regression: scalar agreement must remain within the existing
  tolerance.
- Gradient overclaim: gradient agreement to FilterFlow is not analytic-gradient
  correctness.
- Over-scoped patch: keep the change in the experimental annealed transport
  component only.
- Diagnostics erasure: retain a labelled raw transport-gradient mode.
- Diagnostic preservation: the localization runner must explicitly request raw
  transport gradients for its `raw` mode after the component default changes.
- Comparator drift: validate FilterFlow status through the existing runner.

The audit passes because the localization artifact identified exactly one
FilterFlow-specific backward rule, and the planned patch mirrors that rule
without changing production code or FilterFlow source.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_surface_2026-06-03.json >/tmp/dpf_filterflow_float64_smoothness_gradient_surface.json
rg -n "^(import numpy|from numpy)" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
rg -n "student|controlled_dpf|highdim|DSGE|NAWM|\\.localsource/filterflow" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-plan-2026-06-03.md docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-result-2026-06-03.md experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
git diff --check
git status --short -- bayesfilter tests docs/chapters
git -C .localsource/filterflow status --short --branch
git status --short --branch
```
