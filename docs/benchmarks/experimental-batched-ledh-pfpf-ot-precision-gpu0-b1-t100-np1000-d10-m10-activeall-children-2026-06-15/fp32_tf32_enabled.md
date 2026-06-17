# Streaming Experimental Batched LEDH-PFPF-OT LGSSM Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-precision-gpu0-b1-t100-np1000-d10-m10-activeall-children-2026-06-15/fp32_tf32_enabled.json`
- Shape: `{'batch_size': 1, 'time_steps': 100, 'num_particles': 1000, 'state_dim': 10, 'obs_dim': 10}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True, 'fp64_default_preserved_when_unspecified': False}`
- Proposal mode: `callback`
- Return history: `True`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 512, 'col_chunk_size': 512, 'sinkhorn_iterations': 4, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `13.56369158392772`
- Warm-call timing summary seconds: `{'min': 3.1095922680106014, 'median': 3.1095922680106014, 'mean': 3.1095922680106014, 'max': 3.1095922680106014}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- streaming removes dense transport storage but not all-pairs OT compute
