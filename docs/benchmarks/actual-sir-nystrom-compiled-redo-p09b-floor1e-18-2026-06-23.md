# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09b-floor1e-18-2026-06-23.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09B-FLOOR1E-18`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['nystrom:nonfinite_log_likelihood', 'nystrom:nonfinite_nystrom_factors', 'nystrom:nonfinite_nystrom_particles']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `23.100109250983223` | `0.10688727907836437` | `[]` |
| nystrom | `FAIL` | `16.541514484910294` | `0.2555037059355527` | `['nonfinite_log_likelihood', 'nonfinite_nystrom_factors', 'nonfinite_nystrom_particles']` |

## Paired Comparability

- log_likelihood_max_abs_delta: `nan`
- log_likelihood_mean_abs_delta: `nan`
- warm_median_streaming_over_nystrom_descriptive: `0.4183394471206817`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
