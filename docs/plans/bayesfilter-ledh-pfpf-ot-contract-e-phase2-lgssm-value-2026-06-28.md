# Contract E LGSSM Value Diagnostic

Date: 2026-06-28T12:11:08.908289+00:00

Status: `passed`

## Manifest

- gate_mode: `material`
- num_particles: `1000`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[1, 2]`
- settings: `[{'epsilon': 0.5, 'steps': 20, 'label': 'eps0.5_steps20'}]`
- device_scope: `visible`
- logical_gpus: `["LogicalDevice(name='/device:GPU:0', device_type='GPU')"]`
- xla: `True`
- tf32_execution_enabled: `True`

## Value Table

| dim | setting | arm | mean | Kalman | delta | sd | mcse | abs z MCSE | cov residual | condition |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | eps0.5_steps20 | `ledh_no_ot` | -6.912147 | -6.914505 | 0.002358 | 0.004565 | 0.001444 | 1.634 | NA | NA |
| 1 | eps0.5_steps20 | `old_barycentric_ot` | -6.619977 | -6.914505 | 0.294528 | 0.007235 | 0.002288 | 128.728 | NA | NA |
| 1 | eps0.5_steps20 | `contract_e` | -6.917480 | -6.914505 | -0.002975 | 0.007323 | 0.002316 | 1.285 | 3.804e-07 | 1.000e+00 |
| 2 | eps0.5_steps20 | `ledh_no_ot` | -13.793434 | -13.784139 | -0.009296 | 0.021238 | 0.006716 | 1.384 | NA | NA |
| 2 | eps0.5_steps20 | `old_barycentric_ot` | -12.963488 | -13.784139 | 0.820651 | 0.018899 | 0.005976 | 137.314 | NA | NA |
| 2 | eps0.5_steps20 | `contract_e` | -13.792360 | -13.784139 | -0.008221 | 0.019730 | 0.006239 | 1.318 | 8.003e-07 | 1.328e+00 |

## Gate

```json
{
  "fixture_gates": [
    {
      "arms_distinguishable_metadata": true,
      "conditioning_ok": true,
      "contract_abs_delta": 0.0029754061121973763,
      "contract_condition": 1.0000001192092896,
      "contract_covariance_residual": 3.804406389917858e-07,
      "contract_mcse": 0.0023157317796788446,
      "covariance_restoration_ok": true,
      "finite_values": true,
      "improves_old_barycentric_abs_delta": true,
      "old_abs_delta": 0.29452796989488306,
      "setting": "eps0.5_steps20",
      "state_dim": 1,
      "status": "pass",
      "within_kalman_2mcse": true
    },
    {
      "arms_distinguishable_metadata": true,
      "conditioning_ok": true,
      "contract_abs_delta": 0.008221083492344405,
      "contract_condition": 1.327636480331421,
      "contract_covariance_residual": 8.002880917956645e-07,
      "contract_mcse": 0.0062390331342564945,
      "covariance_restoration_ok": true,
      "finite_values": true,
      "improves_old_barycentric_abs_delta": true,
      "old_abs_delta": 0.8206505004462556,
      "setting": "eps0.5_steps20",
      "state_dim": 2,
      "status": "pass",
      "within_kalman_2mcse": true
    }
  ],
  "gpu_claim_ok": true,
  "primary_criterion": "material Contract E mean within 2 MCSE of exact Kalman and smaller absolute Kalman-value error than old_barycentric_ot on every fixture",
  "status": "passed"
}
```

## Nonclaims

- This diagnostic does not certify gradients.
- This diagnostic does not certify SIR/SV/nonlinear correctness.
- This diagnostic does not certify production readiness, HMC readiness, or posterior correctness.
