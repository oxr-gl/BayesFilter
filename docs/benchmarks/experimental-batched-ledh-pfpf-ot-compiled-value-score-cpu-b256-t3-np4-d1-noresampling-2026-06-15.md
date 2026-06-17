# Experimental Batched LEDH-PFPF-OT Benchmark: compiled-value-score

Authoritative JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-score-cpu-b256-t3-np4-d1-noresampling-2026-06-15.json`.

| Field | Value |
| --- | --- |
| Mode | `compiled-value-score` |
| Device arg | `/CPU:0` |
| Device scope | `cpu` |
| CUDA_VISIBLE_DEVICES | `-1` |
| TensorFlow | `2.20.0` |
| Shape | `{'batch_size': 256, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}` |
| Transport | `{'policy': 'no-resampling', 'gradient_mode': 'raw', 'sinkhorn_iterations': 10}` |
| Compiler | `{'tf_function': True, 'jit_compile': True, 'compile_and_first_call_seconds': 6.245071802055463, 'warm_calls_exclude_compile': True, 'compiled_unit': 'batched_value_score'}` |
| Timing summary | `{'min_seconds': 0.009563067927956581, 'median_seconds': 0.009943582466803491, 'mean_seconds': 0.010002010711468756, 'max_seconds': 0.010390395997092128}` |
| Finite outputs | `True` |

Non-claims: no production/default readiness, no classical particle-filter score correctness, no posterior validity, and no HMC/NeuTra readiness.
