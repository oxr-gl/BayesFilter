# Phase 1 Subplan: Generic SR-UKF Derivation

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Patch the LaTeX document with a generic factor-propagating SR-UKF value and
first-derivative score derivation that does not rely on strict-SPD
principal-square-root derivatives.

## Entry Conditions Inherited From Previous Phase

- Phase 0 governance artifacts exist and pass launch review.
- The program boundary separates the generic SR-UKF backend from the actual-SV
  augmented-noise adapter.

## Required Artifacts

- Patched `docs/chapters/ch17_square_root_sigma_point.tex` or a clearly cited
  companion section.
- Labels for core equations: factor placement, weighted moment factor,
  innovation factor, log-likelihood solve, first derivative of placement,
  first derivative of moments, score, filtered state derivative, and factor
  reconstruction.
- Phase 1 result.
- Refreshed Phase 2 audit subplan.

## Required Checks/Tests/Reviews

- `rg` checks for labels and forbidden route language.
- MathDevMCP label lookup readiness check for newly added labels if labels are
  available before Phase 2.
- Bounded Claude read-only review of the derivation section.
- `git diff --check` on touched LaTeX and plan files.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the LaTeX state a generic factor-propagating SR-UKF analytical score backend independent of strict-SPD principal-root derivatives? |
| Baseline/comparator | Existing `ch17` square-root contract, `ch12` factor derivative contract, and current `ch18` strict-SPD principal-root section as a non-target comparator. |
| Primary criterion | The derivation defines factor propagation and first derivatives with explicit branch/failure conditions and forbidden-route separation. |
| Veto diagnostics | Use of principal-root/Sylvester derivative as the generic SR-UKF derivative path, hidden covariance/eigendecomposition score route, missing factor reconstruction contract, or unsupported leaderboard/HMC claim. |
| Explanatory diagnostics | Notes about negative UKF covariance weights, QR/cholupdate policy, jitter, and downdate failure. |
| Not concluded | No implementation correctness or actual-SV adapter correctness. |
| Artifact | Patched LaTeX and Phase 1 result. |

## Forbidden Claims/Actions

- Do not claim the actual-SV adapter has been derived.
- Do not claim exact likelihood correctness.
- Do not edit implementation code.
- Do not remove historical SVD docs; demote/contrast them where necessary.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if the generic derivation has stable labels, local text
checks pass, and Claude has no material revision request or revisions are
patched visibly.

## Stop Conditions

- The derivation cannot state a branch-safe factor update/downdate policy.
- Claude or MathDevMCP finds a material flaw that cannot be repaired in five
  rounds.

## End-Of-Phase Procedure

1. Run local checks.
2. Write Phase 1 result/close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
