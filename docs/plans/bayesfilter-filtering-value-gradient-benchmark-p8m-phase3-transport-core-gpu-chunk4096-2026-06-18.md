# P8m Generic Transport-Core Benchmark

- JSON artifact: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-transport-core-gpu-chunk4096-2026-06-18.json`
- Shape: `{'model_family': 'synthetic_transport_core', 'batch_size': 5, 'num_particles': 10000, 'state_dim': 18}`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0', '/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 4096, 'col_chunk_size': 4096, 'sinkhorn_iterations': 10, 'sinkhorn_epsilon': 1.0, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `5.885974899865687`
- Warm-call timing summary seconds: `{'min': 0.8072548019699752, 'median': 0.8091801085975021, 'mean': 0.8091801085975021, 'max': 0.811105415225029}`
- Finite output: `True`
- Max row residual: `4.112720489501953e-05`
- Max column residual: `0.0`

## Nonclaims

- generic synthetic transport-core benchmark only
- not SIR d18 or any model-specific evidence
- not particle-count adequacy evidence
- not leaderboard completion
- not exact likelihood correctness
- not DPF gradient correctness
- not HMC/NUTS readiness
- not production/default readiness
