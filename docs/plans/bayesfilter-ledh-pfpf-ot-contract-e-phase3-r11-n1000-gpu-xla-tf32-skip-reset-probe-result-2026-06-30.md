# Contract E LGSSM GPU XLA TF32 Score Diagnostic

Date: 2026-06-29T19:13:12.674656+00:00

Status: `failed`

## Manifest

- num_particles: `1000`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[2]`
- settings: `[{'epsilon': 0.55, 'steps': 2, 'label': 'eps0.55_steps2'}]`
- device_scope: `visible`
- logical_gpus: `["LogicalDevice(name='/device:GPU:0', device_type='GPU')"]`
- xla: `True`
- tf32_execution_enabled: `True`
- reset_factorization: `cholesky-ridge`
- chol_ridge_abs: `1e-10`
- chol_ridge_rel: `1e-08`

## Value Gate

| dim | value mean | Kalman | delta | sd | MCSE | z | status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | -12.845723 | -13.784139 | 0.938415 | 0.019735 | 0.006241 | 150.367 | `False` |

## Score Gate

| dim | parameter | score mean | Kalman | delta | sd | MCSE | z | status |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | `ar_coefficient` | nan | -4.971697 | nan | nan | nan | nan | `False` |
| 2 | `log_transition_variance` | nan | -3.932431 | nan | nan | nan | nan | `False` |
| 2 | `log_observation_variance` | nan | -5.503183 | nan | nan | nan | nan | `False` |

## Gate

```json
{
  "fixture_gates": [
    {
      "conditioning_ok": false,
      "covariance_restoration_ok": false,
      "finite_base": false,
      "kalman_value": -13.784138554721768,
      "parameter_gates": [
        {
          "delta_to_kalman": NaN,
          "gradient_mcse": NaN,
          "gradient_mean": NaN,
          "gradient_sd": NaN,
          "kalman_gradient": -4.971696633032736,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": NaN
        },
        {
          "delta_to_kalman": NaN,
          "gradient_mcse": NaN,
          "gradient_mean": NaN,
          "gradient_sd": NaN,
          "kalman_gradient": -3.932431459463813,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": NaN
        },
        {
          "delta_to_kalman": NaN,
          "gradient_mcse": NaN,
          "gradient_mean": NaN,
          "gradient_sd": NaN,
          "kalman_gradient": -5.503182556558847,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": NaN
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps2",
      "state_dim": 2,
      "status": "fail",
      "value_delta_to_kalman": 0.9384153071936918,
      "value_mcse": 0.006240835165604202,
      "value_mean": -12.845723247528076,
      "value_sd": 0.0197352536249834,
      "value_within_2_mcse_of_kalman": false,
      "value_z_over_mcse": 150.3669432523523
    }
  ],
  "gpu_visible": true,
  "primary_criterion": "GPU/XLA/TF32 batched Contract E seed-mean value and score are within 2 MCSE of exact FP64 Kalman for every requested fixture.",
  "route_ok": false,
  "status": "failed",
  "tf32_execution_enabled": true,
  "xla_enabled": true
}
```

## Nonclaims

- This is not a CPU LEDH result.
- This diagnostic does not run the 13-point finite-difference ladder.
- This diagnostic does not certify SIR/SV/nonlinear correctness, HMC readiness, or production readiness.
