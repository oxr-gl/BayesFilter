# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [180, 200) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [180, 200) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `180` |
| `row_count` | `20` |
| `row_stop_exclusive` | `200` |
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
  "max_abs_gradient_delta": 0.10729067053580366,
  "max_relative_gradient_delta": 5.270826714854101e-05,
  "max_scalar_delta": 1.862991894086008e-08,
  "rmse_max_abs_gradient_delta": 0.029826011574874908,
  "rmse_scalar_delta": 1.026030556634143e-08,
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
      31.673537302382496
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      34263.8397384544,
      253.90625249110005
    ],
    "gradient_matrix": [
      [
        34263.8397384544,
        1867.134006842051
      ],
      [
        7979.012062353852,
        253.90625249110005
      ]
    ],
    "mean_log_likelihood": -191.36566937176588,
    "mesh_index": 180,
    "theta": [
      0.9736842105263158,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.421548293253416
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      12486.249262867084,
      291.7064808724655
    ],
    "gradient_matrix": [
      [
        12486.249262867084,
        553.4372245316205
      ],
      [
        7074.696606879705,
        291.7064808724655
      ]
    ],
    "mean_log_likelihood": -143.16750540883245,
    "mesh_index": 199,
    "theta": [
      0.9736842105263158,
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
      3.4106099018133547
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      34263.83951281415,
      253.9062601559571
    ],
    "log_likelihoods": [
      -191.3656693645626
    ],
    "max_column_residual": 1.0658141036401503e-14,
    "max_row_residual": 1.2301667109526626e-05,
    "mean_log_likelihood": -191.3656693645626,
    "mesh_index": 180,
    "resampling_count": 99,
    "theta": [
      0.9736842105263158,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8131435011020205
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      12486.249216017131,
      291.7064778405013
    ],
    "log_likelihoods": [
      -143.1675054038722
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.2693550592635106e-05,
    "mean_log_likelihood": -143.1675054038722,
    "mesh_index": 199,
    "resampling_count": 99,
    "theta": [
      0.9736842105263158,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [180, 200) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.862991894086008e-08`. Max absolute gradient delta: `0.10729067053580366`.

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
