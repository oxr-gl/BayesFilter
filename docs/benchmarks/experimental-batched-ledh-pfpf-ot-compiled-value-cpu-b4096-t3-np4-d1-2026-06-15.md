# Experimental Batched LEDH-PFPF-OT Benchmark: compiled-value

Authoritative JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-cpu-b4096-t3-np4-d1-2026-06-15.json`.

| Field | Value |
| --- | --- |
| Mode | `compiled-value` |
| Device arg | `/CPU:0` |
| Device scope | `cpu` |
| CUDA_VISIBLE_DEVICES | `-1` |
| TensorFlow | `2.20.0` |
| Shape | `{'batch_size': 4096, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}` |
| Transport | `{'policy': 'active', 'gradient_mode': 'raw', 'sinkhorn_iterations': 10}` |
| Compiler | `{'tf_function': True, 'jit_compile': True, 'compile_and_first_call_seconds': 3.6594360119197518, 'warm_calls_exclude_compile': True, 'compiled_unit': 'batched_value'}` |
| Timing summary | `{'min_seconds': 0.030336604919284582, 'median_seconds': 0.03366596600972116, 'mean_seconds': 0.03325060671195388, 'max_seconds': 0.035342244897037745}` |
| Finite outputs | `True` |

Non-claims: no production/default readiness, no classical particle-filter score correctness, no posterior validity, and no HMC/NeuTra readiness.
