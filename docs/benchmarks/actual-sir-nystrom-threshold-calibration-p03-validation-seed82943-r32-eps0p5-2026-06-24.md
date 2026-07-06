# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-seed82943-r32-eps0p5-2026-06-24.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-SEED82943`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_log_likelihood_mean_abs_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.676348416134715` | `1.1799634417984635` | `[]` |
| nystrom | `PASS` | `12.356681011151522` | `0.18557946104556322` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `6.77288818359375`
- log_likelihood_mean_abs_delta: `6.77288818359375`
- warm_median_streaming_over_nystrom_descriptive: `6.358265268960774`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
