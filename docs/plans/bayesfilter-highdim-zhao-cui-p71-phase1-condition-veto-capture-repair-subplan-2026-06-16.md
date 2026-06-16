# P71 Phase 1 Subplan: Condition-Veto Capture And Repair Gate

metadata_date: 2026-06-16
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 1

## Phase Objective

Capture and, if fixable, repair the P70 Phase 6 first-row
`CONDITION_NUMBER_VETO` so later d18 validation phases can inspect failed-fit
diagnostics instead of losing them to an immediate exception.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result records the exact blocker and source-governance anchors.
- No full d18 validation command has run under P71.
- The P70 Phase 6 result remains the active blocker.

## Required Artifacts

- Phase 1 result note.
- Patch, if needed, limited to diagnostic-safe fit-status capture or
  failure-payload preservation.
- Focused unit tests proving a condition-veto fit records per-core/design
  diagnostics before blocking.
- Refreshed Phase 2 subplan if the repair changes the admissible command.

## Required Checks/Tests/Reviews

- CPU-only compile/test checks for touched highdim files.
- Focused pytest for the condition-veto capture behavior.
- `git diff --check` over touched files.
- Claude read-only review of the patch and Phase 2 handoff if implementation
  changes are made.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the condition-number-veto path preserve actionable diagnostics without weakening the veto? |
| Baseline/comparator | P70 Phase 6 failed first row: `rank_candidate_1_2_fit36`, degree 1, rank 2, fit count 36. |
| Primary criterion | A condition-veto fit produces a blocked result or failure payload containing fit status, per-core condition records when available, design shape/threshold metadata, and unchanged source-route nonclaims. |
| Veto diagnostics | Raising before preserving diagnostics, changing thresholds after seeing failures, accepting a vetoed fit as OK, or changing rank/degree/row semantics. |
| Explanatory diagnostics | Condition numbers, warning/veto thresholds, row adequacy, branch hashes, channel activity, and fitted status. |
| Not concluded | No d18 validation, no rank-channel repair success, no accuracy, no HMC readiness. |
| Artifact | Phase 1 result note plus focused test output. |

## Forbidden Claims/Actions

- Do not rerun the full four-row P70 diagnostic in this phase.
- Do not lower condition-number thresholds to make the row pass.
- Do not change source-route target semantics.
- Do not launch GPU/HMC commands.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if Phase 1 either:

- passes focused tests showing diagnostic-safe condition-veto capture while
  preserving the veto; or
- writes a blocker stating that P71 cannot continue until a human approves a
  broader fitting-design repair.

## Stop Conditions

Stop if the repair would require changing thresholds, model semantics, source
route, or pass/fail criteria after seeing outputs.
