# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.json`
- Status: `FAIL`
- Phase: `p06-positive-projected-r32-eps0p25`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_log_likelihood_max_abs_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `23.06391632813029` | `0.11221770686097443` | `[]` |
| nystrom | `PASS` | `19.905844224849716` | `0.1276532649062574` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `12.91107177734375`
- log_likelihood_mean_abs_delta: `3.94317626953125`
- warm_median_streaming_over_nystrom_descriptive: `0.8790821522926334`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
