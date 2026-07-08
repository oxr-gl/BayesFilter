# P82 Phase 9 Result: Closeout After P7 N10000 OOM

status: STOPPED_AT_P7_N10000_OOM_CLAUDE_AGREE
date: 2026-06-23
phase: P9-CLOSEOUT

## Decision

P82 is stopped at P7.  The reviewed P6-P8 completion plan cannot proceed to P8
because P7 did not produce the required valid N10000 actual-gradient artifact.

Governing reviewed plan:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p82-p6-p8-completion-plan-2026-06-23.md
```

## Phase Outcomes

| Phase | Outcome | Artifact |
|---|---|---|
| P5 | Manual streaming transport-gradient wiring passed local checks and Claude review. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-result-2026-06-23.md` |
| P6 | Tiny trusted GPU smoke passed local checks, GPU preflight, route metadata, finite values, and Claude review. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md` |
| P7 N1000 | Actual-gradient feasibility rung passed with finite five-seed gradients and finite MCSE. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json` |
| P7 N10000 | Blocked by GPU `ResourceExhaustedError`; no N10000 output/progress JSON exists. | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md` |
| P8 | Not run. | N/A |

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Question | Could the P5-wired manual streaming route finish the governed FD-only P82 program? |
| Answer | No under the reviewed P7 N10000 command: N10000 actual-gradient feasibility failed by GPU OOM before P8 could start. |
| Comparator | Same-scalar FD comparator was not run because P8 entry conditions were not met. |
| Primary criterion | Not satisfied: missing valid N10000 actual-gradient artifact. |
| Veto diagnostics | Triggered: OOM / missing N10000 artifact. |
| Not concluded | No FD agreement, no posterior correctness, no HMC/default readiness, no production readiness, no scientific superiority, no Zhao-Cui comparator readiness. |

## What Was Established

- The P82 benchmark path can select and record the manual streaming gradient
  route.
- The route can execute a tiny GPU-visible SIR d18 smoke with finite objective
  and finite gradients.
- The same route can complete the five-seed N1000 actual-gradient feasibility
  rung under GPU/TF32 with finite gradient components and finite seed MCSE.

## What Failed

The reviewed N10000 actual-gradient feasibility command failed with TensorFlow
`ResourceExhaustedError: failed to allocate memory` on GPU during the manual
streaming finite transport path.  No P7 N10000 JSON or progress JSON was
written.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `a463bb012df35bb120a9b232df067e69bf915add` |
| Python / TensorFlow | Python `3.11.14`, TensorFlow `2.19.1` |
| Execution environment | `/home/chakwong/BayesFilter`; conda env path visible in warnings as `/home/chakwong/anaconda3/envs/tf-gpu`; GPU commands run with trusted/escalated permissions. |
| CPU/GPU status | P7 local checks used `CUDA_VISIBLE_DEVICES=-1`; P7 GPU preflight and P7 GPU rungs did not hide GPU devices. |
| GPU preflight | `nvidia-smi` at 2026-06-23 01:16:22 saw NVIDIA GeForce RTX 4080 SUPER-class GPU, driver `591.86`, CUDA `13.1`, 16376 MiB memory. |
| TensorFlow GPU probe | TensorFlow saw `[CPU:0, GPU:0]` and `[GPU:0]`; plugin-registration warnings appeared but did not veto. |
| Seeds | `81120,81121,81122,81123,81124`, evaluated with `seed_microbatch_size=1`. |
| N1000 wall time | `69.97849530700114` benchmark seconds; artifact written. |
| N10000 wall time | Failed after GPU initialization and before output/progress JSON creation; exact benchmark elapsed unavailable because the command exited by exception before writing result JSON. |
| N10000 stderr/log artifact | No separate stderr file was written; the exception trace was captured in the Codex execution transcript and summarized in `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md`. |
| N10000 output artifact | Missing: `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json` |
| N10000 progress artifact | Missing: `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-progress-2026-06-23.json` |

Failed N10000 command:

```bash
MPLCONFIGDIR=/tmp timeout 7200 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 7 manual streaming actual-gradient N10000 GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-progress-2026-06-23.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json
```

## What Was Not Run

- P8 governed N1000 13-point regression FD was not launched.
- No FD-vs-actual comparison was computed.
- No N10000 rerun with altered allocator, chunking, AD mode, or seed grouping
  was attempted.

## Next Justified Action

Write a new reviewed remediation subplan before any further GPU experiment.
Candidate remediation questions include:

- whether `TF_GPU_ALLOCATOR=cuda_malloc_async` changes the N10000 memory
  behavior;
- whether smaller row/column/particle chunks avoid the failure;
- whether a different actual-gradient evaluation route avoids retaining the
  failing graph state;
- whether P7 should add intermediate rungs between N1000 and N10000.

These are not authorized by this closeout.

## Non-Claims

This closeout does not claim LEDH-PFPF-OT gradient validation, FD agreement,
manual-adjoint correctness at N10000, posterior correctness, HMC/default
readiness, production readiness, scientific superiority, or Zhao-Cui
source-faithfulness/comparator readiness.

## Handoff

Current status:

```text
P82_STOPPED_AT_P7_N10000_GPU_OOM_P8_NOT_RUN
```

Claude R2 review returned `VERDICT: AGREE`.  Stop and wait for a new
human-approved or reviewed remediation plan.
