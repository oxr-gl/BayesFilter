# P8j TF32 Batched Actual-SIR Probe

- JSON artifact: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it10-stability-2026-06-18.json`
- Row: `zhao_cui_spatial_sir_austria_j9_T20`
- Shape: `{'batch_size': 5, 'batch_seed_count': 5, 'time_steps': 20, 'num_particles': 10000, 'state_dim': 18, 'obs_dim': 9}`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`
- History mode: `value-only`
- Compile plus first call seconds: `22.11197322793305`
- Warm-call timing summary seconds: `{'min': 8.316487872973084, 'median': 8.554354273481295, 'mean': 8.554354273481295, 'max': 8.792220673989505}`
- Speedup vs scalar comparator: `92.32206648820492`
- Finite output: `True`

## Nonclaims

- actual SIR d18 TF32/GPU feasibility probe only
- not SIR d18 particle-count adequacy evidence
- not leaderboard completion
- not MC-SE adequacy evidence
- not exact likelihood correctness
- not DPF gradient correctness
- not HMC/NUTS readiness
- not Zhao-Cui TT/SIRT or MATLAB parity
- not production/default readiness
