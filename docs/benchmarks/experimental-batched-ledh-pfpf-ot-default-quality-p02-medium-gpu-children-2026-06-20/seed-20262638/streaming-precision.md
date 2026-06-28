# Streaming LEDH-PFPF-OT Precision Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/seed-20262638/streaming-precision.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 12, 'num_particles': 128, 'state_dim': 6, 'obs_dim': 6}`
- Device request: `/GPU:0`

## Arms

| arm | dtype | TF32 mode | TF32 enabled | finite | compile+first s | warm median s |
| --- | --- | --- | --- | --- | ---: | ---: |
| fp64_reference | float64 | disabled | False | True | 10.4144 | 0.09607788198627532 |
| fp32_tf32_disabled | float32 | disabled | False | True | 9.88059 | 0.07476754114031792 |
| fp32_tf32_enabled | float32 | enabled | True | True | 10.8169 | 0.06988768116571009 |

## Drift Vs FP64

| arm | output | max abs | rms abs | max relative |
| --- | --- | ---: | ---: | ---: |
| fp32_tf32_disabled | ess_by_time | 6.20612e-05 | 4.05578e-05 | 4.84853e-07 |
| fp32_tf32_disabled | filtered_means | 7.22336e-08 | 2.31852e-08 | 7.22336e-08 |
| fp32_tf32_disabled | filtered_variances | 2.0319e-09 | 3.25813e-10 | 2.0319e-09 |
| fp32_tf32_disabled | log_likelihood | 9.80615e-06 | 9.80615e-06 | 6.6329e-07 |
| fp32_tf32_enabled | ess_by_time | 0.000181726 | 5.86731e-05 | 1.43681e-06 |
| fp32_tf32_enabled | filtered_means | 3.49393e-05 | 1.33601e-05 | 3.49393e-05 |
| fp32_tf32_enabled | filtered_variances | 1.7648e-06 | 3.49057e-07 | 1.7648e-06 |
| fp32_tf32_enabled | log_likelihood | 0.00172779 | 0.00172779 | 0.000116868 |

## Nonclaims

- single deterministic LGSSM-shaped fixture only
- production/default target by owner directive
- no posterior validity claim
- no HMC readiness or energy-conservation claim
- no statistical ranking from single-run timings
- TF32 flag is recorded as requested; not every TensorFlow op necessarily uses TF32
