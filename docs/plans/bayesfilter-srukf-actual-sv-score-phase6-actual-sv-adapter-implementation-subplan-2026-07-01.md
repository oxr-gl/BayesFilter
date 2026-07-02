# Phase 6 Subplan: Actual-SV Adapter Implementation

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Implement the actual-SV augmented-noise adapter and analytical score wrapper on
top of the generic SR-UKF backend.

## Entry Conditions Inherited From Previous Phase

- Generic SR-UKF backend tests pass.
- Adapter derivation has passed MathDevMCP and Claude audit.
- Phase 5 result must preserve the exact four-route forbidden set:
  `GradientTape`, `tf_svd_sigma_point_filter`, historical SVD/eigenderivative
  derivatives, and strict-SPD principal-root derivative helpers.

## Required Artifacts

- Actual-SV adapter code.
- Analytical score wrapper with explicit provenance.
- Tests for adapter law, dimensions, finite value/score, and static route
  guards.
- Phase 6 result.
- Refreshed Phase 7 test ladder subplan.
- Static route guard evidence preserving the exact four-route forbidden set:
  `GradientTape`, `tf_svd_sigma_point_filter`, historical SVD/eigenderivative
  derivatives, and strict-SPD principal-root derivative helpers.
- Mapping table from audited labels to generic backend API calls:
  `eq:bf-hd-actual-sv-srukf-augmented-law` to augmented mean/factor,
  `eq:bf-hd-actual-sv-srukf-transition-map` to `transition_fn`,
  `eq:bf-hd-actual-sv-srukf-observation-map` to `observation_fn`,
  `eq:bf-hd-actual-sv-srukf-transition-derivatives` to transition derivative
  callbacks,
  `eq:bf-hd-actual-sv-srukf-observation-state-derivative` and
  `eq:bf-hd-actual-sv-srukf-observation-parameter-derivatives` to observation
  derivative callbacks, and
  `eq:bf-hd-actual-sv-srukf-initial-derivatives` plus
  `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives` to initial handoff.

## Required Checks/Tests/Reviews

- Static no-autodiff/no-SVD/no-principal-root-substitution checks.
- Negative route-guard preservation checks for `GradientTape`,
  `tf_svd_sigma_point_filter`, historical SVD/eigenderivative derivatives, and
  strict-SPD principal-root derivative helpers.
- Actual-SV short-prefix finite value/score tests.
- Adapter dimension and parameterization tests.
- Same-scalar FD consistency against the same SR-UKF scalar objective.
- Claude read-only review of implementation result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the actual-SV adapter faithfully map the audited augmented-noise law to the generic SR-UKF backend and produce an analytical score? |
| Baseline/comparator | Phase 3/4 adapter derivation and current value-only diagnostic route. |
| Primary criterion | Focused actual-SV adapter tests pass with analytical provenance and no forbidden score route. |
| Veto diagnostics | Wrong sigma-point law, missing observation shock, nonfinite score, failed FD, or forbidden dependency. |
| Explanatory diagnostics | UKF approximation gap versus SGQF/dense diagnostic routes. |
| Not concluded | Full leaderboard readiness or HMC readiness. |
| Artifact | Code diff, tests, Phase 6 result. |

## Forbidden Claims/Actions

- Do not regenerate leaderboard admission yet.
- Do not claim exact likelihood.
- Do not run long/GPU tests unless Phase 7 refresh explicitly authorizes them.
- Do not import or call `GradientTape`, `tf_svd_sigma_point_filter`,
  historical SVD/eigenderivative derivatives, or strict-SPD principal-root
  derivative helpers from the admitted actual-SV SR-UKF analytical score path.

## Exact Next-Phase Handoff Conditions

Advance to Phase 7 only if adapter implementation passes focused tests and
Claude review converges, and the Phase 7 subplan preserves the exact four-route
forbidden set: `GradientTape`, `tf_svd_sigma_point_filter`, historical
SVD/eigenderivative derivatives, and strict-SPD principal-root derivative
helpers.

## Skeptical Plan Audit Before Execution

- Wrong target risk: Phase 6 implements the raw Gaussian-closure surrogate
  adapter only; it must not claim exact or same-target transformed actual-SV
  likelihood.
- Route-drift risk: the old value-only `tf_svd_sigma_point_filter` diagnostic
  path and `GradientTape` score path must remain historical diagnostics, not
  implementation dependencies.
- Hidden-derivative risk: the stationary initial variance and scalar factor
  derivative handoff must use the audited labels, not an implicit tape.
- Proxy-promotion risk: short-prefix FD consistency is an implementation check,
  not leaderboard or HMC readiness.
- Artifact-answer risk: Phase 6 result must include the mapping table, static
  guard evidence, exact tests, and nonclaims.

Audit status before execution:

- PASSED_PHASE_6_START. Phase 5 result closed with bounded Claude
  `VERDICT: AGREE`, and this subplan preserves the exact four-route forbidden
  set.

## Stop Conditions

- Actual-SV adapter requires changing the audited target law.
- Same-scalar FD consistency fails and cannot be explained as branch
  non-smoothness under the documented stop rules.

## End-Of-Phase Procedure

1. Run local checks.
2. Write Phase 6 result/close record.
3. Draft or refresh Phase 7 subplan.
4. Review Phase 7 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
