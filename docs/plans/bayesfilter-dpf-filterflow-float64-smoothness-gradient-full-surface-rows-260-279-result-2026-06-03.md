# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [260, 280) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [260, 280) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

## Scalar Contract

| Key | Value |
| --- | --- |
| `filterflow_scalar` | `tf.reduce_mean(final_state.log_likelihoods)` |
| `bayesfilter_scalar` | `tf.reduce_mean(log_likelihoods)` |
| `resampling_correction` | `False` |
| `batch_size_note` | `batch_size=1 makes mean and single-batch total equal` |
| `per_time_normalization` | `not used` |
| `sign` | `positive log-likelihood convention as emitted by filterflow` |

## Gradient Contract

| Key | Value |
| --- | --- |
| `filterflow_gradient` | `tf.linalg.diag_part(tape.gradient(scalar, transition_matrix_variable))` |
| `bayesfilter_gradient` | `tape.gradient(scalar, theta_variable)` |
| `theta_parameterization` | `transition_matrix=diag(theta)+[[0,1],[0,0]]` |
| `correction_term` | `not included` |
| `finite_difference_status` | `not primary in this runner` |

## Model Contract

| Key | Value |
| --- | --- |
| `model` | `filterflow_simple_linear_smoothness_constant_velocity_lgssm` |
| `transition_matrix` | `A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]` |
| `transition_covariance` | `[[0.3333333333333333, 0.5], [0.5, 1.0]]` |
| `observation_matrix` | `[[1.0, 0.0]]` |
| `observation_covariance` | `[[0.01]]` |
| `T` | `100` |
| `batch_size` | `1` |
| `num_particles` | `50` |
| `mesh_size` | `20` |
| `row_start` | `260` |
| `row_count` | `20` |
| `row_stop_exclusive` | `280` |
| `script_default_mesh_size` | `20` |
| `data_seed` | `123` |
| `filter_seed` | `1234` |
| `epsilon` | `0.25` |
| `scaling` | `0.85` |
| `convergence_threshold` | `1e-06` |
| `max_iter` | `500` |
| `resampling_neff` | `0.9999` |
| `optimal_proposal` | `True` |
| `dtype` | `float64` |

## Comparison Summary

```json
{
  "finite_rows": 20,
  "first_failure": {
    "status": "no_failure"
  },
  "gradient_rows_within_tolerance": 20,
  "implementation_agreement": true,
  "max_abs_gradient_delta": 0.008013652774025104,
  "max_relative_gradient_delta": 6.80244050939685e-07,
  "max_scalar_delta": 1.8405842183710774e-08,
  "rmse_max_abs_gradient_delta": 0.002132129809619098,
  "rmse_scalar_delta": 1.0589851071299675e-08,
  "row_count": 20,
  "scalar_rows_within_tolerance": 20
}
```

## First And Last Rows

### FilterFlow

```json
{
  "first_row": {
    "final_ess": [
      33.028997581274815
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      3839.9518171921227,
      935.8343394038004
    ],
    "gradient_matrix": [
      [
        3839.9518171921227,
        221.18862691901379
      ],
      [
        29250.71596275558,
        935.8343394038004
      ]
    ],
    "mean_log_likelihood": -170.57202160685895,
    "mesh_index": 260,
    "theta": [
      0.9842105263157894,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.619513114350525
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      11780.555468225106,
      16.272519387753857
    ],
    "gradient_matrix": [
      [
        11780.555468225106,
        198.1943374739008
      ],
      [
        -2929.9264801923723,
        16.272519387753857
      ]
    ],
    "mean_log_likelihood": -141.42666751457472,
    "mesh_index": 279,
    "theta": [
      0.9842105263157894,
      1.0
    ]
  }
}
```

### BayesFilter

```json
{
  "first_row": {
    "final_log_neff": [
      3.5670076113131115
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      3839.9534768910357,
      935.8342618051577
    ],
    "log_likelihoods": [
      -170.57202159706983
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.2405007401961043e-05,
    "mean_log_likelihood": -170.57202159706983,
    "mesh_index": 260,
    "resampling_count": 99,
    "theta": [
      0.9842105263157894,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8319081441492573
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      11780.547454572332,
      16.273527110748354
    ],
    "log_likelihoods": [
      -141.42666750967382
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.277776153685295e-05,
    "mean_log_likelihood": -141.42666750967382,
    "mesh_index": 279,
    "resampling_count": 99,
    "theta": [
      0.9842105263157894,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [260, 280) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.8405842183710774e-08`. Max absolute gradient delta: `0.008013652774025104`.

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
- No analytic smoothness-gradient correctness is concluded.
- No production dtype default is concluded.
- Finite gradients alone are smoke evidence only.
