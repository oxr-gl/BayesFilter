# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-seed82968-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P06-SVD-VALIDATION-SEED82968`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `40.686342251021415` | `24.097483278950676` | `[]` |
| nystrom | `PASS` | `36.51638640486635` | `23.305560522945598` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.17327880859375`
- log_likelihood_mean_abs_delta: `2.17327880859375`
- warm_median_streaming_over_nystrom_descriptive: `1.0339799918232127`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
