# P73 Phase 1 Subplan: Source, Literature, And Objective Boundary Audit

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_USER_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Classify the P73 proposal operations and identify what source/literature
support exists before mathematical design.  This phase is a boundary audit,
not an implementation phase.

## Entry Conditions Inherited From Phase 0

Phase 1 may begin only if:

- Phase 0 proposal result exists and records Claude `VERDICT: AGREE`;
- P73 proposal status is reviewed;
- P73 master program and visible runbook exist and have passed review;
- user approves launching the visible runbook beyond planning;
- no implementation code has been changed for P73.

## Required Artifacts

Phase 1 must produce:

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md`;
- a per-operation source-anchor ledger for:
  - staged sample renewal;
  - empirical cross-entropy / forward-KL objective terms;
  - line/support enrichment;
  - strict audit exclusion;
  - normalizer and conditioning gates;
  - any NeuTra-inspired claim;
- each ledger row must state:
  - classification: `source_faithful`, `fixed_hmc_adaptation`, or
    `extension_or_invention`;
  - exact inspected source or literature artifact;
  - exact source file/line, paper section/equation, or local document anchor
    when an anchor exists;
  - `NO_ANCHOR_FOUND_IN_INSPECTED_SCOPE` when no such anchor exists;
  - bounded conclusion permitted by the inspected evidence;
  - unresolved gap for Phase 2 or later;
- refreshed Phase 2 design subplan;
- updated execution and review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-result-2026-06-17.md
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md
rg -n "extension_or_invention|fixed_hmc_adaptation|source_faithful|NeuTra|cross-entropy|forward-KL|Never certify" docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md
rg -n "NO_ANCHOR_FOUND_IN_INSPECTED_SCOPE|source file/line|paper section/equation|bounded conclusion|unresolved gap" docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md
```

Claude review:

- read-only review of Phase 1 result and Phase 2 subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Which P73 operations are fixed-HMC adaptations, which are source-faithful, and which are extensions/inventions requiring separate evidence? |
| Exact baseline/comparator | P72 Phase 5 blocked diagnostic and P73 proposal. |
| Primary pass/fail criterion | Every proposed P73 operation has a ledger row with classification, exact inspected sources, exact anchors or `NO_ANCHOR_FOUND_IN_INSPECTED_SCOPE`, bounded conclusion, and unresolved gap.  Any literature/NeuTra support is bounded to what was actually inspected. |
| Veto diagnostics | Source-faithfulness overclaim, NeuTra analogy promoted to proof, missing classification, implementation launch, or downstream validation launch. |
| Explanatory only | Local NeuTra docs, prior P72 ledgers, and source-route context. |
| What will not be concluded | No mathematical design approval, no implementation approval, no diagnostic pass, no validation/HMC/scaling claim. |
| Artifact preserving result | Phase 1 result, classification ledger, Phase 2 subplan, ledgers. |

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run diagnostics, validation, HMC, scaling, GPU, or rank-promotion
  experiments.
- Do not call staged renewal or density-aware objective source-faithful unless
  exact paper and author-source anchors are inspected and cited.
- Do not use local NeuTra experience as proof that P73 will work.
- Do not authorize Phase 2 until classifications and boundary conditions are
  explicit.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 result exists;
- every proposed operation has a source-anchor ledger row with classification,
  inspected sources, exact anchors or `NO_ANCHOR_FOUND_IN_INSPECTED_SCOPE`,
  bounded conclusion, and unresolved gap;
- source/literature support and gaps are listed in that auditable form;
- Phase 2 subplan exists with objective, entry conditions, artifacts, checks,
  evidence contract, forbidden actions, handoff conditions, and stop
  conditions;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- classification cannot be made without more source/literature inspection;
- a proposed operation requires a project-direction decision;
- Claude and Codex do not converge after five rounds for the same blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it does not implement
or diagnose anything; it only constrains claims and evidence before design.
