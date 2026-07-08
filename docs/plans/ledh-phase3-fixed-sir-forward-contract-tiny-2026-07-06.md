# P8j TF32 Batched Actual-SIR Probe

- JSON artifact: `docs/plans/ledh-phase3-fixed-sir-forward-contract-tiny-2026-07-06.json`
- Row: `zhao_cui_spatial_sir_austria_j9_T20`
- Shape: `{'batch_size': 1, 'batch_seed_count': 1, 'time_steps': 1, 'num_particles': 4, 'state_dim': 18, 'obs_dim': 9}`
- Output devices: `['/job:localhost/replica:0/task:0/device:CPU:0']`
- Precision: `{'precision_default_policy': 'production_ledh_pfpf_ot_gpu_tf32', 'default_execution_target': 'gpu', 'default_algorithm_target': 'ledh_pfpf_ot_tf32', 'default_target_status': 'production_default_by_owner_directive', 'default_route_acceptance': 'accepted_default_use_whenever_possible', 'default_route_guidance': 'use for BayesFilter DPF LEDH-PFPF-OT work whenever GPU execution and the streaming fixed-branch contract are applicable', 'default_route_rationale': 'streaming GPU TF32 LEDH-PFPF-OT avoids dense transport/history storage for large-particle DPF transport while preserving explicit reference and fallback arms', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'production_ledh_pfpf_ot_gpu_tf32_default_lane', 'historical_module_path': 'experiments/dpf_implementation', 'public_api_exposure': 'separately_gated', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'disabled', 'tf32_execution_enabled': False}`
- History mode: `value-only`
- Compile plus first call seconds: `8.214400461874902`
- Warm-call timing summary seconds: `{'min': 0.0018852399662137032, 'median': 0.0018852399662137032, 'mean': 0.0018852399662137032, 'max': 0.0018852399662137032}`
- Speedup vs scalar comparator: `None`
- Finite output: `True`

## Nonclaims

- actual SIR d18 TF32/GPU feasibility probe only
- production/default target by owner directive
- not SIR d18 particle-count adequacy evidence
- not leaderboard completion
- not MC-SE adequacy evidence
- not exact likelihood correctness
- not DPF gradient correctness
- not HMC/NUTS readiness
- not Zhao-Cui TT/SIRT or MATLAB parity
