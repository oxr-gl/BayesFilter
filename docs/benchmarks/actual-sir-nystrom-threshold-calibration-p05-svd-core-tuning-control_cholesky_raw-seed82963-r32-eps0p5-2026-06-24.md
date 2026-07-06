# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-control_cholesky_raw-seed82963-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P05-CONTROL_CHOL_RAW-SEED82963`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.9344405089505` | `1.1771941299084574` | `[]` |
| nystrom | `PASS` | `12.406809519045055` | `0.1868232348933816` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.30877685546875`
- log_likelihood_mean_abs_delta: `0.30877685546875`
- warm_median_streaming_over_nystrom_descriptive: `6.301112014146805`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
