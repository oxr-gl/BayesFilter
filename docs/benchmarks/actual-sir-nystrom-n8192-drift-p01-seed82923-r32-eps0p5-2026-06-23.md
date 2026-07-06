# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-N8192-DRIFT-P01-SEED82923`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.080519531853497` | `1.1736021279357374` | `[]` |
| nystrom | `PASS` | `12.474037502193823` | `0.184649215079844` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.7215576171875`
- log_likelihood_mean_abs_delta: `3.7215576171875`
- warm_median_streaming_over_nystrom_descriptive: `6.355846827879886`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
