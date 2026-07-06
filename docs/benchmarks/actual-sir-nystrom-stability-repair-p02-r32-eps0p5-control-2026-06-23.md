# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-STABILITY-REPAIR-P02-R32-EPS0P5-CONTROL`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `22.633406691951677` | `0.11001369683071971` | `[]` |
| nystrom | `PASS` | `18.276535650948063` | `0.13721206597983837` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.20867919921875`
- log_likelihood_mean_abs_delta: `1.72391357421875`
- warm_median_streaming_over_nystrom_descriptive: `0.8017785902799894`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
