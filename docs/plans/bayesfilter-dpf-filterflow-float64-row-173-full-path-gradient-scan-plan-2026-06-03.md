# Plan: FilterFlow Float64 Row 173 Full-Path Gradient Scan

## Question

For smoothness mesh row `173`, theta
`[0.9710526315789474, 0.9842105263157894]`, at what cumulative time does the
BayesFilter TF/TFP clipped/default gradient first differ from the local float64
FilterFlow reference under the same full-path GradientTape contract?

This is a cross-implementation difference audit only. It does not assert that
either implementation is mathematically correct.

## Evidence Contract

- Comparator: local executable FilterFlow checkout on branch
  `bayesfilter-py311-float64-reference`.
- BayesFilter backend: TensorFlow / TensorFlow Probability only.
- Primary criterion: first cumulative time index where scalar is aligned but the
  diagonal gradient exceeds `2e-4` absolute and relative tolerance.
- Veto diagnostics: FilterFlow reference drift, scalar mismatch before gradient
  localization, non-finite scalar or gradient, non-CPU-only execution, protected
  path mutation, or missing JSON artifact.
- Explanatory diagnostics: resampling flag, FilterFlow/BayesFilter gradient
  components, raw deltas, relative deltas, and sample rows around the first
  true residual.
- Not concluded: mathematical correctness of either implementation,
  analytic-gradient correctness, posterior correctness, production readiness,
  public API readiness, HMC readiness, nonlinear-SSM validity, DSGE/NAWM
  validation, or monograph claims.

## Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_full_path_gradient_scan_tf
```

## Outputs

- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_full_path_gradient_scan_tf.py`
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-full-path-gradient-scan-result-2026-06-03.md`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-full-path-gradient-scan-2026-06-03.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_full_path_gradient_scan_2026-06-03.json`

## Skeptical Pre-Execution Audit

- Wrong baseline: use only the local float64 FilterFlow executable reference.
- Wrong objective: localize BayesFilter-vs-FilterFlow differences, not
  correctness.
- Old diagnostic artifact: do not reuse the old step-local FilterFlow gradient
  as a full-path comparator.
- Hidden scalar mismatch: require scalar deltas before interpreting gradient
  deltas.
- Overclaim risk: finite gradients are smoke evidence only.
- Protected paths: do not edit `bayesfilter/`, `tests/`, `docs/chapters/`, the
  high-dimensional lane, student code, or `.localsource/filterflow`.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_full_path_gradient_scan_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_full_path_gradient_scan_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_full_path_gradient_scan_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_full_path_gradient_scan_2026-06-03.json
rg -n "^(import numpy|from numpy)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_full_path_gradient_scan_tf.py
rg -n "student|controlled_dpf|highdim|DSGE|NAWM" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_full_path_gradient_scan_tf.py
git diff --check
git status --short -- bayesfilter tests docs/chapters
```
