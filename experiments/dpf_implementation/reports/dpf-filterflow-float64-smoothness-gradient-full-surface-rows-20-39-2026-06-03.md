# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [20, 40) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [20, 40) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `20` |
| `row_count` | `20` |
| `row_stop_exclusive` | `40` |
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
  "max_abs_gradient_delta": 0.017246467186851078,
  "max_relative_gradient_delta": 1.3245212628022567e-06,
  "max_scalar_delta": 1.6371387800973025e-08,
  "rmse_max_abs_gradient_delta": 0.004104636846019011,
  "rmse_scalar_delta": 7.81364749680405e-09,
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
      28.391576548790745
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      15542.8750987455,
      1927.925488161385
    ],
    "gradient_matrix": [
      [
        15542.8750987455,
        1153.181917193024
      ],
      [
        29540.9923297234,
        1927.925488161385
      ]
    ],
    "mean_log_likelihood": -249.6973540621534,
    "mesh_index": 20,
    "theta": [
      0.9526315789473684,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      34.88067923983173
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      13020.90624831734,
      1219.1898692317277
    ],
    "gradient_matrix": [
      [
        13020.90624831734,
        717.8349410674832
      ],
      [
        16567.204647616316,
        1219.1898692317277
      ]
    ],
    "mean_log_likelihood": -148.38991206667305,
    "mesh_index": 39,
    "theta": [
      0.9526315789473684,
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
      3.190883777022573
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      15542.877104755882,
      1927.9254986876656
    ],
    "log_likelihoods": [
      -249.69735405672827
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.0669978714683559e-05,
    "mean_log_likelihood": -249.69735405672827,
    "mesh_index": 20,
    "resampling_count": 99,
    "theta": [
      0.9526315789473684,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.763906918712234
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      13020.923494784527,
      1219.1955439706437
    ],
    "log_likelihoods": [
      -148.38991205798752
    ],
    "max_column_residual": 5.329070518200751e-15,
    "max_row_residual": 1.3682192336883503e-05,
    "mean_log_likelihood": -148.38991205798752,
    "mesh_index": 39,
    "resampling_count": 99,
    "theta": [
      0.9526315789473684,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [20, 40) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.6371387800973025e-08`. Max absolute gradient delta: `0.017246467186851078`.

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
