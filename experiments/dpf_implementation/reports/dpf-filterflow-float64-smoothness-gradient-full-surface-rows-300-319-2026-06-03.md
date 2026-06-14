# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [300, 320) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [300, 320) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `300` |
| `row_count` | `20` |
| `row_stop_exclusive` | `320` |
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
  "max_abs_gradient_delta": 0.2514907238964952,
  "max_relative_gradient_delta": 2.98244011632445e-05,
  "max_scalar_delta": 2.2036800828573178e-08,
  "rmse_max_abs_gradient_delta": 0.05731179175666465,
  "rmse_scalar_delta": 1.0792178243269565e-08,
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
      33.64295539331506
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      21649.129233829775,
      592.6394400735659
    ],
    "gradient_matrix": [
      [
        21649.129233829775,
        795.6874811993134
      ],
      [
        21015.44602513326,
        592.6394400735659
      ]
    ],
    "mean_log_likelihood": -162.16060225628502,
    "mesh_index": 300,
    "theta": [
      0.9894736842105263,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.69825123985564
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      15268.741902372634,
      -5.857191992899696
    ],
    "gradient_matrix": [
      [
        15268.741902372634,
        425.9919132695526
      ],
      [
        -13.090632724715945,
        -5.857191992899696
      ]
    ],
    "mean_log_likelihood": -140.7890137064227,
    "mesh_index": 319,
    "theta": [
      0.9894736842105263,
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
      3.6465943974465493
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      21649.129049353254,
      592.6394339847596
    ],
    "log_likelihoods": [
      -162.1606022432157
    ],
    "max_column_residual": 8.881784197001252e-15,
    "max_row_residual": 1.1588574468035517e-05,
    "mean_log_likelihood": -162.1606022432157,
    "mesh_index": 300,
    "resampling_count": 99,
    "theta": [
      0.9894736842105263,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.839511968005911
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      15268.741809195782,
      -5.857187663369185
    ],
    "log_likelihoods": [
      -140.78901370082227
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.2083726437239761e-05,
    "mean_log_likelihood": -140.78901370082227,
    "mesh_index": 319,
    "resampling_count": 99,
    "theta": [
      0.9894736842105263,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [300, 320) smoothness scalar and diagonal gradient surface. Max scalar delta: `2.2036800828573178e-08`. Max absolute gradient delta: `0.2514907238964952`.

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
