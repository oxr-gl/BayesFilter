# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p5-control-t4-2026-06-23.json`
- Status: `PASS`
- Phase: `p03-r32-eps0p5-control-t4`
- Shape: `{'batch_size': 5, 'time_steps': 4, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `23.22442622995004` | `0.1254993579350412` | `[]` |
| nystrom | `PASS` | `17.368332392070442` | `0.05943766608834267` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `1.023773193359375`
- log_likelihood_mean_abs_delta: `0.315264892578125`
- warm_median_streaming_over_nystrom_descriptive: `2.1114449169069074`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
