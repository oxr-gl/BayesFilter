# Streaming LEDH-PFPF-OT Precision Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 5, 'num_particles': 32, 'state_dim': 4, 'obs_dim': 4}`
- Device request: `/GPU:0`

## Arms

| arm | dtype | TF32 mode | TF32 enabled | finite | compile+first s | warm median s |
| --- | --- | --- | --- | --- | ---: | ---: |
| fp64_reference | float64 | disabled | False | True | 9.82582 | 0.021421320969238877 |
| fp32_tf32_disabled | float32 | disabled | False | True | 9.76173 | 0.017371173948049545 |
| fp32_tf32_enabled | float32 | enabled | True | True | 10.1566 | 0.016212651040405035 |

## Drift Vs FP64

| arm | output | max abs | rms abs | max relative |
| --- | --- | ---: | ---: | ---: |
| fp32_tf32_disabled | ess_by_time | 6.97182e-06 | 5.41043e-06 | 2.194e-07 |
| fp32_tf32_disabled | filtered_means | 1.40866e-08 | 6.35389e-09 | 1.40866e-08 |
| fp32_tf32_disabled | filtered_variances | 1.52536e-09 | 4.20857e-10 | 1.52536e-09 |
| fp32_tf32_disabled | log_likelihood | 1.47303e-06 | 1.47303e-06 | 3.64885e-07 |
| fp32_tf32_enabled | ess_by_time | 6.36001e-05 | 2.98248e-05 | 2.00147e-06 |
| fp32_tf32_enabled | filtered_means | 1.48333e-05 | 6.51148e-06 | 1.48333e-05 |
| fp32_tf32_enabled | filtered_variances | 1.38521e-06 | 4.87507e-07 | 1.38521e-06 |
| fp32_tf32_enabled | log_likelihood | 0.000144524 | 0.000144524 | 3.58001e-05 |

## Nonclaims

- single deterministic LGSSM-shaped fixture only
- production/default target by owner directive
- no posterior validity claim
- no HMC readiness or energy-conservation claim
- no statistical ranking from single-run timings
- TF32 flag is recorded as requested; not every TensorFlow op necessarily uses TF32
