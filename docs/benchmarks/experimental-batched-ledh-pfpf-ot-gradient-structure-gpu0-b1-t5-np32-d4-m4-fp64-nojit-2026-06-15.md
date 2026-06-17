# LEDH-PFPF-OT Gradient Structure Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-gradient-structure-gpu0-b1-t5-np32-d4-m4-fp64-nojit-2026-06-15.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 5, 'num_particles': 32, 'state_dim': 4, 'obs_dim': 4, 'parameter_dim': 3}`
- Precision: `{'dtype': 'float64', 'tf_dtype': 'float64', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`

## Arms

| arm | finite | compile+first s | warm median s | score preview |
| --- | --- | ---: | ---: | --- |
| original_dense_tensor | True | 10.0732 | 0.11666458006948233 | `[-0.5255336369453034, -3.85855025566792, -5.943467907625774]` |
| streaming_dense_tensor | True | 4.41985 | 0.21710404194891453 | `[-0.5255336369453035, -3.8585502556679194, -5.943467907625773]` |
| streaming_streaming_tensor | True | 9.59637 | 0.30765779595822096 | `[-0.5255336369453035, -3.858550255667919, -5.943467907625772]` |
| streaming_streaming_equivalent_callback | True | 9.01766 | 0.31001743697561324 | `[-0.5255336369453035, -3.858550255667919, -5.943467907625772]` |

## Drift Vs Original Dense Tensor

| arm | value max abs | score max abs | score rel | score cosine | norm ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| streaming_dense_tensor | 0 | 8.88178e-16 | 1.49438e-16 | 1 | 1 |
| streaming_streaming_tensor | 0 | 1.77636e-15 | 2.98875e-16 | 1 | 1 |
| streaming_streaming_equivalent_callback | 0 | 1.77636e-15 | 2.98875e-16 | 1 | 1 |

## Nonclaims

- focused deterministic gradient-structure diagnostic only
- dense arm is a small-reference oracle, not a scalable implementation
- no HMC convergence or energy-conservation claim
- no posterior validity claim
- single fixture and single seed only
