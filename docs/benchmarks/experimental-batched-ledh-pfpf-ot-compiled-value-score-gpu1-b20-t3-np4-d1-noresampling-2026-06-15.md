# Experimental Batched LEDH-PFPF-OT Benchmark: compiled-value-score

Authoritative JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-score-gpu1-b20-t3-np4-d1-noresampling-2026-06-15.json`.

| Field | Value |
| --- | --- |
| Mode | `compiled-value-score` |
| Device arg | `/GPU:0` |
| Device scope | `visible` |
| CUDA_VISIBLE_DEVICES | `1` |
| TensorFlow | `2.20.0` |
| Shape | `{'batch_size': 20, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}` |
| Transport | `{'policy': 'no-resampling', 'gradient_mode': 'raw', 'sinkhorn_iterations': 10}` |
| Compiler | `{'tf_function': True, 'jit_compile': True, 'compile_and_first_call_seconds': 8.72824621386826, 'warm_calls_exclude_compile': True, 'compiled_unit': 'batched_value_score'}` |
| Timing summary | `{'min_seconds': 0.0017481420654803514, 'median_seconds': 0.0017819565255194902, 'mean_seconds': 0.001785598718561232, 'max_seconds': 0.0018272609449923038}` |
| Finite outputs | `True` |

Non-claims: no production/default readiness, no classical particle-filter score correctness, no posterior validity, and no HMC/NeuTra readiness.
