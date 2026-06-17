# LEDH-PFPF-OT Gradient Structure Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp32-notf32-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 8, 'state_dim': 2, 'obs_dim': 2, 'parameter_dim': 3}`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`

## Arms

| arm | finite | compile+first s | warm median s | score preview |
| --- | --- | ---: | ---: | --- |
| original_dense_tensor | True | 7.57832 | 0.001221772050485015 | `[-0.21649643778800964, -1.1460654735565186, -1.770790934562683]` |
| streaming_dense_tensor | True | 4.62251 | 0.00113142398186028 | `[-0.21649643778800964, -1.1460652351379395, -1.770790934562683]` |
| streaming_streaming_tensor | True | 3.7689 | 0.0012838100083172321 | `[-0.21649643778800964, -1.1460652351379395, -1.770790934562683]` |
| streaming_streaming_equivalent_callback | True | 3.79521 | 0.0017691708635538816 | `[-0.21649643778800964, -1.1460652351379395, -1.770790934562683]` |

## Drift Vs Original Dense Tensor

| arm | value max abs | score max abs | score rel | score cosine | norm ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| streaming_dense_tensor | 0 | 2.38419e-07 | 2.08032e-07 | 1 | 0.999999939 |
| streaming_streaming_tensor | 0 | 2.38419e-07 | 2.08032e-07 | 1 | 0.999999939 |
| streaming_streaming_equivalent_callback | 0 | 2.38419e-07 | 2.08032e-07 | 1 | 0.999999939 |

## Nonclaims

- focused deterministic gradient-structure diagnostic only
- dense arm is a small-reference oracle, not a scalable implementation
- no HMC convergence or energy-conservation claim
- no posterior validity claim
- single fixture and single seed only
