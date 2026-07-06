# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81139_81140-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json`
- Status: `PASS`
- Phase: `ASLR-N3072-SR-r16_eps0p125_alpha1em08_it120`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 2, 'time_steps': 20, 'num_particles': 3072, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `20` | `20` | `7.614717622054741` | `0.6346776882807413` | `9.5367431640625e-07` | `[]` |
| low_rank | `PASS` | `20` | `20` | `0.7545652920380235` | `0.6346776882807413` | `9.5367431640625e-07` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.97552490234375`
- log_likelihood_mean_abs_delta: `1.7257080078125`
- filtered_mean_relative_l2: `0.0008683099090988481`
- filtered_mean_rms: `0.14790900745758545`
- filtered_variance_relative_l2: `0.08734641149471267`
- filtered_variance_rms: `0.11206082347648405`
- final_particle_mean_relative_l2: `0.0005612295217771006`
- final_particle_mean_abs_l2: `0.09597746114324289`
- warm_median_streaming_over_low_rank: `10.091529125979234`

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --low-rank-timing-source compiled_core --batch-seeds 81139,81140 --time-steps 20 --num-particles 3072 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --low-rank-rank 16 --low-rank-assignment-epsilon 0.125 --low-rank-alpha 1e-08 --low-rank-max-projection-iterations 120 --low-rank-convergence-threshold 1e-06 --low-rank-denominator-floor 1e-30 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --phase-id ASLR-N3072-SR-r16_eps0p125_alpha1em08_it120 --output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81139_81140-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json --markdown-output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81139_81140-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.md --jit-compile --cuda-visible-devices 1`
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
