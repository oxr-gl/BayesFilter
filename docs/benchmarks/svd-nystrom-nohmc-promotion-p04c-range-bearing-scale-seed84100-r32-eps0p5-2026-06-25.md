# SVD-Nystrom Range-Bearing Gate

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5-2026-06-25.json`
- Status: `PASS`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P04C-RANGE-BEARING-SCALE-SEED84100`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 4, 'obs_dim': 2}`
- Fixture: `range_bearing_gaussian_moderate`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | ESS fraction min | Hard vetoes |
| --- | --- | ---: | ---: | ---: | --- |
| streaming | `PASS` | `12.187477448023856` | `0.8170916410163045` | `0.24928796291351318` | `[]` |
| nystrom | `PASS` | `83.88165987376124` | `0.9877944411709905` | `0.24928796291351318` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.481616973876953`
- normalized_max_abs_delta: `0.11204042434692382`
- warm_median_streaming_over_nystrom_descriptive: `0.8271879319827669`

## Nonclaims

- P04 range-bearing nonlinear Gaussian DPF gate only
- no default promotion claim
- no posterior correctness claim
- no statistical superiority claim
- no HMC readiness claim
- no broad nonlinear validity claim
