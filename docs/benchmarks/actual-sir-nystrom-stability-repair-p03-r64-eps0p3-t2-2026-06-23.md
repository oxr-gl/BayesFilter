# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t2-2026-06-23.json`
- Status: `PASS`
- Phase: `p03-r64-eps0p3-t2`
- Shape: `{'batch_size': 5, 'time_steps': 2, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `22.550652779173106` | `0.04882577294483781` | `[]` |
| nystrom | `PASS` | `17.96733031095937` | `0.05349771794863045` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.0197906494140625`
- log_likelihood_mean_abs_delta: `0.01557464599609375`
- warm_median_streaming_over_nystrom_descriptive: `0.9126702000956614`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
