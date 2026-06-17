# Experimental Batched LEDH-PFPF-OT Benchmark: compiled-value-score

Authoritative JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-score-gpu1-b256-t3-np4-d1-noresampling-2026-06-15.json`.

| Field | Value |
| --- | --- |
| Mode | `compiled-value-score` |
| Device arg | `/GPU:0` |
| Device scope | `visible` |
| CUDA_VISIBLE_DEVICES | `1` |
| TensorFlow | `2.20.0` |
| Shape | `{'batch_size': 256, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}` |
| Transport | `{'policy': 'no-resampling', 'gradient_mode': 'raw', 'sinkhorn_iterations': 10}` |
| Compiler | `{'tf_function': True, 'jit_compile': True, 'compile_and_first_call_seconds': 8.727717956993729, 'warm_calls_exclude_compile': True, 'compiled_unit': 'batched_value_score'}` |
| Timing summary | `{'min_seconds': 0.0018587831873446703, 'median_seconds': 0.001891492516733706, 'mean_seconds': 0.0019011530559509993, 'max_seconds': 0.0019669511821120977}` |
| Finite outputs | `True` |

Non-claims: no production/default readiness, no classical particle-filter score correctness, no posterior validity, and no HMC/NeuTra readiness.
