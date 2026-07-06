# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-N4096-DIAGNOSTIC`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.963599339826033` | `1.5411376350093633` | `[]` |
| nystrom | `PASS` | `10.773117518983781` | `0.14315718389116228` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.57757568359375`
- log_likelihood_mean_abs_delta: `0.57757568359375`
- warm_median_streaming_over_nystrom_descriptive: `10.765353111311828`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
