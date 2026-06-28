# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-seed82944-r32-eps0p5-2026-06-24.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P03-SEED82944`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_log_likelihood_mean_abs_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.72250338899903` | `1.252096096985042` | `[]` |
| nystrom | `PASS` | `12.588508524931967` | `0.20316766714677215` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `5.7003173828125`
- log_likelihood_mean_abs_delta: `5.7003173828125`
- warm_median_streaming_over_nystrom_descriptive: `6.1628708670484675`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
