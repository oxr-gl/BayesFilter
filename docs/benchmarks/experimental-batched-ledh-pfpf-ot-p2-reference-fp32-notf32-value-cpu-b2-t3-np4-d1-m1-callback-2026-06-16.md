# Streaming Experimental Batched LEDH-PFPF-OT LGSSM Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p2-reference-fp32-notf32-value-cpu-b2-t3-np4-d1-m1-callback-2026-06-16.json`
- Shape: `{'batch_size': 2, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1}`
- Device request: `/CPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:CPU:0']`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`
- Proposal mode: `callback`
- Return history: `False`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 4, 'col_chunk_size': 4, 'sinkhorn_iterations': 3, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `6.449566636001691`
- Warm-call timing summary seconds: `{'min': 0.0018239468336105347, 'median': 0.0018239468336105347, 'mean': 0.0018239468336105347, 'max': 0.0018239468336105347}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- streaming removes dense transport storage but not all-pairs OT compute
