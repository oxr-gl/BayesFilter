# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03-moderate-b1-t20-n1024-2026-06-22.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P03-MODERATE-B1-T20-N1024`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `15.772794160991907` | `0.062396966852247715` | `[]` |
| nystrom | `PASS` | `804.5176504359115` | `0.09494141908362508` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.1632080078125`
- log_likelihood_mean_abs_delta: `0.1632080078125`
- warm_median_streaming_over_nystrom_descriptive: `0.6572154435282669`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
