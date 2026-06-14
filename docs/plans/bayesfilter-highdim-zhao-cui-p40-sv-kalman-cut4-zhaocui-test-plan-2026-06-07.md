# P40 Plan: SV Kalman--CUT4--Zhao-Cui Test Ladder

metadata_date: 2026-06-07
phase: P40

## Decision Target

Add governed tests that tie the transformed stochastic-volatility
Gaussian-mixture CUT4 comparator to a clean Kalman-mixture oracle, then compare
that target to available Zhao--Cui/BayesFilter SV lanes without overclaiming
unsupported multidimensional or generalized behavior.

## Skeptical Plan Audit

Status: `PASS_WITH_SCOPE_RESTRICTIONS`.

- Wrong baseline risk: native SV, transformed mixture SV, CUT4, Kalman-mixture
  oracle, dense quadrature, and Zhao--Cui TT/dense lanes are not the same object
  unless the target is named.  P40 therefore promotes only same-target
  transformed-mixture comparisons.
- Dimension ambiguity: existing `StochasticVolatilitySSM` and Zhao--Cui short
  TT value path are scalar.  "Dimension 1, 2, 3" will mean independent
  transformed-mixture SV panels for the Kalman/CUT4 oracle ladder: diagonal
  AR(1) latent dynamics and coordinatewise log-square observations whose
  finite-mixture likelihood factorizes across coordinates.  Zhao--Cui
  comparison is dimension 1 only unless a multivariate Zhao--Cui lane is first
  implemented.
- Proxy metric risk: finite values are veto/diagnostic only.  The pass
  criterion is numerical agreement with an analytic Kalman-mixture oracle on
  tiny deterministic fixtures.
- CUT4 exactness risk: for the simple transformed-mixture SV panel, conditional
  component observations are linear Gaussian.  CUT4 agreement validates
  component bookkeeping, Gaussian projection reduction, and moment collapse,
  not nonlinear CUT4 accuracy.
- Generalized SV risk: a model such as
  \(y_t=\beta s_t+\exp(h_t/2)\epsilon_t\) is not jointly Kalman-exact when both
  \(s_t\) and \(h_t\) are latent.  P40 may include a diagnostic generalized-SV
  CUT4 fixture and a moment-matched Kalman approximation, but it must not call
  that approximation exact.
- Artifact adequacy: plan, tests, result note, and Claude review ledger are
  required before promotion.

## Evidence Contract

Question:

- Can the transformed KSC-mixture SV CUT4 implementation agree with an exact
  component-enumerated Kalman-mixture oracle for dimensions 1, 2, and 3 on tiny
  deterministic conditionally linear Gaussian fixtures?
- Can the existing Zhao--Cui/BayesFilter scalar SV lane be compared honestly to
  that transformed-mixture target?
- Can a generalized SV diagnostic test show where CUT4 is useful without
  calling a moment-matched Kalman approximation exact?

Primary pass/fail criteria:

- Dimension 1, 2, and 3 independent transformed-mixture SV fixtures:
  component-enumerated Kalman-mixture oracle and CUT4 transformed-mixture filter
  agree on log likelihood, per-step log normalizers, posterior means,
  posterior covariance diagonals, and normalized component weights within
  declared tight local tolerances.
- Dimension 1 scalar P39 dense reference is a secondary corroborating
  comparator against the Kalman-mixture oracle and CUT4.  It is not the primary
  exact oracle.
- Existing Zhao--Cui scalar native SV lane remains explicitly an explanatory
  different-target comparison unless a transformed-mixture Zhao--Cui/TT lane is
  added.

Veto diagnostics:

- mixture constants not shifted by `-1.2704`;
- component weights fail to normalize;
- Kalman innovation covariance is non-PD;
- CUT4 diagnostics are nonfinite;
- dimension 2 or 3 test silently routes through scalar-only Zhao--Cui helpers;
- generalized SV moment-matched Kalman approximation is described as exact;
- native SV, CNS, same-target TT, or production-default readiness is claimed.

Explanatory diagnostics:

- CUT4 point counts and augmented dimensions;
- gaps between native scalar Zhao--Cui value path and transformed-mixture oracle;
- generalized SV moment-matched Kalman approximation residuals.

What will not be concluded:

- no exact native SV filtering claim;
- no KSC importance reweighting or sampler implementation;
- no multivariate Zhao--Cui TT implementation;
- no generalized CNS estimator;
- no nonlinear CUT4 accuracy claim from the conditionally linear fixtures;
- no coupled multivariate SV claim from independent-product panel fixtures;
- no paper-scale, HMC, DSGE, GPU, derivative, or production-default readiness.

Artifacts:

- `bayesfilter/highdim/sv_mixture_cut4.py`
- `tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p40-sv-kalman-cut4-zhaocui-test-result-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p40-sv-kalman-cut4-zhaocui-claude-review-ledger-2026-06-07.md`

## Implementation Plan

1. Add an independent Kalman-mixture oracle for transformed SV panels:
   - dimensions 1, 2, and 3;
   - tiny deterministic `T=2` fixtures only;
   - independent AR(1) latent volatilities with diagonal covariance;
   - coordinatewise transformed observations
     \(z_{i,t}=\log(y_{i,t}^2+c_i)\);
   - KSC mixture components enumerated as `7^d` per time step;
   - posterior collapsed to a single Gaussian after each observation using
     log-sum-exp weights and law of total covariance.
   This is a tractability-bounded oracle for tests, not a scalable validation
   route.
2. Add a multidimensional transformed-mixture CUT4 comparator:
   - same independent-panel target;
   - enumerate the same per-coordinate component grid;
   - run component-wise affine structural CUT4 updates;
   - collapse component moments identically to the Kalman oracle;
   - record point counts, augmented dimensions, polynomial degree, and
     non-claims.
   Because each component observation is affine Gaussian, passing this ladder
   validates CUT4 reduction to the Gaussian component update plus component-grid
   bookkeeping and moment collapse.  It does not validate CUT4 accuracy for
   nonlinear observation maps.
3. Add tests for dimensions 1, 2, and 3:
   - two-observation deterministic fixtures;
   - Kalman oracle versus CUT4;
   - for dimension 1, Kalman oracle versus existing scalar P39 dense reference;
   - scalar Zhao--Cui native lane is finite and different-target explanatory.
4. Add generalized SV diagnostic test:
   - model \(y_t=\beta s_t+\exp(h_t/2)\epsilon_t\) with independent linear
     Gaussian states `(s, h)`;
   - run a moment-matched Kalman approximation for `s` as explanatory only;
   - run CUT4 on the nonlinear raw observation closure or transformed residual
     closure, depending on local structural support;
   - assert finite diagnostics and explicit non-claims, not equivalence.
5. Run CPU-only tests and guardrails.
6. Run Claude plan review before implementation and Claude code review after
   implementation, looping to convergence or max five iterations.

## Review Gates

- Plan review: `PASS_P40_PLAN_GOVERNANCE` or `BLOCKED_P40_PLAN_GOVERNANCE`.
- Code review: `PASS_P40_CODE_GOVERNANCE` or `BLOCKED_P40_CODE_GOVERNANCE`.
- Stop only for a blocker that Codex and Claude cannot resolve without a
  human target decision.
