# DPF Common Filter-Path No-Resampling Result

metadata_date: 2026-06-06

## Decision

`common_filter_path_noresampling_all_matched`

## Summary

- Cells: `3`
- Status counts: `{'MATCHED': 3}`
- Max absolute filter-path delta: `1.7763568394002505e-15`
- Scalar absolute deltas: `{'lgssm_2d_linear': 0.0, 'sv_1d_synthetic': 2.220446049250313e-16, 'range_bearing_2d_cv': 0.0}`

## Cell Table

| model | family | status | scalar delta | max path delta | backend note |
|---|---|---:|---:|---:|---|
| lgssm_2d_linear | linear_gaussian | `MATCHED` | `0.0` | `0.0` | filterflow_builtin_linear_gaussian_noresampling |
| sv_1d_synthetic | stochastic_volatility | `MATCHED` | `2.220446049250313e-16` | `1.3322676295501878e-15` | filterflow_builtin_sv_noresampling |
| range_bearing_2d_cv | range_bearing | `MATCHED` | `0.0` | `1.7763568394002505e-15` | filterflow_local_range_bearing_noresampling |

## Interpretation

BayesFilter and executable float64 FilterFlow agree on the deterministic
fixed-noise no-resampling bootstrap value path for the common LGSSM,
stochastic-volatility, and range-bearing model suite.  This is the next
stronger common-sense tie-out after density-component equality: the two sides
now match the propagated particles, likelihood ledgers, normalized weights,
predictive log-normalizer scalar, ESS, and weighted moments under a shared
contract.

The result is intentionally scoped.  It does not test resampling, pathwise
gradients, random-number generator equivalence, student repositories, TT
filters, or scientific correctness of the filtering algorithm.

## Non-Claims

- no filtering-algorithm correctness claim
- no implementation is treated as an oracle
- no resampling correctness claim
- no gradient correctness claim
- range-bearing FilterFlow coverage uses a local subprocess adapter
- no student-repository tie-out claim
- no TT-filter correctness claim
- no paper-scale, HMC, DSGE, GPU, or production-readiness claim
