# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P04-SERIOUS-B5-T20-N1024`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.750352774048224` | `0.10740198497660458` | `[]` |
| nystrom | `PASS` | `14.019542706897482` | `0.05731428205035627` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.85498046875`
- log_likelihood_mean_abs_delta: `1.9035400390625`
- warm_median_streaming_over_nystrom_descriptive: `1.8739131178899058`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
