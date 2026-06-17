# Experimental Batched LEDH-PFPF-OT Benchmark: compiled-value

Authoritative JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-compiled-value-gpu1-b4096-t3-np4-d1-2026-06-15.json`.

| Field | Value |
| --- | --- |
| Mode | `compiled-value` |
| Device arg | `/GPU:0` |
| Device scope | `visible` |
| CUDA_VISIBLE_DEVICES | `1` |
| TensorFlow | `2.20.0` |
| Shape | `{'batch_size': 4096, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}` |
| Transport | `{'policy': 'active', 'gradient_mode': 'raw', 'sinkhorn_iterations': 10}` |
| Compiler | `{'tf_function': True, 'jit_compile': True, 'compile_and_first_call_seconds': 4.726531384978443, 'warm_calls_exclude_compile': True, 'compiled_unit': 'batched_value'}` |
| Timing summary | `{'min_seconds': 0.0015851040370762348, 'median_seconds': 0.0016138739883899689, 'mean_seconds': 0.0016486677806824446, 'max_seconds': 0.0018265219405293465}` |
| Finite outputs | `True` |

Non-claims: no production/default readiness, no classical particle-filter score correctness, no posterior validity, and no HMC/NeuTra readiness.
