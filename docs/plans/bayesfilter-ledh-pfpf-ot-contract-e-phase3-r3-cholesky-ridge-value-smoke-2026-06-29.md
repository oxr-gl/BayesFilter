# Contract E LGSSM Value Diagnostic

Date: 2026-06-28T19:59:36.074530+00:00

Status: `smoke_passed`

## Manifest

- gate_mode: `smoke`
- num_particles: `16`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[1]`
- settings: `[{'epsilon': 0.5, 'steps': 2, 'label': 'eps0.5_steps2'}]`
- device_scope: `cpu`
- logical_gpus: `[]`
- xla: `False`
- tf32_execution_enabled: `True`

## Value Table

| dim | setting | arm | mean | Kalman | delta | sd | mcse | abs z MCSE | cov residual | condition |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | eps0.5_steps2 | `ledh_no_ot` | -6.871020 | -6.914505 | 0.043485 | 0.096010 | 0.030361 | 1.432 | NA | NA |
| 1 | eps0.5_steps2 | `old_barycentric_ot` | -6.509170 | -6.914505 | 0.405335 | 0.084982 | 0.026874 | 15.083 | NA | NA |
| 1 | eps0.5_steps2 | `contract_e` | -6.855388 | -6.914505 | 0.059117 | 0.088097 | 0.027859 | 2.122 | 2.517e-04 | 1.000e+00 |

## Gate

```json
{
  "fixture_gates": [
    {
      "arms_distinguishable_metadata": true,
      "conditioning_ok": true,
      "contract_abs_delta": 0.05911737111804616,
      "contract_condition": 1.0,
      "contract_covariance_residual": 0.00025171006564050913,
      "contract_mcse": 0.02785878409627821,
      "covariance_restoration_ok": true,
      "finite_values": true,
      "improves_old_barycentric_abs_delta": true,
      "old_abs_delta": 0.4053354087233316,
      "setting": "eps0.5_steps2",
      "state_dim": 1,
      "status": "fail",
      "within_kalman_2mcse": false
    }
  ],
  "gpu_claim_ok": true,
  "primary_criterion": "material Contract E mean within 2 MCSE of exact Kalman and smaller absolute Kalman-value error than old_barycentric_ot on every fixture",
  "status": "smoke_passed"
}
```

## Nonclaims

- This diagnostic does not certify gradients.
- This diagnostic does not certify SIR/SV/nonlinear correctness.
- This diagnostic does not certify production readiness, HMC readiness, or posterior correctness.
