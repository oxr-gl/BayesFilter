# P88 Phase 1 Subplan: Degree-Convergence Protocol Freeze

Date: 2026-06-27

Status: `P88_PHASE1_REVIEWED_CLOSED_PHASE2_BLOCKER_READY`

## Phase Objective

Freeze the degree-convergence protocol before any new fitting command. The
protocol must define target identity, degree ladder, rank policy, L1 tuning,
sample budgets, validation/holdout/audit separation, optimizer schedule,
promotion criteria, and veto diagnostics.

## Entry Conditions Inherited From Previous Phase

- Phase 0 must close with reviewed P87/P86 blocker inheritance.
- P88 baseline is `D18_SOURCE_ROUTE_EXECUTION_ONLY`.
- Degree convergence remains unresolved.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase1-degree-convergence-protocol-result-2026-06-27.md`
- Frozen degree-convergence protocol section embedded in the Phase 1 result.
- Refreshed Phase 2 execution subplan with exact commands or explicit blocker:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md`
- Updated P88 execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-execution-ledger-2026-06-27.md`
- Updated P88 Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-claude-review-ledger-2026-06-27.md`

## Required Checks/Tests/Reviews

Execution target: local artifact/protocol audit only. No new fitting command is
allowed in Phase 1.

Required local checks must include:

```bash
set -euo pipefail
rg -n "training-base|L1|validation|holdout|audit|plateau|early_stop_after|degree convergence|extension_or_invention|source-faithful" docs/plans/bayesfilter-highdim-zhao-cui-p86*.md scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
rg -n "training-base|L1|validation|holdout|audit|plateau|early_stop_after|degree convergence|extension_or_invention|source-faithful|exact commands|runtime|stop conditions|evidence contract|no fitting|plan-only" docs/plans/bayesfilter-highdim-zhao-cui-p88-phase1-degree-convergence-protocol-subplan-2026-06-27.md docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
```

Claude review required for the Phase 1 protocol and refreshed Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact degree-convergence protocol would justify reopening `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`? |
| Baseline/comparator | P86 rank pass with `Lagrangep(4,8)`, P86 favorable `Lagrangep(3,8)` comparator, and P87 execution-only final label. |
| Primary criterion | Protocol defines same-target identity, candidate/reference rungs, L1 tuning, sample budgets, scheduler, pass/fail thresholds, overfit checks, audit isolation, and exact commands or a blocker. |
| Veto diagnostics | Audit tuning, ALS revival, proxy correctness, favorable comparator promoted to convergence, non-default basis called source-faithful, max-epoch hit without plateau explanation, validation degradation, stale target. |
| Explanatory diagnostics | Validation curves, final/best holdout, LR-drop events, parameter/sample counts, multi-seed or deterministic-repeat rationale. |
| Not concluded | No degree convergence or rank/degree-stable label until Phase 2 executes/evaluates the frozen protocol. |
| Artifact | Phase 1 result and refreshed Phase 2 subplan. |

## Forbidden Claims/Actions

- Do not run fits in Phase 1.
- Do not use the P86 order-3 favorable result as convergence by itself.
- Do not claim non-default bases are source-faithful author defaults.
- Do not revive ALS.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only with a reviewed Phase 1 result and a refreshed Phase 2
subplan containing exact commands, budgets, runtime posture, stop conditions,
and evidence contract.

## Stop Conditions

- Degree protocol cannot define a fair same-target comparison.
- Required sample budgets or runtime envelope are infeasible without a new
  runtime decision.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Draft or refresh all required Phase 1 closeout artifacts first: Phase 1
   result/close or blocker record, Phase 2 subplan, execution ledger, and
   Claude review ledger. Only the Phase 2 subplan may be refreshed here; Phase
   2 implementation edits, fitting/training commands, runtime execution, GPU
   work, and production/HMC execution must not begin in Phase 1.
2. Enumerate the exact required check set in the Phase 1 result before running
   checks. For this phase the required set is exactly the `rg` protocol-discipline
   check, the P88 Phase 1/Phase 2 direct-content grep, and
   `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p88*.md` check
   listed in `Required Checks/Tests/Reviews`.
3. Run the enumerated required local checks after the closeout artifacts and
   ledgers have been prepared for review. Any failed required check vetoes Phase
   1 closure until fixed, rerun, and passed.
4. Remediation before Phase 1 closure is limited to P88 document and ledger
   edits. If a failed check or review issue would require implementation edits,
   fitting/training, runtime execution, GPU execution, Phase 2 execution, HMC, or
   production/default-policy work, do not remediate in Phase 1; write a blocker
   result and leave Phase 1 open.
5. Refresh the Phase 1 result so it records the final passed check outcomes
   before bounded review.
6. Send the final Phase 1 result to bounded Claude review before closing Phase
   1.
7. Send the refreshed Phase 2 subplan to bounded Claude review for consistency,
   correctness, feasibility, artifact coverage, command exactness, runtime
   boundaries, and safety. This approves only the Phase 2 subplan, not Phase 2
   execution.
8. Close Phase 1 only if enumerated required local checks pass, bounded Claude
   review agrees with the final recorded Phase 1 result, and bounded Claude
   review approves the refreshed Phase 2 subplan as a plan-only handoff. If any
   artifact is patched after local checks or review, rerun the affected local
   checks and resend the affected artifact to bounded Claude review before
   closure. If review disagreement remains unresolved or remediation would cross
   the document/ledger-only boundary, write a blocker result and do not close
   Phase 1.
