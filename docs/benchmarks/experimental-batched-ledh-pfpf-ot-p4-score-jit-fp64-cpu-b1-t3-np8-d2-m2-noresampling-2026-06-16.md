# LEDH-PFPF-OT Gradient Structure Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 8, 'state_dim': 2, 'obs_dim': 2, 'parameter_dim': 3}`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float64', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float64', 'tf_dtype': 'float64', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`

## Arms

| arm | finite | compile+first s | warm median s | score preview |
| --- | --- | ---: | ---: | --- |
| original_dense_tensor | True | 7.47038 | 0.0008197668939828873 | `[-0.21649639770032508, -1.1460654231991982, -1.7707907402907987]` |
| streaming_dense_tensor | True | 4.57207 | 0.0015706929843872786 | `[-0.21649639770032508, -1.1460654231991985, -1.7707907402907983]` |
| streaming_streaming_tensor | True | 3.74466 | 0.0013871239498257637 | `[-0.21649639770032508, -1.1460654231991985, -1.7707907402907983]` |
| streaming_streaming_equivalent_callback | True | 3.79978 | 0.0013982742093503475 | `[-0.21649639770032508, -1.1460654231991985, -1.7707907402907983]` |

## Drift Vs Original Dense Tensor

| arm | value max abs | score max abs | score rel | score cosine | norm ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| streaming_dense_tensor | 0 | 4.44089e-16 | 2.50786e-16 | 1 | 1 |
| streaming_streaming_tensor | 0 | 4.44089e-16 | 2.50786e-16 | 1 | 1 |
| streaming_streaming_equivalent_callback | 0 | 4.44089e-16 | 2.50786e-16 | 1 | 1 |

## Nonclaims

- focused deterministic gradient-structure diagnostic only
- dense arm is a small-reference oracle, not a scalable implementation
- no HMC convergence or energy-conservation claim
- no posterior validity claim
- single fixture and single seed only
