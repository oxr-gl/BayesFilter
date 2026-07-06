# SVD-Nystrom Range-Bearing Gate

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5-2026-06-25.json`
- Status: `FAIL`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P04-RANGE-BEARING-SEED84000`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 4, 'obs_dim': 2}`
- Fixture: `range_bearing_gaussian_moderate`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_normalized_log_likelihood_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | ESS fraction min | Hard vetoes |
| --- | --- | ---: | ---: | ---: | --- |
| streaming | `PASS` | `11.435113555984572` | `0.8551208861172199` | `0.253101110458374` | `[]` |
| nystrom | `PASS` | `80.80719372001477` | `1.1360743502154946` | `0.253101110458374` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.790477752685547`
- normalized_max_abs_delta: `0.09476194381713868`
- warm_median_streaming_over_nystrom_descriptive: `0.7526979954745194`

## Nonclaims

- P04 range-bearing nonlinear Gaussian DPF gate only
- no default promotion claim
- no posterior correctness claim
- no statistical superiority claim
- no HMC readiness claim
- no broad nonlinear validity claim
