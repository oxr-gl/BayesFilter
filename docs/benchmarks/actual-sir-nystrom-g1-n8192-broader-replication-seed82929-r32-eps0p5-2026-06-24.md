# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82929-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-G1-N8192-SEED82929`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.313828550977632` | `1.1852087879087776` | `[]` |
| nystrom | `PASS` | `12.83746176911518` | `0.18711537984199822` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.813720703125`
- log_likelihood_mean_abs_delta: `2.813720703125`
- warm_median_streaming_over_nystrom_descriptive: `6.334106736226481`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
