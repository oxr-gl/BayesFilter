# Actual-SIR Low-Rank Route Validation

- JSON artifact: `docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-LR-ROUTE-VALIDATION`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 128, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `3` | `3` | `0.011875582160428166` | `0.6112725138664246` | `0.0` | `[]` |
| low_rank | `PASS` | `3` | `3` | `0.007439447101205587` | `0.6112725138664246` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.025787353515625`
- log_likelihood_mean_abs_delta: `0.025787353515625`
- filtered_mean_relative_l2: `0.00010064070458943695`
- filtered_mean_rms: `0.03251108907392829`
- filtered_variance_relative_l2: `0.03377490395200103`
- filtered_variance_rms: `0.07557301434953136`
- final_particle_mean_relative_l2: `0.00017094537951849086`
- final_particle_mean_abs_l2: `0.22024112502166995`
- warm_median_streaming_over_low_rank: `1.5962990258380476`

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Command: `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --batch-seeds 81120 --time-steps 3 --num-particles 128 --low-rank-rank 32 --low-rank-assignment-epsilon 0.25 --low-rank-max-projection-iterations 120 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-compiled-rerun-p01-smoke-2026-06-23.md`
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
