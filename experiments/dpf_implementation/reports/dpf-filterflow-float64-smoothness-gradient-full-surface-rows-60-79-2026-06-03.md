# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [60, 80) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [60, 80) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `60` |
| `row_count` | `20` |
| `row_stop_exclusive` | `80` |
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
  "max_abs_gradient_delta": 0.01310537319204741,
  "max_relative_gradient_delta": 1.947364671584783e-06,
  "max_scalar_delta": 1.5602353187205154e-08,
  "rmse_max_abs_gradient_delta": 0.004564766979144345,
  "rmse_scalar_delta": 8.620363450231415e-09,
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
      29.227092791729262
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      17056.176936026874,
      1491.8503131780267
    ],
    "gradient_matrix": [
      [
        17056.176936026874,
        1455.8061175099733
      ],
      [
        27401.145933934335,
        1491.8503131780267
      ]
    ],
    "mean_log_likelihood": -233.00753131036552,
    "mesh_index": 60,
    "theta": [
      0.9578947368421052,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.03277907065735
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      609.2208818533014,
      1845.1783312572757
    ],
    "gradient_matrix": [
      [
        609.2208818533014,
        112.94004721392123
      ],
      [
        29336.277500845717,
        1845.1783312572757
      ]
    ],
    "mean_log_likelihood": -146.87029091311808,
    "mesh_index": 79,
    "theta": [
      0.9578947368421052,
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
      3.226471055663624
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      17056.17684389893,
      1491.8503196201932
    ],
    "log_likelihoods": [
      -233.00753130711
    ],
    "max_column_residual": 1.4210854715202004e-14,
    "max_row_residual": 1.0748082634126632e-05,
    "mean_log_likelihood": -233.00753130711,
    "mesh_index": 60,
    "resampling_count": 99,
    "theta": [
      0.9578947368421052,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.7780641018333947
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      609.2212914281937,
      1845.1783149219402
    ],
    "log_likelihoods": [
      -146.8702909031629
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.3412391612677155e-05,
    "mean_log_likelihood": -146.8702909031629,
    "mesh_index": 79,
    "resampling_count": 99,
    "theta": [
      0.9578947368421052,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [60, 80) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.5602353187205154e-08`. Max absolute gradient delta: `0.01310537319204741`.

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
