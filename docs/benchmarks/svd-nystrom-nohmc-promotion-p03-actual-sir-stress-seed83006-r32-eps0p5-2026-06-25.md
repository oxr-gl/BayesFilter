# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83006-r32-eps0p5-2026-06-25.json`
- Status: `PASS`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P03-ACTUAL-SIR-STRESS-SEED83006`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.77120614494197` | `1.8193529290147126` | `[]` |
| nystrom | `PASS` | `16.181258874945343` | `3.008136878022924` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.1468505859375`
- log_likelihood_mean_abs_delta: `0.1468505859375`
- warm_median_streaming_over_nystrom_descriptive: `0.6048105531057048`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
