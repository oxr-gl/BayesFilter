# DPF Common Filter-Path Fixed-Resampling Result

metadata_date: 2026-06-06

## Decision

`common_filter_path_fixed_resampling_all_matched`

## Summary

- Cells: `3`
- Status counts: `{'MATCHED': 3}`
- Max absolute fixed-resampling path delta: `1.7763568394002505e-15`
- Scalar absolute deltas: `{'lgssm_2d_linear': 0.0, 'sv_1d_synthetic': 0.0, 'range_bearing_2d_cv': 0.0}`
- Resampling counts: `{'lgssm_2d_linear': {'bayesfilter': 1, 'filterflow': 1}, 'sv_1d_synthetic': {'bayesfilter': 1, 'filterflow': 1}, 'range_bearing_2d_cv': {'bayesfilter': 1, 'filterflow': 1}}`

## Cell Table

| model | family | status | scalar delta | max path delta | resampling counts | backend note |
|---|---|---:|---:|---:|---|---|
| lgssm_2d_linear | linear_gaussian | `MATCHED` | `0.0` | `0.0` | `{'bayesfilter': 1, 'filterflow': 1}` | filterflow_builtin_linear_gaussian_fixed_ancestor |
| sv_1d_synthetic | stochastic_volatility | `MATCHED` | `0.0` | `8.881784197001252e-16` | `{'bayesfilter': 1, 'filterflow': 1}` | filterflow_builtin_sv_fixed_ancestor |
| range_bearing_2d_cv | range_bearing | `MATCHED` | `0.0` | `1.7763568394002505e-15` | `{'bayesfilter': 1, 'filterflow': 1}` | filterflow_local_range_bearing_fixed_ancestor |

## Interpretation

BayesFilter and executable float64 FilterFlow agree on the deterministic
fixed-ancestor resampling bootstrap value path for the common LGSSM,
stochastic-volatility, and range-bearing model suite.  The shared branch
resamples before the second proposal, gathers ancestors `[0, 0, 2]`, resets
weights to uniform, and then continues the fixed-noise bootstrap recursion.

This is stronger than the no-resampling path tie-out because it checks the
post-resampling carry-forward semantics and weight reset.  It remains a replay
test: it does not test random resampling distribution correctness, RNG
agreement, differentiable resampling, or gradients.

## Non-Claims

- no filtering-algorithm correctness claim
- no implementation is treated as an oracle
- no random-number-generator equality claim
- no resampling distribution correctness claim
- no differentiable-resampling or gradient correctness claim
- range-bearing FilterFlow coverage uses a local subprocess adapter
- no student-repository tie-out claim
- no TT-filter correctness claim
- no paper-scale, HMC, DSGE, GPU, or production-readiness claim
