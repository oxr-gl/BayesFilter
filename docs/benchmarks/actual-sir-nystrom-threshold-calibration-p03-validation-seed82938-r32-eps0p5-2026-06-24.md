# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-seed82938-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-SEED82938`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.39634355995804` | `1.2449482551310211` | `[]` |
| nystrom | `PASS` | `12.42411465710029` | `0.18905673292465508` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.15972900390625`
- log_likelihood_mean_abs_delta: `2.15972900390625`
- warm_median_streaming_over_nystrom_descriptive: `6.585051142437605`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
