# Manual Adjoint Phase 7 Subplan: Return-To-P82 Validation Handoff

status: DRAFT_READY_AFTER_M6_CLAUDE_R3_ONE_PATH_AGREE
date: 2026-06-22
phase: M7-P82-HANDOFF

## Phase Objective

Prepare the reviewed handoff that allows P82 FD-only validation to resume using
the memory-disciplined LEDH-PFPF-OT actual-gradient route instead of raw
`transport_ad_mode=full` full-graph AD/JVP.

## Entry Conditions

- M6 streaming/chunked route local checks pass and the M6 review gate is
  resolved by Claude R3 one-path agreement.
- Supported modes, unsupported modes, and tiny memory-shape/runtime evidence
  are recorded.
- P82 FD comparator protocol remains unchanged.

## Required Artifacts

- Return-to-P82 handoff:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-p82-validation-handoff-2026-06-22.md`
- Draft refreshed P82 validation subplan, or blocker if P82 cannot resume.
- Phase 7 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-result-2026-06-22.md`
- Refreshed M8 closeout subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

- Verify the handoff states:
  - supported route and transport modes;
  - stopped/frozen/replayed quantities;
  - primitive parity summary;
  - tiny memory-shape/runtime evidence and remaining large-N uncertainty;
  - exact P82 actual-gradient command;
  - exact P82 regression-FD command;
  - stop conditions.
- Claude read-only review is required before P82 can resume.
- `git diff --check` on touched plan artifacts.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there enough reviewed evidence to hand P82 a bounded streaming actual-gradient route candidate and preserve the 13-point FD comparator protocol? |
| Baseline/comparator | M2-M6 parity/memory evidence and the P82 FD-only correction. |
| Primary criterion | Handoff gives exact commands, route metadata, supported/unsupported modes, large-N stop conditions, and nonclaims without unsupported promotion. |
| Veto diagnostics | Missing M6 review convergence; missing primitive parity summary; raw full-AD N10000 reintroduced; P82 FD protocol weakened; treating tiny M6 memory-shape evidence as N10000 feasibility; Claude review not converged for material handoff. |
| Explanatory diagnostics | Route metadata, expected runtime/memory envelope, seed manifest, and FD comparator manifest. |
| Not concluded | P82 has not yet passed; no HMC/default/posterior/scientific-superiority readiness. |

## Forbidden Claims / Actions

- Do not run P82 validation in M7.  M7 writes the handoff and refreshed P82
  subplan only.
- Do not change the FD protocol.
- Do not describe the handoff as proof of gradient correctness.
- Do not describe M6 as Zhao-Cui source-faithful evidence.  If the handoff or
  refreshed P82 plan makes any Zhao-Cui source-route or source-faithfulness
  claim, it must cite the paper/math and local author-source anchors required
  by repo-root `memory.md`.
- Do not allow Claude to authorize scientific or runtime boundary crossings.

## Next-Phase Handoff Conditions

M8 may proceed after M7 records either:

- `P82_RETURN_READY`, with reviewed handoff and refreshed P82 subplan; or
- `P82_RETURN_BLOCKED`, with a concrete blocker and no validation launch.

## Stop Conditions

Stop if the handoff cannot state exact commands, if the M6 streaming route is
not ready even as a bounded N10000 planning candidate, if the P82 FD protocol
would need to change, or if review finds unresolved material boundary issues.
