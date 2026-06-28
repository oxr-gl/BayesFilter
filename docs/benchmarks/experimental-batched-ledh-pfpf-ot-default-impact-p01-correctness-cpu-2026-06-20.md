# Streaming LEDH-PFPF-OT Correctness Gate

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json`
- Overall passed: `True`
- Shape: `{'batch_size': 2, 'time_steps': 2, 'num_particles': 3, 'state_dim': 1, 'obs_dim': 1, 'parameter_dim': 3}`
- Source diagnostics: `{'module': '/home/ubuntu/python/BayesFilter/experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py', 'uses_python_time_loop': False, 'uses_tf_while_loop': True, 'default_transport_plan_mode_streaming': True, 'default_return_history_false': True, 'stores_python_history_lists': False, 'calls_numpy': False}`

## Checks

- finite_outputs: `True` (promotion_veto)
- streaming_vs_baseline_parity: `True` (promotion_veto)
- likelihood_only_omits_history: `True` (promotion_veto)
- device_placement: `True` (promotion_veto)
- jit_compile_smoke: `True` (promotion_veto)
- source_uses_tf_while_loop_not_python_time_loop: `True` (promotion_veto)

## Nonclaims

- streaming DPF correctness gate only
- production/default target by owner directive
- no GPU performance claim
- no posterior validity claim
- no active-transport finite-difference score equivalence claim
- no HMC/NeuTra readiness claim
