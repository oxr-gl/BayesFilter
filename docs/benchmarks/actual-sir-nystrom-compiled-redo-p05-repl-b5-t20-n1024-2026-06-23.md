# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P05-REPL-B5-T20-N1024`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.843501010909677` | `0.1679728280287236` | `[]` |
| nystrom | `PASS` | `13.852564461063594` | `0.07246675505302846` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `7.10369873046875`
- log_likelihood_mean_abs_delta: `3.2791748046875`
- warm_median_streaming_over_nystrom_descriptive: `2.317929482364808`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
