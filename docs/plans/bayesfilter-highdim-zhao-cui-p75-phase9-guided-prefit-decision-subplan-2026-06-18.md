# P75 Phase 9 Subplan: Guided Prefit Decision And Next Handoff

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE9
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Interpret the Phase 8 source-guided prefit result and decide the next bounded
action.  The decision must separate mechanism success from lower-gate repair
and must not launch the large pilot.

## Entry Conditions Inherited From Phase 8

Phase 9 may begin only if:

- Phase 8 result exists;
- Phase 8 JSON exists and is valid;
- local checks in the Phase 8 result passed;
- the result preserves same-draw, train/audit split, and nonclaim boundaries;
- Claude returns `VERDICT: AGREE` for the Phase 8 result and this subplan, or
  fixable issues have been patched and re-reviewed.

## Required Artifacts

Phase 9 must produce:

- Phase 9 decision result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-result-2026-06-18.md`;
- either a stop handoff or a next-phase subplan for a bounded capacity/sample
  diagnostic;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json
rg -n "source_guided_prefit|audit_line_veto|lower-gate|validation|larger-pilot|degree 2/rank 4" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-subplan-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-subplan-2026-06-18.md
```

Review:

- Claude read-only review of Phase 8 result and this Phase 9 subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What should P75 do after source-guided prefit passes a tiny mechanism test but audit-line still blocks? |
| Exact baseline/comparator | Phase 8 same-draw random, calibrated-constant, and source-guided-prefit arms. |
| Primary criterion | Produce a decision that correctly classifies the Phase 8 result and selects either a bounded next diagnostic or a stop handoff. |
| Diagnostics that can veto | Treating the tiny mechanism pass as lower-gate repair; ignoring audit-line block; launching the large pilot; changing metrics after seeing outputs; claiming validation/HMC/scaling/source-faithfulness. |
| Explanatory only | Holdout/replay residual magnitudes, line residual magnitudes, prefit loss, rho range, gradient norm, runtime. |
| What will not be concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithfulness, or final rank/sample policy. |
| Artifact preserving result | Phase 9 decision result, next subplan or stop handoff, ledgers, Claude review. |

## Forbidden Claims/Actions

- Do not run additional training diagnostics in Phase 9.
- Do not run the degree 2/rank 4/batch 1024/up-to-500 pilot.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not claim lower-gate repair from the Phase 8 mechanism pass.
- Do not use audit data for model selection or hyperparameter tuning.

## Exact Next-Phase Handoff Conditions

A next phase may begin only if:

- Phase 9 result exists;
- the next action is bounded and has its own evidence contract;
- the next action does not cross human-required boundaries;
- the next action is a bounded diagnostic or a stop handoff, not the
  degree-2/rank-4/batch-1024/500-batch pilot;
- any recommendation to run the degree-2/rank-4/batch-1024/500-batch pilot is
  recorded only as a possible future human decision and cannot be authorized
  by Phase 9 documentation review alone;
- Claude review agrees, or unresolved blockers are escalated to the user.

## Stop Conditions

Stop for human direction if:

- Phase 8 result is found to have provenance leakage or same-draw mismatch;
- the only sensible next action would be the large pilot;
- the user has not separately approved a new reviewed plan for the large
  pilot;
- deciding the next action requires a scientific claim not supported by Phase
  8;
- Claude identifies an unrepaired material blocker.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it does not promote
the tiny mechanism pass into a lower-gate claim, names the audit-line block as
a veto for repair claims, and forbids any additional run until a new bounded
plan is written and reviewed.
