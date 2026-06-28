# Streaming Default GPU LEDH-PFPF-OT TF32 LGSSM Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/seed-20261629/children/fp32_tf32_enabled.json`
- Shape: `{'batch_size': 1, 'time_steps': 12, 'num_particles': 128, 'state_dim': 6, 'obs_dim': 6}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'production_ledh_pfpf_ot_gpu_tf32', 'default_execution_target': 'gpu', 'default_algorithm_target': 'ledh_pfpf_ot_tf32', 'default_target_status': 'production_default_by_owner_directive', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'production_ledh_pfpf_ot_gpu_tf32_default_lane', 'historical_module_path': 'experiments/dpf_implementation', 'public_api_exposure': 'separately_gated', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`
- Proposal mode: `callback`
- Warm-start mode: `none`
- Return history: `True`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 64, 'col_chunk_size': 64, 'sinkhorn_iterations': 3, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `10.896982291946188`
- Warm-call timing summary seconds: `{'min': 0.07358131906948984, 'median': 0.07358131906948984, 'mean': 0.07358131906948984, 'max': 0.07358131906948984}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- production/default target by owner directive
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- no HMC readiness claim
- streaming removes dense transport storage but not all-pairs OT compute
