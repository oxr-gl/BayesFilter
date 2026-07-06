# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-route-validation-p03-gpu1-pilot-b1-t3-n128.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-P03-GPU1-PILOT-B1-T3-N128`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 128, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `3` | `3` | `0.011133016087114811` | `0.677178680896759` | `0.0` | `[]` |
| low_rank | `PASS` | `3` | `3` | `0.8416791860945523` | `0.677178680896759` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.0072021484375`
- log_likelihood_mean_abs_delta: `0.0072021484375`
- filtered_mean_relative_l2: `5.854510336321461e-05`
- filtered_mean_rms: `0.01891072400372485`
- filtered_variance_relative_l2: `0.03281402423857326`
- filtered_variance_rms: `0.07344178512742626`
- final_particle_mean_relative_l2: `9.536511051882375e-05`
- final_particle_mean_abs_l2: `0.12282905353751702`
- warm_median_streaming_over_low_rank: `0.013227149097951144`

## Run Manifest

- Git commit: `c4690d153e6a73173e20f33f55c44827ee5f298d`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --batch-seeds 81120 --time-steps 3 --num-particles 128 --transport-policy active-all --sinkhorn-iterations 3 --row-chunk-size 64 --col-chunk-size 64 --particle-chunk-size 64 --low-rank-rank 32 --low-rank-assignment-epsilon 0.25 --low-rank-max-projection-iterations 120 --warmups 0 --repeats 1 --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --tf32-mode enabled --phase-id ACTUAL-SIR-LR-P03-GPU1-PILOT-B1-T3-N128 --output docs/benchmarks/actual-sir-low-rank-route-validation-p03-gpu1-pilot-b1-t3-n128.json --markdown-output docs/benchmarks/actual-sir-low-rank-route-validation-p03-gpu1-pilot-b1-t3-n128.md`
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
