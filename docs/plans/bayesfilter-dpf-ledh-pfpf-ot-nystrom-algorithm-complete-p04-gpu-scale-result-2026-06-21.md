# P04 Result: Trusted GPU Scale Envelope

Date: 2026-06-22T02:06:37+08:00

Status: `P04_GPU_SCALE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Passed: Nystrom ran on the selected trusted GPU at all required medium/large rows without hard operational failures. |
| Baseline/comparator | Same candidate route across the predeclared GPU ladder; streaming default context remains explanatory only. |
| Primary criterion | Passed: all required rows passed, optional row was attempted and passed, outputs were finite, TF32 was recorded enabled, GPU evidence was present, residual/ESS/log-weight gates passed, and no candidate dense transport matrix was materialized. |
| Veto diagnostics | No hard veto fired. |
| Explanatory diagnostics | Runtime, memory proxy, optional row, and device metadata. |
| Not concluded | No statistical speedup, no default change, no posterior correctness, no HMC readiness, no public API readiness, and no broad large-N guarantee. |

## GPU Preflight

Trusted `nvidia-smi` preflight selected physical GPU1.

| GPU | Memory used MiB | Utilization % | Decision |
| ---: | ---: | ---: | --- |
| 0 | 1245 | 27 | Unsuitable by utilization >= `20%` rule |
| 1 | 18 | 0 | Selected |

The listed display/remote processes were on GPU0. No compute process was listed
for GPU1.

## Commands And Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Trusted GPU preflight | `PASS` | `nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader,nounits` and compute-app query |
| Exact P04 run | `PASS` | `CUDA_VISIBLE_DEVICES=1 timeout 7200 python docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py --mode gpu-scale --device-scope visible --cuda-visible-devices 1 --output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.md > docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.log 2>&1` |
| JSON parse | `PASS` | `python -m json.tool docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json` |

## Diagnostic Summary

| Metric | Value |
| --- | ---: |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Passed rows | `4 / 4` |
| Max row residual | `3.540515899658203e-05` |
| Max column residual | `1.1920928955078125e-07` |
| Max output log-weight residual | `0.0` |
| Min ESS fraction | `0.9999862909317017` |
| Wall time | `12.462970233988017` seconds in the recorded JSON |
| CUDA visible devices | `1` |
| TF32 recorded enabled | `True` |
| Logical GPUs | `['/device:GPU:0']` |

## Rows

| Fixture id | Required | N | Rank | Status | ESS fraction | Row residual | Column residual | Wall time seconds |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `nystrom_gpu_n1024_rank16` | `True` | 1024 | 16 | `PASS` | `0.9999866485595703` | `2.1696090698242188e-05` | `5.960464477539063e-08` | `4.071431024000049` |
| `nystrom_gpu_n4096_rank32` | `True` | 4096 | 32 | `PASS` | `0.9999880790710449` | `2.5153160095214844e-05` | `5.960464477539063e-08` | `1.0177238639444113` |
| `nystrom_gpu_n8192_rank32` | `True` | 8192 | 32 | `PASS` | `0.9999862909317017` | `2.0384788513183594e-05` | `5.960464477539063e-08` | `2.0567268361337483` |
| `nystrom_gpu_n16384_rank64` | `False` | 16384 | 64 | `PASS` | `0.9999880790710449` | `3.540515899658203e-05` | `1.1920928955078125e-07` | `4.213112940080464` |

## Artifacts

- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json`
- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.md`
- `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-result-2026-06-21.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to P05 closeout | `PASS` | No P04 veto fired | Broader leaderboard comparison and statistical ranking remain untested | Write closeout with exact nonclaims and handoff | No speedup, posterior correctness, HMC readiness, default readiness, public API readiness, or ranking |

