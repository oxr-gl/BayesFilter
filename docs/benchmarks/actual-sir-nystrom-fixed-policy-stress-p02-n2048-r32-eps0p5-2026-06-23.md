# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n2048-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-STRESS-P02-N2048-R32-EPS0P5`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 2048, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.20302305696532` | `0.13861045008525252` | `[]` |
| nystrom | `PASS` | `14.3825078450609` | `0.08603927306830883` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.3642578125`
- log_likelihood_mean_abs_delta: `4.3642578125`
- warm_median_streaming_over_nystrom_descriptive: `1.6110137282913357`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
