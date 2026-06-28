# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09b-eps0p375-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09B-EPS0P375`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `23.286987856961787` | `0.10780181107111275` | `[]` |
| nystrom | `PASS` | `16.066952373133972` | `0.06030270014889538` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.39056396484375`
- log_likelihood_mean_abs_delta: `1.42574462890625`
- warm_median_streaming_over_nystrom_descriptive: `1.7876780111825135`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
