# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-r16-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09-SENSITIVITY-R16-EPS0P5`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.582022823859006` | `0.10225209896452725` | `[]` |
| nystrom | `PASS` | `14.201082793064415` | `0.05317273293621838` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.66204833984375`
- log_likelihood_mean_abs_delta: `1.0049560546875`
- warm_median_streaming_over_nystrom_descriptive: `1.9230175565205652`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
