# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-LARGER-N-B5-T20-N2048`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 2048, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `20.986187719972804` | `0.41184131195768714` | `[]` |
| nystrom | `PASS` | `14.94269566400908` | `0.1320293180178851` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.65521240234375`
- log_likelihood_mean_abs_delta: `2.67186279296875`
- warm_median_streaming_over_nystrom_descriptive: `3.1193171194135676`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
