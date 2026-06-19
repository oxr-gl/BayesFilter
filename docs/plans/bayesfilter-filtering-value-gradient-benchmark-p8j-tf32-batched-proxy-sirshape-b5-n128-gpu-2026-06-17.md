# Streaming Experimental Batched LEDH-PFPF-OT LGSSM Benchmark

- JSON artifact: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-proxy-sirshape-b5-n128-gpu-2026-06-17.json`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 128, 'state_dim': 18, 'obs_dim': 9}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`
- Proposal mode: `callback`
- Return history: `False`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 128, 'col_chunk_size': 128, 'sinkhorn_iterations': 10, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `8.949548204895109`
- Warm-call timing summary seconds: `{'min': 0.2666434459388256, 'median': 0.281383722089231, 'mean': 0.2774832146242261, 'max': 0.28442247584462166}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- streaming removes dense transport storage but not all-pairs OT compute
