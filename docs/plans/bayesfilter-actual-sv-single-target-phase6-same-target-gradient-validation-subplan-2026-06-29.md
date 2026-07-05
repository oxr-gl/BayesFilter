# Phase 6 Subplan: Same-Target Gradient Validation

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Validate gradients only after the underlying same-target value route has passed.

## Entry Conditions Inherited From Previous Phase

- Phase 5 value-validation result is reviewed.
- Same-target value route(s) and scalar authority are frozen.
- No final decision phase has started.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase5-same-target-value-validation-result-2026-06-29.md`
- Phase 6 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase6-same-target-gradient-validation-result-2026-06-29.md`
- Refreshed Phase 7 subplan:
  `docs/plans/bayesfilter-actual-sv-single-target-phase7-final-decision-handoff-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks/commands are to be filled in only after the value phase
passes and the exact gradient comparator set is known.

Claude review is required for:

- the Phase 6 result,
- the gradient decision table,
- the Phase 7 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the reviewed gradients differentiate the same transformed actual-SV scalar that passed the value-validation phase? |
| Baseline/comparator | same-target value-pass route(s), reviewed finite-difference or analytical same-target comparators, and scalar authority frozen in earlier phases. |
| Primary criterion | Every compared gradient path is explicitly tied to the same scalar and passes the reviewed gradient gate without target mismatch or branch/pathology vetoes. |
| Veto diagnostics | wrong-scalar gradient; value pass absent; FD/analytic comparison across different scalars; nonfinite gradients; branch mismatch; tests-passed-but-wrong-question. |
| Explanatory diagnostics | FD ladders, componentwise gaps, branch-validity summaries, and wrapper-contract notes. |
| Not concluded | No HMC readiness, no production/default claim, no broad scientific validation beyond gradient identity for the reviewed scalar. |
| Artifact | Phase 6 result with gradient decision table. |

## Forbidden Claims/Actions

- Do not run gradient validation if the value route is still blocked.
- Do not use self-consistency of a surrogate scalar as same-target gradient evidence.
- Do not treat FD agreement as a truth oracle for the scientific model.

## Exact Next-Phase Handoff Conditions

Phase 7 may start only if:

- the Phase 6 result is reviewed;
- gradient statuses are explicit per route;
- the Phase 7 subplan exists and is reviewed.

## Stop Conditions

- The value route has not passed or its scalar authority is ambiguous.
- Gradient work exposes a new wrong-scalar path.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Fill the reviewed command/check list only after Phase 5 passes.
2. Execute the smallest reviewed same-target gradient checks.
3. Write the Phase 6 result.
4. Refresh the Phase 7 subplan.
5. Review the gradient result and next subplan.
