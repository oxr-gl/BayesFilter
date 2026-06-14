# P51-M1 Subplan: Stable Score API Contract

metadata_date: 2026-06-09
phase: P51-M1
status: PLAN_REVIEW_CONVERGED

## Objective

Promote the experimental `bayesfilter.highdim` score API only if it has a
stable, tested subpackage contract for value, gradient, metadata, route labels,
dtype/shape, and nonclaims.  A root-level `bayesfilter` public export is a
separate public-API policy decision and is not silently authorized by this
phase.

This phase is the traceability owner for the original P50
`stable_top_level_score_api` gap.  The result must explicitly classify that
original gap as one of:

- closed by reviewed root-level public API policy plus implementation/tests;
- partially closed by a stable `bayesfilter.highdim` contract while root-level
  export remains `BLOCKED_PUBLIC_API_DECISION`; or
- blocked entirely.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can `bayesfilter.highdim` expose a stable score API contract for P51-supported deterministic filtering targets? |
| Baseline/comparator | `bayesfilter/highdim/score_api.py`, P47/P50 score readiness tests, P50 M4 calibration rules, and P50 M7 tier boundaries. |
| Primary pass criterion | Stable subpackage API contract, guard tests, manifest, and documentation pass; the original P50 `stable_top_level_score_api` row is explicitly mapped to closed, partially closed with `BLOCKED_PUBLIC_API_DECISION`, or blocked; no HMC readiness, production model readiness, or root-level public API stability is claimed unless separately approved and tested. |
| Veto diagnostics | API hides target identity; gradient value is disconnected from scalar; finite gradient is labeled HMC-ready; root-level public export is changed without reviewed policy. |
| Not concluded | No HMC readiness, sampler health, production readiness, or stable root-level `bayesfilter` public API unless explicitly approved, implemented, and tested. |

## Planned Work

1. Audit current score API surface and tests.
2. Define a stable subpackage-scoped API or record why promotion is blocked.
3. Preserve the original `stable_top_level_score_api` row in the result and
   manifest.  If root-level `bayesfilter` export is not approved and tested,
   mark that subclaim `BLOCKED_PUBLIC_API_DECISION` even if the subpackage
   contract passes.
4. Add tests for value/gradient metadata and nonclaims.
5. Write result and manifest artifacts and submit to Claude review.

## Repair Loop

Patch contract/tests for fixable API ambiguity. Stop for a public API policy
decision beyond subpackage scope.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-result-2026-06-09.md`

Required token:

`PASS_P51_M1_STABLE_SCORE_API` or `BLOCK_P51_M1_STABLE_SCORE_API`

Required manifest:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-manifest-2026-06-09.json`
