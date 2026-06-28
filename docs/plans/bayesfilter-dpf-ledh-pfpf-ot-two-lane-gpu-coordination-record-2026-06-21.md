# LEDH-PFPF-OT Two-Lane GPU Coordination Record

Date: 2026-06-21

Status: ACTIVE_COORDINATION_NOTE

## Purpose

This file is the common coordination record for the two independent LEDH-PFPF-OT
algorithm lanes. It is not an execution authority and does not merge algorithm
ownership. It exists to prevent timing/memory-sensitive GPU runs from silently
sharing the same physical GPU and producing uninterpretable efficiency evidence.

There are only two active algorithm lanes:

- positive-feature / streaming production-default LEDH-PFPF-OT lane;
- low-rank coupling solver-route lane.

Do not introduce Agent A/B/C/D labels in this coordination record.

## Independence Boundary

- Each lane owns its own algorithm implementation, tests, plans, and result
  artifacts.
- Lanes should not wait for each other for code implementation or non-GPU local
  checks.
- Shared interaction should be limited to:
  - result artifact references;
  - final comparison/closeout notes;
  - GPU lease coordination for timing/memory-sensitive runs.

## GPU Lease Rule

P02-style GPU selection is not a durable lease. Any timing/memory-sensitive GPU
run must perform a just-in-time trusted `nvidia-smi` check immediately before
launch.

For a timing/memory-sensitive run, the selected physical GPU is clean only if:

- it is present;
- it satisfies that lane's memory/utilization threshold rule;
- it has no unrelated compute process on the selected physical GPU.

If unrelated compute appears on the selected GPU during startup/rungs:

- stop only the processes launched by the current lane;
- preserve completed artifacts as contaminated diagnostic-only evidence;
- do not interrupt the peer lane without explicit human approval;
- write or refresh the lane result/stop handoff before retrying.

Display/remoting processes on GPU0 are not algorithm-lane compute, but GPU0
still must satisfy the utilization/memory thresholds before fallback use.

## Current State

### Positive-Feature / Streaming Lane

- Current active phase: P03 streaming large-`N` reach ladder.
- Status: P03 passed after clean GPU1 rerun; ready for P04.
- First P03 attempt was interrupted because GPU1 was shared with the peer
  low-rank lane.
- Clean P03 rerun passed mandatory `1000`, `5000`, and `10000` rungs and
  optional `20000`.
- Contaminated diagnostic-only artifacts:
  - `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-children-2026-06-21/streaming_tf32_n1000.json`
  - `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-children-2026-06-21/streaming_tf32_n5000.json`
- Clean rerun artifacts:
  - `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.json`
  - `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.md`
- Next action: P04 same-route TF32-vs-FP32 runtime check, using a fresh
  just-in-time GPU lease check.

### Low-Rank Coupling Solver-Route Lane

- Current observed run: paired GPU efficiency run on physical GPU1 through
  `CUDA_VISIBLE_DEVICES=1`.
- Observed command family:

```text
docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu
```

- Positive-feature lane must not stop or manage this run without explicit human
  approval.

## Note For The Peer Lane

No code merge or synchronization is requested from the peer low-rank lane for
this blocker. The peer lane may continue its current GPU run. When it finishes,
please update or append to this coordination record with:

- end time;
- whether GPU1 is released;
- final low-rank result artifact paths;
- any remaining long GPU runs expected from that lane.

After GPU1 is released, the positive-feature / streaming lane will rerun its
P03 ladder from a clean just-in-time GPU preflight.
