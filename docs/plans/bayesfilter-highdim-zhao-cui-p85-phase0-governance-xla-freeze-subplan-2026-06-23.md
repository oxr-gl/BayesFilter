# P85 Phase 0 Subplan: Governance, Scope, And XLA Boundary Freeze

Date: 2026-06-23

Status: `DRAFT_PENDING_MASTER_REVIEW`

## Phase Objective

Freeze the P85 scope, role contract, approval gates, source-anchor standard,
and XLA/static-configuration boundary before any author inventory, interface
design, implementation, or test execution begins.

## Entry Conditions Inherited From Previous Phase

- P84 Phase 1 is blocked by
  `BLOCK_P84_PHASE1_AUTHOR_BASIS_DOMAIN_PARITY_NOT_CLOSED`.
- P85 has no previous phase; it inherits P84's stop condition that Phase 2
  fitting must not run until Phase 1 parity is repaired or explicitly kept
  blocked.
- P83 execution-only evidence remains diagnostic and cannot be promoted.

## Required Artifacts

- P85 master program.
- P85 visible gated execution runbook.
- P85 execution ledger.
- P85 Claude review ledger.
- P85 stop handoff.
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase0-governance-xla-freeze-result-2026-06-23.md`
- Refreshed Phase 1 subplan.

## Required Checks / Tests / Reviews

- Required-section scan over every P85 subplan.
- Boundary scan for forbidden production/fitting/GPU/HMC/LEDH claims.
- `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p85*.md`
- Trailing-whitespace scan over P85 artifacts.
- Claude read-only review of the P85 master program.
- Local review of the Phase 1 subplan; Claude review if material.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is P85 safe to launch as a visible, doc-first repair program for the P84 basis/domain blocker? |
| Baseline/comparator | P84 Phase 1 blocker and P84 stop handoff. |
| Primary criterion | Master/runbook/subplans contain required gates, evidence contracts, stop conditions, and role boundaries, and local checks plus Claude review converge. |
| Veto diagnostics | Missing source-anchor gate; missing XLA setup-static boundary; missing human-required stop conditions; unapproved runtime/fitting/GPU scope. |
| Explanatory diagnostics | Local grep scans, diff checks, Claude plan review. |
| Not concluded | No source semantics, implementation correctness, fit quality, production readiness, or P84 Phase 1 repair. |
| Artifact | Phase 0 result and refreshed Phase 1 subplan. |

## Forbidden Claims / Actions

- Do not edit BayesFilter algorithmic code.
- Do not run fitting, validation, GPU, HMC, LEDH, d=50/d=100, or long commands.
- Do not claim P84 Phase 1 is repaired.
- Do not treat Claude as an execution authority.
- Do not send Claude a whole-file packet or broad repo prompt.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 local checks pass;
- Claude review of the master program returns `VERDICT: AGREE` or all material
  revisions are patched and rereviewed up to the five-round cap;
- the Phase 1 subplan is refreshed and reviewed for consistency, feasibility,
  artifact coverage, and boundary safety;
- the execution ledger records the Phase 0 gate.

## Stop Conditions

Stop if:

- local checks fail and cannot be patched within P85 docs;
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
