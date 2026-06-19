# P69 Phase 1 Subplan: Holdout/Replay Diagnostic Design

metadata_date: 2026-06-15
status: DRAFT_PENDING_PHASE0_CLOSEOUT_AND_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design source-route-consistent holdout and replay diagnostics for the
fixed-TTSIRT fit path used by the P59/P67/P68 Zhao--Cui SIR fixed-HMC
adaptation.  The design must let later phases decide whether adjacent-ladder
rows are interpretable without changing thresholds after seeing new results.

This phase is design only.  It must not implement code or run new ladders.

## Entry Conditions Inherited From Phase 0

- P69 governance artifacts exist and have passed Phase 0 review.
- The target lane is fixed-HMC adaptation, not adaptive Zhao--Cui parity.
- P68 is the immediate technical predecessor: condition and fit residuals are
  exposed, but holdout is unavailable for every row and the degree ladder still
  exceeds thresholds.
- The next diagnostic must preserve source-route invariants, fixed branch
  identity, and clean-room boundaries.

## Required Artifacts

- Phase 1 result/close record:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-result-2026-06-15.md`.
- A design contract for holdout/replay diagnostics, including:
  - source-route-consistent holdout point construction;
  - replay identity fields;
  - row status taxonomy;
  - pass/block/inconclusive semantics;
  - exact fields to add to P59/P67/P68 manifests in Phase 2;
  - tests required before any rerun.
- Refreshed Phase 2 implementation subplan.

## Required Checks, Tests, And Reviews

- Read current anchors:
  - P68 result;
  - P67 runner path;
  - `bayesfilter/highdim/source_route.py` fit-quality paths;
  - `bayesfilter/highdim/fitting.py` holdout support.
- Local text check that the Phase 1 design:
  - does not change thresholds;
  - does not claim validation;
  - does not classify holdout residual as correctness by itself;
  - preserves `fixed_hmc_adaptation`.
- Claude read-only review of the Phase 1 design result and Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What holdout/replay diagnostics should be added so adjacent-ladder rows can be interpreted without silently changing the fixed branch or thresholds? |
| Baseline/comparator | P68 row diagnostics: fit residuals and condition numbers exposed; holdout unavailable; degree ladder threshold failures remain. |
| Primary pass criterion | A reviewed design specifies holdout/replay construction, manifest fields, status taxonomy, checks, and Phase 2 implementation scope without overclaiming validation. |
| Veto diagnostics | Thresholds changed after seeing P68; holdout residual promoted to correctness; holdout points change the fitted branch without recording a new branch identity; adaptive source behavior claimed; source-route invariants weakened. |
| Explanatory diagnostics | Candidate holdout residuals, replay residuals, branch hashes, point hashes, condition numbers, fit residuals, degree/rank deltas. |
| Not concluded | No implementation, no ladder rerun, no convergence, no d18 correctness, no HMC readiness. |
| Artifact preserving result | Phase 1 result/close record. |

## Forbidden Claims And Actions

- Do not implement holdout/replay in Phase 1.
- Do not rerun P67/P68 ladders in Phase 1.
- Do not change thresholds or row definitions after seeing P68.
- Do not use holdout residual alone as a promotion criterion.
- Do not call the design source-faithful adaptive Zhao--Cui.
- Do not require GPU or HMC commands.

## Exact Next-Phase Handoff Conditions

Phase 1 may hand off to Phase 2 only if:

- the design contract is written and reviewed;
- required manifest fields are explicit;
- required tests are explicit;
- fixed-branch identity and source-route invariants are preserved;
- Claude returns `VERDICT: AGREE`;
- Phase 2 implementation subplan is drafted or refreshed.

## Stop Conditions

Stop and write a blocker result if:

- a source-route-consistent holdout/replay design cannot be stated without
  changing the branch being fitted;
- the design cannot distinguish fitted-branch data from diagnostic-only replay
  data;
- source anchors or current code anchors are insufficient to define Phase 2;
- Claude and Codex do not converge after five review rounds;
- implementation is needed to answer the design question.

## Planned Local Commands

Read-only checks only:

```bash
rg -n "holdout|fit_quality|FixedTTFitSampleBatch|p67|adjacent" bayesfilter/highdim scripts tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p6*.md
rg -n "threshold|correctness|fixed_hmc_adaptation|source-faithful|HMC readiness" docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-*.md
```
