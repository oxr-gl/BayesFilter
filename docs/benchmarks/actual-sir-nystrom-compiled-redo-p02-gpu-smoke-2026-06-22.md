# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p02-gpu-smoke-2026-06-22.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P02-GPU-SMOKE`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 128, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `15.939500648993999` | `0.011182473972439766` | `[]` |
| nystrom | `PASS` | `103.2542302198708` | `0.013364152982831001` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.32093048095703125`
- log_likelihood_mean_abs_delta: `0.32093048095703125`
- warm_median_streaming_over_nystrom_descriptive: `0.8367514190241574`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
