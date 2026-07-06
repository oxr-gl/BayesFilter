# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-g3-history-full-n2048-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-G3-HISTORY-FULL-N2048`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 2048, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.528404660057276` | `0.1523261801339686` | `[]` |
| nystrom | `PASS` | `14.39125936687924` | `0.09232353186234832` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.61895751953125`
- log_likelihood_mean_abs_delta: `2.61895751953125`
- warm_median_streaming_over_nystrom_descriptive: `1.6499171669589339`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
