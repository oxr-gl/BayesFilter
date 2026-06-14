# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_surface_pass | 16 of 16 bounded mesh rows within gradient tolerance | pass | bounded mesh only; no analytic-gradient correctness is concluded | rerun on the full mesh_size=20 surface or add Kalman finite-difference context | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `mesh_size` | `4` |
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
  "finite_rows": 16,
  "first_failure": {
    "status": "no_failure"
  },
  "gradient_rows_within_tolerance": 16,
  "implementation_agreement": true,
  "max_abs_gradient_delta": 0.1233334128792194,
  "max_relative_gradient_delta": 1.4123389604429983e-05,
  "max_scalar_delta": 1.4924950164640904e-08,
  "rmse_max_abs_gradient_delta": 0.031213201130162273,
  "rmse_scalar_delta": 8.905779290840865e-09,
  "row_count": 16,
  "scalar_rows_within_tolerance": 16
}
```

## First And Last Rows

### FilterFlow

```json
{
  "first_row": {
    "final_ess": [
      27.982214166117192
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      18935.6850725171,
      2073.5151524806142
    ],
    "gradient_matrix": [
      [
        18935.6850725171,
        1678.5016416026954
      ],
      [
        31902.57896987284,
        2073.5151524806142
      ]
    ],
    "mean_log_likelihood": -258.58524847172157,
    "mesh_index": 0,
    "theta": [
      0.95,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.81367996831653
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      35791.40398997006,
      -403.76052378891296
    ],
    "gradient_matrix": [
      [
        35791.40398997006,
        799.7043386742762
      ],
      [
        -13985.206967897842,
        -403.76052378891296
      ]
    ],
    "mean_log_likelihood": -139.95535907215373,
    "mesh_index": 15,
    "theta": [
      1.0,
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
      3.17850829839299
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      18935.685049167038,
      2073.51515897136
    ],
    "log_likelihoods": [
      -258.5852484624214
    ],
    "max_column_residual": 2.1316282072803006e-14,
    "max_row_residual": 1.0943960801146346e-05,
    "mean_log_likelihood": -258.5852484624214,
    "mesh_index": 0,
    "resampling_count": 99,
    "theta": [
      0.95,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8497426895828952
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      35791.40342711416,
      -403.76051821822625
    ],
    "log_likelihoods": [
      -139.95535907215407
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.1939412243755498e-05,
    "mean_log_likelihood": -139.95535907215407,
    "mesh_index": 15,
    "resampling_count": 99,
    "theta": [
      1.0,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the bounded smoothness scalar and diagonal gradient surface. Max scalar delta: `1.4924950164640904e-08`. Max absolute gradient delta: `0.1233334128792194`.

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
- No full mesh_size=20 surface agreement is concluded.
- No production dtype default is concluded.
- Finite gradients alone are smoke evidence only.
