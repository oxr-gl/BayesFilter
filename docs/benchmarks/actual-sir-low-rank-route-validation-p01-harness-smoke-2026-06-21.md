# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-route-validation-p01-harness-smoke-2026-06-21.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-ROUTE-VALIDATION`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 1, 'time_steps': 1, 'num_particles': 8, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `1` | `1` | `0.17374507384374738` | `0.7240559458732605` | `0.0` | `[]` |
| low_rank | `PASS` | `1` | `1` | `0.12349515105597675` | `0.7240559458732605` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.0`
- log_likelihood_mean_abs_delta: `0.0`
- filtered_mean_relative_l2: `0.0`
- filtered_mean_rms: `0.0`
- filtered_variance_relative_l2: `0.0`
- filtered_variance_rms: `0.0`
- final_particle_mean_relative_l2: `1.5926423869693278e-06`
- final_particle_mean_abs_l2: `0.0022926322632342345`
- warm_median_streaming_over_low_rank: `1.4068979418065881`

## Run Manifest

- Git commit: `c4690d153e6a73173e20f33f55c44827ee5f298d`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --batch-seeds 81120 --time-steps 1 --num-particles 8 --transport-policy active-all --sinkhorn-iterations 2 --row-chunk-size 8 --col-chunk-size 8 --particle-chunk-size 8 --low-rank-rank 4 --low-rank-assignment-epsilon 0.25 --low-rank-max-projection-iterations 80 --warmups 0 --repeats 1 --device-scope cpu --device /CPU:0 --expect-device-kind cpu --tf32-mode disabled --output docs/benchmarks/actual-sir-low-rank-route-validation-p01-harness-smoke-2026-06-21.json --markdown-output docs/benchmarks/actual-sir-low-rank-route-validation-p01-harness-smoke-2026-06-21.md`
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
