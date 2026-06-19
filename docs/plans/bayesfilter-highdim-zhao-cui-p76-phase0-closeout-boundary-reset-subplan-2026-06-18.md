# P76 Phase 0 Subplan: Closeout And Boundary Reset

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE0
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
predecessor_erratum: docs/plans/bayesfilter-highdim-zhao-cui-p75-closeout-erratum-ukf-hypothesis-untested-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Close the P75 planning lane for the UKF hypothesis and establish P76's
boundary: the next live method is a true UKF-informed warm start followed by
mini-batch stochastic density training.

## Entry Conditions Inherited From Planning Spine

Phase 0 may begin only if:

- the P75 erratum exists;
- the P76 master program exists;
- this subplan exists;
- the visible runbook and ledgers exist;
- local planning checks pass;
- Claude agrees the planning spine is internally consistent, or fixable issues
  are patched and re-reviewed.

## Required Artifacts

Phase 0 must produce:

- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase0-closeout-boundary-reset-result-2026-06-18.md`;
- reviewed Phase 1 mathematical UKF-initializer subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-subplan-2026-06-18.md`;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
rg -n "UKF|scout_not_truth|source-route prefit|mini-batch|P75|P76|not supported|forbid" docs/plans/bayesfilter-highdim-zhao-cui-p75-closeout-erratum-ukf-hypothesis-untested-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase0-closeout-boundary-reset-subplan-2026-06-18.md
rg -n "P52_UKF_SCOUT_CLAIM|scout_not_truth|UKF scout cannot promote stronger claims" bayesfilter/highdim/ukf_scout.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-closeout-erratum-ukf-hypothesis-untested-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase0-closeout-boundary-reset-subplan-2026-06-18.md
```

Review:

- Claude read-only review of P75 erratum, P76 master program, visible runbook,
  and this Phase 0 subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is P76 correctly scoped to the actual UKF warm-start plus mini-batch training hypothesis, rather than another source-prefit ladder? |
| Exact baseline/comparator | P75 Phase 10 negative source-prefit result and P75 erratum. |
| Primary criterion | The boundary result must close P75 for the UKF hypothesis, forbid repeating failed methods as live repairs, and draft Phase 1 to design a true UKF initializer from \((m_U,P_U)\). |
| Diagnostics that can veto | Any plan that substitutes source-route prefit for UKF initialization; promotes UKF to truth; authorizes large pilot; uses audit data; or treats P75 as evidence against UKF. |
| Explanatory only | P75 row results, p50 UKF equations, P70 branch-builder notes, `ukf_scout.py` manifests. |
| What will not be concluded | No implementation, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy, and no source-faithful Zhao--Cui claim. |
| Artifact preserving result | Phase 0 result, Phase 1 subplan, ledgers, Claude review. |

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 0.
- Do not run training diagnostics in Phase 0.
- Do not claim UKF initialization works.
- Do not claim P75 disproves UKF warm-starting.
- Do not reopen random, calibrated constant, or source-route prefit as live
  repair candidates.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 result exists;
- Phase 1 subplan exists;
- Phase 0 explicitly binds P76 to UKF moments \((m_U,P_U)\);
- Phase 0 preserves UKF as `scout_not_truth`;
- Phase 0 forbids source-route prefit as a substitute target;
- local checks pass;
- Claude agrees or a blocker is escalated.

## Stop Conditions

Stop if:

- the planning spine cannot distinguish true UKF initialization from
  source-route prefit;
- the current codebase has no discoverable UKF moment source and Phase 1 cannot
  reasonably design one;
- Claude identifies a material blocker that cannot be repaired within five
  rounds;
- continuing would require implementation edits, training, GPU, package
  installation, or network access.

## Skeptical Plan Audit

This Phase 0 subplan is designed to prevent the exact P75 error: replacing the
live UKF hypothesis with a weaker convenient prefit.  It does not execute
scientific diagnostics; it resets the boundary so Phase 1 can define the
actual UKF initializer before code changes.
