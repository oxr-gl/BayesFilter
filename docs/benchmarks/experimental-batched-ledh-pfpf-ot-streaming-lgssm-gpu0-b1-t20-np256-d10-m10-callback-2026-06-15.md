# Streaming Experimental Batched LEDH-PFPF-OT LGSSM Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t20-np256-d10-m10-callback-2026-06-15.json`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 256, 'state_dim': 10, 'obs_dim': 10}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Proposal mode: `callback`
- Return history: `False`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 128, 'col_chunk_size': 128, 'sinkhorn_iterations': 4, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `9.670936548151076`
- Warm-call timing summary seconds: `{'min': 0.26548448810353875, 'median': 0.26548448810353875, 'mean': 0.26548448810353875, 'max': 0.26548448810353875}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- streaming removes dense transport storage but not all-pairs OT compute
