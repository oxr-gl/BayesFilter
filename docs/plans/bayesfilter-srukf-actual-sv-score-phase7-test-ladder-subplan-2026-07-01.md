# Phase 7 Subplan: Thorough Test Ladder

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Run a thorough validation ladder for the generic SR-UKF backend and actual-SV
adapter before any leaderboard admission.

## Entry Conditions Inherited From Previous Phase

- Generic backend and actual-SV adapter implementation phases passed.
- Focused implementation tests are green.
- Phase 6 result preserves the exact four-route forbidden set:
  `GradientTape`, `tf_svd_sigma_point_filter`, historical SVD/eigenderivative
  derivatives, and strict-SPD principal-root derivative helpers.

## Required Artifacts

- Test run manifest.
- Test result note.
- Score-at-true-parameter consistency artifact.
- Phase 7 result.
- Refreshed Phase 8 leaderboard/release subplan.
- Static route-guard evidence preserving the exact four-route forbidden set:
  `GradientTape`, `tf_svd_sigma_point_filter`, historical SVD/eigenderivative
  derivatives, and strict-SPD principal-root derivative helpers.

## Required Checks/Tests/Reviews

- Static route guards.
- Negative route-guard preservation checks for `GradientTape`,
  `tf_svd_sigma_point_filter`, historical SVD/eigenderivative derivatives, and
  strict-SPD principal-root derivative helpers.
- Generic affine/Kalman parity.
- Factor reconstruction and derivative reconstruction.
- Same-scalar FD tests.
- Actual-SV T=1 and short-prefix tests.
- Multi-seed score-at-true-parameter consistency: generate multiple datasets at
  theta0, compute analytical scores at theta0, and check whether zero is within
  a predeclared two-standard-error/uncertainty interval.
- Optional CPU/GPU performance diagnostics only if refreshed with exact
  commands and trusted execution requirements.
- Claude review of test result interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the SR-UKF analytical score route pass the necessary engineering and statistical sanity checks for leaderboard admission consideration? |
| Baseline/comparator | Own scalar SR-UKF objective for FD; Kalman affine exact score for affine parity; score-at-true-parameter consistency for actual-SV statistical sanity. |
| Primary criterion | All veto tests pass and result note preserves uncertainty and nonclaims. |
| Veto diagnostics | Failed static guard, failed factor reconstruction, failed affine parity, failed same-scalar FD under smooth fixed branch, nonfinite score, or score-at-true-parameter interval excluding zero without a documented modeling explanation. |
| Explanatory diagnostics | Runtime, SGQF/dense gaps, and finite precision sensitivity. |
| Not concluded | Exact likelihood correctness, HMC readiness, or method superiority. |
| Artifact | Phase 7 result and manifests. |

## Forbidden Claims/Actions

- Do not claim HMC readiness.
- Do not tune thresholds after seeing results.
- Do not use FD as a gradient oracle beyond same-objective consistency.
- Do not import or call `GradientTape`, `tf_svd_sigma_point_filter`,
  historical SVD/eigenderivative derivatives, or strict-SPD principal-root
  derivative helpers from the admitted actual-SV SR-UKF analytical score path.

## Exact Next-Phase Handoff Conditions

Advance to Phase 8 only if Phase 7 result passes veto tests, Claude review
converges, Phase 8 admission subplan lists exact leaderboard changes, and
Phase 8 preserves the exact four-route forbidden set: `GradientTape`,
`tf_svd_sigma_point_filter`, historical SVD/eigenderivative derivatives, and
strict-SPD principal-root derivative helpers.

## Skeptical Plan Audit Before Execution

- Wrong baseline risk: FD must compare the analytical score to the exact same
  SR-UKF scalar objective only, not to an exact likelihood oracle.
- Proxy-promotion risk: same-scalar FD and short-prefix checks are necessary
  implementation diagnostics, not leaderboard or HMC readiness.
- Statistical-overclaim risk: score-at-true-parameter consistency is an
  aggregate sanity check with uncertainty, not proof of exactness.
- Environment risk: CPU-only checks must hide GPU devices and record that
  choice; any GPU/XLA probe requires trusted execution.
- Route-drift risk: every admitted score path in this ladder must preserve the
  exact four-route forbidden set.

Audit status before execution:

- READY_FOR_PHASE_7_AFTER_PHASE_6_CLAUDE_REVIEW_CONVERGES.

## Stop Conditions

- Material test failure cannot be repaired without changing derivation or target
  law.
- GPU/HMC execution becomes necessary without a trusted runtime subplan.

## End-Of-Phase Procedure

1. Run required local checks.
2. Write Phase 7 result/close record.
3. Draft or refresh Phase 8 subplan.
4. Review Phase 8 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
