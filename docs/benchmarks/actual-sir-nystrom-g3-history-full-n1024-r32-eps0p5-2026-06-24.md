# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-g3-history-full-n1024-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-G3-HISTORY-FULL-N1024`
- Shape: `{'batch_size': 3, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `18.32646277011372` | `0.08728151605464518` | `[]` |
| nystrom | `PASS` | `14.642232771031559` | `0.0898106771055609` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.889892578125`
- log_likelihood_mean_abs_delta: `3.0362345377604165`
- warm_median_streaming_over_nystrom_descriptive: `0.9718389713514461`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
