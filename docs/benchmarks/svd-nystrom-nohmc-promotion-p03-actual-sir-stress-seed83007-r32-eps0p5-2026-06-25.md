# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83007-r32-eps0p5-2026-06-25.json`
- Status: `PASS`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P03-ACTUAL-SIR-STRESS-SEED83007`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.662347017088905` | `1.863593647023663` | `[]` |
| nystrom | `PASS` | `16.451974218944088` | `3.2329099129419774` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.13653564453125`
- log_likelihood_mean_abs_delta: `0.13653564453125`
- warm_median_streaming_over_nystrom_descriptive: `0.5764446573544562`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
