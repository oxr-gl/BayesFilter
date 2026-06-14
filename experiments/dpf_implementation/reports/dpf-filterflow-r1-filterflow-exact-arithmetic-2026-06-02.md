# R1 Filterflow-Exact Arithmetic

## Decision

`r1_filterflow_exact_arithmetic_r1_match`

## Contract

This artifact compares BayesFilter against the local executable filterflow checkout only.
It does not assert correctness of either implementation.

## Arithmetic Policy

| Control | Value |
| --- | --- |
| `exact_path_dtype` | `tf.float32` |
| `distance_formula` | `filterflow xx - 2xy + yy with clipping` |
| `log_weight_policy` | `do not renormalize before transport; record residual` |
| `annealing_start` | `filterflow max_min(scaled_x, scaled_x)^2 without pre-clamp` |
| `fixed_target_sinkhorn` | `not used` |

## Cases

| Case | Status | Exact scalar delta | Exact max field delta | First failure |
| --- | --- | ---: | ---: | --- |
| `matched_control_generated_T100` | `pass` | `9.5367431640625e-07` | `6.67572021484375e-06` | `no_field_failure@None:[]` |
| `r1_prefix_T4` | `pass` | `0.0` | `4.656612873077393e-10` | `no_field_failure@None:[]` |
| `r1_filterflow_observation_path_T100` | `pass` | `0.0` | `4.656612873077393e-10` | `no_field_failure@None:[]` |

## BF64 Contrast

| Case | BF64 scalar delta | BF64 max field delta | BF64 first failure |
| --- | ---: | ---: | --- |
| `matched_control_generated_T100` | `6.720575727925393e-06` | `6.7110503643164066e-06` | `no_field_failure@None:[]` |
| `r1_prefix_T4` | `0.00014738302797923097` | `0.0001630433775972051` | `failed@3:['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` |
| `r1_filterflow_observation_path_T100` | `2.20523002743721` | `1.2030607901979238` | `failed@3:['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` |

## Source Audit

`passed`

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
- No correctness claim is made for either implementation.
- No production dtype default is concluded.
- No tolerance policy change is concluded.
