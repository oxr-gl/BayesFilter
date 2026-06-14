# 1D LGSSM Step Gradient Comparison

## Decision

`one_d_lgssm_step_gradient_filterflow_contract_matches_fd_veto`

## Setup

| Key | Value |
| --- | --- |
| theta0 | `0.7` |
| horizon | `2` |
| particles | `4` |
| Q | `0.04` |
| R | `0.04` |
| ESS threshold | `3.9996` |
| epsilon | `0.25` |
| scaling | `0.9` |

This report evidences matched fixed numeric inputs, same scalar ledger,
matched executable transport output, and AD-vs-finite-difference
mismatch for the same scalar. It does not verify or compare
filterflow's internal annealing iteration count, epsilon schedule,
or convergence trajectory.

## Scalar And Gradient

| Metric | BayesFilter | filterflow | delta |
| --- | ---: | ---: | ---: |
| total scalar | `0.06241077425770425` | `0.062410712242126465` | `6.201557778418021e-08` |
| GradientTape gradient | `-1.7820385507243621` | `-1.7820383310317993` | `2.1969256280840455e-07` |
| finite-difference gradient | `-1.6753548204218038` | `-1.6754865646362305` | `0.0001317442144266323` |

## Max Step-Ledger Deltas

| Field | max abs delta | tolerance |
| --- | ---: | ---: |
| `predicted_particles` | `4.7683715642676816e-08` | `5e-05` |
| `observation_log_likelihoods` | `1.833844299525822e-06` | `5e-05` |
| `normalized_log_weights` | `1.980896389142117e-06` | `5e-05` |
| `transport_cost_matrix` | `3.5174783219460437e-07` | `5e-05` |
| `transport_matrix` | `1.487370374642083e-07` | `5e-05` |
| `post_transport_particles` | `4.768371586472142e-08` | `5e-05` |
| `per_step_log_normalizer` | `3.165210882283276e-08` | `5e-05` |
| `row_residual` | `7.853376371436127e-08` | `0.0001` |
| `column_residual` | `1.1920928910669204e-07` | `0.0001` |

## Pass Status

| Check | Status |
| --- | --- |
| `trigger_match` | `True` |
| `expected_trigger_pattern` | `True` |
| `finite_values` | `True` |
| `scalar_within_tolerance` | `True` |
| `gradient_within_tolerance` | `True` |
| `bayesfilter_gradient_fd_within_tolerance` | `False` |
| `filterflow_gradient_fd_within_tolerance` | `False` |
| `ledger_within_tolerance` | `True` |
| `absolute_residuals_within_tolerance` | `True` |

## Absolute Residuals

| Field | value | tolerance |
| --- | ---: | ---: |
| `bayesfilter_max_row_residual` | `3.77402173978858e-06` | `0.0001` |
| `bayesfilter_max_column_residual` | `4.440892098500626e-16` | `0.0001` |
| `filterflow_max_row_residual` | `3.6954879760742188e-06` | `0.0001` |
| `filterflow_max_column_residual` | `1.1920928955078125e-07` | `0.0001` |

## Transport Diagnostic Availability

| Diagnostic | BayesFilter | filterflow | Comparison status |
| --- | --- | --- | --- |
| triggered-step iteration count | `62.0` | not available from this wrapper | explanatory only; not compared |
| epsilon schedule | not serialized | not serialized | not compared |
| convergence trajectory | not serialized | not serialized | not compared |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No gradient correctness beyond this fixed 1D scalar fixture is concluded.
