# Actual-SIR Nystrom Default-Promotion Pilot

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-P02-GPU0-FALLBACK-B1-T3-N128`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 128, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `3` | `3` | `3.5849189849104732` | `0.677178680896759` | `0.0` | `[]` |
| nystrom | `PASS` | `3` | `3` | `1.0852115859743208` | `0.677178680896759` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `0.00679779052734375`
- log_likelihood_mean_abs_delta: `0.00679779052734375`
- filtered_mean_relative_l2: `3.9791576582646976e-05`
- filtered_mean_rms: `0.012853146001979234`
- filtered_variance_relative_l2: `0.04104982135193494`
- filtered_variance_rms: `0.09175880070111714`
- final_particle_mean_relative_l2: `6.274204511133432e-05`
- final_particle_mean_abs_l2: `0.08081171095793331`
- warm_median_streaming_over_nystrom: `3.3034285951636555`

## Inference Status

| Ledger | Status |
| --- | --- |
| `hard_veto_screen` | `PASS` |
| `statistically_supported_ranking` | `NO` |
| `descriptive_only_differences` | `runtime and memory are descriptive in this pilot` |
| `default_readiness` | `NO` |
| `next_evidence_needed` | `P02 GPU pilot pass, then B=5,T=20,N=1024 actual-SIR row and replicated ladder` |

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Command: `docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120 --time-steps 3 --num-particles 128 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note GPU1 unavailable for pilot: 30799 MiB used and 15 percent utilization; fallback to GPU0 with 1239 MiB used and 34 percent utilization --phase-id ACTUAL-SIR-NYSTROM-P02-GPU0-FALLBACK-B1-T3-N128 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.md`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `0`
- Selected physical GPU: `{'status': 'selected', 'index': '0', 'name': 'NVIDIA GeForce RTX 4080 SUPER', 'uuid': 'GPU-a008e90f-259e-df57-7988-63b6831fff68', 'memory_used_mib': '30692', 'utilization_gpu_percent': '39'}`

## Nonclaims

- actual-SIR d18 Nystrom viability screen only
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no statistical ranking claim
