# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t2-2026-06-23.json`
- Status: `PASS`
- Phase: `p03-r32-eps0p25-t2`
- Shape: `{'batch_size': 5, 'time_steps': 2, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `23.540808568010107` | `0.02959367400035262` | `[]` |
| nystrom | `PASS` | `17.671953696059063` | `0.028072522021830082` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.0223846435546875`
- log_likelihood_mean_abs_delta: `0.01360626220703125`
- warm_median_streaming_over_nystrom_descriptive: `1.0541865094037381`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
