# Predator-Prey Same-Target LEDH Forward Scalar

- JSON artifact: `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json`
- Row: `zhao_cui_predator_prey_T20`
- Shape: `{'batch_size': 5, 'batch_seed_count': 5, 'time_steps': 20, 'num_particles': 10000, 'state_dim': 2, 'obs_dim': 2}`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'production_ledh_pfpf_ot_gpu_tf32', 'default_execution_target': 'gpu', 'default_algorithm_target': 'ledh_pfpf_ot_tf32', 'default_target_status': 'production_default_by_owner_directive', 'default_route_acceptance': 'accepted_default_use_whenever_possible', 'default_route_guidance': 'use for BayesFilter DPF LEDH-PFPF-OT work whenever GPU execution and the streaming fixed-branch contract are applicable', 'default_route_rationale': 'streaming GPU TF32 LEDH-PFPF-OT avoids dense transport/history storage for large-particle DPF transport while preserving explicit reference and fallback arms', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'production_ledh_pfpf_ot_gpu_tf32_default_lane', 'historical_module_path': 'experiments/dpf_implementation', 'public_api_exposure': 'separately_gated', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`
- History mode: `value-only`
- Compile plus first call seconds: `34.134711731923744`
- Warm-call timing summary seconds: `{'min': 19.095908388961107, 'median': 19.095908388961107, 'mean': 19.095908388961107, 'max': 19.095908388961107}`
- Finite output: `True`
- Admission status: `n10000_same_target_value_admitted`

## Nonclaims

- not score admission
- not score correctness
- not exact nonlinear likelihood correctness evidence
- not Zhao-Cui TT/SIRT source-faithfulness evidence
- not HMC readiness evidence
- not posterior correctness evidence
- not runtime ranking evidence
