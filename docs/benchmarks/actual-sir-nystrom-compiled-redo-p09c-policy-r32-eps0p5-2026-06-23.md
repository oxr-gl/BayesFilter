# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09c-policy-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09C-POLICY-R32-EPS0P5`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `24.573047617916018` | `1.2354246410541236` | `[]` |
| nystrom | `PASS` | `16.61751942615956` | `0.31807074206881225` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.67596435546875`
- log_likelihood_mean_abs_delta: `2.21041259765625`
- warm_median_streaming_over_nystrom_descriptive: `3.8841190894158024`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
