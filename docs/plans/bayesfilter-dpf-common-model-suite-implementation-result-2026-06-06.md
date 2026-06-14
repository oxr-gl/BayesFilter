# DPF Common Model Suite Tie-Out Result

metadata_date: 2026-06-06

## Decision

`common_model_suite_density_all_matched`

## Summary

- Cells: `3`
- Status counts: `{'MATCHED': 3}`
- Max absolute density delta: `1.7763568394002505e-15`

## Cell Table

| model | family | status | max abs delta | backend note |
|---|---|---:|---:|---|
| lgssm_2d_linear | linear_gaussian | `MATCHED` | `0.0` | filterflow_builtin_linear_gaussian |
| sv_1d_synthetic | stochastic_volatility | `MATCHED` | `1.1102230246251565e-16` | filterflow_builtin_sv_plus_stationary_initial |
| range_bearing_2d_cv | range_bearing | `MATCHED` | `1.7763568394002505e-15` | filterflow_local_range_bearing_adapter |

## Interpretation

BayesFilter and executable float64 FilterFlow now share a small common model
suite at the density-component level: a 2D LGSSM, a 1D stochastic-volatility
model, and a nonlinear range-bearing model.  This establishes a reusable
contract for later full filter-path value and gradient matching.  It does not
claim full particle-filter correctness, because proposal, resampling,
random-number, scalar-objective, and branch-gradient contracts still need to
be fixed per model.

## Non-Claims

- no filtering-algorithm correctness claim
- no implementation is treated as an oracle
- density agreement is not full particle-filter path agreement
- range-bearing FilterFlow coverage uses a local subprocess adapter, not an upstream built-in model
- no TT-filter correctness claim
- no paper-scale validation claim
- no HMC/DSGE/GPU/production readiness claim
