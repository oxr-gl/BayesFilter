# Contract E LGSSM GPU XLA TF32 Score Diagnostic

Date: 2026-07-02T21:37:50.765606+00:00

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
- score_route: `manual-reverse-scan`
- chol_ridge_abs: `1e-10`
- chol_ridge_rel: `1e-08`

## Value Gate

| dim | value mean | Kalman | delta | sd | MCSE | z | rel err | HMC gate | reason |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2 | -13.797056 | -13.784139 | -0.012917 | 0.019898 | 0.006292 | -2.053 | 0.094% | `True` | `within_1pct_relative_error` |

## Score Gate

| dim | parameter | score mean | Kalman | delta | sd | MCSE | z | rel err | HMC gate | reason |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2 | `ar_coefficient` | -5.032490 | -4.971697 | -0.060793 | 0.051022 | 0.016135 | -3.768 | 1.223% | `False` | `failed_hmc_direction_gate` |
| 2 | `log_transition_variance` | -3.936852 | -3.932431 | -0.004420 | 0.007085 | 0.002240 | -1.973 | 0.112% | `True` | `within_2_mcse` |
| 2 | `log_observation_variance` | -5.511692 | -5.503183 | -0.008510 | 0.008816 | 0.002788 | -3.052 | 0.155% | `True` | `within_1pct_relative_error` |

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
          "delta_to_kalman": -0.06079328662973982,
          "gradient_mcse": 0.016134575235906768,
          "gradient_mean": -5.032489919662476,
          "gradient_sd": 0.051022006824813934,
          "hmc_direction_gate": false,
          "hmc_direction_gate_reason": "failed_hmc_direction_gate",
          "kalman_gradient": -4.971696633032736,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "ar_coefficient",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.012227875334512497,
          "within_1pct_relative_error_to_kalman": false,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": -3.7678888809199704
        },
        {
          "delta_to_kalman": -0.004420423470757218,
          "gradient_mcse": 0.002240467761743477,
          "gradient_mean": -3.9368518829345702,
          "gradient_sd": 0.00708498115128885,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_2_mcse",
          "kalman_gradient": -3.932431459463813,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_transition_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0011240942191424596,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": -1.9729913307555704
        },
        {
          "delta_to_kalman": -0.008509824346304207,
          "gradient_mcse": 0.0027878477013662576,
          "gradient_mean": -5.511692380905151,
          "gradient_sd": 0.008815948505982284,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -5.503182556558847,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_observation_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0015463460023076938,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": -3.0524710306569993
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps2",
      "state_dim": 2,
      "status": "fail",
      "value_delta_to_kalman": -0.012917452663486984,
      "value_hmc_direction_gate": true,
      "value_hmc_direction_gate_reason": "within_1pct_relative_error",
      "value_mcse": 0.006292387774698677,
      "value_mcse_decreases_with_n_certificate": false,
      "value_mean": -13.797056007385255,
      "value_relative_error_limit": 0.01,
      "value_relative_error_to_kalman": 0.0009371244065928298,
      "value_sd": 0.019898277289046248,
      "value_within_1pct_relative_error_to_kalman": true,
      "value_within_2_mcse_of_kalman": false,
      "value_within_4_mcse_of_kalman": true,
      "value_within_4_mcse_with_n_ladder_mcse_decrease": false,
      "value_z_over_mcse": -2.0528697731292573
    }
  ],
  "gpu_visible": true,
  "manual_score_route": true,
  "primary_criterion": "GPU/XLA/TF32 batched Contract E seed-mean value and score satisfy the HMC-direction gate against exact FP64 Kalman: within 2 MCSE, or within 4 MCSE with an explicit N-ladder MCSE-decrease certificate, or within 1% relative error.",
  "route_ok": true,
  "status": "failed",
  "tf32_execution_enabled": true,
  "xla_enabled": true
}
```

## Nonclaims

- This is not a CPU LEDH result.
- This diagnostic does not run the 13-point finite-difference ladder.
- This diagnostic does not certify SIR/SV/nonlinear correctness, HMC readiness, or production readiness.
