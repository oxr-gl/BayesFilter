# FilterFlow Float64 Smoothness Gradient Surface Comparison

## Decision

`filterflow_float64_smoothness_gradient_full_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_gradient_full_surface_pass | 20 of 20 full script-default mesh_size=20 row window [80, 100) rows within gradient tolerance | pass | full script-default mesh_size=20 row window [80, 100) only; no analytic-gradient correctness is concluded | add Kalman finite-difference context or multi-seed smoke only if needed | correctness of either implementation, analytic gradient correctness, production readiness |

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
| `row_start` | `80` |
| `row_count` | `20` |
| `row_stop_exclusive` | `100` |
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
  "max_abs_gradient_delta": 0.050149621078162454,
  "max_relative_gradient_delta": 3.7868574939856105e-06,
  "max_scalar_delta": 1.718296971375821e-08,
  "rmse_max_abs_gradient_delta": 0.011324648153996003,
  "rmse_scalar_delta": 8.918324883577626e-09,
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
      29.651087160654885
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -37279.712826647235,
      2745.6975693620875
    ],
    "gradient_matrix": [
      [
        -37279.712826647235,
        -2050.3428121649467
      ],
      [
        48682.13947499317,
        2745.6975693620875
      ]
    ],
    "mean_log_likelihood": -225.21074637794837,
    "mesh_index": 80,
    "theta": [
      0.9605263157894737,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.10502072681638
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      20180.785364852636,
      -115.68892302412553
    ],
    "gradient_matrix": [
      [
        20180.785364852636,
        1365.2943484575103
      ],
      [
        218.3962232464663,
        -115.68892302412553
      ]
    ],
    "mean_log_likelihood": -146.16229127688277,
    "mesh_index": 99,
    "theta": [
      0.9605263157894737,
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
      3.2508060311433837
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      -37279.713435976875,
      2745.697574165913
    ],
    "log_likelihoods": [
      -225.210746373455
    ],
    "max_column_residual": 1.7763568394002505e-14,
    "max_row_residual": 1.0843374971925002e-05,
    "mean_log_likelihood": -225.210746373455,
    "mesh_index": 80,
    "resampling_count": 99,
    "theta": [
      0.9605263157894737,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.7844720454421417
    ],
    "finite_gradient": true,
    "finite_scalar": true,
    "gradient_diag": [
      20180.78536398227,
      -115.68892482093959
    ],
    "log_likelihoods": [
      -146.16229126816808
    ],
    "max_column_residual": 5.329070518200751e-15,
    "max_row_residual": 1.3631709678829651e-05,
    "mean_log_likelihood": -146.16229126816808,
    "mesh_index": 99,
    "resampling_count": 99,
    "theta": [
      0.9605263157894737,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the full script-default mesh_size=20 row window [80, 100) smoothness scalar and diagonal gradient surface. Max scalar delta: `1.718296971375821e-08`. Max absolute gradient delta: `0.050149621078162454`.

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
