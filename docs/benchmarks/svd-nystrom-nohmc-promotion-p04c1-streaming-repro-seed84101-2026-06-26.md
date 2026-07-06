# SVD-Nystrom Range-Bearing Gate

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101-2026-06-26.json`
- Status: `FAIL`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P04C1-STREAMING-REPRO-SEED84101`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 4, 'obs_dim': 2}`
- Fixture: `range_bearing_gaussian_moderate`
- Route request: `streaming`
- JIT compile: `True`
- Hard vetoes: `['streaming:nonfinite_log_likelihood', 'streaming:nonfinite_filtered_means', 'streaming:nonfinite_filtered_variances', 'streaming:nonfinite_ess_by_time']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | ESS fraction min | Hard vetoes |
| --- | --- | ---: | ---: | ---: | --- |
| streaming | `FAIL` | `10.97846591938287` | `0.45790097396820784` | `nan` | `['nonfinite_log_likelihood', 'nonfinite_filtered_means', 'nonfinite_filtered_variances', 'nonfinite_ess_by_time']` |

## Paired Comparability

- Not applicable.

## Nonclaims

- P04 range-bearing nonlinear Gaussian DPF gate only
- no default promotion claim
- no posterior correctness claim
- no statistical superiority claim
- no HMC readiness claim
- no broad nonlinear validity claim
