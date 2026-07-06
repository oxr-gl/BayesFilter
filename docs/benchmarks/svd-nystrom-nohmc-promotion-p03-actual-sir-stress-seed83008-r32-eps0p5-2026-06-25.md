# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-seed83008-r32-eps0p5-2026-06-25.json`
- Status: `PASS`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P03-ACTUAL-SIR-STRESS-SEED83008`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.232096299994737` | `3.865215513855219` | `[]` |
| nystrom | `PASS` | `17.753863096004352` | `4.626989187905565` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.1309814453125`
- log_likelihood_mean_abs_delta: `0.1309814453125`
- warm_median_streaming_over_nystrom_descriptive: `0.8353629880870399`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
