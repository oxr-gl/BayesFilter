# P73 Phase 2 Subplan: Density-Aware Renewal Design Contract

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE2_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Write the mathematical design contract for the P73 fixed-variant repair before
implementation.  The phase must define the renewal sets, density-aware
objective candidates, audit split, gates, thresholds, provenance, and stop
rules in mathematical terms, using the Phase 1 classification boundary.

This phase is a document/math-design phase only.  It must not edit
implementation code or run numerical diagnostics.

## Entry Conditions Inherited From Phase 1

Phase 2 may begin only if:

- Phase 1 result exists and records the per-operation source-anchor ledger;
- every P73 operation has classification, inspected sources, exact anchors or
  `NO_ANCHOR_FOUND_IN_INSPECTED_SCOPE`, bounded conclusion, and unresolved gap;
- Phase 1 result preserves the P72 Phase 5 blocked diagnostic as comparator;
- Phase 1 result does not claim P73 success, validation, HMC readiness,
  scaling, rank promotion, or adaptive Zhao--Cui parity;
- Claude returns `VERDICT: AGREE` for the Phase 1 result and this Phase 2
  subplan.

## Required Artifacts

Phase 2 must produce:

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md`;
- mathematical definitions for:
  - fit, guard, enrichment, audit, line, and fresh-renewal sets;
  - density object \(q_\theta(z)\);
  - square-root regression term;
  - optional empirical cross-entropy / forward-KL term;
  - normalizer and defensive-mass terms;
  - condition/effective-rank diagnostics;
  - provenance predicates that prove audit exclusion;
  - pass/block semantics;
- a decision on whether the density-aware objective is included in Phase 4,
  deferred, or quarantined pending a separate derivation/literature audit;
- refreshed Phase 3 implementation-surface subplan;
- updated execution and review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md
rg -n "NO_ANCHOR_FOUND_IN_INSPECTED_SCOPE|extension_or_invention|fixed_hmc_adaptation|source_faithful|P72 Phase 5|NeuTra|cross-entropy|forward-KL" docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md
rg -n "F_r|G_r|A_r|L_r|q_\\\\theta|Z_\\\\theta|NO_AUDIT_COEFFICIENT_SELECTION|Never certify|condition|normalizer|provenance|lambda_ce|extension_or_invention|DENSITY_AWARE_OBJECTIVE_STATUS|included|deferred|quarantined" docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md
```

Review:

- Claude read-only review of the Phase 2 result and Phase 3 subplan;
- MathDevMCP may be used for bounded equality/proof-obligation checks if the
  Phase 2 result introduces labeled algebraic identities;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What exact mathematical contract should a P73 density-aware renewed-support fixed fit implement and diagnose? |
| Exact baseline/comparator | P72 real Phase 5 blocked diagnostic and Phase 1 classification ledger. |
| Primary pass/fail criterion | The result freezes all design choices needed for implementation: sets, objective, weights, thresholds, audit exclusion, provenance, gates, and stop rules, with each design component classified by Phase 1. |
| Veto diagnostics | Missing set definitions, audit points allowed into same-round fitting, certifying on newly added points, unanchored source-faithfulness, NeuTra promoted to proof, thresholds left vague, density-aware objective included without derivation or quarantine decision, implementation or diagnostic launch. |
| Explanatory only | Candidate objective variants, literature notes, optional future stable-LS or NeuTra audits, runtime estimates. |
| What will not be concluded | No implementation correctness, no diagnostic pass, no P73 repair, no validation/HMC/scaling claim, no rank/degree promotion, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 2 result, Phase 3 subplan, execution/review ledgers. |

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run Python diagnostics, validation, HMC, scaling, GPU, or
  rank-promotion experiments.
- Do not change P72 comparator facts.
- Do not call staged renewal, cross-entropy/forward-KL fitting, line/support
  enrichment, audit exclusion, or P73 gate thresholds source-faithful without
  exact paper and author-source anchors.
- Do not allow same-round audit points into coefficient selection.
- Do not certify on points just added to training.
- Do not make the density-aware objective a default policy change.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Phase 2 result exists;
- Phase 2 result freezes all mathematical definitions and thresholds needed by
  Phase 3;
- density-aware objective status is explicit: included, deferred, or
  quarantined;
- every included component is labeled using the Phase 1 classification ledger;
- Phase 3 subplan exists with objective, entry conditions, artifacts, checks,
  evidence contract, forbidden actions, handoff conditions, and stop
  conditions;
- local checks pass;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- the density-aware objective cannot be stated without an unreviewed
  mathematical or project-direction decision;
- exact audit exclusion/provenance cannot be specified;
- threshold choices would be tuned from already-seen P73 diagnostic output;
- the design would require implementation or diagnostic execution to finish
  Phase 2;
- Claude and Codex do not converge after five rounds for the same blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it freezes a
mathematical contract before implementation, keeps P72 as comparator, treats
training loss as explanatory only, requires an explicit quarantine decision for
the density-aware objective, and forbids implementation/diagnostic launch.
