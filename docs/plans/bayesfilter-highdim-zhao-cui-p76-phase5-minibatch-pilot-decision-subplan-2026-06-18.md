# P76 Phase 5 Subplan: Mini-Batch Pilot Decision

metadata_date: 2026-06-18
status: LOCAL_CHECKS_PASSED_CLAUDE_REVIEW_PENDING
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Decide, from the Phase 4 tiny smoke, whether P76 should stop, repair the
initializer mechanics, or draft a bounded mini-batch pilot plan.  Phase 5 is a
decision/planning phase.  It must not run the pilot unless a later reviewed
phase and the required approvals authorize it.

## Entry Conditions Inherited From Phase 4

Phase 5 may begin only if:

- Phase 4 result exists;
- smoke JSON exists and parses;
- smoke JSON records finite initializer cores, finite total loss, finite
  gradient norm, finite rho, finite normalizer, finite log density, and
  `train_step_count: 1`;
- smoke JSON records `source_route_prefit_used: false`,
  `audit_data_used: false`, and `cpu_only: true`;
- Phase 4 local checks pass;
- Claude agrees Phase 4 and this subplan are consistent, or repairable issues
  are patched and re-reviewed.

## Required Artifacts

Phase 5 must produce:

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-result-2026-06-18.md`;
- if justified, a bounded pilot subplan or request-for-approval note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-subplan-2026-06-18.md`;
- updated execution and Claude review ledgers;
- updated stop handoff or runbook closeout status.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
rg -n "P76_PHASE4_TINY_SMOKE_COMPLETED|finite_total_loss|finite_gradient_norm|finite_rho_theta|finite_normalizer|finite_log_density|source_route_prefit_used|audit_data_used|cpu_only|train_step_count" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
rg -n "Decision Table|bounded mini-batch pilot|not lower-gate repair|not validation|not HMC readiness|separate approval" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-result-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Review:

- Claude read-only review of the Phase 5 decision result and any Phase 6
  subplan/request;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the tiny UKF-initializer smoke justify drafting a bounded mini-batch pilot plan? |
| Exact baseline/comparator | Phase 4 smoke JSON and P75 negative-method context; not a method ranking. |
| Primary criterion | A decision table states stop/repair/draft-pilot, explains why, and preserves all nonclaims and approval boundaries. |
| Diagnostics that can veto | Missing smoke artifact, false finite flag, source-prefit/audit flag true, treating smoke as lower-gate repair, authorizing a large pilot, changing defaults, or using audit metrics as selection criteria. |
| Explanatory only | Tiny total loss, gradient norm, rho range, normalizer, log-density range, runtime. |
| What will not be concluded | No generalization, no lower-gate repair, no validation/HMC readiness, no final sample/rank policy. |
| Artifact preserving result | Phase 5 result, optional Phase 6 bounded-pilot subplan/request, ledgers, Claude review. |

## Required Decision Content

The Phase 5 result must state:

- whether Phase 4 passed its primary smoke criterion;
- whether any veto fired;
- why this is not enough to claim the bug is fixed;
- whether the next justified action is:
  - stop;
  - repair mechanics;
  - draft a bounded mini-batch pilot plan;
- if a bounded pilot is drafted, what approval is required before execution;
- what data are excluded from training/stopping/selection;
- what outcomes would count as pilot failure, tuning failure, or evidence
  against the UKF warm-start hypothesis.

## Forbidden Claims/Actions

- Do not launch a large mini-batch pilot in Phase 5.
- Do not change defaults.
- Do not use GPU/CUDA.
- Do not claim lower-gate repair, validation readiness, HMC readiness, or
  source-faithfulness.
- Do not use audit samples for initialization, training, stopping, or
  hyperparameter selection.
- Do not resurrect random, calibrated constant, or source-route prefit as live
  repair ladders.

## Exact Next-Phase Handoff Conditions

If Phase 5 drafts a Phase 6 bounded-pilot subplan, Phase 6 may begin only if:

- Phase 5 result exists;
- Phase 6 subplan exists and is reviewed;
- the subplan states exact CPU-only or GPU-approved commands, budget, seeds,
  sample/batch counts, evidence contract, stop conditions, and approval
  boundary;
- the user gives any approval required by the Phase 6 subplan;
- Claude agrees, or a blocker is escalated.

## Stop Conditions

Stop if:

- Phase 4 smoke JSON is missing, nonparseable, or fails a required finite flag;
- the only possible next step would be a large pilot without separate approval;
- the decision would rely on audit samples for selection;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

Phase 5 is deliberately a decision phase.  It cannot treat a one-step smoke as
evidence that mini-batch training generalizes or that the original fitting bug
is fixed.
