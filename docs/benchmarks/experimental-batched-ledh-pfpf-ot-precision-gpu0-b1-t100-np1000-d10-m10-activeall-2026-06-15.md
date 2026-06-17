# Streaming LEDH-PFPF-OT Precision Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-precision-gpu0-b1-t100-np1000-d10-m10-activeall-2026-06-15.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 100, 'num_particles': 1000, 'state_dim': 10, 'obs_dim': 10}`
- Device request: `/GPU:0`

## Arms

| arm | dtype | TF32 mode | TF32 enabled | finite | compile+first s | warm median s |
| --- | --- | --- | --- | --- | ---: | ---: |
| fp64_reference | float64 | disabled | False | True | 14.4599 | 7.368514051893726 |
| fp32_tf32_disabled | float32 | disabled | False | True | 14.9054 | 5.491417262004688 |
| fp32_tf32_enabled | float32 | enabled | True | True | 13.5637 | 3.1095922680106014 |

## Drift Vs FP64

| arm | output | max abs | rms abs | max relative |
| --- | --- | ---: | ---: | ---: |
| fp32_tf32_disabled | ess_by_time | 0.000718192 | 0.000314267 | 7.18404e-07 |
| fp32_tf32_disabled | filtered_means | 8.43576e-07 | 7.72385e-08 | 8.43576e-07 |
| fp32_tf32_disabled | filtered_variances | 7.55266e-07 | 5.62208e-08 | 7.55266e-07 |
| fp32_tf32_disabled | log_likelihood | 0.000163244 | 0.000163244 | 7.93425e-07 |
| fp32_tf32_enabled | ess_by_time | 0.293593 | 0.0297156 | 0.00029368 |
| fp32_tf32_enabled | filtered_means | 0.000205953 | 2.3687e-05 | 0.000205953 |
| fp32_tf32_enabled | filtered_variances | 9.62888e-05 | 7.04565e-06 | 9.62888e-05 |
| fp32_tf32_enabled | log_likelihood | 0.0359756 | 0.0359756 | 0.000174855 |

## Nonclaims

- single deterministic LGSSM-shaped fixture only
- no production default readiness claim
- no posterior validity claim
- no HMC readiness or energy-conservation claim
- no statistical ranking from single-run timings
- TF32 flag is recorded as requested; not every TensorFlow op necessarily uses TF32
