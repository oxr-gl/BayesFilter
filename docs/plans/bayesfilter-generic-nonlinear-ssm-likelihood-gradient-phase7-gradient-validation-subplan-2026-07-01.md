# Phase 7 Subplan: Gradient Validation And Scoped Score Admission

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Validate same-branch analytical gradients only after the value gate passes, and
admit only the scoped score authority justified by the reviewed evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 6 value validation is reviewed closed for any lane being considered in
  this phase.
- Reviewed lane semantics and derivative obligations are frozen.
- No HMC/top-level/production promotion is authorized yet.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-result-2026-07-01.md`
- refreshed Phase 8 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase8-final-decision-subplan-2026-07-01.md`
- score-admission manifests/tests named by the executable refresh.

## Required Checks/Tests/Reviews

This phase requires a reviewed executable refresh before any runtime.
That refresh must define:

- exact same-branch FD ladders,
- exact branch-signature checks,
- exact score API admission checks,
- exact CPU/GPU policy,
- exact nonclaims to preserve.

Required read-only Claude reviews:

- Phase 7 result,
- refreshed Phase 8 subplan.

## Skeptical Plan Audit

| Risk Checked | Phase 7 Control |
| --- | --- |
| Wrong baseline | Gradient validation is allowed only on lanes whose value gate already passed. |
| Proxy metric promoted | FD agreement is necessary but not sufficient without same-branch validity and declared-scalar alignment. |
| Missing stop condition | Branch mismatch or wrong-scalar tieout blocks admission immediately. |
| Unfair comparison | Score routes are compared only to derivatives of the same declared scalar. |
| Hidden assumption | A model-provided score, autodiff fallback, and analytically admitted score must be kept in separate categories. |
| Stale context | Admission uses only reviewed Phase 6-passing lanes and reviewed derivative contracts. |
| Environment mismatch | Runtime commands require reviewed CPU/GPU policy. |
| Artifact-answer mismatch | Phase 7 must yield only scoped score admission, not HMC or top-level production admission. |

Audit status: executable only after a refreshed reviewed gradient-validation subplan is written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the candidate analytical-gradient lanes differentiate the same declared scalar on the same branch well enough to admit scoped score authority? |
| Baseline/comparator | reviewed value-passing lanes, same-branch FD ladders, and branch-signature contracts. |
| Primary criterion | Phase 7 passes only when branch-valid FD ladders and same-scalar evidence support the claimed scoped score authority for the lane. |
| Veto diagnostics | same-branch mismatch, wrong-scalar FD tieout, fallback/autodiff route overpromoted as analytical, or HMC/top-level scope promoted without reviewed authority. |
| Explanatory diagnostics | FD error tables, branch signatures, derivative method telemetry, and runtime summaries. |
| Not concluded | No HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | reviewed gradient-validation result and refreshed Phase 8 subplan. |

## Forbidden Claims/Actions

- Do not claim HMC readiness or top-level API promotion from this phase.
- Do not treat autodiff fallback as analytically admitted unless the reviewed
  contract explicitly authorizes that category.
- Do not run runtime commands not named by the reviewed executable refresh.

## Exact Next-Phase Handoff Conditions

Phase 8 may start only if:

- the executable Phase 7 refresh is reviewed `AGREE` before runtime;
- the Phase 7 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 8 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records which score lanes are admitted, which remain
  fallback-only, and which remain blocked.

## Stop Conditions

- A lane fails same-branch FD validation.
- A lane's score route is fallback-only but is being promoted as analytical.
- Focused runtime checks fail and cannot be repaired within reviewed scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require wider runtime authority than the reviewed executable
  refresh provides.

## End-Of-Phase Requirements

1. Write an executable refresh before runtime.
2. Run the reviewed focused gradient checks.
3. Write the Phase 7 result.
4. Refresh the Phase 8 subplan.
5. Review the Phase 7 result and refreshed Phase 8 subplan.
6. Update the execution ledger and Claude review ledger.
