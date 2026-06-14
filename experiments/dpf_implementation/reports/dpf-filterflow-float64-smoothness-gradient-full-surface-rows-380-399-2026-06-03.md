# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [380, 400) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [380, 400) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `380` |
| `row_count` | `20` |
| `row_stop_exclusive` | `400` |
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
  "max_abs_gradient_delta": 0.19238746349947178,
  "max_relative_gradient_delta": 2.7575876528499674e-05,
  "max_scalar_delta": 1.1149467127324897e-08,
  "rmse_max_abs_gradient_delta": 0.04628274063742594,
  "rmse_scalar_delta": 6.932468083270764e-09,
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
      34.74228753584714
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -4060.4815654199333,
      770.5989753447385
    ],
    "gradient_matrix": [
      [
        -4060.4815654199333,
        -73.50851398780304
      ],
      [
        34653.46662015521,
        770.5989753447385
      ]
    ],
    "mean_log_likelihood": -149.2332518403611,
    "mesh_index": 380,
    "theta": [
      1.0,
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
    "mesh_index": 399,
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
      3.769363439183099
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -4060.4814447880713,
      770.5989841463539
    ],
    "log_likelihoods": [
      -149.23325182921164
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.347932660755724e-05,
    "mean_log_likelihood": -149.23325182921164,
    "mesh_index": 380,
    "resampling_count": 99,
    "theta": [
      1.0,
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
    "mesh_index": 399,
    "resampling_count": 99,
    "theta": [
      1.0,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [380, 400) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.1149467127324897e-08`. Max absolute gradient delta: `0.19238746349947178`.

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
