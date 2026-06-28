# SVD-Nystrom Range-Bearing Gate

- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5-2026-06-25.json`
- Status: `FAIL`
- Phase: `SVD-NYSTROM-NOHMC-PROMOTION-P04A-RANGE-BEARING-RANK128-SEED84000`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 4, 'obs_dim': 2}`
- Fixture: `range_bearing_gaussian_moderate`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `['paired:paired_normalized_log_likelihood_delta']`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | ESS fraction min | Hard vetoes |
| --- | --- | ---: | ---: | ---: | --- |
| streaming | `PASS` | `15.304639866109937` | `0.9632789571769536` | `0.253101110458374` | `[]` |
| nystrom | `PASS` | `132.03929909598082` | `17.028885655105114` | `0.253101110458374` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.886159896850586`
- normalized_max_abs_delta: `0.09715399742126465`
- warm_median_streaming_over_nystrom_descriptive: `0.05656735130452713`

## Nonclaims

- P04 range-bearing nonlinear Gaussian DPF gate only
- no default promotion claim
- no posterior correctness claim
- no statistical superiority claim
- no HMC readiness claim
- no broad nonlinear validity claim
