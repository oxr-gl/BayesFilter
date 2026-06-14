# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [220, 240) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [220, 240) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `220` |
| `row_count` | `20` |
| `row_stop_exclusive` | `240` |
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
  "max_abs_gradient_delta": 0.44026599840617564,
  "max_relative_gradient_delta": 5.379982982351086e-05,
  "max_scalar_delta": 1.7788721606848412e-08,
  "rmse_max_abs_gradient_delta": 0.09962914822339294,
  "rmse_scalar_delta": 1.0590833985119382e-08,
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
      32.37870982611706
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      28996.785321803578,
      678.318542654411
    ],
    "gradient_matrix": [
      [
        28996.785321803578,
        847.6405014569506
      ],
      [
        11447.24641396358,
        678.318542654411
      ]
    ],
    "mean_log_likelihood": -180.2941359974748,
    "mesh_index": 220,
    "theta": [
      0.9789473684210526,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.52718570321805
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      8183.408755203472,
      350.63189148491483
    ],
    "gradient_matrix": [
      [
        8183.408755203472,
        109.38849222320897
      ],
      [
        5912.272975723326,
        350.63189148491483
      ]
    ],
    "mean_log_likelihood": -142.2210489394442,
    "mesh_index": 239,
    "theta": [
      0.9789473684210526,
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
      3.486028251059707
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      28996.78447193709,
      678.3198886572749
    ],
    "log_likelihoods": [
      -180.29413598998408
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.1941445639873649e-05,
    "mean_log_likelihood": -180.29413598998408,
    "mesh_index": 220,
    "resampling_count": 99,
    "theta": [
      0.9789473684210526,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.822993749352573
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      8183.849021201878,
      350.60801075229114
    ],
    "log_likelihoods": [
      -142.2210489323514
    ],
    "max_column_residual": 8.881784197001252e-15,
    "max_row_residual": 1.2743525138692036e-05,
    "mean_log_likelihood": -142.2210489323514,
    "mesh_index": 239,
    "resampling_count": 99,
    "theta": [
      0.9789473684210526,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [220, 240) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.7788721606848412e-08`. Max absolute gradient delta: `0.44026599840617564`.

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
