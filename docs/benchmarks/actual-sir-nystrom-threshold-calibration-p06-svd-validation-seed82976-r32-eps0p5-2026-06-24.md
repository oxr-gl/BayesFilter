# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-seed82976-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P06-SVD-VALIDATION-SEED82976`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `37.53168429294601` | `23.27984587312676` | `[]` |
| nystrom | `PASS` | `29.775022062007338` | `19.416581499157473` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.08599853515625`
- log_likelihood_mean_abs_delta: `3.08599853515625`
- warm_median_streaming_over_nystrom_descriptive: `1.1989672782583753`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
