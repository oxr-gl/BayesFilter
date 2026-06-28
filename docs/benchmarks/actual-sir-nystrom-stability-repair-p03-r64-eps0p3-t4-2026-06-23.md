# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t4-2026-06-23.json`
- Status: `FAIL`
- Phase: `p03-r64-eps0p3-t4`
- Shape: `{'batch_size': 5, 'time_steps': 4, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['nystrom:nystrom_row_residual_threshold', 'nystrom:nystrom_column_residual_threshold', 'nystrom:nonfinite_nystrom_particles']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `22.72600160795264` | `0.20150916394777596` | `[]` |
| nystrom | `FAIL` | `18.15528322290629` | `0.13921904610469937` | `['nystrom_row_residual_threshold', 'nystrom_column_residual_threshold', 'nonfinite_nystrom_particles']` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.7570343017578125`
- log_likelihood_mean_abs_delta: `0.3998291015625`
- warm_median_streaming_over_nystrom_descriptive: `1.44742525958863`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
