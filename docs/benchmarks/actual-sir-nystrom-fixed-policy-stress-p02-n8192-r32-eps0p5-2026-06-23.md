# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p02-n8192-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-STRESS-P02-N8192-R32-EPS0P5`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.58891815901734` | `1.2583262950647622` | `[]` |
| nystrom | `PASS` | `12.671761007979512` | `0.1889614760875702` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.5208740234375`
- log_likelihood_mean_abs_delta: `2.5208740234375`
- warm_median_streaming_over_nystrom_descriptive: `6.659168424793727`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
