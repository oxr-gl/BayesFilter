# Phase 5 Subplan: Same-Target Value Validation

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Validate surviving same-target actual-SV value routes against the transformed
exact target only.

## Entry Conditions Inherited From Previous Phase

- Phase 4 route decision is explicit and reviewed.
- The surviving same-target comparator set is frozen.
- No gradient phase has started.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase4-route-decision-result-2026-06-29.md`
- Phase 5 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase5-same-target-value-validation-result-2026-06-29.md`
- Refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-actual-sv-single-target-phase6-same-target-gradient-validation-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks/commands are to be filled in only after the route decision
freezes the exact same-target comparator set. Until then, this phase is plan-only.

Claude review is required for:

- the Phase 5 result,
- the value-validation decision table,
- the Phase 6 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the surviving same-target value routes agree with the transformed exact target to the declared approximation tolerance and without branch/pathology vetoes? |
| Baseline/comparator | transformed exact dense reference plus the surviving same-target comparator set from Phase 4. |
| Primary criterion | Every compared quantity is same-target, finite, and interpretable against the transformed exact target; the result writes an explicit pass/fail/blocked decision table. |
| Veto diagnostics | wrong-scalar comparator included; nonfinite values; branch failure; target mismatch disguised as approximation gap; contract violation in benchmark/test language. |
| Explanatory diagnostics | value gaps, branch-validity summaries, and route complexity notes. |
| Not concluded | No gradient identity, no HMC readiness, no benchmark promotion beyond same-target value evidence. |
| Artifact | Phase 5 result with decision table. |

## Forbidden Claims/Actions

- Do not compare same-target routes against a surrogate or historical wrong-scalar baseline.
- Do not promote gradient or benchmark claims from value-only evidence.
- Do not weaken the route classes frozen in Phase 4.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if:

- the value-validation result is reviewed;
- underlying value scalar(s) passed or are explicitly blocked;
- the Phase 6 subplan exists and is reviewed.

## Stop Conditions

- Same-target comparator set is not actually same-target on inspection.
- Value validation reveals a new scalar-identity contradiction.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Fill the reviewed command/check list only after Phase 4 freezes the route set.
2. Execute the smallest reviewed same-target value checks.
3. Write the Phase 5 result.
4. Refresh the Phase 6 subplan.
5. Review the value result and next subplan.
