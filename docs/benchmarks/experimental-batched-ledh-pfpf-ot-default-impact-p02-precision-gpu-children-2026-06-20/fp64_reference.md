# Streaming Default GPU LEDH-PFPF-OT TF32 LGSSM Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-children-2026-06-20/fp64_reference.json`
- Shape: `{'batch_size': 1, 'time_steps': 5, 'num_particles': 32, 'state_dim': 4, 'obs_dim': 4}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'production_ledh_pfpf_ot_gpu_tf32', 'default_execution_target': 'gpu', 'default_algorithm_target': 'ledh_pfpf_ot_tf32', 'default_target_status': 'production_default_by_owner_directive', 'default_dtype': 'float32', 'active_dtype': 'float64', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'production_ledh_pfpf_ot_gpu_tf32_default_lane', 'historical_module_path': 'experiments/dpf_implementation', 'public_api_exposure': 'separately_gated', 'dtype': 'float64', 'tf_dtype': 'float64', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`
- Proposal mode: `callback`
- Warm-start mode: `none`
- Return history: `True`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 16, 'col_chunk_size': 16, 'sinkhorn_iterations': 2, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `9.825822681887075`
- Warm-call timing summary seconds: `{'min': 0.021421320969238877, 'median': 0.021421320969238877, 'mean': 0.021421320969238877, 'max': 0.021421320969238877}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- production/default target by owner directive
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- no HMC readiness claim
- streaming removes dense transport storage but not all-pairs OT compute
