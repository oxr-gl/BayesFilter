# P03 Streaming Large-N Reach Ladder Result

Date: 2026-06-21

Status: PASSED_AFTER_CLEAN_RERUN

This result supersedes the earlier same-day `INTERRUPTED_CONTAMINATED` P03
attempt. The first attempt was correctly invalidated because a peer low-rank
GPU run shared physical GPU1. After patching the P03 just-in-time GPU
lease/contamination rule and waiting for GPU1 to become clean, P03 was rerun on
physical GPU1 with `CUDA_VISIBLE_DEVICES=1`.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Advance to P04 same-route TF32-vs-FP32 runtime check. |
| Primary criterion status | Passed: mandatory rungs `1000`, `5000`, and `10000` passed hard finite/device/storage/default-metadata gates on clean physical GPU1. Optional `20000` was attempted and also passed. |
| Veto diagnostic status | No hard P03 veto fired in the clean rerun. |
| Main uncertainty | Runtime remains descriptive single-run evidence; P03 does not establish statistical speedup, posterior correctness, or HMC readiness. |
| Next justified action | Run P04 at matched shape, preferably `10000` particles under the P04 downgrade rule, using the same clean GPU lease discipline. |
| Not concluded | No TF32 speedup, no posterior correctness, no dense equivalence, no HMC readiness, no public API readiness, no statistical ranking. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current default streaming GPU TF32 route run the predeclared large-`N` ladder with finite outputs and no dense storage artifacts on an uncontaminated selected GPU? |
| Baseline/comparator | Primary candidate only: streaming FP32+TF32 default. Dense is not a large-`N` comparator in this phase. |
| Primary criterion | Mandatory rungs `1000`, `5000`, and `10000` pass hard finite/device/storage/default-metadata gates, parent/child GPU metadata is complete, and no unrelated compute process contaminates selected GPU execution. |
| Veto diagnostics | Mandatory-rung OOM/timeout, non-finite output, CPU fallback, missing artifact, dense matrix materialized, full pre-flow storage, `return_history=True`, wrong precision metadata, missing selected-GPU metadata, missing child remapped-device evidence, or unrelated selected-GPU compute-process contamination. |
| Explanatory diagnostics | Warm-call median, compile plus first-call time, memory metadata, stdout/stderr tails, and output previews. |
| Artifact | This result, completed child artifacts, and the patched P03 subplan. |

## Clean Rerun Artifacts

- Parent JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.json`
- Parent Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.md`
- Child artifact directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-children-2026-06-21/`
- Monitor log:
  `docs/benchmarks/logs/large-particle-p03-gpu1-monitor-2026-06-21.log`

## Clean Rerun Summary

| Rung | Required | Hard gate | Child elapsed s | Warm median s | Compile+first s |
| --- | --- | --- | ---: | ---: | ---: |
| `1000` | yes | passed | 18.094 | 0.954 | 13.865 |
| `5000` | yes | passed | 27.060 | 5.237 | 18.464 |
| `10000` | yes | passed | 40.147 | 11.880 | 24.885 |
| `20000` | optional | passed | 74.790 | 29.241 | 42.197 |

All rungs recorded:

- finite output;
- GPU output device after `CUDA_VISIBLE_DEVICES=1` remapped physical GPU1 to
  logical `/GPU:0`;
- streaming transport plan mode;
- no dense transport matrix materialized;
- no full pre-flow particle storage;
- `return_history=False`;
- production-default TF32 metadata with TF32 execution enabled.

Parent summary:

- `mandatory_passed`: `true`
- `overall_passed`: `true`
- `phase_elapsed_seconds`: `160.094`
- optional `20000`: attempted and passed

## Superseded Interrupted Attempt

The first P03 attempt remains recorded as invalid/non-promotional:

The first P03 attempt was launched on physical GPU1 using `CUDA_VISIBLE_DEVICES=1` and child
logical `/GPU:0`. During monitoring, trusted `nvidia-smi` showed a peer low-rank
efficiency job also using physical GPU1:

```text
docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu
```

This made the timing and memory evidence non-interpretable for the P03
large-particle efficiency question. I stopped only the P03 processes launched by
this lane and did not interrupt the peer low-rank lane.

### Diagnostic Artifacts Preserved From Interrupted Attempt

Completed child artifacts are preserved only as contaminated diagnostic smoke
evidence:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-children-2026-06-21/streaming_tf32_n1000.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-children-2026-06-21/streaming_tf32_n5000.json`

The `1000` child artifact shows finite GPU output, streaming plan mode, no dense
transport matrix, no full pre-flow storage, `return_history=False`, and TF32
enabled metadata. These are smoke diagnostics only because the selected GPU was
not clean for the P03 run.

## Planning Repair Preserved

The planning error was treating P02 GPU selection as if it were a durable GPU
lease. The repaired P03 contract now requires:

- trusted `nvidia-smi` immediately before P03 launch;
- no unrelated compute process on the selected physical GPU at launch;
- startup/rung monitoring for unrelated selected-GPU compute;
- stopping only this lane's launched processes if contamination appears;
- preserving partial artifacts as contaminated diagnostic-only evidence.

## Handoff

P04 may start because P03 passed the mandatory clean-rerun rungs. P04 must use
the same just-in-time GPU lease rule and must preserve the single-run
descriptive timing boundary unless a replicated uncertainty plan is added.
