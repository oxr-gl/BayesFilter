# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09b-floor1e-24-2026-06-23.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09B-FLOOR1E-24`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['nystrom:nonfinite_log_likelihood', 'nystrom:nonfinite_nystrom_factors', 'nystrom:nonfinite_nystrom_particles']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `23.726060506887734` | `0.11543262493796647` | `[]` |
| nystrom | `FAIL` | `16.818943275138736` | `0.2624748160596937` | `['nonfinite_log_likelihood', 'nonfinite_nystrom_factors', 'nonfinite_nystrom_particles']` |

## Paired Comparability

- log_likelihood_max_abs_delta: `nan`
- log_likelihood_mean_abs_delta: `nan`
- warm_median_streaming_over_nystrom_descriptive: `0.4397855256014887`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
