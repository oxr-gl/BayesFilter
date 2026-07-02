# Contract E LGSSM Gradient Diagnostic

Date: 2026-06-28T13:15:39.106346+00:00

Status: `smoke_failed`

## Manifest

- gate_mode: `smoke`
- num_particles: `32`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[1]`
- settings: `[{'epsilon': 0.5, 'steps': 4, 'label': 'eps0.5_steps4'}]`
- fd_steps: `[0.0005, 0.001, 0.001]`
- device_scope: `cpu`
- logical_gpus: `[]`
- xla: `True`
- tf32_execution_enabled: `True`

## Gradient Gate Table

| dim | parameter | grad mean | Kalman | grad MCSE | exact z | FD slope | FD SE | reverse-FD z | status |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `ar_coefficient` | nan | -2.480625 | nan | nan | -2.479169 | 0.000913 | nan | `False` |
| 1 | `log_transition_variance` | nan | -1.952888 | nan | nan | -1.959500 | 0.000445 | nan | `False` |
| 1 | `log_observation_variance` | nan | -2.741817 | nan | nan | -2.765825 | 0.000439 | nan | `False` |

## Gate

```json
{
  "fixture_gates": [
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": false,
      "parameter_gates": [
        {
          "exact_delta": NaN,
          "exact_z_over_gradient_mcse": NaN,
          "fd_protocol_ok": true,
          "fd_regression_slope": -2.4791691519997436,
          "fd_regression_slope_se": 0.0009127155230152119,
          "gradient_mcse": NaN,
          "gradient_mean": NaN,
          "kalman_gradient": -2.4806245544996957,
          "parameter": "ar_coefficient",
          "reverse_fd_combined_se": NaN,
          "reverse_minus_fd": NaN,
          "reverse_minus_fd_z": NaN,
          "within_2_combined_se_of_fd": false,
          "within_2_gradient_mcse_of_kalman": false
        },
        {
          "exact_delta": NaN,
          "exact_z_over_gradient_mcse": NaN,
          "fd_protocol_ok": true,
          "fd_regression_slope": -1.9595003128051647,
          "fd_regression_slope_se": 0.00044466293917836037,
          "gradient_mcse": NaN,
          "gradient_mean": NaN,
          "kalman_gradient": -1.9528883319744628,
          "parameter": "log_transition_variance",
          "reverse_fd_combined_se": NaN,
          "reverse_minus_fd": NaN,
          "reverse_minus_fd_z": NaN,
          "within_2_combined_se_of_fd": false,
          "within_2_gradient_mcse_of_kalman": false
        },
        {
          "exact_delta": NaN,
          "exact_z_over_gradient_mcse": NaN,
          "fd_protocol_ok": true,
          "fd_regression_slope": -2.765824578025141,
          "fd_regression_slope_se": 0.000438606030868608,
          "gradient_mcse": NaN,
          "gradient_mean": NaN,
          "kalman_gradient": -2.741816797091193,
          "parameter": "log_observation_variance",
          "reverse_fd_combined_se": NaN,
          "reverse_minus_fd": NaN,
          "reverse_minus_fd_z": NaN,
          "within_2_combined_se_of_fd": false,
          "within_2_gradient_mcse_of_kalman": false
        }
      ],
      "setting": "eps0.5_steps4",
      "state_dim": 1,
      "status": "smoke_fail",
      "value_within_2_mcse_of_kalman": true
    }
  ],
  "primary_criterion": "Contract E value/gradient means within two uncertainty units of exact Kalman and reverse diagnostic within two combined SE of 13-point FD regression",
  "status": "smoke_failed"
}
```

## Nonclaims

- This diagnostic does not certify SIR/SV/nonlinear correctness.
- This diagnostic does not certify production readiness, HMC readiness, or posterior correctness.
- Reverse-mode gradients are diagnostics, not an oracle.
