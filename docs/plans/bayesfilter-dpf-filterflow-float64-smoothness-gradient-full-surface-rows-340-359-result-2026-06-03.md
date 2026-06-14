# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [340, 360) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [340, 360) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `340` |
| `row_count` | `20` |
| `row_stop_exclusive` | `360` |
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
  "max_abs_gradient_delta": 0.004515929535045871,
  "max_relative_gradient_delta": 1.0859564828721587e-06,
  "max_scalar_delta": 1.520038495073095e-08,
  "rmse_max_abs_gradient_delta": 0.0011053809815573376,
  "rmse_scalar_delta": 8.98931287708342e-09,
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
      34.22069343958061
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      31724.21026833168,
      4.427976469267573
    ],
    "gradient_matrix": [
      [
        31724.21026833168,
        896.3683647925723
      ],
      [
        283.7325793344745,
        4.427976469267573
      ]
    ],
    "mean_log_likelihood": -155.05155184867397,
    "mesh_index": 340,
    "theta": [
      0.9947368421052631,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.76065949446108
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      34031.54484277105,
      -384.2299067018334
    ],
    "gradient_matrix": [
      [
        34031.54484277105,
        928.8212620624788
      ],
      [
        -12039.522321221988,
        -384.2299067018334
      ]
    ],
    "mean_log_likelihood": -140.30606091504978,
    "mesh_index": 359,
    "theta": [
      0.9947368421052631,
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
      3.717098043051042
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      31724.210082469282,
      4.427981950580623
    ],
    "log_likelihoods": [
      -155.05155183347358
    ],
    "max_column_residual": 5.329070518200751e-15,
    "max_row_residual": 1.229537487557053e-05,
    "mean_log_likelihood": -155.05155183347358,
    "mesh_index": 340,
    "resampling_count": 99,
    "theta": [
      0.9947368421052631,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8457061206557186
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      34031.5448021861,
      -384.229906814583
    ],
    "log_likelihoods": [
      -140.30606091166635
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.203066264054975e-05,
    "mean_log_likelihood": -140.30606091166635,
    "mesh_index": 359,
    "resampling_count": 99,
    "theta": [
      0.9947368421052631,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [340, 360) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.520038495073095e-08`. Max absolute gradient delta: `0.004515929535045871`.

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
