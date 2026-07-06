# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23-b2-t20-n2048-r16-eps0p25-a1em08-it120-seed81133_81134-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-en-h8c7ae49655e617e7.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-TUNING-r16_eps0p25_alpha1em08_it120`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 2, 'time_steps': 20, 'num_particles': 2048, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `20` | `20` | `3.650278764893301` | `0.6400983333587646` | `0.0` | `[]` |
| low_rank | `PASS` | `20` | `20` | `0.5094342195661739` | `0.6400983333587646` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.15838623046875`
- log_likelihood_mean_abs_delta: `0.09588623046875`
- filtered_mean_relative_l2: `0.00016389443843131294`
- filtered_mean_rms: `0.02792184715878946`
- filtered_variance_relative_l2: `0.009848763750494514`
- filtered_variance_rms: `0.01260599854257433`
- final_particle_mean_relative_l2: `0.00033614127126040377`
- final_particle_mean_abs_l2: `0.057494421465554155`
- warm_median_streaming_over_low_rank: `7.165358400937064`

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --low-rank-timing-source compiled_core --batch-seeds 81133,81134 --time-steps 20 --num-particles 2048 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --low-rank-rank 16 --low-rank-assignment-epsilon 0.25 --low-rank-alpha 1e-08 --low-rank-max-projection-iterations 120 --low-rank-convergence-threshold 1e-06 --low-rank-denominator-floor 1e-30 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --device /GPU:0 --expect-device-kind gpu --phase-id ACTUAL-SIR-LR-TUNING-r16_eps0p25_alpha1em08_it120 --output docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23-b2-t20-n2048-r16-eps0p25-a1em08-it120-seed81133_81134-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-en-h8c7ae49655e617e7.json --markdown-output docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23-b2-t20-n2048-r16-eps0p25-a1em08-it120-seed81133_81134-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-en-h8c7ae49655e617e7.md --jit-compile --cuda-visible-devices 1`
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
