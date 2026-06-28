# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n4096-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-STRESS-P02-N4096-R32-EPS0P5`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.359824236948043` | `0.3957582979928702` | `[]` |
| nystrom | `PASS` | `12.597565095173195` | `0.12149465596303344` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.37554931640625`
- log_likelihood_mean_abs_delta: `2.37554931640625`
- warm_median_streaming_over_nystrom_descriptive: `3.257413215880751`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
