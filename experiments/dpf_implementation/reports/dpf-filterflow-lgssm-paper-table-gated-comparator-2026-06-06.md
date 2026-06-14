# LGSSM Paper-Table Gated Comparator

## Decision

`lgssm_table_full_within_filterflow_mc_band`

## Contract

- Mode: `full`
- T: `150`
- Particles: `25`
- Replications: `100`
- Theta grid: `[0.25, 0.5, 0.75]`
- Epsilon grid: `[0.25, 0.5, 0.75]`
- Solver: `{'scaling': 0.9, 'convergence_threshold': 1e-08, 'max_iter': 500}`

## Kalman Alignment

- Max absolute log-likelihood delta: `2.274e-13`
- Within tolerance: `True`

## Summary

- Executed rows: `9/9`
- All within one FilterFlow SD: `True`
- All within two FilterFlow SE: `True`
- Max absolute per-time error delta: `0.03441404318951735`
- Max BayesFilter residual: `0.15970622641208965`
- Rows exceeding residual diagnostic tolerance: `9`
- Residual policy: `diagnostic-only after same-state localization showed executable FilterFlow shares the smoke residual breach`

## Comparison

| eps | theta | FilterFlow mean | BayesFilter mean | delta | FF SD | within 1 SD | BF residual | residual flag | BF iter | status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | --- |
| 0.25 | 0.25 | -1.03977 | -1.04872 | -0.00895299 | 0.171968 | True | 0.159706 | True | 52 | `executed` |
| 0.25 | 0.5 | -0.864707 | -0.874145 | -0.00943737 | 0.173091 | True | 0.101431 | True | 51 | `executed` |
| 0.25 | 0.75 | -0.914302 | -0.945177 | -0.0308749 | 0.189317 | True | 0.138119 | True | 50 | `executed` |
| 0.5 | 0.25 | -1.03984 | -1.0491 | -0.00926673 | 0.171497 | True | 0.0185991 | True | 41 | `executed` |
| 0.5 | 0.5 | -0.863692 | -0.876192 | -0.0124999 | 0.172954 | True | 0.00562092 | True | 41 | `executed` |
| 0.5 | 0.75 | -0.914297 | -0.945264 | -0.0309667 | 0.186296 | True | 0.00577246 | True | 41 | `executed` |
| 0.75 | 0.25 | -1.03988 | -1.04926 | -0.00938356 | 0.170963 | True | 0.00131276 | True | 38 | `executed` |
| 0.75 | 0.5 | -0.862899 | -0.876957 | -0.0140581 | 0.172884 | True | 0.00859321 | True | 38 | `executed` |
| 0.75 | 0.75 | -0.914553 | -0.948967 | -0.034414 | 0.185335 | True | 0.00206699 | True | 38 | `executed` |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No general nonlinear-SSM validity is concluded.
- No claim that finite relaxed OT is categorical PF is concluded.
- No claim that patched filterflow is untouched upstream code is concluded.
