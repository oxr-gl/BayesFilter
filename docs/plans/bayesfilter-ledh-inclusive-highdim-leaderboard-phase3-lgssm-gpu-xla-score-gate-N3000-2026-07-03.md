# Contract E LGSSM GPU XLA TF32 Score Diagnostic

Date: 2026-07-02T21:41:41.412227+00:00

Status: `passed`

## Manifest

- num_particles: `3000`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[2]`
- settings: `[{'epsilon': 0.55, 'steps': 2, 'label': 'eps0.55_steps2'}]`
- device_scope: `visible`
- logical_gpus: `["LogicalDevice(name='/device:GPU:0', device_type='GPU')"]`
- xla: `True`
- tf32_execution_enabled: `True`
- reset_factorization: `cholesky-ridge`
- score_route: `manual-reverse-scan`
- chol_ridge_abs: `1e-10`
- chol_ridge_rel: `1e-08`

## Value Gate

| dim | value mean | Kalman | delta | sd | MCSE | z | rel err | HMC gate | reason |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2 | -13.788123 | -13.784139 | -0.003984 | 0.013033 | 0.004121 | -0.967 | 0.029% | `True` | `within_2_mcse` |

## Score Gate

| dim | parameter | score mean | Kalman | delta | sd | MCSE | z | rel err | HMC gate | reason |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2 | `ar_coefficient` | -5.003586 | -4.971697 | -0.031890 | 0.034769 | 0.010995 | -2.900 | 0.641% | `True` | `within_1pct_relative_error` |
| 2 | `log_transition_variance` | -3.939871 | -3.932431 | -0.007439 | 0.005376 | 0.001700 | -4.376 | 0.189% | `True` | `within_1pct_relative_error` |
| 2 | `log_observation_variance` | -5.510846 | -5.503183 | -0.007664 | 0.003732 | 0.001180 | -6.494 | 0.139% | `True` | `within_1pct_relative_error` |

## Gate

```json
{
  "fixture_gates": [
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -13.784138554721768,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.03188965923410958,
          "gradient_mcse": 0.010994846466715755,
          "gradient_mean": -5.003586292266846,
          "gradient_sd": 0.034768757358676475,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -4.971696633032736,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "ar_coefficient",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.006414240768881523,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": -2.9004187853507393
        },
        {
          "delta_to_kalman": -0.007439160310051651,
          "gradient_mcse": 0.0017000945778979605,
          "gradient_mean": -3.9398706197738647,
          "gradient_sd": 0.005376171103860111,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -3.932431459463813,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_transition_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0018917457015426228,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": -4.375733213177831
        },
        {
          "delta_to_kalman": -0.007663724492789292,
          "gradient_mcse": 0.0011801704724620262,
          "gradient_mean": -5.510846281051636,
          "gradient_sd": 0.0037320267202570275,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -5.503182556558847,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_observation_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.001392598630706054,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": -6.493743634173057
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps2",
      "state_dim": 2,
      "status": "pass",
      "value_delta_to_kalman": -0.003984099239414007,
      "value_hmc_direction_gate": true,
      "value_hmc_direction_gate_reason": "within_2_mcse",
      "value_mcse": 0.00412146316179652,
      "value_mcse_decreases_with_n_certificate": false,
      "value_mean": -13.788122653961182,
      "value_relative_error_limit": 0.01,
      "value_relative_error_to_kalman": 0.00028903505457359547,
      "value_sd": 0.013033210883756072,
      "value_within_1pct_relative_error_to_kalman": true,
      "value_within_2_mcse_of_kalman": true,
      "value_within_4_mcse_of_kalman": true,
      "value_within_4_mcse_with_n_ladder_mcse_decrease": false,
      "value_z_over_mcse": -0.966671078451994
    }
  ],
  "gpu_visible": true,
  "manual_score_route": true,
  "primary_criterion": "GPU/XLA/TF32 batched Contract E seed-mean value and score satisfy the HMC-direction gate against exact FP64 Kalman: within 2 MCSE, or within 4 MCSE with an explicit N-ladder MCSE-decrease certificate, or within 1% relative error.",
  "route_ok": true,
  "status": "passed",
  "tf32_execution_enabled": true,
  "xla_enabled": true
}
```

## Nonclaims

- This is not a CPU LEDH result.
- This diagnostic does not run the 13-point finite-difference ladder.
- This diagnostic does not certify SIR/SV/nonlinear correctness, HMC readiness, or production readiness.
