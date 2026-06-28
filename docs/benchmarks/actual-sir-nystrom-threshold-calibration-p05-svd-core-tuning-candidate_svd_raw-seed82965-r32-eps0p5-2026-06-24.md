# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-candidate_svd_raw-seed82965-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P05-CANDIDATE_SVD_RAW-SEED82965`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.898900707019493` | `1.1796291088685393` | `[]` |
| nystrom | `PASS` | `15.551288357935846` | `1.8768082919996232` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `1.3131103515625`
- log_likelihood_mean_abs_delta: `1.3131103515625`
- warm_median_streaming_over_nystrom_descriptive: `0.6285293569391243`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
