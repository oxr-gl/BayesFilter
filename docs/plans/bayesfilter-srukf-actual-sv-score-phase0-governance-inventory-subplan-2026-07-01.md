# Phase 0 Subplan: Governance And Drift Inventory

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Freeze the SR-UKF actual-SV program boundary, inventory current drift evidence,
confirm artifacts exist, and launch only documentation/audit-first execution.

## Entry Conditions Inherited From Previous Phase

- User requested a master program, phase subplans, bounded Claude review, a
  visible gated runbook, and launch.
- No previous SR-UKF program phase has executed.
- Current known drift: actual-SV UKF value is a diagnostic route, while the
  current actual-SV UKF score wrapper is autodiff and not leaderboard-admitted.

## Required Artifacts

- Master program.
- Visible gated execution runbook.
- Execution ledger.
- Claude review ledger.
- Stop handoff.
- Drift inventory section in the Phase 0 result that records current code/doc
  anchors for:
  - current actual-SV UKF value-only diagnostic route;
  - current actual-SV UKF autodiff score wrapper;
  - current KSC strict-SPD principal-root derivative score comparator;
  - current leaderboard admission guard excluding autodiff and historical SVD
    score provenance.
- Phase 0 result.
- Refreshed Phase 1 generic derivation subplan.

## Required Checks/Tests/Reviews

- Local text checks that all phase artifacts exist and include required
  subplan fields.
- Local drift-inventory checks that the Phase 0 result names both products:
  generic factor-propagating SR-UKF backend and actual-SV augmented-noise
  adapter.
- Local forbidden-route checks that the Phase 0 result explicitly forbids
  admitted score use of `GradientTape`, historical SVD/eigenderivative score
  provenance, and strict-SPD principal-root derivative substitution.
- `git diff --check` for the new plan artifacts.
- Bounded Claude read-only review of this subplan or master/runbook if material
  issues remain.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the governance artifacts sufficient to launch derivation-first SR-UKF repair without repeating the UKF drift? |
| Baseline/comparator | User request, local runbook template, `AGENTS.md` Claude prompt shape, current code/doc inventory. |
| Primary criterion | All launch artifacts exist, the Phase 0 result preserves a drift inventory, names the two separate products, forbids old drift routes, and specifies the Phase 1 handoff. |
| Veto diagnostics | Missing required artifact, missing forbidden-route guard, detached/nested launch, or unbounded Claude review. |
| Explanatory diagnostics | Dirty worktree inventory and current code/doc anchors. |
| Not concluded | No derivation, implementation, numerical correctness, or leaderboard readiness is concluded in Phase 0. |
| Artifact | Phase 0 result and updated ledger. |

## Forbidden Claims/Actions

- Do not claim SR-UKF derivation correctness.
- Do not edit implementation code.
- Do not run numerical TensorFlow tests as evidence.
- Do not launch detached or nested agents.
- Do not ask for human approval for administrative steps that the runbook can
  handle.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- master, runbook, ledgers, stop handoff, and all phase subplans exist;
- local text checks pass;
- the Phase 0 result contains the required drift inventory and passes local
  forbidden-route checks;
- material launch artifacts means the master program, visible runbook, and
  Phase 0 subplan; convergence means each required material Claude review has
  `VERDICT: AGREE` or all `VERDICT: REVISE` findings have been visibly patched
  and rereviewed with no material blocker;
- Phase 1 subplan is present and locally reviewed.

## Stop Conditions

- Missing or contradictory owner boundary.
- Missing, stale, or contradictory drift-inventory evidence.
- Claude review identifies a material governance flaw that cannot be repaired in
  five rounds.
- Launch would require detached execution, network fetch, package install, or
  runtime/GPU execution outside the reviewed scope.

## End-Of-Phase Procedure

1. Run local checks.
2. Write Phase 0 result/close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
