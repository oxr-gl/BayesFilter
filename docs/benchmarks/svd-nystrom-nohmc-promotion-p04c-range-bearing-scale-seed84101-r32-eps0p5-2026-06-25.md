# SVD-Nystrom Range-Bearing Gate

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5-2026-06-25.json`
- Status: `FAIL`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P04C-RANGE-BEARING-SCALE-SEED84101`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 4, 'obs_dim': 2}`
- Fixture: `range_bearing_gaussian_moderate`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['streaming:nonfinite_log_likelihood', 'streaming:nonfinite_filtered_means', 'streaming:nonfinite_filtered_variances', 'streaming:nonfinite_ess_by_time']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | ESS fraction min | Hard vetoes |
| --- | --- | ---: | ---: | ---: | --- |
| streaming | `FAIL` | `11.107151532080024` | `0.4614949272945523` | `nan` | `['nonfinite_log_likelihood', 'nonfinite_filtered_means', 'nonfinite_filtered_variances', 'nonfinite_ess_by_time']` |
| nystrom | `PASS` | `81.78585737664253` | `1.1726400288753211` | `0.24748775362968445` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `nan`
- normalized_max_abs_delta: `nan`
- warm_median_streaming_over_nystrom_descriptive: `0.3935520841269354`

## Nonclaims

- P04 range-bearing nonlinear Gaussian DPF gate only
- no default promotion claim
- no posterior correctness claim
- no statistical superiority claim
- no HMC readiness claim
- no broad nonlinear validity claim
