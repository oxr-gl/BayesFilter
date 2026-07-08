# Phase 8 Subplan: Closeout, Reset Memo, And Boundary Decision

Date: 2026-07-04

Status: `DRAFT_READY_FOR_PRECHECK`

## Phase Objective

Close the visible program with a reset memo, final artifact index, residual risk
ledger, and explicit boundary decisions about what can and cannot be claimed
from the completed evidence.

Phase 7 currently ends at a launch-smoke classification only. Phase 8 must not
pretend the launch smoke established convergence, ranking, or replicated
evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 7 classified the launch-smoke hard vetoes and recorded which admitted
  candidates passed or failed the launch tier.
- All planned repairs either completed or have blocker records.
- No default-policy, public API, or production-readiness claim may be made
  without a separate approved gate.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-result-2026-07-04.md`
- Reset memo for future agents.
- Final artifact index with plan, result, benchmark, log, and review paths.
- Decision table and inference-status table.
- Residual risk and nonclaims ledger.
- Final Claude read-only review bundle if the closeout makes material
  scientific or engineering decisions.

## Required Checks, Tests, And Reviews

- Verify every phase has a result or blocker artifact.
- Verify run manifests exist for serious runs.
- Verify final claims match evidence class and uncertainty support.
- Verify dirty worktree summary separates Codex-created plan/work files from
  unrelated user changes.
- Claude read-only review for final decision text if Phase 7 produced material
  evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What can safely be handed off after the SSL-LSTM filter-HMC launch-smoke phase, and what remains unproved? |
| Baseline/comparator | All accepted phase artifacts and review ledgers. |
| Primary pass criterion | Final result and reset memo accurately index artifacts, decisions, evidence classes, residual risks, and nonclaims, while preserving the distinction between launch-smoke evidence and later replicated evidence. |
| Veto diagnostics | Missing phase result, unsupported final claim, missing run manifest, unclassified stochastic ranking, or dirty worktree confusion. |
| Explanatory diagnostics | Artifact counts, review rounds, and unresolved TODO inventory. |
| Not concluded | Anything not supported by the recorded evidence, especially method superiority, exact posterior correctness, source-faithfulness, and default readiness. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not change repository default policy.
- Do not claim production/default readiness unless a separate approved gate did
  that work.
- Do not summarize stochastic comparisons as rankings without statistical
  evidence.
- Do not hide failed or blocked candidates.
- Do not revert unrelated dirty worktree changes.
- Do not promote launch-smoke evidence to convergence evidence.

## Exact Next-Phase Handoff Conditions

There is no automatic next phase. Any continuation must start from the reset
memo and either:

- address a recorded blocker;
- run a separately reviewed longer validation plan;
- request human approval for a boundary crossing; or
- prepare a separate default/API/productization plan.

## Stop Conditions

- Final claims cannot be reconciled with the evidence.
- Required artifacts are missing and cannot be reconstructed.
- Human direction is needed to decide whether to continue beyond research
  evidence into product/default policy.
- Claude and Codex do not converge on final claim boundaries after five rounds.

## End-Of-Phase Protocol

1. Run final artifact, manifest, and claim-boundary checks.
2. Write the Phase 8 result/close record and reset memo.
3. Review final artifacts for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
4. Send final material closeout to Claude if required.
