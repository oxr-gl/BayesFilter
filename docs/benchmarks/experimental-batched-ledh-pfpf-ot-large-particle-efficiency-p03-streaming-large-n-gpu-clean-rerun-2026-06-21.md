# Large-Particle LEDH-PFPF-OT Efficiency Parent Result

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.json`
- Run kind: `streaming-ladder`
- Overall passed: `True`
- Device request: `/GPU:0`
- CUDA visible devices: `1`
- Selected physical GPU: `1`
- GPU selection reason: `jit_clean_gpu1_monitor_monitor_large_particle_p03_gpu1.sh`

## Children

| arm | passed | elapsed s | hard/context gate | artifact |
| --- | --- | ---: | --- | --- |
| streaming_tf32_n1000 | True | 18.0944 | True | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-children-2026-06-21/streaming_tf32_n1000.json` |
| streaming_tf32_n5000 | True | 27.0597 | True | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-children-2026-06-21/streaming_tf32_n5000.json` |
| streaming_tf32_n10000 | True | 40.1469 | True | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-children-2026-06-21/streaming_tf32_n10000.json` |
| streaming_tf32_n20000 | True | 74.79 | True | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-children-2026-06-21/streaming_tf32_n20000.json` |

## Optional Decisions

- `{'particle_count': 20000, 'decision': 'attempted', 'passed': True}`

## Nonclaims

- parent orchestration/reporting wrapper only
- single synthetic LGSSM-shaped benchmark fixture
- runtime and memory are descriptive unless a separate uncertainty plan is used
- no posterior correctness claim
- no HMC readiness claim
- no dense Sinkhorn equivalence claim
- no public API readiness claim
