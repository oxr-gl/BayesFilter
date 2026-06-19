# P75 Phase 5 Subplan: Result Decision And Collapse Diagnosis

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE5
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Decide why the Phase 4 target smoke collapsed to the defensive floor and
produce the next bounded repair or diagnostic plan.  This phase is a decision
and diagnosis phase, not a larger training run.

## Entry Conditions Inherited From Phase 4

Phase 5 may begin only if:

- the Phase 4 target-smoke JSON exists;
- the Phase 4 result exists;
- the Phase 4 result records that the larger degree 2/rank 4 pilot was not
  launched;
- local result-file checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 4 result and this subplan, or
  fixable issues have been patched and re-reviewed.

## Required Artifacts

Phase 5 must produce:

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-17.md`;
- if needed, a Phase 6 subplan for one focused repair, not a broad sweep;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json >/tmp/p75-target-smoke-jsoncheck.txt
rg -n "audit_line_veto|rho_min|rho_max|normalizer|gradient_norm|completed_batches|P75_TARGET_PILOT_COMPLETED" docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-result-2026-06-17.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-subplan-2026-06-17.md
```

Review:

- Claude read-only review of the Phase 4 result and this Phase 5 subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What is the most likely cause of the Phase 4 defensive-floor collapse, and what is the smallest justified next action? |
| Exact baseline/comparator | Phase 4 tiny target smoke JSON; Phase 1 objective design; P73 blocked diagnostic as historical context only. |
| Primary pass/fail criterion | The result must separate execution success from diagnostic failure and identify whether the next action is objective scaling, initialization, capacity/sample budget, or target-generation repair. |
| Diagnostics that can veto | Treating the blocked audit as success; launching the larger pilot without a reviewed repair; changing thresholds after seeing outputs; claiming lower-gate repair, validation, HMC, or source-faithfulness. |
| Explanatory only | Loss cancellation, tiny gradient norm, line residual magnitude, holdout/replay relative residuals, runtime. |
| What will not be concluded | No final algorithmic success/failure, no production readiness, no rank/sample policy, no Zhao--Cui source-faithful parity. |
| Artifact preserving result | Phase 5 result and updated ledgers. |

## Forbidden Claims/Actions

- Do not run the degree 2/rank 4/batch 1024/up-to-500 pilot in Phase 5.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not claim the Phase 4 smoke repaired the lower gate.
- Do not claim source-faithful Zhao--Cui.
- Do not use audit samples for training or hyperparameter selection.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- Phase 5 result exists;
- the root-cause hypothesis is stated with evidence and uncertainty;
- exactly one next repair/diagnostic action is selected;
- a Phase 6 subplan exists with bounded commands, artifacts, and stop
  conditions;
- Claude review agrees or the unresolved blocker is escalated to the user.

## Stop Conditions

Stop for human direction if:

- the Phase 4 JSON is missing or malformed;
- the result cannot distinguish execution mechanics from scientific evidence;
- the next action would require a GPU, long run, package install, source-route
  default change, or implementation-code edit outside a reviewed Phase 6
  subplan;
- Claude identifies a material blocker that cannot be repaired within this
  phase.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it treats the Phase 4
audit veto as blocking, preserves the distinction between a runnable command
surface and a successful method, and forbids the larger pilot until the
defensive-floor collapse has a reviewed next action.
