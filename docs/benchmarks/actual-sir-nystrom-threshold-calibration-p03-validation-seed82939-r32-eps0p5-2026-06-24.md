# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-seed82939-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-SEED82939`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.655450398102403` | `1.1733430249150842` | `[]` |
| nystrom | `PASS` | `12.349439225858077` | `0.1856293580494821` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.9122314453125`
- log_likelihood_mean_abs_delta: `4.9122314453125`
- warm_median_streaming_over_nystrom_descriptive: `6.320891464820523`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
