# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [200, 220) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [200, 220) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `200` |
| `row_count` | `20` |
| `row_stop_exclusive` | `220` |
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
  "max_abs_gradient_delta": 0.5853975304144114,
  "max_relative_gradient_delta": 3.964940104564585e-05,
  "max_scalar_delta": 1.768029278537142e-08,
  "rmse_max_abs_gradient_delta": 0.13148534009239074,
  "rmse_scalar_delta": 1.0199731731915096e-08,
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
      32.03436148071077
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      14764.34737918185,
      1038.2509834276939
    ],
    "gradient_matrix": [
      [
        14764.34737918185,
        542.5478505018825
      ],
      [
        22080.10960923376,
        1038.2509834276939
      ]
    ],
    "mean_log_likelihood": -185.65276137162232,
    "mesh_index": 200,
    "theta": [
      0.9763157894736842,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.47553918664449
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      6790.513171800634,
      419.5131195276923
    ],
    "gradient_matrix": [
      [
        6790.513171800634,
        267.29570124576304
      ],
      [
        10063.530985754714,
        419.5131195276923
      ]
    ],
    "mean_log_likelihood": -142.6789965663768,
    "mesh_index": 219,
    "theta": [
      0.9763157894736842,
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
      3.4467542065778742
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      14764.932776712265,
      1038.2458007295725
    ],
    "log_likelihoods": [
      -185.6527613639943
    ],
    "max_column_residual": 1.0658141036401503e-14,
    "max_row_residual": 1.2483539364893659e-05,
    "mean_log_likelihood": -185.6527613639943,
    "mesh_index": 200,
    "resampling_count": 99,
    "theta": [
      0.9763157894736842,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.818113069279058
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      6790.512114149763,
      419.51316594112836
    ],
    "log_likelihoods": [
      -142.6789965597784
    ],
    "max_column_residual": 5.329070518200751e-15,
    "max_row_residual": 1.273079134422872e-05,
    "mean_log_likelihood": -142.6789965597784,
    "mesh_index": 219,
    "resampling_count": 99,
    "theta": [
      0.9763157894736842,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [200, 220) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.768029278537142e-08`. Max absolute gradient delta: `0.5853975304144114`.

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
