# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [100, 120) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [100, 120) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `100` |
| `row_count` | `20` |
| `row_stop_exclusive` | `120` |
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
  "max_abs_gradient_delta": 0.06487561568610545,
  "max_relative_gradient_delta": 5.457471905414558e-06,
  "max_scalar_delta": 1.7700813259580173e-08,
  "rmse_max_abs_gradient_delta": 0.014530313473312377,
  "rmse_scalar_delta": 8.962281600529447e-09,
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
      30.072300688139745
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -23976.028205016577,
      2541.9751586633006
    ],
    "gradient_matrix": [
      [
        -23976.028205016577,
        -1613.338582339016
      ],
      [
        42562.79539378033,
        2541.9751586633006
      ]
    ],
    "mean_log_likelihood": -217.75544834371144,
    "mesh_index": 100,
    "theta": [
      0.9631578947368421,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.174423793883975
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      7088.691648086452,
      1254.066078242996
    ],
    "gradient_matrix": [
      [
        7088.691648086452,
        509.34203331480535
      ],
      [
        22502.772590800796,
        1254.066078242996
      ]
    ],
    "mean_log_likelihood": -145.49088708743673,
    "mesh_index": 119,
    "theta": [
      0.9631578947368421,
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
      3.278417296391424
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -23976.030082335674,
      2541.9752320215744
    ],
    "log_likelihoods": [
      -217.75544833756717
    ],
    "max_column_residual": 8.881784197001252e-15,
    "max_row_residual": 1.0674305422231356e-05,
    "mean_log_likelihood": -217.75544833756717,
    "mesh_index": 100,
    "resampling_count": 99,
    "theta": [
      0.9631578947368421,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.790633032812296
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      7088.691512636923,
      1254.0661128098097
    ],
    "log_likelihoods": [
      -145.49088707881563
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.3128017531061076e-05,
    "mean_log_likelihood": -145.49088707881563,
    "mesh_index": 119,
    "resampling_count": 99,
    "theta": [
      0.9631578947368421,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [100, 120) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.7700813259580173e-08`. Max absolute gradient delta: `0.06487561568610545`.

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
