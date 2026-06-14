# Plan: FilterFlow Float64 Row 173 Time 93 VJP Decomposition

## Question

At smoothness mesh row `173`, theta
`[0.9710526315789474, 0.9842105263157894]`, what carries the first true
same-contract clipped/default gradient residual at `time_index=93`?

This is a BayesFilter-vs-local-FilterFlow difference audit only. It does not
assert correctness of either implementation.

## Evidence Contract

- Comparator: local executable FilterFlow checkout on branch
  `bayesfilter-py311-float64-reference`.
- BayesFilter backend: TensorFlow / TensorFlow Probability only.
- Primary criterion: value tensors remain aligned while total gradient and VJP
  fields identify where the residual enters.
- Veto diagnostics: scalar/value mismatch, reference drift, non-finite values,
  non-CPU-only execution, or protected-path mutation.
- Explanatory diagnostics: VJP deltas for pre-resampling particles/log weights,
  transport matrix, post-resampling particles/log weights, proposal terms,
  likelihood terms, and normalized weights.
- Not concluded: mathematical correctness of either implementation,
  analytic-gradient correctness, posterior correctness, production readiness,
  HMC readiness, or monograph claims.

## Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_vjp_decomposition_tf --target-time-index 93 --tag row-173-time-93
```

## Outputs

- Result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-vjp-decomposition-result-2026-06-03.md`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-time-93-vjp-decomposition-2026-06-03.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_time_93_vjp_decomposition_2026-06-03.json`
