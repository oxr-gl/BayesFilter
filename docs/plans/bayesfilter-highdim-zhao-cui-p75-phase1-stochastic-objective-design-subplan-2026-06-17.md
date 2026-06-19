# P75 Phase 1 Subplan: Stochastic Objective Design Contract

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE1
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Derive and freeze the mathematical pilot objective for stochastic
differentiable density training before any implementation edit.

Phase 1 must decide the first bounded pilot target: objective, sample
distribution, normalizer treatment, regularization, train/eval split, batch
schedule, gates, nonclaims, and exact implementation handoff.

## Entry Conditions Inherited From Phase 0

Phase 1 may begin only if:

- Phase 0 result exists;
- Phase 0 classifies P75 as `extension_or_invention`;
- Phase 0 identifies the current optimizer gap;
- Phase 1 subplan exists;
- Phase 0 local checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 0 result and this subplan.

## Required Artifacts

Phase 1 must produce:

- Phase 1 design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md`;
- Phase 2 implementation-surface subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md`;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md
rg -n "extension_or_invention|SquaredTTDensity|FixedTTFitter|P73_B_OPTIMIZER_BLOCKED|No training was run" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md
rg -n "rho_theta|log Z|KL|cross-entropy|audit holdout|finite-gradient|CPU-only|not validation" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

Review:

- Claude read-only review of the Phase 1 mathematical design and Phase 2
  implementation-surface subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What exact stochastic density objective should the first P75 pilot implement? |
| Exact baseline/comparator | P73 blocked diagnostic and Phase 0 objective-boundary result. |
| Primary pass/fail criterion | Phase 1 passes if it freezes an implementable pilot objective, training/evaluation split, normalizer handling, sample schedule, gates, and Phase 2 handoff without implementation edits. |
| Diagnostics that can veto | Objective not mathematically defined, audit holdout used for training, proxy loss promoted to validation, unbounded runtime, GPU requirement without approval, source-faithfulness overclaim. |
| Explanatory only | Candidate parameter counts, planned batch sizes, rough runtime estimates, candidate penalties. |
| What will not be concluded | No implementation correctness, no pilot result, no lower-gate repair, no validation readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 1 design result, Phase 2 subplan, ledgers. |

## Required Design Decisions

Phase 1 must explicitly decide:

- target density representation:
  \(\rho_\theta(z)=h_\theta(z)^2+\tau q_0(z)\);
- objective, for example
  \[
  L(\theta)=-E_{z\sim q}\log \rho_\theta(z)+\log Z_\theta+R(\theta);
  \]
- whether \(Z_\theta\) is exact via squared-TT contractions in the pilot;
- training distribution \(q\) and how fresh batches are generated;
- audit holdout and audit-line exclusion from training;
- degree/rank pilot values and whether degree 2/rank 4 is immediate or a
  post-smoke rung;
- batch size, number of batches, and stop/runtime limits;
- optimizer, learning rate, gradient clipping, and parameter regularization;
- finite loss/gradient gates and fresh-audit evaluation gates;
- what counts as pass, block, and explanatory-only.

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run training.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not change P73/P75 thresholds after seeing outputs.
- Do not train on audit holdout or audit-line samples.
- Do not claim the design is source-faithful Zhao--Cui.
- Do not claim pilot success before implementation and execution.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 result exists and passes local checks;
- Phase 1 freezes a single first-pilot objective and schedule;
- Phase 1 states all pass/block/nonclaim criteria;
- Phase 2 subplan exists and maps the design to code/test surfaces without
  implementation edits;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- the objective cannot be made mathematically coherent;
- exact or estimated normalizer handling is not implementable in TensorFlow;
- audit-holdout separation cannot be preserved;
- the first meaningful pilot would require GPU, long runtime, package install,
  network setup, or a project-direction decision not already reviewed;
- Claude and Codex do not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it freezes the
mathematical target before code, keeps implementation/training out of Phase 1,
requires explicit audit separation, and blocks proxy-loss promotion.
