# DPF Common Fixed-Branch Gradient Result

metadata_date: 2026-06-06

## Decision

`common_fixed_branch_gradient_all_matched`

## Summary

- Cells: `3`
- Status counts: `{'MATCHED': 3}`
- Max scalar delta: `0.0`
- Max gradient delta: `0.0`
- Max BayesFilter AD-vs-FD delta: `1.0343861767125873e-07`
- Max FilterFlow AD-vs-FD delta: `1.0343861767125873e-07`

## Cell Table

| model | status | knobs | scalar delta | max gradient delta | BF FD delta | FF FD delta |
|---|---:|---|---:|---:|---:|---:|
| lgssm_2d_linear | `MATCHED` | `transition_matrix_scale` | `0.0` | `0.0` | `8.091749492677991e-12` | `8.091749492677991e-12` |
| sv_1d_synthetic | `MATCHED` | `gamma,beta` | `0.0` | `0.0` | `1.9265300466031476e-10` | `1.7599965929093742e-10` |
| range_bearing_2d_cv | `MATCHED` | `sigma_range` | `0.0` | `0.0` | `1.0343861767125873e-07` | `1.0343861767125873e-07` |

## Interpretation

BayesFilter and executable float64 FilterFlow agree on gradients of the same
fixed-noise, fixed-ancestor bootstrap scalar for the common LGSSM,
stochastic-volatility, and range-bearing model suite.  The gradient knobs are
explicit physical parameters: a transition-matrix scale for LGSSM,
`(gamma,beta)` for stochastic volatility, and range observation noise scale for
range-bearing.

This result is a branch replay gradient check.  Ancestor indices are fixed and
nondifferentiated, so the result does not test gradients through random
resampling, differentiable resampling, or any student repository.

## Non-Claims

- no filtering-algorithm correctness claim
- no implementation is treated as an oracle
- no random-number-generator equality claim
- no stochastic-resampler or differentiable-resampler correctness claim
- no gradient through random or discrete ancestor selection
- no student-repository tie-out claim
- no TT-filter correctness claim
- no paper-scale, HMC, DSGE, GPU, or production-readiness claim
