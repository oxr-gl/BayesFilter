# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-r16-eps1p0-2026-06-23.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09-SENSITIVITY-R16-EPS1P0`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_log_likelihood_max_abs_delta', 'paired:paired_log_likelihood_mean_abs_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.962640949059278` | `0.10144459293223917` | `[]` |
| nystrom | `PASS` | `14.877965098945424` | `0.05446005007252097` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `10.30291748046875`
- log_likelihood_mean_abs_delta: `5.30792236328125`
- warm_median_streaming_over_nystrom_descriptive: `1.862734110548042`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
