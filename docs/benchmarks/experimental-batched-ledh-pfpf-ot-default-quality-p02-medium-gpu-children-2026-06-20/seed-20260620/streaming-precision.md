# Streaming LEDH-PFPF-OT Precision Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/seed-20260620/streaming-precision.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 12, 'num_particles': 128, 'state_dim': 6, 'obs_dim': 6}`
- Device request: `/GPU:0`

## Arms

| arm | dtype | TF32 mode | TF32 enabled | finite | compile+first s | warm median s |
| --- | --- | --- | --- | --- | ---: | ---: |
| fp64_reference | float64 | disabled | False | True | 10.3835 | 0.09951867279596627 |
| fp32_tf32_disabled | float32 | disabled | False | True | 9.88893 | 0.07220645900815725 |
| fp32_tf32_enabled | float32 | enabled | True | True | 10.7031 | 0.07445378415286541 |

## Drift Vs FP64

| arm | output | max abs | rms abs | max relative |
| --- | --- | ---: | ---: | ---: |
| fp32_tf32_disabled | ess_by_time | 6.68222e-05 | 3.86421e-05 | 5.22048e-07 |
| fp32_tf32_disabled | filtered_means | 7.64414e-08 | 2.21407e-08 | 7.64414e-08 |
| fp32_tf32_disabled | filtered_variances | 2.15278e-09 | 3.18175e-10 | 2.15278e-09 |
| fp32_tf32_disabled | log_likelihood | 9.24034e-06 | 9.24034e-06 | 6.24185e-07 |
| fp32_tf32_enabled | ess_by_time | 0.000120042 | 5.84769e-05 | 9.37832e-07 |
| fp32_tf32_enabled | filtered_means | 4.22228e-05 | 1.37371e-05 | 4.22228e-05 |
| fp32_tf32_enabled | filtered_variances | 1.40778e-06 | 4.23133e-07 | 1.40778e-06 |
| fp32_tf32_enabled | log_likelihood | 0.00190383 | 0.00190383 | 0.000128604 |

## Nonclaims

- single deterministic LGSSM-shaped fixture only
- production/default target by owner directive
- no posterior validity claim
- no HMC readiness or energy-conservation claim
- no statistical ranking from single-run timings
- TF32 flag is recorded as requested; not every TensorFlow op necessarily uses TF32
