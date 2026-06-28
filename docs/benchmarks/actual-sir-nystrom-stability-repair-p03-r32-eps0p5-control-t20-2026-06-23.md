# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p5-control-t20-2026-06-23.json`
- Status: `PASS`
- Phase: `p03-r32-eps0p5-control-t20`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `24.467250163899735` | `1.2572842040099204` | `[]` |
| nystrom | `PASS` | `17.89030892099254` | `0.6118852200452238` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.20867919921875`
- log_likelihood_mean_abs_delta: `1.72391357421875`
- warm_median_streaming_over_nystrom_descriptive: `2.054771324460159`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
