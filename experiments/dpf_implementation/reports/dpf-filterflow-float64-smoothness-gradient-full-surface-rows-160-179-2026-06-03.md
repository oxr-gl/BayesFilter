# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_gradient_mismatch`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_gradient_mismatch | scalar agrees, gradient mismatch: {'mesh_index': 173, 'theta': [0.9710526315789474, 0.9842105263157894], 'scalar_delta': 7.407919611068792e-09, 'max_abs_gradient_delta': 5.302726526244442, 'relative_gradient_delta': 0.0007553879350500595, 'scalar_within_tolerance': True, 'gradient_within_tolerance': False, 'finite': True} | gradient mismatch observed | full script-default mesh_size=20 row window [160, 180) only; no analytic-gradient correctness is concluded | localize the first failing mesh row by per-time gradient contributions | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `160` |
| `row_count` | `20` |
| `row_stop_exclusive` | `180` |
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
    "finite": true,
    "gradient_within_tolerance": false,
    "max_abs_gradient_delta": 5.302726526244442,
    "mesh_index": 173,
    "relative_gradient_delta": 0.0007553879350500595,
    "scalar_delta": 7.407919611068792e-09,
    "scalar_within_tolerance": true,
    "theta": [
      0.9710526315789474,
      0.9842105263157894
    ]
  },
  "gradient_rows_within_tolerance": 19,
  "implementation_agreement": false,
  "max_abs_gradient_delta": 5.302726526244442,
  "max_relative_gradient_delta": 0.0007553879350500595,
  "max_scalar_delta": 1.8167327198170824e-08,
  "rmse_max_abs_gradient_delta": 1.1871339655531146,
  "rmse_scalar_delta": 9.567750404357872e-09,
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
      31.293746736686646
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      22536.851548756935,
      998.0991491631033
    ],
    "gradient_matrix": [
      [
        22536.851548756935,
        905.6228992955146
      ],
      [
        18084.695134669342,
        998.0991491631033
      ]
    ],
    "mean_log_likelihood": -197.43509396216828,
    "mesh_index": 160,
    "theta": [
      0.9710526315789474,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.36411497144235
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -2747.5586854051844,
      1225.9300185950399
    ],
    "gradient_matrix": [
      [
        -2747.5586854051844,
        74.03989935318239
      ],
      [
        27601.641851446464,
        1225.9300185950399
      ]
    ],
    "mean_log_likelihood": -143.69750316149867,
    "mesh_index": 179,
    "theta": [
      0.9710526315789474,
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
      3.3750441809641325
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      22536.85147218782,
      998.0991534494278
    ],
    "log_likelihoods": [
      -197.4350939552069
    ],
    "max_column_residual": 7.105427357601002e-15,
    "max_row_residual": 1.2655203944778037e-05,
    "mean_log_likelihood": -197.4350939552069,
    "mesh_index": 160,
    "resampling_count": 99,
    "theta": [
      0.9710526315789474,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.807875222649842
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -2747.5590514184582,
      1225.9297647682265
    ],
    "log_likelihoods": [
      -143.69750315549535
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.304074774743924e-05,
    "mean_log_likelihood": -143.69750315549535,
    "mesh_index": 179,
    "resampling_count": 99,
    "theta": [
      0.9710526315789474,
      1.0
    ]
  }
}
```

## Interpretation

The scalar surface still agrees, but a gradient mismatch remains. First failure: `{'mesh_index': 173, 'theta': [0.9710526315789474, 0.9842105263157894], 'scalar_delta': 7.407919611068792e-09, 'max_abs_gradient_delta': 5.302726526244442, 'relative_gradient_delta': 0.0007553879350500595, 'scalar_within_tolerance': True, 'gradient_within_tolerance': False, 'finite': True}`.

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
