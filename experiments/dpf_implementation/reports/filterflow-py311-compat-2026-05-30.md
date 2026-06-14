# Filterflow Python 3.11 Compatibility Patch Report

## Summary

The external filterflow checkout now has a local compatibility branch:
`bayesfilter-py311-compat`.

The patch fixes Python 3.11 / modern SciPy compatibility only.  It does not
change filterflow model, resampling, likelihood, Sinkhorn, or TensorFlow
semantics.

## Changed External Files

- `.localsource/filterflow/scripts/base.py`
- `.localsource/filterflow/scripts/simple_linear_common.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`

Diff summary:

```text
3 files changed, 13 insertions(+), 5 deletions(-)
```

## What Was Fixed

- Legacy pykalman/SciPy wrapper no longer passes obsolete `debug` positional
  argument to `scipy.linalg.solve_triangular`.
- Legacy pykalman can access `inspect.getargspec` on Python 3.11 via a minimal
  alias to `inspect.getfullargspec`.

## Verified Commands

- Wrapper dense/masked triangular-solve equivalence: pass.
- `py_compile` on changed filterflow files: pass.
- simple-linear import without caller shim: pass.
- simple-linear Kalman command: pass.
- simple-linear PF command: pass.
- simple-linear regularized transform commands for `epsilon=0.25`, `0.5`,
  `0.75`: pass.

Exact command templates are recorded in
`docs/plans/bayesfilter-dpf-filterflow-py311-compat-result-2026-05-30.md`.

## Bounded LGSSM Outputs

Settings: `T=150`, `batch_size=100`, `n_particles=25`, `data_seed=111`,
`filter_seed=555`, resampling threshold `0.5`.

| Method | eps | theta 0.25 | theta 0.5 | theta 0.75 |
| --- | ---: | ---: | ---: | ---: |
| Kalman | N/A | -3.052 | -2.958 | -3.015 |
| Multinomial PF | N/A | -4.077 / 0.176 | -3.818 / 0.153 | -3.938 / 0.198 |
| Regularized transform | 0.25 | -4.077 / 0.179 | -3.815 / 0.155 | -3.930 / 0.193 |
| Regularized transform | 0.5 | -4.078 / 0.179 | -3.817 / 0.154 | -3.938 / 0.190 |
| Regularized transform | 0.75 | -4.078 / 0.178 | -3.818 / 0.154 | -3.943 / 0.189 |

## Caveats

This is not a full Section 5.1 reproduction and not BayesFilter correctness
evidence.  It only establishes that the external filterflow reference code is
runnable locally for future matched comparisons.

Machine-readable output:
`experiments/dpf_implementation/reports/outputs/filterflow_py311_compat_2026-05-30.json`.
