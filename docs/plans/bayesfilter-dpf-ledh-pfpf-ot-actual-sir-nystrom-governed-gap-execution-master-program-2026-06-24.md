# Actual-SIR Nystrom Governed Gap Execution Master Program

Date: 2026-06-24

Status: `G1_VISIBLE_EXECUTION_READY`

## Objective

Execute the actual-SIR Nystrom evidence-governance gap plan in visible gated
phases, starting with the broader `N=8192` fixed-policy replication gate.

Codex in the current conversation is supervisor and executor.  Claude, if used,
is a read-only reviewer only and cannot authorize benchmark launch, default
promotion, scientific claims, model-file changes, or human/product boundaries.

## Governing Plan

- Governance and gap plan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-evidence-governance-and-gap-plan-2026-06-24.md`

## Current Phase

Phase G1:

- Subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-subplan-2026-06-24.md`
- Result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-result-2026-06-24.md`

## Phase Index

| Phase | Name | Status | Next Action |
| --- | --- | --- | --- |
| G0 | Governance and gap lock | `COMPLETE` | Use governance plan as gate source. |
| G1 | Broader `N=8192` fixed-policy replication | `READY` | Run only after local skeptical audit and trusted GPU preflight. |
| G2 | Repair selection or scope decision | `PENDING_G1_RESULT` | Draft after G1 close record. |
| G3 | Fixed-policy history/memory gate | `PENDING_G2_HANDOFF` | Not launchable yet. |
| G4 | Nystrom-specific gradient mechanics gate | `PENDING_G3_HANDOFF` | Not launchable yet. |
| G5 | Evidence package/default-readiness review | `PENDING_G4_HANDOFF` | Human approval required for any default change. |

## Evidence Boundary

This master program may produce hard-screen and diagnostic evidence.  It must
not claim:

- default readiness;
- HMC readiness;
- posterior correctness;
- dense Sinkhorn equivalence;
- statistical superiority or ranking;
- broad Nystrom rejection.

## Visible Execution Rules

- Run commands in the current conversation, not detached supervisors.
- Redirect full benchmark stdout/stderr to log files.
- Print only bounded summaries in chat.
- Preserve unrelated dirty worktree changes.
- Use trusted/elevated GPU commands for GPU/CUDA checks and benchmark runs.
- Prefer physical GPU1 if available; otherwise use GPU0 and record the fallback.
- Stop if a required artifact is missing, malformed, or inconsistent with the
  subplan evidence contract.
