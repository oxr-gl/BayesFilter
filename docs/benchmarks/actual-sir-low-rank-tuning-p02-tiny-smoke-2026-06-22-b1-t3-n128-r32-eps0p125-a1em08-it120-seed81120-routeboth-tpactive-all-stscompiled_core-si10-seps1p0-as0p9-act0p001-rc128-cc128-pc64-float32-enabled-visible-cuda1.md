# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22-b1-t3-n128-r32-eps0p125-a1em08-it120-seed81120-routeboth-tpactive-all-stscompiled_core-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-TUNING-r32_eps0p125_alpha1em08_it120`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 128, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `3` | `3` | `0.01009068894200027` | `0.677178680896759` | `0.0` | `[]` |
| low_rank | `PASS` | `3` | `3` | `1.5187453660182655` | `0.677178680896759` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.04239654541015625`
- log_likelihood_mean_abs_delta: `0.04239654541015625`
- filtered_mean_relative_l2: `0.0004274042235803586`
- filtered_mean_rms: `0.13805657778175653`
- filtered_variance_relative_l2: `0.45201384329487887`
- filtered_variance_rms: `1.0103880308138231`
- final_particle_mean_relative_l2: `0.000770086549599649`
- final_particle_mean_abs_l2: `0.9918709463233105`
- warm_median_streaming_over_low_rank: `0.006644095295879186`

## Run Manifest

- Git commit: `5ea363e594516be236ca7c78ab2067b28a5b6eb5`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --batch-seeds 81120 --time-steps 3 --num-particles 128 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --low-rank-rank 32 --low-rank-assignment-epsilon 0.125 --low-rank-alpha 1e-08 --low-rank-max-projection-iterations 120 --low-rank-convergence-threshold 1e-06 --low-rank-denominator-floor 1e-30 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --phase-id ACTUAL-SIR-LR-TUNING-r32_eps0p125_alpha1em08_it120 --output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22-b1-t3-n128-r32-eps0p125-a1em08-it120-seed81120-routeboth-tpactive-all-stscompiled_core-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22-b1-t3-n128-r32-eps0p125-a1em08-it120-seed81120-routeboth-tpactive-all-stscompiled_core-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.md --cuda-visible-devices 1`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- Selected physical GPU: `{'status': 'selected', 'index': '1', 'name': 'NVIDIA GeForce RTX 4080 SUPER', 'uuid': 'GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3', 'memory_used_mib': '30693', 'utilization_gpu_percent': '0'}`

## Nonclaims

- actual-SIR d18 route-validation harness only
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no statistical ranking claim
