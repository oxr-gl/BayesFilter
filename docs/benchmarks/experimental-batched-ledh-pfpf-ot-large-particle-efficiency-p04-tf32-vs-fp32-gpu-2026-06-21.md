# Large-Particle LEDH-PFPF-OT Efficiency Parent Result

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json`
- Run kind: `tf32-vs-fp32`
- Overall passed: `True`
- Device request: `/GPU:0`
- CUDA visible devices: `1`
- Selected physical GPU: `1`
- GPU selection reason: `jit_clean_gpu1_p04_preflight`

## Children

| arm | passed | elapsed s | hard/context gate | artifact |
| --- | --- | ---: | --- | --- |
| fp32_tf32_enabled | True | 40.3499 | True | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-children-2026-06-21/fp32_tf32_enabled.json` |
| fp32_tf32_disabled | True | 39.0618 | True | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-children-2026-06-21/fp32_tf32_disabled.json` |

## Comparison

- enabled_warm_median_seconds: `11.870695133926347`
- disabled_warm_median_seconds: `12.24538614996709`
- enabled_to_disabled_warm_median_ratio: `0.9694014536208195`
- timing_interpretation: `descriptive_only`
- matched_config_except_tf32: `True`

## Nonclaims

- parent orchestration/reporting wrapper only
- single synthetic LGSSM-shaped benchmark fixture
- runtime and memory are descriptive unless a separate uncertainty plan is used
- no posterior correctness claim
- no HMC readiness claim
- no dense Sinkhorn equivalence claim
- no public API readiness claim
