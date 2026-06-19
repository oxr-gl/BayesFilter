# P8j TF32 Batched Actual-SIR Probe

- JSON artifact: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk1024-2026-06-18.json`
- Row: `zhao_cui_spatial_sir_austria_j9_T20`
- Shape: `{'batch_size': 5, 'batch_seed_count': 5, 'time_steps': 20, 'num_particles': 50000, 'state_dim': 18, 'obs_dim': 9}`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Precision: `{'precision_default_policy': 'experimental_ledh_pfpf_ot_gpu_tf32', 'default_dtype': 'float32', 'active_dtype': 'float32', 'default_tf32_mode': 'enabled', 'fp64_reference_requires_explicit_dtype': True, 'scope': 'experimental_batched_ledh_pfpf_ot_gpu_performance_lane', 'dtype': 'float32', 'tf_dtype': 'float32', 'tf32_mode': 'enabled', 'tf32_execution_enabled': True}`
- History mode: `full`
- Compile plus first call seconds: `157.4267661301419`
- Warm-call timing summary seconds: `{'min': 140.19528393400833, 'median': 140.19528393400833, 'mean': 140.19528393400833, 'max': 140.19528393400833}`
- Speedup vs scalar comparator: `5.633254142641117`
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
