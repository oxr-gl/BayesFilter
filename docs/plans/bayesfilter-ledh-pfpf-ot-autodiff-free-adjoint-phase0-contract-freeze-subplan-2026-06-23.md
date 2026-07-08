# Phase 0 Subplan: Contract Freeze

status: DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P0-CONTRACT-FREEZE

## Phase Objective

Freeze the no-autodiff production-route contract, inherit the reviewed S7R
blocker state, and make plan drift itself a veto condition.

## Entry Conditions

- Master program exists.
- Visible runbook exists.
- Inherited state is `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED`.
- No new GPU or FD run has been launched after the reviewed blocker.

## Required Artifacts

- Contract: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-contract-2026-06-23.md`
- Result: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase0-contract-freeze-result-2026-06-23.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-execution-ledger-2026-06-23.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-stop-handoff-2026-06-23.md`
- Phase 1 subplan aligned with the frozen contract:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-subplan-2026-06-23.md`

## Required Checks/Tests/Reviews

- Local artifact existence checks for master, runbook, ledgers, and subplans.
- Cross-artifact alignment check that the contract, P0 result, execution
  ledger, stop handoff, and P1 subplan all preserve:
  - the no-production-autodiff invariant;
  - the inherited `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED` state;
  - the fact that no new GPU or FD run is authorized by P0.
- `git diff --check` on P0 artifacts.
- Bounded exact-path Claude review of the P0 subplan before execution.
- Bounded exact-path Claude review of the P0 result if it changes contract
  language materially.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the no-autodiff invariant explicit enough to govern all later phases? |
| Baseline/comparator | Prior partial route with outer `GradientTape`, S7R reviewed blocker. |
| Primary criterion | Contract artifact exists, contains an explicit production-vs-diagnostic boundary and forbidden API list, locks the inherited `S7R_BLOCKED_N2500_GPU_OOM_REVIEWED` state, blocks GPU/FD advancement, and aligns with the P0 result, execution ledger, stop handoff, and P1 subplan. |
| Veto diagnostics | Missing forbidden API list; ambiguous production-vs-diagnostic boundary; no inherited stop-state lock; Claude review does not converge. |
| Explanatory only | Current source leak scan, if run. |
| Not concluded | No implementation, no audit tool, no no-autodiff route, no GPU feasibility. |

## Forbidden Claims/Actions

- Do not implement code in P0 except plan/contract artifacts.
- Do not run GPU rungs or FD.
- Do not claim existing route is no-autodiff.
- Do not change pass/fail criteria after review.

## Exact Next-Phase Handoff Conditions

Advance to P1 only if:

- contract artifact exists;
- P0 result records local checks;
- execution ledger and stop handoff are updated at the exact required paths;
- cross-artifact alignment check passes for the no-production-autodiff
  invariant, inherited blocker state, and no-new-GPU/FD state;
- P1 subplan is present and aligned with the contract;
- Claude review, if required, returns `VERDICT: AGREE`.

## Stop Conditions

- Contract cannot define production-vs-diagnostic boundary.
- User direction conflicts with no-autodiff invariant.
- Claude review fails to converge within five rounds for the same blocker.
