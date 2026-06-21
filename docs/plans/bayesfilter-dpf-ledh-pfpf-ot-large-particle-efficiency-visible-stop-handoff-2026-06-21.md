# LEDH-PFPF-OT Large-Particle Efficiency Visible Stop Handoff

Date: 2026-06-21

Status: P03_PASSED_READY_FOR_P04

## Current State

The large-particle efficiency lane has been initialized. P00 and P01 passed.
P02 was repaired and passed, selecting physical GPU1 for P03. The first P03
attempt was invalidated because a peer low-rank efficiency run also occupied
physical GPU1. After the peer run finished, a clean rerun of P03 passed the
mandatory `1000`, `5000`, and `10000` rungs and also passed optional `20000`.

## Active Question

Can current GPU TF32 streaming LEDH-PFPF-OT make the LGSSM-shaped
LEDH-PFPF-OT benchmark operational at large particle counts by avoiding dense
transport storage, and does TF32 show descriptive same-route runtime benefit?

## Last Completed Phase

P01 harness implementation and static checks passed.

## Next Action

Proceed to P04 same-route TF32-vs-FP32 runtime check, using the same
just-in-time GPU lease rule:

- physical GPU selected for P03: GPU1;
- child command must use `CUDA_VISIBLE_DEVICES=1`;
- child logical device should be `/GPU:0` after CUDA remapping.
- trusted `nvidia-smi` must show no unrelated compute process on the selected
  physical GPU immediately before launch and during startup/rungs.

## Boundaries

- GPU1 is preferred unless busy or unsuitable; GPU0 may be used only with a
  recorded reason.
- P02 selection is not a durable GPU lease. Timing/memory-sensitive phases need
  a just-in-time uncontaminated selected-GPU check.
- Dense/non-streaming remains small-`N` context only.
- Runtime is descriptive unless a later replicated uncertainty plan is written.
- No posterior correctness, HMC readiness, or public API readiness claim is
  allowed from this lane.

## Clean P03 Evidence

P03 clean rerun artifacts:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-clean-rerun-2026-06-21.md`

Summary:

- mandatory rungs `1000`, `5000`, `10000`: passed;
- optional rung `20000`: attempted and passed;
- hard gates: finite GPU output, streaming plan mode, no dense matrix, no full
  pre-flow storage, no history, TF32 enabled metadata;
- runtime/memory: descriptive only.

## Superseded Blocker Evidence

Trusted GPU preflight after the interrupted run showed GPU1 still occupied by
the peer low-rank efficiency lane:

```text
docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu
```

GPU0 was above the utilization threshold, so immediate fallback is also blocked.

## Superseded Blocker Evidence

Trusted `nvidia-smi` previously reported GPU0 at high utilization and GPU1 with
a small unrelated Python allocation. The GPU1 allocation was below the repaired
busy threshold, so it should have been a warning rather than a stop condition.

The superseded process command was:

```text
/home/ubuntu/anaconda3/envs/tfgpu/bin/python /home/ubuntu/python/dsge_hmc/scripts/train_nk_svd_ukf_neutra_phase2_canary.py ...
```
