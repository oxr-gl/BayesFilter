# LEDH-PFPF-OT Gradient Structure Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json`
- Overall passed: `False`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 8, 'state_dim': 2, 'obs_dim': 2, 'parameter_dim': 3}`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float64', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float64', 'tf_dtype': 'float64', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`

## Arms

| arm | finite | compile+first s | warm median s | score preview |
| --- | --- | ---: | ---: | --- |
| original_dense_tensor | True | 7.48186 | 0.0007799160666763783 | `[-0.1981248322435411, -1.1501220769486298, -1.7740456265903712]` |
| streaming_dense_tensor | True | 6.15818 | 0.0020849499851465225 | `[-0.19812483224354108, -1.1501220769486298, -1.7740456265903708]` |
| streaming_streaming_tensor | False | 12.9491 | 0.008060710970312357 | `[nan, nan, nan]` |
| streaming_streaming_equivalent_callback | False | 12.367 | 0.008067860966548324 | `[nan, nan, nan]` |

## Drift Vs Original Dense Tensor

| arm | value max abs | score max abs | score rel | score cosine | norm ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| streaming_dense_tensor | 0 | 4.44089e-16 | 2.50326e-16 | 1 | 1 |
| streaming_streaming_tensor | 0 | nan | nan | nan | nan |
| streaming_streaming_equivalent_callback | 0 | nan | nan | nan | nan |

## Nonclaims

- focused deterministic gradient-structure diagnostic only
- dense arm is a small-reference oracle, not a scalable implementation
- no HMC convergence or energy-conservation claim
- no posterior validity claim
- single fixture and single seed only
