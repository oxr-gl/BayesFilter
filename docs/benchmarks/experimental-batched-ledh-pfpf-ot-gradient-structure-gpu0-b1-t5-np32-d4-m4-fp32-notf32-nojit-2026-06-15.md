# LEDH-PFPF-OT Gradient Structure Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-gradient-structure-gpu0-b1-t5-np32-d4-m4-fp32-notf32-nojit-2026-06-15.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 5, 'num_particles': 32, 'state_dim': 4, 'obs_dim': 4, 'parameter_dim': 3}`
- Precision: `{'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`

## Arms

| arm | finite | compile+first s | warm median s | score preview |
| --- | --- | ---: | ---: | --- |
| original_dense_tensor | True | 9.70659 | 0.09681132296100259 | `[-0.5255336761474609, -3.8585500717163086, -5.943467140197754]` |
| streaming_dense_tensor | True | 4.34179 | 0.23695311206392944 | `[-0.5255336761474609, -3.8585503101348877, -5.943467140197754]` |
| streaming_streaming_tensor | True | 9.5763 | 0.3504844100680202 | `[-0.5255336761474609, -3.8585500717163086, -5.943467140197754]` |
| streaming_streaming_equivalent_callback | True | 8.76364 | 0.31413344806060195 | `[-0.5255336761474609, -3.8585500717163086, -5.943467140197754]` |

## Drift Vs Original Dense Tensor

| arm | value max abs | score max abs | score rel | score cosine | norm ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| streaming_dense_tensor | 0 | 2.38419e-07 | 6.17897e-08 | 1 | 1.00000002 |
| streaming_streaming_tensor | 2.38419e-07 | 0 | 0 | 1 | 1 |
| streaming_streaming_equivalent_callback | 2.38419e-07 | 0 | 0 | 1 | 1 |

## Nonclaims

- focused deterministic gradient-structure diagnostic only
- dense arm is a small-reference oracle, not a scalable implementation
- no HMC convergence or energy-conservation claim
- no posterior validity claim
- single fixture and single seed only
