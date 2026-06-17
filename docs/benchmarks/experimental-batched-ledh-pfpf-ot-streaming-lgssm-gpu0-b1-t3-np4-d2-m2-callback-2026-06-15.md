# Streaming Experimental Batched LEDH-PFPF-OT LGSSM Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t3-np4-d2-m2-callback-2026-06-15.json`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 4, 'state_dim': 2, 'obs_dim': 2}`
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Proposal mode: `callback`
- Return history: `False`
- Transport: `{'plan_mode': 'streaming', 'gradient_mode': 'raw', 'row_chunk_size': 2, 'col_chunk_size': 2, 'sinkhorn_iterations': 4, 'sinkhorn_epsilon': 0.5, 'annealed_scaling': 0.9, 'annealed_convergence_threshold': 0.001, 'dense_transport_matrix_materialized': False}`
- Compile plus first call seconds: `8.035441073821858`
- Warm-call timing summary seconds: `{'min': 0.007213623961433768, 'median': 0.007213623961433768, 'mean': 0.007213623961433768, 'max': 0.007213623961433768}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no posterior validity claim
- no active transport gradient validation claim
- streaming removes dense transport storage but not all-pairs OT compute
