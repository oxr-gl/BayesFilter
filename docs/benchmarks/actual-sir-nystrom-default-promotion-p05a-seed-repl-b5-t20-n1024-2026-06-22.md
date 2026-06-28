# Actual-SIR Nystrom Default-Promotion Pilot

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-P05A-SEED-REPL-B5-T20-N1024`
- Route request: `both`
- Hard vetoes: `[]`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Actual-SIR semantics pass: `True`

## Routes

| Route | Status | Invocations | Active steps | Warm median seconds | ESS fraction min | Final logsumexp residual | Hard vetoes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| streaming | `PASS` | `20` | `20` | `313.9717076071538` | `0.6537096500396729` | `0.0` | `[]` |
| nystrom | `PASS` | `20` | `20` | `34.23629658506252` | `0.6537096500396729` | `0.0` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.45458984375`
- log_likelihood_mean_abs_delta: `2.49368896484375`
- filtered_mean_relative_l2: `0.00097213458885444`
- filtered_mean_rms: `0.16561167869890225`
- filtered_variance_relative_l2: `0.014587687775281098`
- filtered_variance_rms: `0.018617196951760853`
- final_particle_mean_relative_l2: `0.0030060412977140514`
- final_particle_mean_abs_l2: `0.8133871677233709`
- warm_median_streaming_over_nystrom: `9.170726361336095`

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
- Command: `docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81220,81221,81222,81223,81224 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 1 --gpu-selection-note GPU1 selected for P05A: 18 MiB used and 0 percent utilization; GPU0 had 1236 MiB used and 26 percent utilization --phase-id ACTUAL-SIR-NYSTROM-P05A-SEED-REPL-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.md`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- Selected physical GPU: `{'status': 'selected', 'index': '1', 'name': 'NVIDIA GeForce RTX 4080 SUPER', 'uuid': 'GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3', 'memory_used_mib': '30693', 'utilization_gpu_percent': '0'}`

## Nonclaims

- actual-SIR d18 Nystrom viability screen only
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no statistical ranking claim
