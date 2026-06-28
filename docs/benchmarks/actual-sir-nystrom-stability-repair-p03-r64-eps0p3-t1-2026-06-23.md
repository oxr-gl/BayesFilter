# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t1-2026-06-23.json`
- Status: `PASS`
- Phase: `p03-r64-eps0p3-t1`
- Shape: `{'batch_size': 5, 'time_steps': 1, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `18.074075978947803` | `0.004402115009725094` | `[]` |
| nystrom | `PASS` | `16.439877156866714` | `0.019437390146777034` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.0`
- log_likelihood_mean_abs_delta: `0.0`
- warm_median_streaming_over_nystrom_descriptive: `0.22647665023357164`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
