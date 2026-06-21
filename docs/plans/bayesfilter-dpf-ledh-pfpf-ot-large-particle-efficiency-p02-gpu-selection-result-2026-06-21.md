# P02 Trusted GPU Selection Preflight Result

Date: 2026-06-21

Status: PASSED_AFTER_REPAIR

This record supersedes the earlier same-day `BLOCKED` P02 decision. The earlier
decision treated any unrelated active compute process as a GPU-busy veto. That
was a planning error: the repaired rule classifies a GPU as busy/unsuitable only
when it is absent, total memory used is at least 2048 MiB, utilization is at
least 20%, or any single non-display compute process uses at least 2048 MiB.
Light shared compute below threshold is recorded as a warning, not a launch
veto.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Select physical GPU1 for P03. |
| Primary criterion status | Passed: trusted GPU evidence was obtained and GPU1 is usable by the repaired threshold rule. |
| Veto diagnostic status | No GPU-selection continuation veto fired. GPU1 is present, uses 18 MiB of 32760 MiB, has 0% utilization, and has no listed compute apps. |
| Main uncertainty | Later benchmark runtime/memory behavior is still unknown until P03 runs. |
| Next justified action | Launch P03 on physical GPU1 with `CUDA_VISIBLE_DEVICES=1` and child logical device `/GPU:0`. |
| Not concluded | No large-`N` GPU pass, no TF32 runtime benefit, no algorithmic scalability verdict. |

## Trusted GPU Evidence

Command:

```bash
nvidia-smi --query-gpu=index,uuid,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits
```

Output:

```text
0, GPU-a008e90f-259e-df57-7988-63b6831fff68, NVIDIA GeForce RTX 4080 SUPER, 1226, 32760, 28
1, GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3, NVIDIA GeForce RTX 4080 SUPER, 18, 32760, 0
```

Command:

```bash
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader,nounits
```

Output included:

```text
GPU-a008e90f-259e-df57-7988-63b6831fff68, 5627, /usr/libexec/gnome-remote-desktop-daemon, 251
GPU-a008e90f-259e-df57-7988-63b6831fff68, 6374, /usr/NX/bin/nxnode.bin, 312
```

## GPU Selection Rule Application

- GPU1 is preferred by user policy.
- GPU1 is present, has 18 MiB total memory used, has 0% utilization, and has no
  listed compute apps.
- GPU1 is usable by the repaired threshold rule.
- GPU0 fallback is not needed. If fallback were considered, GPU0 would be
  unsuitable because utilization is 28%, above the 20% threshold.

Selected physical GPU for P03: GPU1.

Child-process mapping for P03: use `CUDA_VISIBLE_DEVICES=1`; inside the child
process, the selected physical GPU is expected to appear as logical `/GPU:0`.

## Handoff

P03 may launch after focused review confirms the repaired GPU rule and this
selection are consistent with the master program/runbook boundary.

## Superseded Blocker Note

The earlier blocker evidence in this file was valid trusted hardware evidence
but the blocker interpretation was too conservative. Under the repaired
threshold rule, the prior GPU1 state (`271 MiB`, `0%`, one Python process using
`248 MiB`) would have been a light shared-GPU warning rather than a continuation
veto.
