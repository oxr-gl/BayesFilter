# Phase 3 Result - Two-GPU Row Splitting - 2026-06-16

## Status

`PHASE_3_PASSED`

## Objective

Verify that independent DPF value-evaluation rows can be split across GPU 0
and GPU 1 using the current streaming TF32 value worker.

This phase did not shard one filter's particles across GPUs and did not design
distributed OT.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can independent DPF value-evaluation rows be split across two GPUs using the current streaming TF32 value worker? |
| Baseline/comparator | Used the Phase 2 single-GPU TF32 value worker independently on each GPU. |
| Primary pass criterion | Passed. Two per-GPU artifacts exist, are finite, JIT-compiled, GPU-placed, and the row assignment is disjoint. |
| Veto diagnostics | No active veto. Two trusted GPUs were visible, per-GPU artifacts were finite/JIT/GPU/TF32, and no particle-cloud sharding or HMC claim was made. |
| Explanatory diagnostics | Per-GPU compile and warm-call timings are descriptive only. |
| Not concluded | No single-filter distributed OT, no speed superiority, no HMC readiness, no production default, no public API readiness. |

## Trusted GPU Visibility

Trusted `nvidia-smi` query showed:

- GPU 0: NVIDIA GeForce RTX 4080 SUPER, 32760 MiB
- GPU 1: NVIDIA GeForce RTX 4080 SUPER, 32760 MiB

## Per-GPU Artifacts

GPU 0 worker:

- Artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p3-two-gpu-row-split-gpu0-rows0-1-b2-t20-np256-d10-m10-2026-06-16.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p3-two-gpu-row-split-gpu0-rows0-1-b2-t20-np256-d10-m10-2026-06-16.md`
- Assigned logical rows: `[0, 1]`
- `CUDA_VISIBLE_DEVICES`: `0`
- TensorFlow requested device: `/GPU:0`
- finite output: `true`
- JIT compiled: `true`
- TF32 execution enabled: `true`
- output shape: `[2]`
- return history: `false`
- proposal mode: `callback`
- dense transport matrix materialized: `false`

GPU 1 worker:

- Artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p3-two-gpu-row-split-gpu1-rows2-3-b2-t20-np256-d10-m10-2026-06-16.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p3-two-gpu-row-split-gpu1-rows2-3-b2-t20-np256-d10-m10-2026-06-16.md`
- Assigned logical rows: `[2, 3]`
- `CUDA_VISIBLE_DEVICES`: `1`
- TensorFlow requested device: `/GPU:0`
- finite output: `true`
- JIT compiled: `true`
- TF32 execution enabled: `true`
- output shape: `[2]`
- return history: `false`
- proposal mode: `callback`
- dense transport matrix materialized: `false`

Note: with `CUDA_VISIBLE_DEVICES=1`, TensorFlow remaps physical GPU 1 to
logical `/GPU:0` inside the worker process. The physical assignment is therefore
recorded by `CUDA_VISIBLE_DEVICES`, while output device metadata records the
process-local TensorFlow device.

## Row Assignment

| Worker | Physical GPU selector | Assigned independent rows | Seed | Artifact |
| --- | --- | --- | ---: | --- |
| GPU 0 worker | `CUDA_VISIBLE_DEVICES=0` | `[0, 1]` | `202606160` | `experimental-batched-ledh-pfpf-ot-p3-two-gpu-row-split-gpu0-rows0-1-b2-t20-np256-d10-m10-2026-06-16.json` |
| GPU 1 worker | `CUDA_VISIBLE_DEVICES=1` | `[2, 3]` | `202606161` | `experimental-batched-ledh-pfpf-ot-p3-two-gpu-row-split-gpu1-rows2-3-b2-t20-np256-d10-m10-2026-06-16.json` |

The assigned row sets are disjoint. They represent independent filters or
independent parameter/seed rows only.

## Nonclaims

- This is not single-filter multi-GPU particle sharding.
- This is not distributed OT.
- This is not speed superiority evidence.
- This is not HMC readiness.
- This is not production or public API readiness.

## Phase 4 Handoff

Phase 4 may begin only from the dedicated score-path subplan:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-jit-safe-score-path-subplan-2026-06-16.md`

Phase 4 must focus on score-gradient JIT safety and must not use Phase 2/3
value-only evidence as HMC readiness evidence.
