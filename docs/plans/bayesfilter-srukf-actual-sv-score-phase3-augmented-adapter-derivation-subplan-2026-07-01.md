# Phase 3 Subplan: Augmented-Noise Adapter Derivation

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Derive and document the actual-SV augmented-noise adapter that feeds the
generic SR-UKF backend with the correct pre-transition uncertainty law and
manual parameter derivatives.  The product of this phase is a derivation for a
declared raw actual-SV Gaussian-closure surrogate scalar; it is not exact
transformed actual-SV likelihood admission.

## Entry Conditions Inherited From Previous Phase

- Generic SR-UKF derivation has passed Phase 2 audit.
- The actual-SV UKF score remains value-only until this adapter is derived and
  later implemented/tested.

## Required Artifacts

- Patched LaTeX adapter section, likely cross-linked from
  `docs/chapters/ch18b_structural_deterministic_dynamics.tex` and `ch17`.
- Labels for actual-SV augmented variable, transition map, observation map,
  parameterization, derivative maps, score handoff, and nonclaims.
- Explicit augmented variable per panel coordinate.  The default derivation
  must use the three-coordinate pre-observation variable
  `(lagged latent state, state innovation, observation shock)` so both process
  and measurement shocks are declared.  A two-coordinate collapsed-process
  variant may be recorded only as a separately labeled law-equivalent
  specialization after proving the collapse from the scalar AR(1) Gaussian
  prediction; it cannot be the default derivation.
- Explicit unconstrained parameterization
  `theta=[probit_gamma, log_beta]` with fixed `sigma` unless the derivation
  states and labels a reviewed sigma-derivative extension.
- Explicit nonadmission statement that current code routes using
  `tf_svd_sigma_point_filter` for value or `GradientTape` for score are
  historical/diagnostic routes and cannot be used as the admitted leaderboard
  analytical-gradient route.
- Explicit nonadmission statement that strict-SPD principal-root derivative
  routes are comparator/historical diagnostics only and cannot satisfy the
  admitted factor-propagating SR-UKF analytical score route.
- Phase 3 result.
- Refreshed Phase 4 audit subplan.

## Required Checks/Tests/Reviews

- Local text checks for labels and forbidden claims.
- Bounded Claude read-only review of the adapter derivation.
- `git diff --check` on touched LaTeX chapter files and `docs/plans` files.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the adapter derivation apply the generic SR-UKF backend to the actual-SV augmented-noise law without target drift? |
| Baseline/comparator | Existing structural UKF law in `ch18b` and current actual-SV value-only diagnostic route. |
| Primary criterion | The derivation explicitly states the augmented variable, transition, raw observation map, parameter derivatives, SR-UKF handoff, and Gaussian-closure score object without using autodiff, historical SVD/eigenderivative score, strict-SPD principal-root derivative, or wrong post-transition perturbations. |
| Veto diagnostics | Missing observation shock, wrong sigma-point variable, missing parameter derivative, exact-likelihood claim, same-target transformed-likelihood claim, silent use of strict-SPD principal-root derivative, hidden GradientTape score, or historical SVD route reused as admitted SR-UKF. |
| Explanatory diagnostics | Approximation boundary versus exact transformed likelihood, dense Gaussian-closure reference, SGQF Gaussian closure, and current value-only UKF diagnostics. |
| Not concluded | No code or numeric accuracy is concluded. |
| Artifact | Patched adapter LaTeX and Phase 3 result. |

## Forbidden Claims/Actions

- Do not claim exact actual-SV likelihood.
- Do not claim same-target transformed actual-SV likelihood.
- Do not implement code.
- Do not run leaderboard regeneration.
- Do not use current `GradientTape` score routes as analytical-gradient
  evidence.
- Do not reuse the current historical SVD sigma-point value route as the
  admitted factor-propagating SR-UKF implementation.
- Do not use strict-SPD principal-root derivative routes as the admitted
  factor-propagating SR-UKF analytical score route.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if the adapter derivation exists with stable labels,
passes local checks, and receives the required bounded Claude read-only review
with no unresolved material `REVISE`.  The handoff must include the exact labels
Phase 4 must audit and the implementation-facing derivative objects Phase 5/6
will need.

## Stop Conditions

- Adapter law cannot be stated without changing the scientific target.
- Adapter derivation cannot preserve the declared Gaussian-closure surrogate
  boundary without making an exact or same-target transformed-likelihood claim.
- Adapter derivation can proceed only by using the strict-SPD principal-root
  derivative route, historical SVD/eigenderivative route, or `GradientTape`
  score route.
- Claude identifies a material target drift that cannot be repaired in five
  rounds.

## End-Of-Phase Procedure

1. Run local checks.
2. Write Phase 3 result/close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
