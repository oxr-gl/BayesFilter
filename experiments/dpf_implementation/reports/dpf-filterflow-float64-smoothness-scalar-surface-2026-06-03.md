# FilterFlow Float64 Smoothness Scalar Surface Comparison

## Decision

`filterflow_float64_smoothness_scalar_surface_pass`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| filterflow_float64_smoothness_scalar_surface_pass | 16 of 16 bounded mesh rows within scalar tolerance | pass | bounded mesh only; gradients are not tested here | repeat the scalar-surface comparison with gradient recording | correctness of either implementation, gradient correctness, production readiness |

## Scalar Contract

| Key | Value |
| --- | --- |
| `filterflow_scalar` | `tf.reduce_mean(final_state.log_likelihoods)` |
| `bayesfilter_scalar` | `tf.reduce_mean(log_likelihoods)` |
| `batch_size_note` | `batch_size=1 makes mean and single-batch total equal` |
| `per_time_normalization` | `not used` |
| `sign` | `positive log-likelihood convention as emitted by filterflow` |
| `gradient_status` | `not tested in this runner` |

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
| `mesh_size` | `4` |
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
  "finite_rows": 16,
  "first_failure": {
    "status": "no_failure"
  },
  "implementation_agreement": true,
  "max_scalar_delta": 1.4924950164640904e-08,
  "rmse_scalar_delta": 8.905779290840865e-09,
  "row_count": 16,
  "rows_within_tolerance": 16
}
```

## First And Last Rows

### FilterFlow

```json
{
  "first_row": {
    "final_ess": [
      27.982214166117192
    ],
    "finite_scalar": true,
    "mean_log_likelihood": -258.58524847172157,
    "mesh_index": 0,
    "theta": [
      0.95,
      0.95
    ]
  },
  "last_row": {
    "final_ess": [
      35.81367996831653
    ],
    "finite_scalar": true,
    "mean_log_likelihood": -139.95535907215373,
    "mesh_index": 15,
    "theta": [
      1.0,
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
      3.17850829839299
    ],
    "finite_scalar": true,
    "log_likelihoods": [
      -258.5852484624214
    ],
    "max_column_residual": 2.1316282072803006e-14,
    "max_row_residual": 1.0943960801146346e-05,
    "mean_log_likelihood": -258.5852484624214,
    "mesh_index": 0,
    "resampling_count": 99,
    "theta": [
      0.95,
      0.95
    ]
  },
  "last_row": {
    "final_log_neff": [
      3.8497426895828952
    ],
    "finite_scalar": true,
    "log_likelihoods": [
      -139.95535907215407
    ],
    "max_column_residual": 3.552713678800501e-15,
    "max_row_residual": 1.1939412243755498e-05,
    "mean_log_likelihood": -139.95535907215407,
    "mesh_index": 15,
    "resampling_count": 99,
    "theta": [
      1.0,
      1.0
    ]
  }
}
```

## Interpretation

BayesFilter and the local float64 FilterFlow executable agree on the bounded smoothness scalar surface. Max scalar delta: `1.4924950164640904e-08`. Transport residuals remain explanatory only in this artifact.

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
- No smoothness-surface gradient correctness is concluded.
- No full mesh_size=20 surface agreement is concluded.
- No production dtype default is concluded.
- Transport residual magnitude is explanatory only for this difference audit.
