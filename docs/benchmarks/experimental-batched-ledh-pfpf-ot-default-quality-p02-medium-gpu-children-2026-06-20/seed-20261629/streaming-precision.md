# Streaming LEDH-PFPF-OT Precision Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/seed-20261629/streaming-precision.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 12, 'num_particles': 128, 'state_dim': 6, 'obs_dim': 6}`
- Device request: `/GPU:0`

## Arms

| arm | dtype | TF32 mode | TF32 enabled | finite | compile+first s | warm median s |
| --- | --- | --- | --- | --- | ---: | ---: |
| fp64_reference | float64 | disabled | False | True | 10.2738 | 0.09380283509381115 |
| fp32_tf32_disabled | float32 | disabled | False | True | 9.86076 | 0.07577653811313212 |
| fp32_tf32_enabled | float32 | enabled | True | True | 10.897 | 0.07358131906948984 |

## Drift Vs FP64

| arm | output | max abs | rms abs | max relative |
| --- | --- | ---: | ---: | ---: |
| fp32_tf32_disabled | ess_by_time | 5.31464e-05 | 3.25373e-05 | 4.15212e-07 |
| fp32_tf32_disabled | filtered_means | 6.979e-08 | 2.065e-08 | 6.979e-08 |
| fp32_tf32_disabled | filtered_variances | 1.79552e-09 | 2.98101e-10 | 1.79552e-09 |
| fp32_tf32_disabled | log_likelihood | 1.14644e-05 | 1.14644e-05 | 7.7569e-07 |
| fp32_tf32_enabled | ess_by_time | 0.000610813 | 0.000191051 | 4.77206e-06 |
| fp32_tf32_enabled | filtered_means | 3.61148e-05 | 1.30318e-05 | 3.61148e-05 |
| fp32_tf32_enabled | filtered_variances | 3.3208e-06 | 7.21585e-07 | 3.3208e-06 |
| fp32_tf32_enabled | log_likelihood | 0.00192449 | 0.00192449 | 0.000130213 |

## Nonclaims

- single deterministic LGSSM-shaped fixture only
- production/default target by owner directive
- no posterior validity claim
- no HMC readiness or energy-conservation claim
- no statistical ranking from single-run timings
- TF32 flag is recorded as requested; not every TensorFlow op necessarily uses TF32
