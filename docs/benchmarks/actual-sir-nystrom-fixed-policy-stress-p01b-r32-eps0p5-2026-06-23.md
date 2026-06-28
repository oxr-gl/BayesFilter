# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p01b-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-STRESS-P01B-R32-EPS0P5`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.42966226208955` | `0.10097463894635439` | `[]` |
| nystrom | `PASS` | `15.551763308933005` | `0.09584797406569123` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.33306884765625`
- log_likelihood_mean_abs_delta: `2.1892333984375`
- warm_median_streaming_over_nystrom_descriptive: `1.0534874621048276`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
