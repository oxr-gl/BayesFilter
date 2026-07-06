# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83003-r32-eps0p5-2026-06-25.json`
- Status: `PASS`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P03-ACTUAL-SIR-STRESS-SEED83003`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.39148784801364` | `1.769834134960547` | `[]` |
| nystrom | `PASS` | `16.006653475109488` | `2.8653868380934` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.08721923828125`
- log_likelihood_mean_abs_delta: `0.08721923828125`
- warm_median_streaming_over_nystrom_descriptive: `0.617659755894662`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
