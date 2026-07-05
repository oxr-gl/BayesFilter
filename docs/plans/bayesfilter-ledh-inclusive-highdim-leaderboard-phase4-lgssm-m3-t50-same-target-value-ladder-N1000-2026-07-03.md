# Same-Target LEDH LGSSM m3 T50 Value Runner

- JSON artifact: `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N1000-2026-07-03.json`
- Row: `benchmark_lgssm_exact_oracle_m3_T50`
- Target identity: `{'row_id': 'benchmark_lgssm_exact_oracle_m3_T50', 'row_scope': 'main_observed_data_filtering_row', 'dataset_seed': 81100, 'truth_theta': [0.72, 0.55, 0.35, 0.35, 0.45], 'time_steps': 50, 'state_dim': 3, 'obs_dim': 3, 'full_leaderboard_row': True, 'same_target_status': 'same_target_value_only', 'dataset_source': 'scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:_lgssm_dataset', 'model_source': 'scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:_lgssm_benchmark_model', 'exact_value_comparator': 'tf_kalman_log_likelihood on same observations/model', 'exact_total_log_likelihood': -136.0759748579247, 'exact_average_log_likelihood': -2.721519497158494, 'score_status': 'blocked_score_same_target_total_derivative_not_implemented'}`
- Comparison status: `executed_value_only_score_blocked`
- Value status: `executed_same_target_value`
- Score status: `blocked_score_same_target_total_derivative_not_implemented`
- Shape: `{'batch_size': 5, 'batch_seed_count': 5, 'time_steps': 50, 'num_particles': 1000, 'state_dim': 3, 'obs_dim': 3}`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'production_ledh_pfpf_ot_gpu_tf32', 'default_execution_target': 'gpu', 'default_algorithm_target': 'ledh_pfpf_ot_tf32', 'default_target_status': 'production_default_by_owner_directive', 'default_route_acceptance': 'accepted_default_use_whenever_possible', 'default_route_guidance': 'use for BayesFilter DPF LEDH-PFPF-OT work whenever GPU execution and the streaming fixed-branch contract are applicable', 'default_route_rationale': 'streaming GPU TF32 LEDH-PFPF-OT avoids dense transport/history storage for large-particle DPF transport while preserving explicit reference and fallback arms', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'production_ledh_pfpf_ot_gpu_tf32_default_lane', 'historical_module_path': 'experiments/dpf_implementation', 'public_api_exposure': 'separately_gated', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`
- Compile plus first call seconds: `12.033080933964811`
- Warm-call timing summary seconds: `{'min': 1.4286807799944654, 'median': 1.4286807799944654, 'mean': 1.4286807799944654, 'max': 1.4286807799944654}`
- Total log likelihood mean: `-136.01973876953124`
- Total log likelihood SD: `0.174687936823129`
- Total log likelihood MCSE: `0.07812282031714102`
- Average log likelihood mean: `-2.720394775390625`
- Average log likelihood MCSE: `0.0015624564063428585`
- Exact Kalman total log likelihood: `-136.0759748579247`
- Exact Kalman average log likelihood: `-2.721519497158494`
- Average delta to exact: `0.0011247217678693744`
- Average relative error: `0.0004132697814745339`
- Finite output: `True`

## Nonclaims

- value-only LEDH row evidence
- score is blocked because same-target total derivative is not implemented here
- not HMC/NUTS readiness evidence
- not posterior correctness evidence
- not runtime-rankable against frozen non-LEDH rows
- not evidence for nonlinear rows
