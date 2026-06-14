# P43 Plan: SV Value and Gradient CUT4--Zhao-Cui Ladder

metadata_date: 2026-06-07
phase: P43

## Decision Target

Create and execute a governed value-and-gradient diagnostic ladder for
stochastic-volatility fixtures in dimensions 1, 2, and 3, covering:

- KSC Gaussian-mixture transformed SV: CUT4 versus Kalman-mixture for value and
  gradient;
- exact transformed log-chi-square SV: factorized Zhao--Cui/fixed-design TT
  versus dense reference for value and gradient;
- KSC mixture versus exact transformed SV as an approximation comparison, not a
  same-target equality test;
- generalized SV diagnostic coverage, with explicit boundary language rather
  than false equality claims.

This phase is a P42 Tier-1 local diagnostic.  It does not claim HMC readiness.

## Skeptical Plan Audit

Status: `PASS_WITH_SCOPE_RESTRICTIONS`.

- Same-target risk: CUT4 and Zhao--Cui do not currently share one exact target.
  P43 therefore separates same-target checks:
  - CUT4 checks the KSC Gaussian-mixture transformed target against
    Kalman-mixture;
  - Zhao--Cui checks the exact transformed log-chi-square target against dense;
  - KSC versus exact transformed is approximation-only.
- Gradient-reference risk: neither autodiff nor finite differences are
  automatically truth for long/high-dimensional cases.  P43 stays on tiny
  deterministic `T=2`, dimensions 1--3, and uses P42 Tier-1 diagnostics only.
- TT-gradient risk: the existing fixed-design TT value path fits artifacts per
  coordinate.  Autodiff through fitting is not promoted as analytic production
  score.  P43 uses same-target autodiff and directional finite-difference
  checks as diagnostic evidence only.
- Dimension risk: dimensions 2 and 3 remain independent-product panels.  The
  Zhao--Cui lane is a sum of scalar fixed-design TT lanes, not a coupled
  multivariate TT.
- Generalized SV risk: no exact Kalman/CUT4/Zhao--Cui equality exists for
  \(y_t=\beta s_t+\exp(h_t/2)\epsilon_t\) with both states latent.  P43 may
  test finite diagnostic gradients for a declared approximation closure, but it
  must not call that a same-target match.
- Horizon/statistical-scale risk: no long-horizon or Tier-2 sampling-variance
  conclusion is made in P43.

## Evidence Contract

Question:

- On tiny deterministic independent SV fixtures, do value and gradient
  diagnostics agree on the same mathematical target?
- How large is the KSC mixture approximation gradient gap relative to exact
  transformed SV on the same fixtures?
- Does the generalized SV diagnostic produce finite value and gradient outputs
  while preserving non-claim boundaries?

Primary pass/fail criteria:

- KSC transformed-mixture target:
  - CUT4 value matches Kalman-mixture value for dims 1, 2, 3 within P40
    tolerances.
  - CUT4 score, computed by autodiff through the fixed tiny fixture value
    function, matches Kalman-mixture autodiff score on unconstrained parameter
    vectors within local diagnostic tolerances.
  - At least five directional checks per dimension agree with
    candidate-reference score differences.
- Exact transformed SV target:
  - factorized Zhao--Cui/fixed-design TT values match dense values for dims 1,
    2, 3 within P41 tolerances.
  - factorized Zhao--Cui diagnostic scores match dense diagnostic scores within
    local tolerances.
  - At least five directional checks per dimension agree with
    candidate-reference score differences.
- Generalized SV:
  - diagnostic closure returns finite value and finite gradient;
  - diagnostics state that this is not an exact Kalman/CUT4/Zhao--Cui match.

Diagnostic tolerances:

- same-target value gap:
  - KSC CUT4 vs Kalman: `<= 2e-6`;
  - exact transformed TT vs dense: `<= 2e-6` for the implemented diagnostic
    score path, with observed value gaps also reported.
- same-target gradient vector relative error:
  - diagnostic pass: `<= 1e-3`;
  - coordinate absolute error reported regardless of relative error.
- directional checks:
  - use at least five deterministic normalized directions per dimension;
  - report candidate-reference directional residuals;
  - finite-difference/regression derivative is optional in P43 only when the
    same-target score comparison is between two autodiff-through-fixed tiny
    fixture functions.  If used, it must follow the P42 ladder rules.

Veto diagnostics:

- target mismatch is used as evidence of same-target gradient agreement;
- gradients are compared in different parameterizations;
- zero observations enter exact `log(y^2)` tests;
- TT panel lane is described as coupled multivariate TT;
- generalized SV diagnostic is described as exact;
- any nonfinite value/gradient appears;
- autodiff path crosses mutable/adaptive branches without being labeled
  diagnostic-only.

Explanatory diagnostics:

- KSC mixture score gap versus exact transformed dense score;
- per-coordinate and per-time value/score contributions when available;
- directional residuals;
- generalized SV approximation value/gradient finite checks.

What will not be concluded:

- no HMC readiness;
- no Tier-2 sampling-variance or score-covariance claim;
- no Tier-3 Hamiltonian/leapfrog claim;
- no production analytic derivative API claim;
- no coupled multivariate Zhao--Cui TT claim;
- no exact generalized SV filtering claim;
- no KSC mixture exactness claim.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-plan-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-claude-review-ledger-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-result-2026-06-07.md`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- optional helper additions to `bayesfilter/highdim/sv_mixture_cut4.py`

## Implementation Plan

1. Add test-local scalar/panel value functions for:
   - KSC Kalman-mixture value;
   - KSC CUT4 value;
   - exact transformed dense value;
   - exact transformed factorized Zhao--Cui/fixed-design TT value.
2. Use unconstrained parameter vectors per coordinate:
   - parameters per coordinate are `(Phi^{-1}(gamma_i), log(beta_i))`;
   - `sigma_i` remains fixed for these tests.
3. Compute scores with TensorFlow `GradientTape` for tiny fixed fixtures only.
   Record that these are diagnostic autodiff scores, not production analytic
   derivatives.
4. Add deterministic direction sets for dimensions 1, 2, and 3:
   - coordinate directions for each parameter block;
   - fixed normalized mixed directions.
5. Test KSC same-target value/score agreement:
   - CUT4 versus Kalman-mixture.
6. Test exact transformed same-target value/score agreement:
   - factorized Zhao--Cui/fixed-design TT versus dense.
7. Test approximation gap:
   - KSC mixture value/score versus exact transformed dense value/score;
   - report finite nonzero gaps, not pass/fail equality.
8. Test generalized SV diagnostic closure:
   - finite value and score for a declared one-step transformed-residual
     diagnostic;
   - explicit non-claims.
9. Run focused and guardrail tests.
10. Run Claude plan review before implementation and Claude code review after
    implementation, looping to convergence or maximum five iterations at each
    review gate.

## Review Gates

- Plan review: `PASS_P43_PLAN_GOVERNANCE` or `BLOCKED_P43_PLAN_GOVERNANCE`.
- Code review: `PASS_P43_CODE_GOVERNANCE` or `BLOCKED_P43_CODE_GOVERNANCE`.
- Stop after five review iterations without convergence or on a blocker that
  requires a human target decision.
