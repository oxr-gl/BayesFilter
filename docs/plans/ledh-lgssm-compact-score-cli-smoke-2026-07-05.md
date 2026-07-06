# Same-Target LEDH LGSSM m3 T50 Value Runner

- JSON artifact: `docs/plans/ledh-lgssm-compact-score-cli-smoke-2026-07-05.json`
- Row: `benchmark_lgssm_exact_oracle_m3_T50`
- Target identity: `{'row_id': 'benchmark_lgssm_exact_oracle_m3_T50', 'row_scope': 'main_observed_data_filtering_row', 'dataset_seed': 81100, 'truth_theta': [0.72, 0.55, 0.35, 0.35, 0.45], 'time_steps': 2, 'num_particles': 4, 'batch_seeds': [81120], 'transport_policy': 'active-all', 'sinkhorn_iterations': 2, 'sinkhorn_epsilon': 0.5, 'full_row_expected': {'batch_seeds': [81120, 81121, 81122, 81123, 81124], 'num_particles': 1000, 'time_steps': 50, 'transport_policy': 'active-all', 'sinkhorn_iterations': 10, 'sinkhorn_epsilon': 0.5}, 'state_dim': 3, 'obs_dim': 3, 'full_leaderboard_row': False, 'same_target_status': 'prefix_diagnostic_not_full_leaderboard_row', 'dataset_source': 'scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:_lgssm_dataset', 'model_source': 'scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:_lgssm_benchmark_model', 'exact_value_comparator': 'tf_kalman_log_likelihood on same observations/model', 'exact_total_log_likelihood': -8.862150494354594, 'exact_average_log_likelihood': -4.431075247177297, 'score_status': 'executed_compact_score_fd_pass_but_material_gate_blocked', 'score_admission_status': 'blocked_material_gate_not_full_gpu_row'}`
- Comparison status: `executed_prefix_value_diagnostic_score_blocked`
- Value status: `executed_prefix_value_not_full_row`
- Score status: `executed_compact_score_fd_pass_but_material_gate_blocked`
- Shape: `{'batch_size': 1, 'batch_seed_count': 1, 'time_steps': 2, 'num_particles': 4, 'state_dim': 3, 'obs_dim': 3}`
- Output devices: `['/job:localhost/replica:0/task:0/device:CPU:0']`
- Precision: `{'precision_default_policy': 'production_ledh_pfpf_ot_gpu_tf32', 'default_execution_target': 'gpu', 'default_algorithm_target': 'ledh_pfpf_ot_tf32', 'default_target_status': 'production_default_by_owner_directive', 'default_route_acceptance': 'accepted_default_use_whenever_possible', 'default_route_guidance': 'use for BayesFilter DPF LEDH-PFPF-OT work whenever GPU execution and the streaming fixed-branch contract are applicable', 'default_route_rationale': 'streaming GPU TF32 LEDH-PFPF-OT avoids dense transport/history storage for large-particle DPF transport while preserving explicit reference and fallback arms', 'default_dtype': 'float32', 'active_dtype': 'float64', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'production_ledh_pfpf_ot_gpu_tf32_default_lane', 'historical_module_path': 'experiments/dpf_implementation', 'public_api_exposure': 'separately_gated', 'dtype': 'float64', 'tf_dtype': 'float64', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`
- Compile plus first call seconds: `6.451654595090076`
- Warm-call timing summary seconds: `{'min': 0.0026516560465097427, 'median': 0.0026516560465097427, 'mean': 0.0026516560465097427, 'max': 0.0026516560465097427}`
- Total log likelihood mean: `-9.1737491587761`
- Total log likelihood SD: `None`
- Total log likelihood MCSE: `None`
- Average log likelihood mean: `-4.58687457938805`
- Average log likelihood MCSE: `None`
- Exact Kalman total log likelihood: `-8.862150494354594`
- Exact Kalman average log likelihood: `-4.431075247177297`
- Average delta to exact: `-0.15579933221075315`
- Average relative error: `0.03516061531791886`
- Finite output: `True`

## Nonclaims

- not exact Kalman score evidence
- not HMC/NUTS readiness evidence
- not posterior correctness evidence
- not runtime-rankable against frozen non-LEDH rows
- not evidence for nonlinear rows
- compact total score passed same-scalar FD on this run but is not admitted as a full GPU leaderboard score
