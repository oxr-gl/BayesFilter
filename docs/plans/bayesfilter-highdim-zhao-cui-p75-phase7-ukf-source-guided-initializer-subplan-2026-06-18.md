# P75 Phase 7 Subplan: UKF/Source-Guided Initializer Design

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE7
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design, but do not yet run, a proper UKF/source-guided initialization and
prefit route for P75.  The design must generalize the successful
calibrated-constant smoke without overclaiming it as a full UKF solution.

## Entry Conditions Inherited From Phase 6

Phase 7 may begin only if:

- Phase 6 result exists;
- guided warm-start JSON exists and is valid;
- Phase 6 result states audit gates still block;
- Claude returns `VERDICT: AGREE` for Phase 6 result and this subplan, or
  fixable issues have been patched and re-reviewed.

## Required Artifacts

Phase 7 must produce:

- Phase 7 design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md`;
- a Phase 8 implementation subplan if and only if the design is bounded;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
rg -n "UKF|source-route|initialization|prefit|audit|nonclaims" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-subplan-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-subplan-2026-06-18.md
```

Review:

- Claude read-only review of the Phase 7 design result and any Phase 8
  implementation subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What is the smallest mathematically coherent UKF/source-guided initializer and prefit route that could plausibly reduce audit residuals after escaping the defensive floor? |
| Exact baseline/comparator | Phase 6 random-vs-calibrated-constant same-draw smoke. |
| Primary criterion | Produce a bounded design that specifies guide inputs, train/eval split, initialization formula, optional supervised square-root prefit, stochastic objective handoff, and nonclaim boundaries. |
| Diagnostics that can veto | Treating Phase 6 as lower-gate repair, using audit data for hyperparameter selection, claiming UKF truth/source-faithfulness, launching a larger run, missing stop conditions, or failing to state what implementation would test. |
| Explanatory only | Phase 6 residuals, UKF scout metadata, source-route frame/target-cloud scale, loss/gradient evidence. |
| What will not be concluded | No algorithm success, validation readiness, HMC readiness, scaling, rank/sample policy, or source-faithful Zhao--Cui parity. |
| Artifact preserving result | Phase 7 design result, any Phase 8 subplan, ledgers, Claude review. |

## Forbidden Claims/Actions

- Do not run training diagnostics in Phase 7.
- Do not run the degree 2/rank 4/batch 1024/up-to-500 pilot.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not use audit samples for initialization, prefit, stopping, or
  hyperparameter selection.
- Do not claim UKF is truth or source-faithful Zhao--Cui.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin only if:

- Phase 7 design result exists;
- exactly one implementation target is selected;
- Phase 8 subplan exists with bounded tests and commands;
- Claude review agrees or unresolved blockers are escalated to the user.

## Stop Conditions

Stop for human direction if:

- the design requires a full UKF Gaussian TT initializer that is not yet
  locally supported;
- the design cannot separate training and audit data;
- the design would require GPU or a long run;
- the next action cannot be tested with a small smoke before a larger pilot.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it turns the successful
Phase 6 mechanism test into a design phase, keeps audit gates blocking, and
forbids larger execution until the initializer/pretraining route is specified.
