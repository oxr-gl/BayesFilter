# Contract E LGSSM Value Diagnostic

Date: 2026-06-28T12:09:37.999343+00:00

Status: `smoke_passed`

## Manifest

- gate_mode: `smoke`
- num_particles: `64`
- seed_count: `10`
- time_steps: `10`
- state_dims: `[1]`
- settings: `[{'epsilon': 0.5, 'steps': 8, 'label': 'eps0.5_steps8'}]`
- device_scope: `cpu`
- logical_gpus: `[]`
- xla: `True`
- tf32_execution_enabled: `True`

## Value Table

| dim | setting | arm | mean | Kalman | delta | sd | mcse | abs z MCSE | cov residual | condition |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | eps0.5_steps8 | `ledh_no_ot` | -6.902609 | -6.914505 | 0.011896 | 0.021158 | 0.006691 | 1.778 | NA | NA |
| 1 | eps0.5_steps8 | `old_barycentric_ot` | -6.511693 | -6.914505 | 0.402812 | 0.015746 | 0.004979 | 80.896 | NA | NA |
| 1 | eps0.5_steps8 | `contract_e` | -6.906524 | -6.914505 | 0.007981 | 0.024106 | 0.007623 | 1.047 | 3.990e-07 | 1.000e+00 |

## Gate

```json
{
  "fixture_gates": [
    {
      "arms_distinguishable_metadata": true,
      "conditioning_ok": true,
      "contract_abs_delta": 0.00798099664447438,
      "contract_condition": 1.0,
      "contract_covariance_residual": 3.9903170545585454e-07,
      "contract_mcse": 0.007623077749701927,
      "covariance_restoration_ok": true,
      "finite_values": true,
      "improves_old_barycentric_abs_delta": true,
      "old_abs_delta": 0.40281193879840504,
      "setting": "eps0.5_steps8",
      "state_dim": 1,
      "status": "pass",
      "within_kalman_2mcse": true
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
