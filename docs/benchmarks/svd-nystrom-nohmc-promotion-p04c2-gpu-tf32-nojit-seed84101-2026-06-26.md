# SVD-Nystrom Range-Bearing Gate

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101-2026-06-26.json`
- Status: `FAIL`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P04C2-GPU-TF32-NOJIT-SEED84101`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 4, 'obs_dim': 2}`
- Fixture: `range_bearing_gaussian_moderate`
- Route request: `streaming`
- JIT compile: `False`
- Hard vetoes: `['streaming:route_exception']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | ESS fraction min | Hard vetoes |
| --- | --- | ---: | ---: | ---: | --- |
| streaming | `FAIL` | `27.97145091695711` | `None` | `None` | `['route_exception']` |

## Route Exceptions

- streaming: `tensorflow.python.framework.errors_impl.InvalidArgumentError` at `compile_and_first`: `Graph execution error:

Detected at node while/while/MatrixInverse defined at (most recent call last):
  File "/home/ubuntu/python/BayesFilter/docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py", line 1325, in <module>

  File "/home/ubuntu/python/BayesFilter/docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py", line 1312, in main

  File "/home/ubuntu/python/BayesFilter/docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py", line 1063, in build_result

  File "/home/ubuntu/python/BayesFilter/docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py", line 1010, in compiled_streaming

  File "/home/ubuntu/python/BayesFilter/docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py", line 740, in _streaming_outputs

  File "/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py", line 473, in streaming_batched_ledh_pfpf_ot_value_core_tf

  File "/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py", line 537, in streaming_batched_ledh_pfpf_ot_value_core_tf

  File "/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py", line 510, in history_body

  File "/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py", line 370, in step_body

  File "/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py", line 211, in batched_ledh_flow_streaming_particles_tf

  File "/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py", line 192, in body

  File "/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py", line 628, in batched_ledh_flow_core_tf

Input is not invertible.
	 [[{{node while/while/MatrixInverse}}]] [Op:__inference_compiled_streaming_4954]`

## Paired Comparability

- Not applicable.

## Nonclaims

- P04 range-bearing nonlinear Gaussian DPF gate only
- no default promotion claim
- no posterior correctness claim
- no statistical superiority claim
- no HMC readiness claim
- no broad nonlinear validity claim
