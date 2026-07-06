# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t4-2026-06-23.json`
- Status: `FAIL`
- Phase: `p03-r32-eps0p25-t4`
- Shape: `{'batch_size': 5, 'time_steps': 4, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['nystrom:nystrom_row_residual_threshold']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `22.6894579869695` | `0.15249136881902814` | `[]` |
| nystrom | `FAIL` | `17.890998397022486` | `0.14644393790513277` | `['nystrom_row_residual_threshold']` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.43927001953125`
- log_likelihood_mean_abs_delta: `0.1900390625`
- warm_median_streaming_over_nystrom_descriptive: `1.041295194600769`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
