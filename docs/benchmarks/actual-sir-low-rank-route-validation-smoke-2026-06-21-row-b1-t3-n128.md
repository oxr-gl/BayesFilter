# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t3-n128.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-P02-SMOKE-B1-T3-N128`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 128, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `3` | `3` | `1.2020628738682717` | `0.6771839261054993` | `0.0` | `[]` |
| low_rank | `PASS` | `3` | `3` | `0.4825797490775585` | `0.6771839261054993` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.00728607177734375`
- log_likelihood_mean_abs_delta: `0.00728607177734375`
- filtered_mean_relative_l2: `5.845478549533545e-05`
- filtered_mean_rms: `0.018881554881414193`
- filtered_variance_relative_l2: `0.03281563916662742`
- filtered_variance_rms: `0.07344523922773324`
- final_particle_mean_relative_l2: `9.537557740864923e-05`
- final_particle_mean_abs_l2: `0.12284254625354407`
- warm_median_streaming_over_low_rank: `2.490910313095381`

## Run Manifest

- Git commit: `c4690d153e6a73173e20f33f55c44827ee5f298d`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --batch-seeds 81120 --time-steps 3 --num-particles 128 --transport-policy active-all --sinkhorn-iterations 3 --row-chunk-size 64 --col-chunk-size 64 --particle-chunk-size 64 --low-rank-rank 32 --low-rank-assignment-epsilon 0.25 --low-rank-max-projection-iterations 120 --warmups 0 --repeats 1 --device-scope cpu --device /CPU:0 --expect-device-kind cpu --tf32-mode disabled --phase-id ACTUAL-SIR-LR-P02-SMOKE-B1-T3-N128 --output docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t3-n128.json --markdown-output docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t3-n128.md`
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
