# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82930-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-G1-N8192-SEED82930`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.43216896103695` | `1.1978396079503` | `[]` |
| nystrom | `PASS` | `12.908208657987416` | `0.18669576477259398` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.59747314453125`
- log_likelihood_mean_abs_delta: `4.59747314453125`
- warm_median_streaming_over_nystrom_descriptive: `6.4159977566140105`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
