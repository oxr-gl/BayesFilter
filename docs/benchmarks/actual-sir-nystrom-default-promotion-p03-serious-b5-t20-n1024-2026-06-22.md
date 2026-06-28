# Actual-SIR Nystrom Default-Promotion Pilot

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-P03-SERIOUS-B5-T20-N1024`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `20` | `20` | `489.2099703249987` | `0.6536898016929626` | `0.0` | `[]` |
| nystrom | `PASS` | `20` | `20` | `104.42240847204812` | `0.6536898016929626` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.87078857421875`
- log_likelihood_mean_abs_delta: `2.5714111328125`
- filtered_mean_relative_l2: `0.0014205765845258954`
- filtered_mean_rms: `0.2420245515078464`
- filtered_variance_relative_l2: `0.015914764790818416`
- filtered_variance_rms: `0.020333283615234184`
- final_particle_mean_relative_l2: `0.004265115345192201`
- final_particle_mean_abs_l2: `1.1539638091744444`
- warm_median_streaming_over_nystrom: `4.68491368359839`

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
- Command: `docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note GPU1 unavailable for P03: 30799 MiB used and 3 percent utilization; fallback to GPU0 with 1266 MiB used and 31 percent utilization --phase-id ACTUAL-SIR-NYSTROM-P03-SERIOUS-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.md`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `0`
- Selected physical GPU: `{'status': 'selected', 'index': '0', 'name': 'NVIDIA GeForce RTX 4080 SUPER', 'uuid': 'GPU-a008e90f-259e-df57-7988-63b6831fff68', 'memory_used_mib': '30691', 'utilization_gpu_percent': '31'}`

## Nonclaims

- actual-SIR d18 Nystrom viability screen only
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no statistical ranking claim
