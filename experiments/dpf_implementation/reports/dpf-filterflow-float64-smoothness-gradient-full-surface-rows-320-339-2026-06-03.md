# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [320, 340) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [320, 340) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `320` |
| `row_count` | `20` |
| `row_stop_exclusive` | `340` |
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
  "max_abs_gradient_delta": 0.11795222763203128,
  "max_relative_gradient_delta": 4.739159990997975e-05,
  "max_scalar_delta": 2.4028395273489878e-08,
  "rmse_max_abs_gradient_delta": 0.026443605314614694,
  "rmse_scalar_delta": 1.069141775294404e-08,
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
      33.936610730285565
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      38338.0813249532,
      -134.2503121834768
    ],
    "gradient_matrix": [
      [
        38338.0813249532,
        1135.986536242187
      ],
      [
        -3219.123301093371,
        -134.2503121834768
      ]
    ],
    "mean_log_likelihood": -158.45330591767936,
    "mesh_index": 320,
    "theta": [
      0.9921052631578947,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.73093039905208
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      26531.867880682148,
      -280.15992792882577
    ],
    "gradient_matrix": [
      [
        26531.867880682148,
        603.3485715179709
      ],
      [
        -11759.534405073658,
        -280.15992792882577
      ]
    ],
    "mean_log_likelihood": -140.52879053663656,
    "mesh_index": 339,
    "theta": [
      0.9921052631578947,
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
      3.683627857072658
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      38338.08159079103,
      -134.2503184566547
    ],
    "log_likelihoods": [
      -158.45330589365096
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.184252292318888e-05,
    "mean_log_likelihood": -158.45330589365096,
    "mesh_index": 320,
    "resampling_count": 99,
    "theta": [
      0.9921052631578947,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.842821195702854
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      26531.867857193272,
      -280.15992952806937
    ],
    "log_likelihoods": [
      -140.52879053227966
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.201226189273541e-05,
    "mean_log_likelihood": -140.52879053227966,
    "mesh_index": 339,
    "resampling_count": 99,
    "theta": [
      0.9921052631578947,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [320, 340) smoothness scalar and diagonal gradient surface. Max scalar delta: `2.4028395273489878e-08`. Max absolute gradient delta: `0.11795222763203128`.

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
