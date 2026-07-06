# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-seed82949-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-EXT-SEED82949`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.003794853109866` | `1.177939317189157` | `[]` |
| nystrom | `PASS` | `12.545018909033388` | `0.19046864099800587` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.05291748046875`
- log_likelihood_mean_abs_delta: `2.05291748046875`
- warm_median_streaming_over_nystrom_descriptive: `6.184426533507369`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
