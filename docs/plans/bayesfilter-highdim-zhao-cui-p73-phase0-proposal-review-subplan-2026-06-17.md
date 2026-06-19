# P73 Phase 0 Subplan: Proposal Review And Governance Reset

metadata_date: 2026-06-17
status: COMPLETED_CLAUDE_AGREE
proposal: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md
predecessor_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Review the P73 density-aware renewed-support proposal and decide whether it is
a coherent planning basis for a new master program.  This phase produces no
implementation code and runs no numerical diagnostic beyond local artifact
checks.

## Entry Conditions Inherited From P72

Phase 0 may begin only if:

- P72 Phase 5 result exists and records a blocked real diagnostic;
- P72 JSON exists and is not schema-only;
- Claude agreed the P72 closeout is blocked, not promoted;
- the P73 proposal exists under `docs/plans`;
- no downstream validation, HMC, scaling, or rank-promotion action is launched.

## Required Artifacts

Phase 0 must produce:

- reviewed proposal:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md`;
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-result-2026-06-17.md`;
- P73 Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md`;
- P73 execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md`;
- draft P73 master program, runbook, and Phase 1 subplan only if the proposal
  converges.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md
test -s docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json >/tmp/p73_phase0_p72_json_check.json
rg -n "P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_BLOCKED|P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_BLOCKED_CLAUDE_AGREE" docs/plans/bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
rg -n "schema_only_sentinel_present.*true|smoke_only_not_phase5_evidence.*true|exception_type|p72_phase5_row_exception_fail_closed" docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json
rg -n "NORMALIZER_FLOOR_EXCEEDED|Never certify|extension_or_invention|forward-KL|cross-entropy|rank_candidate_1_2_fit36|rank_stronger_1_3_fit36" docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-proposal-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-subplan-2026-06-17.md
```

The sentinel `rg` command is expected to return exit code `1` with no matches;
that is pass evidence that the predecessor JSON is not schema-only,
smoke-only, or an old top-level exception row.

Claude review:

- read-only review of a bounded proposal summary and proposal path;
- loop to convergence or max 5 rounds for the same blocker;
- if Claude stalls, run a tiny probe; if probe responds, redesign the prompt.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is the P73 proposal a coherent, bounded next repair direction for the P72 residual/line/condition/normalizer failures? |
| Exact baseline/comparator | P72 real Phase 5 blocked diagnostic.  The local NeuTra-style training analogy is explanatory context only, not a baseline/comparator. |
| Primary pass/fail criterion | The proposal must explain the P72 failures, classify new operations honestly, forbid validation/promotion claims, and define a testable next master program direction. |
| Veto diagnostics | Source-faithfulness overclaim, treating NeuTra analogy as proof, skipping audit separation, certifying on points added to training, rank-first repair, downstream validation launch, or threshold changes after P72 outputs. |
| Explanatory only | Residual magnitudes, condition numbers, normalizer exception, and NeuTra analogy. |
| What will not be concluded | No P72 repair, no P73 implementation, no lower-gate pass, no d18 validation, no HMC readiness, no scaling, no rank promotion. |
| Artifact preserving result | Phase 0 result, proposal, review ledger, execution ledger. |

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run P72/P73 diagnostics.
- Do not launch downstream validation, HMC, scaling, GPU, or rank-promotion
  experiments.
- Do not claim staged sample renewal or KL/cross-entropy fitting is
  source-faithful Zhao--Cui.
- Do not treat the NeuTra analogy as literature proof without a later
  technical audit.
- Do not certify on points just added to training.

## Exact Next-Phase Handoff Conditions

Phase 1 planning may begin only if:

- local checks pass;
- Claude returns `VERDICT: AGREE` for the proposal after any repairs;
- Phase 0 result records the review trail and nonclaims;
- P73 master program, visible runbook, and Phase 1 subplan are drafted or
  explicitly scheduled as the next planning artifacts.

## Stop Conditions

Stop and write a blocker if:

- Claude identifies a non-fixable flaw in the proposal;
- the proposal would require source-faithful claims without anchors;
- the next action would require implementation before reviewed design;
- the user redirects the lane;
- Claude and Codex do not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This Phase 0 subplan passes the initial skeptical audit because it consumes
the actual blocked P72 diagnostic, forbids implementation and validation, and
requires the proposal to remain a planning hypothesis rather than a proof or
promotion claim.
