# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-P03-GPU1-PAIRED-B5-T20-N1024`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `20` | `20` | `0.9723010780289769` | `0.6536898016929626` | `0.0` | `[]` |
| low_rank | `PASS` | `20` | `20` | `58.549089503940195` | `0.06144050508737564` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `58.0933837890625`
- log_likelihood_mean_abs_delta: `42.93328857421875`
- filtered_mean_relative_l2: `0.024529629672863727`
- filtered_mean_rms: `4.1791288726681`
- filtered_variance_relative_l2: `3.460364375696834`
- filtered_variance_rms: `4.421087662174504`
- final_particle_mean_relative_l2: `0.01441203872214028`
- final_particle_mean_abs_l2: `3.8993016028318315`
- warm_median_streaming_over_low_rank: `0.016606596042173186`

## Run Manifest

- Git commit: `c4690d153e6a73173e20f33f55c44827ee5f298d`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 1024 --transport-policy active-all --warmups 1 --repeats 3 --dtype float32 --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --tf32-mode enabled --phase-id ACTUAL-SIR-LR-P03-GPU1-PAIRED-B5-T20-N1024 --output docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json --markdown-output docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.md`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- Selected physical GPU: `{'status': 'selected', 'index': '1', 'name': 'NVIDIA GeForce RTX 4080 SUPER', 'uuid': 'GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3', 'memory_used_mib': '30693', 'utilization_gpu_percent': '2'}`

## Nonclaims

- actual-SIR d18 route-validation harness only
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no statistical ranking claim
