# Experimental Batched LEDH-PFPF-OT Benchmark: compiled-value

Authoritative JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-cpu-b20-t3-np4-d1-2026-06-15.json`.

| Field | Value |
| --- | --- |
| Mode | `compiled-value` |
| Device arg | `/CPU:0` |
| Device scope | `cpu` |
| CUDA_VISIBLE_DEVICES | `-1` |
| TensorFlow | `2.20.0` |
| Shape | `{'batch_size': 20, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}` |
| Transport | `{'policy': 'active', 'gradient_mode': 'raw', 'sinkhorn_iterations': 10}` |
| Compiler | `{'tf_function': True, 'jit_compile': True, 'compile_and_first_call_seconds': 3.6179225239902735, 'warm_calls_exclude_compile': True, 'compiled_unit': 'batched_value'}` |
| Timing summary | `{'min_seconds': 0.00040966388769447803, 'median_seconds': 0.0004247130127623677, 'mean_seconds': 0.0004238144727423787, 'max_seconds': 0.0004330528900027275}` |
| Finite outputs | `True` |

Non-claims: no production/default readiness, no classical particle-filter score correctness, no posterior validity, and no HMC/NeuTra readiness.
