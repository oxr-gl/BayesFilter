# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-p01-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-P01-R32-EPS0P5`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.34431483782828` | `0.10925720911473036` | `[]` |
| nystrom | `PASS` | `15.877626703120768` | `0.09860881301574409` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.67596435546875`
- log_likelihood_mean_abs_delta: `2.21041259765625`
- warm_median_streaming_over_nystrom_descriptive: `1.1079862516678516`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
