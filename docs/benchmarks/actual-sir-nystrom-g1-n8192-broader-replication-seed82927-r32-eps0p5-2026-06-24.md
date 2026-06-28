# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82927-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-G1-N8192-SEED82927`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.679414363810793` | `1.2848881359677762` | `[]` |
| nystrom | `PASS` | `13.052641784073785` | `0.21481013903394341` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.70166015625`
- log_likelihood_mean_abs_delta: `2.70166015625`
- warm_median_streaming_over_nystrom_descriptive: `5.981506002213161`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
