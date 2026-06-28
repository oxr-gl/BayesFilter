# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-seed82950-r32-eps0p5-2026-06-24.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-EXT-SEED82950`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_log_likelihood_mean_abs_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.00605525984429` | `1.1797773169819266` | `[]` |
| nystrom | `PASS` | `12.442864062031731` | `0.18447330803610384` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `7.06475830078125`
- log_likelihood_mean_abs_delta: `7.06475830078125`
- warm_median_streaming_over_nystrom_descriptive: `6.395382234653854`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
