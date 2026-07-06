# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22-b1-t20-n256-r128-eps0p03125-a1em08-it120-seed81120-routeboth-tpactive-all-stscompiled_core-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json`
- Status: `FAIL`
- Phase: `ACTUAL-SIR-LR-TUNING-r128_eps0p03125_alpha1em08_it120`
- Route request: `both`
- Hard vetoes: `['low_rank:ess_fraction_min_threshold']`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 256, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `20` | `20` | `0.13931178417988122` | `0.6792407631874084` | `0.0` | `[]` |
| low_rank | `FAIL` | `20` | `20` | `18.788773754029535` | `0.007390182930976152` | `0.0` | `['ess_fraction_min_threshold']` |

## Paired Comparability

- log_likelihood_max_abs_delta: `45.3990478515625`
- log_likelihood_mean_abs_delta: `45.3990478515625`
- filtered_mean_relative_l2: `0.03496070863660663`
- filtered_mean_rms: `5.954654059958709`
- filtered_variance_relative_l2: `3.5115865984502337`
- filtered_variance_rms: `4.416826601572537`
- final_particle_mean_relative_l2: `0.06513896178131544`
- final_particle_mean_abs_l2: `7.888355478242987`
- warm_median_streaming_over_low_rank: `0.007414628863153121`

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --batch-seeds 81120 --time-steps 20 --num-particles 256 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --low-rank-rank 128 --low-rank-assignment-epsilon 0.03125 --low-rank-alpha 1e-08 --low-rank-max-projection-iterations 120 --low-rank-convergence-threshold 1e-06 --low-rank-denominator-floor 1e-30 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --phase-id ACTUAL-SIR-LR-TUNING-r128_eps0p03125_alpha1em08_it120 --output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22-b1-t20-n256-r128-eps0p03125-a1em08-it120-seed81120-routeboth-tpactive-all-stscompiled_core-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22-b1-t20-n256-r128-eps0p03125-a1em08-it120-seed81120-routeboth-tpactive-all-stscompiled_core-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.md --cuda-visible-devices 1`
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
