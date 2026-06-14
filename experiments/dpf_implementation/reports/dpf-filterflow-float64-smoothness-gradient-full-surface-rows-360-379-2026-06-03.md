# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [360, 380) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [360, 380) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `360` |
| `row_count` | `20` |
| `row_stop_exclusive` | `380` |
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
  "max_abs_gradient_delta": 0.01831464579117892,
  "max_relative_gradient_delta": 5.947807008092886e-06,
  "max_scalar_delta": 1.2431968343662447e-08,
  "rmse_max_abs_gradient_delta": 0.005445763112452305,
  "rmse_scalar_delta": 7.839938253453954e-09,
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
      34.48911151891793
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      10773.064482574353,
      489.24011079843183
    ],
    "gradient_matrix": [
      [
        10773.064482574353,
        412.5895546789448
      ],
      [
        24810.609411437646,
        489.24011079843183
      ]
    ],
    "mean_log_likelihood": -151.98514533449534,
    "mesh_index": 360,
    "theta": [
      0.9973684210526316,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.788579898270406
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      35554.72545300352,
      -590.5831530772856
    ],
    "gradient_matrix": [
      [
        35554.72545300352,
        734.2525747830978
      ],
      [
        -26206.03908866265,
        -590.5831530772856
      ]
    ],
    "mean_log_likelihood": -140.11585039394055,
    "mesh_index": 379,
    "theta": [
      0.9973684210526316,
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
      3.7455521054490113
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      10773.065022510413,
      489.24009651321785
    ],
    "log_likelihoods": [
      -151.98514532206337
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.2730665192806079e-05,
    "mean_log_likelihood": -151.98514532206337,
    "mesh_index": 360,
    "resampling_count": 99,
    "theta": [
      0.9973684210526316,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8481726569498433
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      35554.725773807346,
      -590.5831293902701
    ],
    "log_likelihoods": [
      -140.11585039071235
    ],
    "max_column_residual": 4.440892098500626e-15,
    "max_row_residual": 1.2328272884110092e-05,
    "mean_log_likelihood": -140.11585039071235,
    "mesh_index": 379,
    "resampling_count": 99,
    "theta": [
      0.9973684210526316,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [360, 380) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.2431968343662447e-08`. Max absolute gradient delta: `0.01831464579117892`.

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
