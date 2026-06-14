# Filterflow Legacy Environment Smoke

## Summary

The external JTT94/filterflow LGSSM simple-linear particle-filter path is now
runnable from `.localenv/filterflow-py311/` against the checkout at
`.localsource/filterflow` commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

This is reference/comparison evidence only.  It does not change the BayesFilter
TF/TFP implementation backend policy.

## What Runs

- `scripts.simple_linear_common` imports.
- `scripts.simple_linear_comparison` imports with a Python 3.11
  `inspect.getargspec` runtime shim.
- Multinomial PF runs for the simple-linear LGSSM.
- Regularized transform runs for `epsilon` values `0.25`, `0.5`, and `0.75`.

## Selected Outputs

Executed settings: `T=150`, `batch_size=100`, `n_particles=25`,
`data_seed=111`, `filter_seed=555`, theta grid
`(0.25, 0.25)`, `(0.5, 0.5)`, `(0.75, 0.75)`.

| Method | epsilon | theta=0.25 mean/std | theta=0.5 mean/std | theta=0.75 mean/std |
| --- | ---: | ---: | ---: | ---: |
| Multinomial PF | N/A | -4.077 / 0.176 | -3.818 / 0.153 | -3.938 / 0.198 |
| Regularized transform | 0.25 | -4.077 / 0.179 | -3.815 / 0.155 | -3.930 / 0.193 |
| Regularized transform | 0.5 | -4.078 / 0.179 | -3.817 / 0.154 | -3.938 / 0.190 |
| Regularized transform | 0.75 | -4.078 / 0.178 | -3.818 / 0.154 | -3.943 / 0.189 |

The values are filterflow's printed `final_state.log_likelihoods / T`
summaries.  They are not yet aligned to the exact Kalman likelihood.

## Remaining Blocker

The filterflow Kalman branch fails on Python 3.11 with modern SciPy because
filterflow's pykalman compatibility wrapper forwards an obsolete positional
`debug` argument to `scipy.linalg.solve_triangular`.

This does not block running filterflow's PF or regularized transform paths.  It
does block using filterflow's own `ResamplingMethodsEnum.KALMAN` command as the
Kalman oracle without a reviewed non-mutating shim or source patch.

## Artifact

Machine-readable summary:
`experiments/dpf_implementation/reports/outputs/filterflow_legacy_env_smoke_2026-05-30.json`.
