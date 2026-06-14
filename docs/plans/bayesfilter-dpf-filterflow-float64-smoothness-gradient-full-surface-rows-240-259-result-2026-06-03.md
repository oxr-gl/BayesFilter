# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_gradient_mismatch`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_gradient_mismatch | scalar agrees, gradient mismatch: {'mesh_index': 244, 'theta': [0.981578947368421, 0.9605263157894737], 'scalar_delta': 1.262566229343065e-08, 'max_abs_gradient_delta': 0.4181312886711339, 'relative_gradient_delta': 0.0003836798271688089, 'scalar_within_tolerance': True, 'gradient_within_tolerance': False, 'finite': True} | gradient mismatch observed | full script-default mesh_size=20 row window [240, 260) only; no analytic-gradient correctness is concluded | localize the first failing mesh row by per-time gradient contributions | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `240` |
| `row_count` | `20` |
| `row_stop_exclusive` | `260` |
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
    "max_abs_gradient_delta": 0.4181312886711339,
    "mesh_index": 244,
    "relative_gradient_delta": 0.0003836798271688089,
    "scalar_delta": 1.262566229343065e-08,
    "scalar_within_tolerance": true,
    "theta": [
      0.981578947368421,
      0.9605263157894737
    ]
  },
  "gradient_rows_within_tolerance": 19,
  "implementation_agreement": false,
  "max_abs_gradient_delta": 0.4181312886711339,
  "max_relative_gradient_delta": 0.0003836798271688089,
  "max_scalar_delta": 1.8498781173548196e-08,
  "rmse_max_abs_gradient_delta": 0.10746562771805528,
  "rmse_scalar_delta": 1.0643606448768452e-08,
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
      32.70912510283677
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      42491.70007675403,
      -21.08437307736597
    ],
    "gradient_matrix": [
      [
        42491.70007675403,
        1797.0069575445073
      ],
      [
        2389.0078806641754,
        -21.08437307736597
      ]
    ],
    "mean_log_likelihood": -175.26307434204585,
    "mesh_index": 240,
    "theta": [
      0.981578947368421,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.57492571343955
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      10666.730516852069,
      -19.289381478723
    ],
    "gradient_matrix": [
      [
        10666.730516852069,
        193.88347497928132
      ],
      [
        -3433.78102832432,
        -19.289381478723
      ]
    ],
    "mean_log_likelihood": -141.8033481390076,
    "mesh_index": 259,
    "theta": [
      0.981578947368421,
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
      3.5270169080611478
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      42491.70014130176,
      -21.084373181327344
    ],
    "log_likelihoods": [
      -175.26307433380757
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.2171687586937097e-05,
    "mean_log_likelihood": -175.26307433380757,
    "mesh_index": 240,
    "resampling_count": 99,
    "theta": [
      0.981578947368421,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8275473029049794
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      10666.939695813251,
      -19.29477675514923
    ],
    "log_likelihoods": [
      -141.8033481339072
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.2731689775113963e-05,
    "mean_log_likelihood": -141.8033481339072,
    "mesh_index": 259,
    "resampling_count": 99,
    "theta": [
      0.981578947368421,
      1.0
    ]
  }
}
```

## Interpretation

The scalar surface still agrees, but a gradient mismatch remains. First failure: `{'mesh_index': 244, 'theta': [0.981578947368421, 0.9605263157894737], 'scalar_delta': 1.262566229343065e-08, 'max_abs_gradient_delta': 0.4181312886711339, 'relative_gradient_delta': 0.0003836798271688089, 'scalar_within_tolerance': True, 'gradient_within_tolerance': False, 'finite': True}`.

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
