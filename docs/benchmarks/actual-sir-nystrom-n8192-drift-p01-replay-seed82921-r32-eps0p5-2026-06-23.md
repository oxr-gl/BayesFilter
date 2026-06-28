# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-NYSTROM-N8192-DRIFT-P01-REPLAY-SEED82921`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_log_likelihood_mean_abs_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.13461397611536` | `1.17632541898638` | `[]` |
| nystrom | `PASS` | `12.714504515053704` | `0.2623653309419751` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `6.96771240234375`
- log_likelihood_mean_abs_delta: `6.96771240234375`
- warm_median_streaming_over_nystrom_descriptive: `4.483539859336586`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
