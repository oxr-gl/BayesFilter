# P71 Phase 3 Subplan: Numeric Evaluator And Value-Finite Gate

metadata_date: 2026-06-16
status: PASS_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 3

## Phase Objective

Prove that the d18 route has a finite numeric evaluator/value path suitable for
later comparison, without claiming filtering accuracy.

## Entry Conditions Inherited From Previous Phase

- Phase 2 passed execution-only reproduction.
- Phase 2 artifacts identify the exact branch hashes and evaluator inputs.
- Phase 2 row adequacy is hard-minimum only:
  `diagnostic_only_below_preferred_rows`.  This permits finite evaluator
  diagnostics only and cannot be used as accuracy, rank, scaling, or HMC
  evidence.
- P60 high-rank comparator remains condition-vetoed; Phase 3 must not try to
  repair or reinterpret same-route rank/degree stability.

## Required Artifacts

- Phase 3 result note.
- Value/evaluator JSON or CSV artifact.
- Manifest tying evaluator inputs to Phase 2 branch identity.
- Refreshed Phase 4 rank/degree ladder subplan.

## Required Checks/Tests/Reviews

- Run focused local evaluator checks before any larger benchmark.
- Run existing target-registry/reference-oracle tests relevant to SIR rows if
  touched.
- `git diff --check` over new artifacts.
- Claude read-only review if evaluator wiring or benchmark row semantics
  change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the d18 source route provide finite numeric values on the reviewed evaluator path? |
| Baseline/comparator | Phase 2 execution-only manifest and existing P8-B6 numeric-pending row; row adequacy remains diagnostic-only below preferred rows. |
| Primary criterion | Finite value/evaluator output with unchanged source-route branch identity and preserved nonclaims. |
| Veto diagnostics | Nonfinite value, evaluator using a different target, branch hash drift, missing manifest path, or proxy metric used as accuracy. |
| Explanatory diagnostics | Runtime, memory, value components, branch hashes, evaluator shape checks. |
| Not concluded | No filtering accuracy, no rank convergence, no scaling, no HMC readiness. |
| Artifact | Phase 3 result note plus value/evaluator artifact. |

## Forbidden Claims/Actions

- Do not use a finite value as correctness evidence.
- Do not rank algorithms by value-only diagnostics.
- Do not change the target row after seeing output.
- Do not run or reinterpret same-route rank/degree ladder evidence.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if Phase 3 passes a finite-value gate with exact branch
identity preserved from Phase 2 and explicitly carries forward the Phase 2
row-adequacy/rank-ladder nonclaims.

## Stop Conditions

Stop if the evaluator is nonfinite, branch identity drifts, or the evaluator
cannot be tied to the d18 source-route artifact.
