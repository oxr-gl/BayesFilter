# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82931-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-G1-N8192-SEED82931`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.978156581055373` | `1.305418172152713` | `[]` |
| nystrom | `PASS` | `13.120605390984565` | `0.19512153696268797` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.3763427734375`
- log_likelihood_mean_abs_delta: `3.3763427734375`
- warm_median_streaming_over_nystrom_descriptive: `6.690282336195112`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
