# SVD-Nystrom Range-Bearing Gate

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0-2026-06-25.json`
- Status: `FAIL`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P04A-RANGE-BEARING-EPS1P0-SEED84000`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 4, 'obs_dim': 2}`
- Fixture: `range_bearing_gaussian_moderate`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_normalized_log_likelihood_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | ESS fraction min | Hard vetoes |
| --- | --- | ---: | ---: | ---: | --- |
| streaming | `PASS` | `15.158778781071305` | `1.0521207638084888` | `0.253101110458374` | `[]` |
| nystrom | `PASS` | `99.34500407008454` | `1.0669907620176673` | `0.253101110458374` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.9405384063720703`
- normalized_max_abs_delta: `0.09851346015930176`
- warm_median_streaming_over_nystrom_descriptive: `0.9860636111028183`

## Nonclaims

- P04 range-bearing nonlinear Gaussian DPF gate only
- no default promotion claim
- no posterior correctness claim
- no statistical superiority claim
- no HMC readiness claim
- no broad nonlinear validity claim
