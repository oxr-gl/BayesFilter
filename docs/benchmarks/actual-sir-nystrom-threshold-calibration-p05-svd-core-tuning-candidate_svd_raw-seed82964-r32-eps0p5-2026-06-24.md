# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-candidate_svd_raw-seed82964-r32-eps0p5-2026-06-24.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-THRESHOLD-CALIBRATION-P05-CANDIDATE_SVD_RAW-SEED82964`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 8192, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.82632117299363` | `1.1760915890336037` | `[]` |
| nystrom | `PASS` | `15.5635109920986` | `1.871093993075192` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `1.65118408203125`
- log_likelihood_mean_abs_delta: `1.65118408203125`
- warm_median_streaming_over_nystrom_descriptive: `0.6285582623781857`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
