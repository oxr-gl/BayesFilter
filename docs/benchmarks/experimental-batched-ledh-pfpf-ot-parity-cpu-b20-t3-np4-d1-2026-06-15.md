# Experimental Batched LEDH-PFPF-OT Benchmark: parity

Authoritative JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-parity-cpu-b20-t3-np4-d1-2026-06-15.json`.

| Field | Value |
| --- | --- |
| Mode | `parity` |
| Device arg | `/CPU:0` |
| Device scope | `cpu` |
| CUDA_VISIBLE_DEVICES | `-1` |
| TensorFlow | `2.20.0` |
| Shape | `{'batch_size': 20, 'time_steps': 3, 'num_particles': 4, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}` |
| Transport | `{'policy': 'active', 'gradient_mode': 'raw', 'sinkhorn_iterations': 10}` |
| Compiler | `{'tf_function': True, 'jit_compile': True, 'compiled_unit': 'batched_value_and_scalar_value_loop', 'warm_calls_exclude_compile': True}` |
| Timing summary | `{'min_seconds': 0.00042723282240331173, 'median_seconds': 0.000441012904047966, 'mean_seconds': 0.000444546186675628, 'max_seconds': 0.00046539283357560635}` |
| Finite outputs | `True` |

Non-claims: no production/default readiness, no classical particle-filter score correctness, no posterior validity, and no HMC/NeuTra readiness.
