# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-control_cholesky_raw-seed82962-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P05-CONTROL_CHOL_RAW-SEED82962`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.90459826705046` | `1.171562171075493` | `[]` |
| nystrom | `PASS` | `12.517436685971916` | `0.18452755804173648` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.3240966796875`
- log_likelihood_mean_abs_delta: `0.3240966796875`
- warm_median_streaming_over_nystrom_descriptive: `6.348982143959814`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
