# P05 Final Closeout And Non-Claim Audit Subplan

Status: `DRAFT_AFTER_P04`

## Phase Objective

Produce the final diagnostic-only closeout, reconcile phase evidence, separate
tuning/implementation/filter-scale outcomes, and preserve explicit non-claims.
The final result must explicitly report whether low-rank resampling executed in
each evidence-bearing active phase.

## Entry Conditions Inherited From Previous Phase

P04 must have written a pass, failure, or trusted-GPU blocker result.  All
previous phase artifacts remain read-only evidence.  P05 must not synthesize
with the positive-feature lane or make broad scalable-OT selection claims.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-result-2026-06-20.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-visible-execution-ledger-2026-06-20.md`
- Updated stop handoff if not passed:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-visible-stop-handoff-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Local artifact existence checks for all phase JSON/Markdown/result files that
  should exist for the observed exit path.
- Local route-execution evidence check over each completed evidence-bearing
  JSON artifact.
- Local non-claim check over final result.
- Claude read-only final review if the result contains a pass or material
  interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exactly did the low-rank filter-integration lane establish, fail to establish, or block on? |
| Baseline/comparator | Phase results P00-P04 and their stated evidence contracts. |
| Primary pass criterion | Final result accurately reflects phase statuses, artifacts, route-execution evidence, fixed-threshold hard vetoes, and non-claims without overstating evidence. |
| Veto diagnostics | Missing phase artifact, missing route-execution evidence for a completed active phase, unsupported claim, conflation of tuning failure with algorithm impossibility, conflation of component and filter-scale evidence, or public/default claim. |
| Explanatory diagnostics | Runtime, memory, selected setting, GPU visibility, and optional 100k result. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |
| Artifact | Final result and ledger. |

## Forbidden Claims And Actions

- Do not perform mid-lane synthesis with the positive-feature lane.
- Do not change code in P05 except documentation artifacts for closeout.
- Do not rank low-rank against any other method.
- Do not claim posterior correctness or production readiness.

## Exact Next-Phase Handoff Conditions

There is no next phase in this lane.  Final handoff must include the exit
status, key artifacts, hard vetoes, selected setting if any, and next justified
action.

## Stop Conditions

- Missing required evidence artifact.
- Unsupported claim that cannot be patched without changing the meaning of the
  result.
- Claude review nonconvergence after five rounds for the same final-result
  blocker.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the final result/close record.
3. Refresh stop handoff if blocked or failed.
4. Review final result for consistency, correctness, feasibility, artifact coverage, and boundary safety.
