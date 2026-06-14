# Plan: FilterFlow Float64 Row 244 Gradient Localization

## Question

Where does BayesFilter TF/TFP first differ from the local float64 FilterFlow
reference on smoothness mesh row `244`, theta
`[0.981578947368421, 0.9605263157894737]`?

This is a cross-implementation difference audit only. It does not assert that
BayesFilter or FilterFlow is mathematically correct.

## Evidence Contract

- Comparator: local executable FilterFlow checkout on branch
  `bayesfilter-py311-float64-reference`.
- BayesFilter backend: TensorFlow / TensorFlow Probability only.
- Primary criterion: identify first cumulative time where BayesFilter gradient
  differs from FilterFlow while scalar/log-likelihood remains aligned.
- Veto diagnostics: FilterFlow reference drift, scalar mismatch before gradient
  localization, non-finite scalar or gradient, non-CPU-only execution, or
  protected-path mutation.
- Explanatory diagnostics: raw transport gradient, FilterFlow-style clipped
  transport upstream gradient, stopped transport matrix, stopped post-resample
  state, stopped proposal mean, stopped proposal log-probability, stopped
  transition log-probability, and stopped normalized weights.
- Not concluded: correctness of either implementation, analytic-gradient
  correctness, posterior correctness, production readiness, public API
  readiness, HMC readiness, nonlinear-SSM validity, DSGE/NAWM validation, or
  monograph claims.

## Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_localization_tf --theta 0.981578947368421 0.9605263157894737 --tag row-244 --mesh-index 244
```

## Outputs

- Result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-result-2026-06-03.md`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-244-gradient-localization-2026-06-03.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_244_gradient_localization_2026-06-03.json`
