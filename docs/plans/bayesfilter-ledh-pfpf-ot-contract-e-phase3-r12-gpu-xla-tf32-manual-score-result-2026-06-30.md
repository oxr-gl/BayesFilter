# Contract E LGSSM GPU XLA TF32 Score Diagnostic

Date: 2026-06-29T20:47:16.270254+00:00

Status: `failed`

## Manifest

- num_particles: `1000`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[2, 1]`
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

| dim | value mean | Kalman | delta | sd | MCSE | z | status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | -13.797057 | -13.784139 | -0.012918 | 0.019899 | 0.006293 | -2.053 | `False` |
| 1 | -6.918275 | -6.914505 | -0.003770 | 0.008133 | 0.002572 | -1.466 | `True` |

## Score Gate

| dim | parameter | score mean | Kalman | delta | sd | MCSE | z | status |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | `ar_coefficient` | -5.032491 | -4.971697 | -0.060795 | 0.051021 | 0.016134 | -3.768 | `False` |
| 2 | `log_transition_variance` | -3.936874 | -3.932431 | -0.004443 | 0.007174 | 0.002269 | -1.958 | `True` |
| 2 | `log_observation_variance` | -5.511692 | -5.503183 | -0.008509 | 0.008818 | 0.002788 | -3.052 | `False` |
| 1 | `ar_coefficient` | -2.525207 | -2.480625 | -0.044582 | 0.031003 | 0.009804 | -4.547 | `False` |
| 1 | `log_transition_variance` | -1.952369 | -1.952888 | 0.000520 | 0.002794 | 0.000884 | 0.588 | `True` |
| 1 | `log_observation_variance` | -2.748014 | -2.741817 | -0.006197 | 0.005078 | 0.001606 | -3.859 | `False` |

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
          "delta_to_kalman": -0.06079452640635097,
          "gradient_mcse": 0.01613431708224228,
          "gradient_mean": -5.032491159439087,
          "gradient_sd": 0.05102119047124783,
          "kalman_gradient": -4.971696633032736,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.7680260091865008
        },
        {
          "delta_to_kalman": -0.0044425010311819335,
          "gradient_mcse": 0.002268506971861065,
          "gradient_mean": -3.936873960494995,
          "gradient_sd": 0.007173648919052465,
          "kalman_gradient": -3.932431459463813,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": -1.958336953021282
        },
        {
          "delta_to_kalman": -0.008509109090566902,
          "gradient_mcse": 0.0027884327466259954,
          "gradient_mean": -5.511691665649414,
          "gradient_sd": 0.00881779858153734,
          "kalman_gradient": -5.503182556558847,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.051574078974265
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps2",
      "state_dim": 2,
      "status": "fail",
      "value_delta_to_kalman": -0.012918215602939043,
      "value_mcse": 0.0062925225612240395,
      "value_mean": -13.797056770324707,
      "value_sd": 0.019898703521464296,
      "value_within_2_mcse_of_kalman": false,
      "value_z_over_mcse": -2.052947045838824
    },
    {
      "conditioning_ok": true,
      "covariance_restoration_ok": true,
      "finite_base": true,
      "kalman_value": -6.914505014954087,
      "parameter_gates": [
        {
          "delta_to_kalman": -0.044582491199147256,
          "gradient_mcse": 0.00980387349973959,
          "gradient_mean": -2.525207042694092,
          "gradient_sd": 0.031002570151343292,
          "kalman_gradient": -2.4806245514949445,
          "parameter": "ar_coefficient",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -4.547436398514471
        },
        {
          "delta_to_kalman": 0.0005197363476783234,
          "gradient_mcse": 0.0008835117644756407,
          "gradient_mean": -1.9523685932159425,
          "gradient_sd": 0.0027939095152972656,
          "kalman_gradient": -1.9528883295636208,
          "parameter": "log_transition_variance",
          "within_2_gradient_mcse_of_kalman": true,
          "z_over_gradient_mcse": 0.5882619435031339
        },
        {
          "delta_to_kalman": -0.006196962970141939,
          "gradient_mcse": 0.0016058762670218135,
          "gradient_mean": -2.7480137586593627,
          "gradient_sd": 0.0050782266441976726,
          "kalman_gradient": -2.7418167956892208,
          "parameter": "log_observation_variance",
          "within_2_gradient_mcse_of_kalman": false,
          "z_over_gradient_mcse": -3.858929294493249
        }
      ],
      "ridge_ok": true,
      "setting": "eps0.55_steps2",
      "state_dim": 1,
      "status": "fail",
      "value_delta_to_kalman": -0.0037704367060689137,
      "value_mcse": 0.002571848276326227,
      "value_mean": -6.918275451660156,
      "value_sd": 0.008132898349568981,
      "value_within_2_mcse_of_kalman": true,
      "value_z_over_mcse": -1.466041656024444
    }
  ],
  "gpu_visible": true,
  "manual_score_route": true,
  "primary_criterion": "GPU/XLA/TF32 batched Contract E seed-mean value and score are within 2 MCSE of exact FP64 Kalman for every requested fixture.",
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
