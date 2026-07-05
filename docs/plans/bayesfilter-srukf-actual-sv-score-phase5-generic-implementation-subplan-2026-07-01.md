# Phase 5 Subplan: Generic Backend Implementation

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Implement the audited generic factor-propagating SR-UKF value/score backend in
TensorFlow/TFP without relying on strict-SPD principal-square-root derivatives.

## Entry Conditions Inherited From Previous Phase

- Generic and adapter derivations have passed audits.
- Implementation scope must match audited labels and branch conditions.
- Phase 4 passed with Claude agreement.  It handed off the exact adapter labels
  and the variance/factor initial derivative distinction, but Phase 5 remains
  generic backend work; actual-SV adapter wiring belongs to Phase 6.

## Required Artifacts

- New or clearly separated TensorFlow SR-UKF backend code.
- Unit tests for generic backend mechanics.
- Diagnostics schema for factor residuals, derivative residuals, branch status,
  update/downdate status, and score provenance.
- Static route guard that rejects admitted-score paths containing
  `GradientTape`, `tf_svd_sigma_point_filter`, historical SVD/eigenderivative
  derivatives, or strict-SPD principal-root derivative helpers.
- Implementation-facing API contract for map callbacks:
  `transition_fn`, `observation_fn`, their state Jacobians, explicit parameter
  derivatives, initial factor/value derivatives, and fixed branch metadata.
- Phase 5 result.
- Refreshed Phase 6 actual-SV adapter implementation subplan.
- Phase 5 result and refreshed Phase 6 subplan must explicitly restate the
  full forbidden-route set: `GradientTape`, `tf_svd_sigma_point_filter`,
  historical SVD/eigenderivative derivatives, and strict-SPD principal-root
  derivative helpers.

## Required Checks/Tests/Reviews

- Static checks: no `GradientTape` in admitted score path, no historical SVD
  score dependency, no `tf_svd_sigma_point_filter` import/call/reference, and
  no strict-SPD principal-root derivative dependency.
- Negative route-guard tests that intentionally present each forbidden token or
  route family and assert rejection: `GradientTape`, `tf_svd_sigma_point_filter`,
  historical SVD/eigenderivative helpers, and strict-SPD principal-root
  derivative helpers.
- Generic affine/Kalman parity tests.
- Factor reconstruction tests.
- Same-scalar FD consistency tests on fixed branch fixtures.
- `python -m py_compile` or equivalent import-safe checks for touched modules.
- Claude read-only review of implementation diff/result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the generic implementation follow the audited SR-UKF derivation and expose analytical score diagnostics? |
| Baseline/comparator | Audited generic LaTeX derivation, Kalman affine fixtures, and historical SVD/principal-root routes only as excluded diagnostic routes. |
| Primary criterion | Focused tests pass and static guards prove admitted score path avoids autodiff, historical SVD, and principal-root derivative substitution. |
| Veto diagnostics | Any forbidden dependency in admitted path, failed reconstruction, failed affine parity, failed FD consistency, or nonfinite branch diagnostics. |
| Explanatory diagnostics | Runtime and branch telemetry. |
| Not concluded | Actual-SV adapter correctness and leaderboard admission. |
| Artifact | Code diff, tests, Phase 5 result, and refreshed Phase 6 subplan. |

## Forbidden Claims/Actions

- Do not modify leaderboard admission.
- Do not run GPU/HMC benchmarks.
- Do not claim actual-SV readiness.
- Do not wire actual-SV adapter code in Phase 5 except as type/API stubs needed
  to prove the generic callback contract.
- Do not import or call strict-SPD principal-root derivative helpers,
  historical SVD/eigenderivative score helpers, `tf_svd_sigma_point_filter`, or
  `GradientTape` from the admitted backend implementation.

## Skeptical Plan Audit Before Execution

- Wrong baseline risk: generic backend tests must compare against affine/Kalman
  fixtures and the audited generic SR-UKF equations, not the historical SVD or
  principal-root score route as a promotion baseline.
- Proxy-promotion risk: FD consistency on a small fixture is necessary but not
  sufficient for actual-SV or leaderboard readiness; it only validates the
  same-scalar generic fixed-branch implementation.
- Hidden-assumption risk: QR/update sign, rank, pivot, jitter, and downdate
  branch choices must be metadata, not implicit TensorFlow behavior.
- Environment mismatch risk: Phase 5 should use CPU-safe unit tests unless a
  later phase explicitly authorizes GPU/XLA checks.
- Artifact-answer risk: a code diff without static route guards and diagnostic
  provenance does not answer the Phase 5 question.

Audit status before execution:

- PASSED_FOR_PHASE_5_START once local checks confirm this subplan names the
  forbidden routes, generic-only boundary, and Phase 6 handoff.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if generic focused tests pass, Claude review converges,
and Phase 6 adapter subplan maps audited adapter objects to concrete API calls
while preserving the exact four-route forbidden set: `GradientTape`,
`tf_svd_sigma_point_filter`, historical SVD/eigenderivative derivatives, and
strict-SPD principal-root derivative helpers.

## Stop Conditions

- Generic implementation requires a new mathematical operation not covered by
  the audited derivation.
- Static guard cannot prevent old route drift.
- Material Claude review blocker persists after five rounds.

## End-Of-Phase Procedure

1. Run local checks.
2. Write Phase 5 result/close record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 subplan for consistency, correctness, feasibility, artifact
   coverage, boundary safety, and verbatim preservation of the four-route
   forbidden set.
