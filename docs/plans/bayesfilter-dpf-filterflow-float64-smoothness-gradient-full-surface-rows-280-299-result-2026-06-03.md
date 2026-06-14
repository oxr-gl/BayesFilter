# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [280, 300) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [280, 300) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `280` |
| `row_count` | `20` |
| `row_stop_exclusive` | `300` |
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
  "max_abs_gradient_delta": 0.0038912757045181934,
  "max_relative_gradient_delta": 1.0660467917753994e-06,
  "max_scalar_delta": 1.973154439838254e-08,
  "rmse_max_abs_gradient_delta": 0.0012402833657648787,
  "rmse_scalar_delta": 1.0857628728416418e-08,
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
      33.338924931003724
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      11002.753020484948,
      901.998939708931
    ],
    "gradient_matrix": [
      [
        11002.753020484948,
        72.55820989638397
      ],
      [
        23673.15431670925,
        901.998939708931
      ]
    ],
    "mean_log_likelihood": -166.20462258390026,
    "mesh_index": 280,
    "theta": [
      0.9868421052631579,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.66082732625865
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      16713.629071923588,
      -75.92690476580252
    ],
    "gradient_matrix": [
      [
        16713.629071923588,
        339.3176912908675
      ],
      [
        -7450.446583972452,
        -75.92690476580252
      ]
    ],
    "mean_log_likelihood": -141.08989313411013,
    "mesh_index": 299,
    "theta": [
      0.9868421052631579,
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
      3.607354997427915
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      11002.75345449366,
      901.9989230777643
    ],
    "log_likelihoods": [
      -166.2046225724012
    ],
    "max_column_residual": 5.329070518200751e-15,
    "max_row_residual": 1.1867820381095129e-05,
    "mean_log_likelihood": -166.2046225724012,
    "mesh_index": 280,
    "resampling_count": 99,
    "theta": [
      0.9868421052631579,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8358855469091737
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      16713.629520712373,
      -75.92692483496049
    ],
    "log_likelihoods": [
      -141.0898931290048
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.2354350577670203e-05,
    "mean_log_likelihood": -141.0898931290048,
    "mesh_index": 299,
    "resampling_count": 99,
    "theta": [
      0.9868421052631579,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [280, 300) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.973154439838254e-08`. Max absolute gradient delta: `0.0038912757045181934`.

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
