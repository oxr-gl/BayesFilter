# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-control_cholesky_raw-seed82966-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P05-CONTROL_CHOL_RAW-SEED82966`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.872108679963276` | `1.1771279168315232` | `[]` |
| nystrom | `PASS` | `12.419674908043817` | `0.18497399287298322` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.6912841796875`
- log_likelihood_mean_abs_delta: `2.6912841796875`
- warm_median_streaming_over_nystrom_descriptive: `6.363748214268295`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
