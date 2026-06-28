# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t20-n256.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-P02-SMOKE-B1-T20-N256`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 256, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `20` | `20` | `8.286113006994128` | `0.6792467832565308` | `0.0` | `[]` |
| low_rank | `PASS` | `20` | `20` | `4.46750571206212` | `0.23121842741966248` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.3004150390625`
- log_likelihood_mean_abs_delta: `2.3004150390625`
- filtered_mean_relative_l2: `0.003008538449022366`
- filtered_mean_rms: `0.512424541405573`
- filtered_variance_relative_l2: `0.8380132643930995`
- filtered_variance_rms: `1.0544851615597268`
- final_particle_mean_relative_l2: `0.002545863819893611`
- final_particle_mean_abs_l2: `0.308313355943584`
- warm_median_streaming_over_low_rank: `1.8547515193146573`

## Run Manifest

- Git commit: `c4690d153e6a73173e20f33f55c44827ee5f298d`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --batch-seeds 81120 --time-steps 20 --num-particles 256 --transport-policy active-all --sinkhorn-iterations 3 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 128 --low-rank-rank 64 --low-rank-assignment-epsilon 0.125 --low-rank-max-projection-iterations 160 --warmups 0 --repeats 1 --device-scope cpu --device /CPU:0 --expect-device-kind cpu --tf32-mode disabled --phase-id ACTUAL-SIR-LR-P02-SMOKE-B1-T20-N256 --output docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t20-n256.json --markdown-output docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t20-n256.md`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
- Selected physical GPU: `{'status': 'cpu_hidden', 'index': None, 'name': None, 'uuid': None}`

## Nonclaims

- actual-SIR d18 route-validation harness only
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no statistical ranking claim
