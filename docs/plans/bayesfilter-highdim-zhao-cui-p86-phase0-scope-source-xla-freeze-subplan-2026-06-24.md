# P86 Phase 0 Subplan: Scope, Source, And XLA Freeze

Date: 2026-06-24

Status: `DRAFT_PENDING_MASTER_REVIEW`

## Phase Objective

Freeze the P86 scope, role contract, approval gates, source-anchor standard,
XLA/static-configuration boundary, and phase ladder before any code or runtime
repair begins.

## Entry Conditions Inherited From Previous Phase

- P85 closed as `PARTIAL_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR_REVIEWED`.
- P85 represented the author SIR setup but intentionally blocked full author
  algebraic `Lagrangep` fitting.
- P84 Phase 2 fitting remains blocked.
- Dirty implementation files exist in the worktree and must not be reverted or
  edited unless a later reviewed phase explicitly requires it.

## Required Artifacts

- P86 master program.
- P86 visible gated execution runbook.
- P86 execution ledger.
- P86 Claude review ledger.
- P86 stop handoff.
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase0-scope-source-xla-freeze-result-2026-06-24.md`
- Refreshed Phase 1 subplan.

## Required Checks / Tests / Reviews

- Required-section scan over every P86 subplan.
- Boundary scan for forbidden production/fitting/GPU/HMC/LEDH/scale claims.
- Source-anchor scan for required author/local anchors.
- `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p86*.md`
- Claude read-only bounded review of the P86 master program.
- Local review of the Phase 1 subplan; Claude review if material.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is P86 safe to launch as a visible, gated repair program for the author algebraic Lagrangep downstream gap? |
| Baseline/comparator | P85 stop handoff, P85 reset memo, P84 production-promotion gates, author source anchors, and current local implementation gaps. |
| Primary criterion | P86 artifacts contain required gates, evidence contracts, source-anchor rules, stop conditions, role boundaries, and local checks plus Claude review converge. |
| Veto diagnostics | Missing source-anchor gate; missing XLA setup-static boundary; missing human-required stop conditions; unsupported production/fitting/GPU/HMC/LEDH/scale scope; broad Claude prompt. |
| Explanatory diagnostics | Local grep scans, diff checks, Claude plan review, local next-subplan review. |
| Not concluded | No implementation correctness, fit quality, posterior correctness, HMC readiness, LEDH comparison, scale, or production readiness. |
| Artifact | Phase 0 result and refreshed Phase 1 subplan. |

## Forbidden Claims / Actions

- Do not edit algorithmic code.
- Do not run fitting, validation, GPU, HMC, LEDH, d=50/d=100, or long commands.
- Do not claim P84 Phase 2 is unblocked.
- Do not claim production readiness or posterior correctness.
- Do not treat Claude as an execution authority.
- Do not send Claude a broad repo prompt or bundled file packet.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 local checks pass;
- Claude review of the master program returns `VERDICT: AGREE`, or all material
  revisions are patched and rereviewed up to the five-round cap;
- the Phase 1 subplan is refreshed and reviewed for consistency, feasibility,
  artifact coverage, boundary safety, stop conditions, and approval needs;
- the execution ledger records the Phase 0 gate.

## Stop Conditions

Stop if:

- local checks fail and cannot be patched within P86 docs;
- Claude and Codex do not converge after five rounds for the same blocker;
- continuing would require code edits or runtime commands before Phase 1;
- source-anchor, XLA, or human-approval boundaries remain ambiguous.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 0 result / close record;
3. draft or refresh the Phase 1 subplan;
4. review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
