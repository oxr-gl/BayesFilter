# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-seed82980-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P06-SVD-VALIDATION-SEED82980`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `36.82212201599032` | `20.27937748306431` | `[]` |
| nystrom | `PASS` | `37.29628375195898` | `14.984806822845712` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.57196044921875`
- log_likelihood_mean_abs_delta: `4.57196044921875`
- warm_median_streaming_over_nystrom_descriptive: `1.3533292569475461`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
