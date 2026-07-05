# Streaming Default GPU LEDH-PFPF-OT TF32 LGSSM Benchmark

- JSON artifact: `docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.json`
- Shape: `{'batch_size': 1, 'time_steps': 200, 'num_particles': 50000, 'state_dim': 20, 'obs_dim': 20}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'production_ledh_pfpf_ot_gpu_tf32', 'default_execution_target': 'gpu', 'default_algorithm_target': 'ledh_pfpf_ot_tf32', 'default_target_status': 'production_default_by_owner_directive', 'default_route_acceptance': 'accepted_default_use_whenever_possible', 'default_route_guidance': 'use for BayesFilter DPF LEDH-PFPF-OT work whenever GPU execution and the streaming fixed-branch contract are applicable', 'default_route_rationale': 'streaming GPU TF32 LEDH-PFPF-OT avoids dense transport/history storage for large-particle DPF transport while preserving explicit reference and fallback arms', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'production_ledh_pfpf_ot_gpu_tf32_default_lane', 'historical_module_path': 'experiments/dpf_implementation', 'public_api_exposure': 'separately_gated', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`
- Proposal mode: `callback`
- Warm-start mode: `none`
- Return history: `False`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 1024, 'col_chunk_size': 1024, 'sinkhorn_iterations': 10, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `921.5817940990091`
- Warm-call timing summary seconds: `{'min': 860.8775105639943, 'median': 860.8775105639943, 'mean': 860.8775105639943, 'max': 860.8775105639943}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- production/default target by owner directive
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- no HMC readiness claim
- streaming removes dense transport storage but not all-pairs OT compute
