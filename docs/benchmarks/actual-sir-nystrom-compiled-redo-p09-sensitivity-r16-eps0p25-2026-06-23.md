# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-r16-eps0p25-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09-SENSITIVITY-R16-EPS0P25`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.539013592060655` | `0.10292791482061148` | `[]` |
| nystrom | `PASS` | `14.112616288941354` | `0.0671288080047816` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `1.90203857421875`
- log_likelihood_mean_abs_delta: `0.67137451171875`
- warm_median_streaming_over_nystrom_descriptive: `1.5332897734945612`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
