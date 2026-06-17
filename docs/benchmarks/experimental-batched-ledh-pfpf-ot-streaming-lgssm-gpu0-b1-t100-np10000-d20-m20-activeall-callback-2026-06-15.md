# Streaming Experimental Batched LEDH-PFPF-OT LGSSM Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t100-np10000-d20-m20-activeall-callback-2026-06-15.json`
- Shape: `{'batch_size': 1, 'time_steps': 100, 'num_particles': 10000, 'state_dim': 20, 'obs_dim': 20}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Proposal mode: `callback`
- Return history: `False`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 512, 'col_chunk_size': 512, 'sinkhorn_iterations': 4, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `269.35449231695384`
- Warm-call timing summary seconds: `{'min': 251.38541664206423, 'median': 251.38541664206423, 'mean': 251.38541664206423, 'max': 251.38541664206423}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- streaming removes dense transport storage but not all-pairs OT compute
