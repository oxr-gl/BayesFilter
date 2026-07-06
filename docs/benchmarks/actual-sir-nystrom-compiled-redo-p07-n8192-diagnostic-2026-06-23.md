# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-N8192-DIAGNOSTIC`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `33.77408173913136` | `17.025218456983566` | `[]` |
| nystrom | `PASS` | `11.30258442601189` | `0.8690328011289239` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.0142822265625`
- log_likelihood_mean_abs_delta: `0.0142822265625`
- warm_median_streaming_over_nystrom_descriptive: `19.59099637535755`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
