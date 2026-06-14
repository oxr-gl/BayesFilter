# Filterflow Float64 Branch Reference Result

## Decision

`filterflow_float64_branch_reference_ready`

## Summary

| Key | Value |
| --- | --- |
| `branch_dtype` | `float64` |
| `kalman_row_count` | `3` |
| `stochastic_row_count` | `12` |
| `finite` | `True` |
| `kalman_all_within_tolerance` | `True` |
| `stochastic_all_within_tolerance` | `True` |
| `max_kalman_abs_delta` | `5.159033200641261e-09` |
| `max_stochastic_abs_delta` | `1.6513289069486348e-08` |

## Reference Policy

| Key | Value |
| --- | --- |
| `future_comparator` | `filterflow_float64_reference_branch` |
| `branch` | `bayesfilter-py311-float64-reference` |
| `commit` | `ff0048060fd4cff43dbea606d14275e40e2ac084` |
| `upstream_base` | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| `dtype` | `float64` |
| `local_reference_status` | `BayesFilter audit reference code, not pristine upstream` |
| `transition_covariance` | `I_2 executable reproduction setting` |
| `fixed_target_sinkhorn` | `local BayesFilter diagnostic/comparator only` |

## Filterflow Branch

| Key | Value |
| --- | --- |
| `branch` | `bayesfilter-py311-float64-reference` |
| `commit` | `ff0048060fd4cff43dbea606d14275e40e2ac084` |
| `status` | `## bayesfilter-py311-float64-reference` |
| `diff_summary` | `clean` |

## Kalman Comparison To Prior Probe

| theta | branch | prior | delta | within tol |
| ---: | ---: | ---: | ---: | --- |
| 0.25 | -3.05175477 | -3.05175478 | 5.159e-09 | True |
| 0.5 | -2.95832537 | -2.95832537 | 3.101e-09 | True |
| 0.75 | -3.01466259 | -3.01466259 | 1.639e-09 | True |

## Table Comparison To Prior Probe

| method | eps | theta | branch mean error | prior mean error | delta | within tol |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| filterflow_pf | N/A | 0.25 | -1.03736363 | -1.03736363 | -4.878e-09 | True |
| filterflow_pf | N/A | 0.5 | -0.862021771 | -0.862021761 | -9.687e-09 | True |
| filterflow_pf | N/A | 0.75 | -0.912981804 | -0.912981789 | -1.530e-08 | True |
| filterflow_regularized | 0.25 | 0.25 | -1.03962816 | -1.03962815 | -5.498e-09 | True |
| filterflow_regularized | 0.25 | 0.5 | -0.864563132 | -0.864563121 | -1.038e-08 | True |
| filterflow_regularized | 0.25 | 0.75 | -0.914134726 | -0.914134717 | -8.743e-09 | True |
| filterflow_regularized | 0.5 | 0.25 | -1.03981871 | -1.0398187 | -5.306e-09 | True |
| filterflow_regularized | 0.5 | 0.5 | -0.863700945 | -0.863700935 | -9.902e-09 | True |
| filterflow_regularized | 0.5 | 0.75 | -0.914230458 | -0.914230443 | -1.464e-08 | True |
| filterflow_regularized | 0.75 | 0.25 | -1.03987302 | -1.03987301 | -5.266e-09 | True |
| filterflow_regularized | 0.75 | 0.5 | -0.862901803 | -0.862901794 | -9.740e-09 | True |
| filterflow_regularized | 0.75 | 0.75 | -0.914533154 | -0.914533138 | -1.651e-08 | True |

## Non-Implications

- No production readiness claim.
- No pristine upstream filterflow claim.
- No paper correctness claim.
- No posterior correctness claim.
- No gradient correctness claim.
- No public API readiness claim.
- No monograph claim.
- No DSGE/NAWM validation claim.
