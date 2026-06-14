# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [140, 160) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [140, 160) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `140` |
| `row_count` | `20` |
| `row_stop_exclusive` | `160` |
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
  "max_abs_gradient_delta": 0.04836560415378699,
  "max_relative_gradient_delta": 1.2181596215918884e-05,
  "max_scalar_delta": 1.5636089756299043e-08,
  "rmse_max_abs_gradient_delta": 0.01662209491670388,
  "rmse_scalar_delta": 9.517708342280896e-09,
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
      30.898744257962342
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      34640.0615705185,
      601.6805867663996
    ],
    "gradient_matrix": [
      [
        34640.0615705185,
        2017.8327175021257
      ],
      [
        13644.235167936155,
        601.6805867663996
      ]
    ],
    "mean_log_likelihood": -203.87231028876317,
    "mesh_index": 140,
    "theta": [
      0.968421052631579,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.30386971793725
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      1446.5205147416684,
      1238.9862251101902
    ],
    "gradient_matrix": [
      [
        1446.5205147416684,
        172.0254367135353
      ],
      [
        24702.382280896232,
        1238.9862251101902
      ]
    ],
    "mean_log_likelihood": -144.2591141807239,
    "mesh_index": 159,
    "theta": [
      0.968421052631579,
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
      3.3415063264220324
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      34640.05909156416,
      601.6809714606931
    ],
    "log_likelihoods": [
      -203.87231027984484
    ],
    "max_column_residual": 8.881784197001252e-15,
    "max_row_residual": 1.2420096436538408e-05,
    "mean_log_likelihood": -203.87231027984484,
    "mesh_index": 140,
    "resampling_count": 99,
    "theta": [
      0.968421052631579,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8023025126953556
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      1446.520321318961,
      1238.9862344478202
    ],
    "log_likelihoods": [
      -144.25911417368127
    ],
    "max_column_residual": 5.329070518200751e-15,
    "max_row_residual": 1.2923995275970768e-05,
    "mean_log_likelihood": -144.25911417368127,
    "mesh_index": 159,
    "resampling_count": 99,
    "theta": [
      0.968421052631579,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [140, 160) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.5636089756299043e-08`. Max absolute gradient delta: `0.04836560415378699`.

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
