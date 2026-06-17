# LEDH-PFPF-OT Gradient Structure Comparison

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-gradient-structure-gpu0-b1-t5-np32-d4-m4-fp32-tf32-nojit-2026-06-15.json`
- Overall passed: `False`
- Shape: `{'batch_size': 1, 'time_steps': 5, 'num_particles': 32, 'state_dim': 4, 'obs_dim': 4, 'parameter_dim': 3}`
- Precision: `{'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`

## Arms

| arm | finite | compile+first s | warm median s | score preview |
| --- | --- | ---: | ---: | --- |
| original_dense_tensor | True | 9.8639 | 0.12384212389588356 | `[-0.5255882143974304, -3.855031728744507, -5.941958427429199]` |
| streaming_dense_tensor | True | 4.41874 | 0.2190146220382303 | `[-0.5255882740020752, -3.8549253940582275, -5.942390441894531]` |
| streaming_streaming_tensor | True | 9.70673 | 0.31475669611245394 | `[-0.5256066918373108, -3.8549764156341553, -5.942390441894531]` |
| streaming_streaming_equivalent_callback | True | 8.92582 | 0.3354514678940177 | `[-0.5256066918373108, -3.8549764156341553, -5.942390441894531]` |

## Drift Vs Original Dense Tensor

| arm | value max abs | score max abs | score rel | score cosine | norm ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| streaming_dense_tensor | 2.38419e-07 | 0.000432014 | 7.27057e-05 | 0.999999999 | 1.00004276 |
| streaming_streaming_tensor | 4.76837e-07 | 0.000432014 | 7.27057e-05 | 0.999999999 | 1.00004685 |
| streaming_streaming_equivalent_callback | 4.76837e-07 | 0.000432014 | 7.27057e-05 | 0.999999999 | 1.00004685 |

## Nonclaims

- focused deterministic gradient-structure diagnostic only
- dense arm is a small-reference oracle, not a scalable implementation
- no HMC convergence or energy-conservation claim
- no posterior validity claim
- single fixture and single seed only
