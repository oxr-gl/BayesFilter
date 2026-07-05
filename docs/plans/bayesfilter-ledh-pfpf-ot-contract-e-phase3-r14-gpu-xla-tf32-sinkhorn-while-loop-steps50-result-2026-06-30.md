# Contract E LGSSM GPU XLA TF32 Score Diagnostic

Date: 2026-06-30T06:19:01.747984+00:00

Status: `passed`

## Manifest

- num_particles: `1000`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[2, 1]`
- settings: `[{'epsilon': 0.55, 'steps': 50, 'label': 'eps0.55_steps50'}]`
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
| 2 | -13.791744 | -13.784139 | -0.007605 | 0.019779 | 0.006255 | -1.216 | 0.055% | `True` | `within_2_mcse` |
| 1 | -6.910906 | -6.914505 | 0.003599 | 0.007079 | 0.002239 | 1.608 | 0.052% | `True` | `within_2_mcse` |

## Score Gate

| dim | parameter | score mean | Kalman | delta | sd | MCSE | z | rel err | HMC gate | reason |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2 | `ar_coefficient` | -4.980262 | -4.971697 | -0.008566 | 0.052418 | 0.016576 | -0.517 | 0.172% | `True` | `within_2_mcse` |
| 2 | `log_transition_variance` | -3.929932 | -3.932431 | 0.002500 | 0.006581 | 0.002081 | 1.201 | 0.064% | `True` | `within_2_mcse` |
| 2 | `log_observation_variance` | -5.494739 | -5.503183 | 0.008443 | 0.009112 | 0.002881 | 2.930 | 0.153% | `True` | `within_1pct_relative_error` |
| 1 | `ar_coefficient` | -2.466454 | -2.480625 | 0.014171 | 0.021189 | 0.006701 | 2.115 | 0.571% | `True` | `within_1pct_relative_error` |
| 1 | `log_transition_variance` | -1.947388 | -1.952888 | 0.005501 | 0.004199 | 0.001328 | 4.142 | 0.282% | `True` | `within_1pct_relative_error` |
| 1 | `log_observation_variance` | -2.733042 | -2.741817 | 0.008775 | 0.006395 | 0.002022 | 4.339 | 0.320% | `True` | `within_1pct_relative_error` |

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
          "delta_to_kalman": -0.008565837212625382,
          "gradient_mcse": 0.016575915552275278,
          "gradient_mean": -4.9802624702453615,
          "gradient_sd": 0.05241764744779772,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_2_mcse",
          "kalman_gradient": -4.971696633032736,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "ar_coefficient",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0017229203318063716,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": -0.5167640475490719
        },
        {
          "delta_to_kalman": 0.0024996519458078126,
          "gradient_mcse": 0.0020810357730654643,
          "gradient_mean": -3.929931807518005,
          "gradient_sd": 0.006580812935176151,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_2_mcse",
          "kalman_gradient": -3.932431459463813,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_transition_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0006356504802625702,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": 1.2011576053427024
        },
        {
          "delta_to_kalman": 0.00844345324158624,
          "gradient_mcse": 0.0028813779813802527,
          "gradient_mean": -5.494739103317261,
          "gradient_sd": 0.009111717221019834,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -5.503182556558847,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_observation_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0015342855074874987,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": 2.9303525244340256
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps50",
      "state_dim": 2,
      "status": "pass",
      "value_delta_to_kalman": -0.007605391353671109,
      "value_hmc_direction_gate": true,
      "value_hmc_direction_gate_reason": "within_2_mcse",
      "value_mcse": 0.0062547587275363255,
      "value_mcse_decreases_with_n_certificate": false,
      "value_mean": -13.791743946075439,
      "value_relative_error_limit": 0.01,
      "value_relative_error_to_kalman": 0.0005517494853580006,
      "value_sd": 0.019779283793831322,
      "value_within_1pct_relative_error_to_kalman": true,
      "value_within_2_mcse_of_kalman": true,
      "value_within_4_mcse_of_kalman": true,
      "value_within_4_mcse_with_n_ladder_mcse_decrease": false,
      "value_z_over_mcse": -1.215936806673082
    },
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -6.914505014954087,
      "parameter_gates": [
        {
          "delta_to_kalman": 0.014170736988413868,
          "gradient_mcse": 0.006700688395132818,
          "gradient_mean": -2.4664538145065307,
          "gradient_sd": 0.02118943721967802,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -2.4806245514949445,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "ar_coefficient",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.005712568223947431,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": true,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": 2.11481808327441
        },
        {
          "delta_to_kalman": 0.005500598488333841,
          "gradient_mcse": 0.001327887826546152,
          "gradient_mean": -1.947387731075287,
          "gradient_sd": 0.004199150009096441,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -1.9528883295636208,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_transition_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0028166477340580798,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": 4.142366831271393
        },
        {
          "delta_to_kalman": 0.008775080067272345,
          "gradient_mcse": 0.002022281112133574,
          "gradient_mean": -2.7330417156219484,
          "gradient_sd": 0.006395014383480467,
          "hmc_direction_gate": true,
          "hmc_direction_gate_reason": "within_1pct_relative_error",
          "kalman_gradient": -2.7418167956892208,
          "mcse_decreases_with_n_certificate": false,
          "parameter": "log_observation_variance",
          "relative_error_limit": 0.01,
          "relative_error_to_kalman": 0.0032004618547339958,
          "within_1pct_relative_error_to_kalman": true,
          "within_2_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_of_kalman": false,
          "within_4_gradient_mcse_with_n_ladder_mcse_decrease": false,
          "z_over_gradient_mcse": 4.339198944509917
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps50",
      "state_dim": 1,
      "status": "pass",
      "value_delta_to_kalman": 0.0035992246251073112,
      "value_hmc_direction_gate": true,
      "value_hmc_direction_gate_reason": "within_2_mcse",
      "value_mcse": 0.0022386749225156467,
      "value_mcse_decreases_with_n_certificate": false,
      "value_mean": -6.91090579032898,
      "value_relative_error_limit": 0.01,
      "value_relative_error_to_kalman": 0.0005205325062782112,
      "value_sd": 0.007079311695850407,
      "value_within_1pct_relative_error_to_kalman": true,
      "value_within_2_mcse_of_kalman": true,
      "value_within_4_mcse_of_kalman": true,
      "value_within_4_mcse_with_n_ladder_mcse_decrease": false,
      "value_z_over_mcse": 1.6077477747697222
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
