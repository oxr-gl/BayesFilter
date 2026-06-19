# P73 Phase 6 Subplan: Result Decision And Root-Cause Handoff

metadata_date: 2026-06-17
status: DRAFT_PENDING_PHASE5_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md
diagnostic_json: docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Interpret the Phase 5 blocked diagnostic and decide the next bounded
root-cause direction.  Phase 6 is a decision and handoff phase only.  It must
not run new numerical diagnostics, validation, HMC, scaling, GPU, or rank
promotion.

## Entry Conditions Inherited From Phase 5

Phase 6 may begin only if:

- Phase 5 result exists;
- Phase 5 JSON exists and is not schema-only or smoke-only;
- local checks for the Phase 5 runner and tests passed;
- Claude returns `VERDICT: AGREE` for the Phase 5 implementation, diagnostic
  artifact, result, and this subplan;
- the run remains covered by the reviewed visible runbook.

## Required Artifacts

Phase 6 must produce:

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-result-2026-06-17.md`;
- either a stop handoff or a next root-cause subplan under `docs/plans`;
- updated execution and review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
rg -n "P73_PHASE5_DENSITY_AWARE_RENEWAL_BLOCKED|line_block|residual_rms_veto|residual_max_veto|NO_AUDIT_COEFFICIENT_SELECTION|P73_B_OPTIMIZER_BLOCKED" docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md
```

Review:

- Claude read-only review of the Phase 6 decision and handoff;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What does the Phase 5 P73-A blocked result justify doing next? |
| Exact baseline/comparator | Phase 5 JSON and result; Phase 2 design; P72 blocked diagnostic context. |
| Primary pass/fail criterion | Phase 6 must classify the block as implementation bug, tuning/capacity failure, cloud-geometry failure, missing objective failure, or unresolved; it must select a smallest next bounded artifact or stop. |
| Diagnostics that can veto | Treating P73-A as repaired despite residual/line vetoes; launching validation/HMC/scaling/rank promotion; changing thresholds; claiming adaptive Zhao--Cui failure; ignoring possible runner-bug explanations. |
| Explanatory only | Cross-entropy value, support warnings, condition spectra, runtime, and fit-cloud residual. |
| What will not be concluded | No repaired lower gate, no validation readiness, no HMC readiness, no scaling, no rank-policy change, no source-faithful parity. |
| Artifact preserving result | Phase 6 result and updated ledgers. |

## Forbidden Claims/Actions

- Do not run new experiments or diagnostics.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not change thresholds.
- Do not conclude the adaptive Zhao--Cui algorithm failed.
- Do not promote fit-cloud residual or cross-entropy to success evidence.
- Do not ignore that the Phase 5 runner was newly patched and therefore needs
  review before strong interpretation.

## Exact Next-Phase Handoff Conditions

If Phase 6 selects a next root-cause program, the handoff must include:

- the exact blocker being targeted;
- the smallest artifact that can discriminate runner bug versus scientific or
  numerical failure;
- required source/code/doc anchors;
- forbidden downstream claims;
- required local checks and Claude review.

If Phase 6 stops, the handoff must state the blocking condition and what human
direction is needed.

## Stop Conditions

Stop and write a blocker if:

- the Phase 5 JSON cannot be parsed or appears to be schema/smoke output;
- Claude finds a material Phase 5 runner bug that invalidates interpretation;
- the next action would require validation, HMC, scaling, GPU, rank promotion,
  threshold changes, or a project-direction decision not already covered by
  the runbook;
- Claude and Codex do not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it is interpretive
only, treats the Phase 5 block as a blocked diagnostic rather than a repaired
result, names runner-bug risk explicitly, and forbids downstream promotion
actions.
