# P75 Phase 0 Subplan: Planning And Objective-Boundary Review

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE0
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_handoff: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-stop-handoff-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Confirm that P75 targets the real objective mismatch: the prior ALS route was
undersampled and optimized pointwise square-root regression rather than a
stochastic density objective with KL/cross-entropy and normalizer terms.

Phase 0 must classify P75 operations, inspect the current local implementation
surface at a planning level, and draft the Phase 1 mathematical design
subplan.  It must not edit implementation code or run training.

## Entry Conditions Inherited From P73

Phase 0 may begin only if:

- P73 visible stop handoff exists and records
  `P73_PHASE6_PASSED_CLAUDE_AGREE_COMPLETE`;
- P73 Phase 5 JSON exists and records
  `P73_PHASE5_DENSITY_AWARE_RENEWAL_BLOCKED`;
- P73 Phase 6 result exists and records the unresolved fresh-audit holdout
  signal;
- the P75 master program and visible runbook have passed local checks and
  Claude review;
- the run remains visible in the current session.

## Required Artifacts

Phase 0 must produce:

- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md`;
- Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-subplan-2026-06-17.md`;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-stop-handoff-2026-06-17.md
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
rg -n "P73_PHASE6_PASSED_CLAUDE_AGREE_COMPLETE|fresh audit|P73-B|blocked" docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-stop-handoff-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-result-2026-06-17.md
rg -n "FixedTTFitter|SquaredTTDensity|log_density|normalizer|GradientTape|Adam|tf.Variable" bayesfilter/highdim scripts tests/highdim
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

Review:

- Claude read-only review of the Phase 0 result and Phase 1 subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is the P75 lane correctly scoped as a stochastic density-objective pilot rather than a larger ALS diagnostic? |
| Exact baseline/comparator | P73 blocked diagnostic and Phase 6 handoff. |
| Primary pass/fail criterion | Phase 0 passes if it classifies P75 as extension/invention, identifies the current implementation gap, forbids proxy promotion, and drafts a Phase 1 design subplan with clear mathematical objectives and boundaries. |
| Diagnostics that can veto | Source-faithfulness overclaim, treating training loss as validation, training on audit holdout, implementation launch, pilot run launch, validation/HMC/scaling/GPU/rank-promotion launch. |
| Explanatory only | Current parameter/sample counts, current ALS surface, existing `SquaredTTDensity` evaluator, existing P73-B blocked status. |
| What will not be concluded | No implementation correctness, no pilot success, no lower-gate repair, no validation readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 0 result, Phase 1 subplan, ledgers. |

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run training or numerical pilot diagnostics.
- Do not claim source-faithful Zhao--Cui behavior for stochastic training.
- Do not claim KL correctness until Phase 1 derives the objective and Phase 3
  implements it.
- Do not use audit holdout or audit-line samples for training in any proposed
  design.
- Do not launch GPU, validation, HMC, scaling, or rank promotion.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 result exists and passes local checks;
- Phase 0 result states the operation classification and implementation gap;
- Phase 1 subplan exists and contains objective, entry conditions, artifacts,
  checks/reviews, evidence contract, forbidden actions, handoff conditions,
  and stop conditions;
- Claude returns `VERDICT: AGREE` for Phase 0 and the Phase 1 subplan.

## Stop Conditions

Stop and write a blocker if:

- P73 predecessor artifacts are missing or schema/smoke-only;
- current code already contains a stochastic training path and the plan would
  duplicate it without review;
- the design cannot avoid audit-holdout training leakage;
- the next action requires GPU, validation, HMC, scaling, rank promotion,
  threshold changes, package/network setup, or default-policy changes;
- Claude and Codex do not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it is planning-only,
uses the actual P73 blocked diagnostic as baseline, targets the objective
mismatch, blocks implementation/training until Phase 1 design is reviewed,
and keeps proxy metrics explanatory.
