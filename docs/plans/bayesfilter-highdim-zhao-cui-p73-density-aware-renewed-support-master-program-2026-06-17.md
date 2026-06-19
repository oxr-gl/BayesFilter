# P73 Master Program: Density-Aware Renewed-Support Fixed Fit

metadata_date: 2026-06-17
status: P73_PHASE6_PASSED_CLAUDE_AGREE_COMPLETE
executor: Codex in the current conversation
reviewer: Claude Opus max effort, read-only and bounded
proposal: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md
predecessor_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md

## Objective

Design, implement, and bounded-diagnose an opt-in density-aware
renewed-support repair for the fixed Zhao--Cui variant after P72 blocked.  The
program targets the P72 residual/line, condition, and normalizer failures while
preserving source-governance and validation boundaries.

P73 is not a source-faithful adaptive Zhao--Cui reproduction lane.  Staged
sample renewal, empirical cross-entropy or forward-KL terms, and line/support
enrichment are `extension_or_invention` unless a later phase supplies paper and
author-source anchors.  They may be useful fixed-variant repairs, but they do
not close a source-faithfulness gap.

## Starting Evidence

The governing baseline is the P72 real Phase 5 blocked diagnostic:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md`;
- `docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json`.

Key P72 facts:

- `rank_candidate_1_2_fit36` is admissible but inaccurate/off-support
  unstable.  It blocks on residual and line gates at step 1 and on residual,
  line, and condition gates at step 2.
- `rank_stronger_1_3_fit36` is inadmissible at step 1.  It blocks on
  residual, line, condition, and `NORMALIZER_FLOOR_EXCEEDED`; step 2 is
  skipped because no retained object exists.
- Claude agreed the P72 closeout is a blocked diagnostic and that Phase 6/P73
  must remain root-cause-only until a lower gate actually passes.

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can staged support renewal plus density-aware fitting reduce the P72 finite-support residual/line/condition/normalizer blockers without overclaiming source-faithfulness or validation? |
| Exact baseline/comparator | P72 real Phase 5 blocked diagnostic. |
| Primary program pass criterion | Each phase produces its required artifact and exact next-phase handoff, or writes a blocker.  A final P73 diagnostic may pass only if fresh-audit residual, line, support, normalizer, condition/effective-rank, rank-activity, and provenance gates pass without using same-round audit points for coefficient selection. |
| Veto diagnostics | Treating NeuTra analogy as proof, certifying on points added to training, audit points entering coefficient selection, threshold changes after outputs, source-faithfulness overclaim, fit/training loss promoted to success, downstream validation/HMC/scaling launch before lower-gate pass. |
| Explanatory diagnostics | Fit/guard/audit residuals, line-channel values, normalizer terms, singular spectra, condition numbers, effective ranks, enrichment provenance, density-aware loss components, runtime. |
| Not concluded | No P72 repair, no P73 success, no d18 validation, no HMC readiness, no scaling, no rank/degree promotion, no adaptive Zhao--Cui parity. |
| Artifacts | Proposal, master program, runbook, execution ledger, review ledger, phase subplans/results, implementation diffs if launched, bounded diagnostic JSONs, stop handoff. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Proposal review and governance reset | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-result-2026-06-17.md` |
| 1 | Source, literature, and objective-boundary audit | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md` |
| 2 | Mathematical design contract | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md` |
| 3 | Implementation surface audit and focused test plan | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-result-2026-06-17.md` |
| 4 | Opt-in implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md` |
| 5 | Bounded renewal diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md` |
| 6 | Result decision and next-root-cause handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-result-2026-06-17.md` |

Only Phase 1 subplan is drafted at master-program creation.  Every later
phase subplan must be drafted or refreshed at the close of the immediately
previous phase.

## Dependency Matrix

| Phase | Must consume | Must produce for next phase |
| --- | --- | --- |
| 0 | P72 blocked result, proposal, Claude proposal review | Proposal closeout and reviewed Phase 1 planning entry |
| 1 | Phase 0 result, P72/P73 proposal, Zhao--Cui source-governance rules, local NeuTra docs as context | Classification ledger, literature/objective-boundary ledger, reviewed Phase 2 design subplan |
| 2 | Phase 1 classification and boundary ledger | Exact mathematical design for renewal sets, density-aware objective, audit split, gates, thresholds, and stop rules; reviewed Phase 3 subplan |
| 3 | Phase 2 design contract and current code | Implementation surface map, focused tests, risk controls, reviewed Phase 4 implementation subplan |
| 4 | Phase 3 surface map and tests | Opt-in code/tests implementing only reviewed surfaces, local checks, reviewed Phase 5 diagnostic subplan |
| 5 | Phase 4 implementation and evidence contract | Bounded diagnostic JSON, serious-run manifest, result note, explicit pass/block decision, reviewed Phase 6 subplan |
| 6 | Phase 5 result and Claude review | Final decision, stop handoff or next root-cause plan |

A phase may repair the blocker handed to it.  A phase must not require the
repair to have already succeeded before it begins.

## Phase Boundaries

### Phase 0: Proposal review and governance reset

Already completed.  Claude converged to `VERDICT: AGREE` after R1/R2 repairs.
No implementation or numerical diagnostic was launched.

### Phase 1: Source, literature, and objective-boundary audit

Classify staged renewal, density-aware objective terms, audit split,
line/support enrichment, and NeuTra analogy support.  Inspect only bounded
local sources or summaries unless a reviewed plan authorizes broader
literature work.  This phase may say an idea is a candidate direction; it must
not claim theorem-level support without checked technical anchors.

### Phase 2: Mathematical design contract

Define the finite training, guard, audit, renewal, enrichment, and line sets;
the density-aware objective; objective weights or gates; normalizer and
condition diagnostics; threshold provenance; and pass/block semantics.  This
phase freezes the diagnostic criteria before implementation.

### Phase 3: Implementation surface audit and focused test plan

Map the Phase 2 contract to current TensorFlow/TensorFlow Probability
implementation surfaces.  Identify exact functions and tests.  No code edits
except planning/result artifacts.

### Phase 4: Opt-in implementation and unit tests

Implement only reviewed surfaces, opt-in by default.  New BayesFilter-owned
algorithmic code must use TensorFlow/TensorFlow Probability.  NumPy is allowed
only for fixtures, independent references, closed-form checks, serialization,
or explicitly reviewed exceptions.

### Phase 5: Bounded renewal diagnostic

Run a bounded P72-style diagnostic comparing P73 against the P72 blocked
baseline under predeclared gates.  Certification must use fresh audit points
not used for coefficient selection.  Fit/training loss is explanatory only.

### Phase 6: Result decision and next-root-cause handoff

Review whether P73 actually repairs the lower gate.  If any veto fails,
downstream validation remains blocked and the next action is repair or human
direction.  If all gates pass, this phase may authorize drafting a separate
validation-ladder plan; it does not itself run that ladder.

## Global Forbidden Actions

- Do not launch a detached process, nested agent, background phase runner, or
  copied-workspace execution.
- Do not execute implementation or long diagnostics before the corresponding
  reviewed subplan and runbook gate authorize them.
- Do not run downstream validation, d18 validation, HMC, scaling, or rank
  promotion during P73.
- Do not change thresholds after seeing outputs.
- Do not use audit clouds or audit-line probes for same-round coefficient
  selection.
- Do not certify on points just added to training.
- Do not call staged renewal or density-aware objective terms source-faithful
  without paper and author-source anchors.
- Do not treat the NeuTra analogy as proof or as the baseline comparator.

## Skeptical Plan Audit

This master program passes the initial skeptical audit because it uses the
actual P72 blocked diagnostic as baseline, preserves source-governance
classification, separates NeuTra motivation from proof, gates implementation
behind mathematical design and user approval, and forbids downstream
validation/promotion until a lower gate passes.  Routine phase transitions
continue under the reviewed visible runbook unless a human-required boundary
appears.
