# Plan: FilterFlow Float64 Row 173 VJP Decomposition

## Question

At smoothness mesh row `173`, theta
`[0.9710526315789474, 0.9842105263157894]`, where does the clipped/default
BayesFilter TF/TFP gradient path differ from the local float64 FilterFlow
reference at the first failing resampling step, `time_index=1`?

This is a cross-implementation difference audit only. It does not assert that
either implementation is mathematically correct.

## Evidence Contract

- Comparator: local executable FilterFlow checkout on branch
  `bayesfilter-py311-float64-reference`.
- BayesFilter backend: TensorFlow / TensorFlow Probability only.
- Primary criterion: compare same fixed observations, initial particles, seeds,
  dtype, scalar, and clipped/default transport backward path at `time_index=1`.
- Veto diagnostics: FilterFlow reference drift, scalar/value mismatch before VJP
  comparison, non-finite scalar or gradient, non-CPU-only execution, protected
  path mutation, or missing JSON artifact.
- Explanatory diagnostics: value deltas and VJP deltas for pre-resampling state,
  transport matrix, clipped transport upstream, post-resample state, proposal
  mean, proposed particles, transition log probability, observation log
  probability, proposal log probability, unnormalized weights, normalized
  weights, and log-likelihood increment.
- Not concluded: mathematical correctness of either implementation,
  analytic-gradient correctness, posterior correctness, production readiness,
  public API readiness, HMC readiness, nonlinear-SSM validity, DSGE/NAWM
  validation, or monograph claims.

## Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_vjp_decomposition_tf
```

## Outputs

- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py`
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-vjp-decomposition-result-2026-06-03.md`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-vjp-decomposition-2026-06-03.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_vjp_decomposition_2026-06-03.json`

## Skeptical Pre-Execution Audit

- Wrong baseline: use only the local float64 FilterFlow executable reference.
- Wrong objective: localize BayesFilter-vs-FilterFlow differences, not
  correctness.
- Hidden scalar mismatch: require scalar/value deltas before interpreting VJPs.
- Raw-gradient distraction: inspect the clipped/default path because the prior
  row localization showed the remaining residual survives clipping.
- Overclaim risk: finite VJPs are smoke evidence only.
- Protected paths: do not edit `bayesfilter/`, `tests/`, `docs/chapters/`, the
  high-dimensional lane, student code, or `.localsource/filterflow`.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_vjp_decomposition_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_vjp_decomposition_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_vjp_decomposition_2026-06-03.json
rg -n "^(import numpy|from numpy)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py
rg -n "student|controlled_dpf|highdim|DSGE|NAWM" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py
git diff --check
git status --short -- bayesfilter tests docs/chapters
```
