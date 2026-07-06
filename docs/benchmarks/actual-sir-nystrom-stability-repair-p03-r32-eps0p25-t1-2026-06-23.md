# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t1-2026-06-23.json`
- Status: `PASS`
- Phase: `p03-r32-eps0p25-t1`
- Shape: `{'batch_size': 5, 'time_steps': 1, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.321344766998664` | `0.005390373058617115` | `[]` |
| nystrom | `PASS` | `15.77515568700619` | `0.011146125849336386` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.0`
- log_likelihood_mean_abs_delta: `0.0`
- warm_median_streaming_over_nystrom_descriptive: `0.4836095636707749`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
