# P41 Plan: Exact Transformed SV Zhao-Cui Ladder

metadata_date: 2026-06-07
phase: P41

## Decision Target

Build and test a same-target ladder for the stochastic-volatility transform
\(z_t=\log(y_t^2)\) without the KSC Gaussian-mixture approximation.  The ladder
must cover dimensions 1, 2, and 3 for tiny deterministic independent-product SV
fixtures and compare:

- exact transformed log-chi-square dense quadrature;
- exact transformed log-chi-square Zhao--Cui/fixed-design TT value path;
- raw native SV likelihood after the known Jacobian correction;
- KSC mixture Kalman/CUT4 as an approximation comparator, not the exact target.

## Skeptical Plan Audit

Status: `PASS_WITH_SCOPE_RESTRICTIONS`.

- Wrong target risk: raw SV, exact transformed SV, and KSC mixture transformed
  SV are different likelihood targets.  P41 makes the exact transformed
  log-chi-square target primary.  Raw SV is compared only after adding the
  observation-only Jacobian relation, and KSC mixture is an approximation
  comparator only.
- Transform risk: using `log(y^2 + c)` changes the target.  P41 exact lanes use
  `z=log(y^2)` with deterministic nonzero observations.  Offset transforms are
  allowed only for the existing KSC diagnostic lane and must be labeled as such.
- Dimension ambiguity: existing Zhao--Cui scalar fixed-design TT machinery is
  scalar.  Dimensions 1, 2, and 3 are independent-product SV panels with
  coordinatewise observations and diagonal latent AR(1) dynamics.  The
  Zhao--Cui panel value path is the sum of independently run scalar
  fixed-design TT lanes, not a coupled multivariate TT implementation.
- Proxy metric risk: finite Zhao--Cui values alone do not establish agreement.
  The primary criteria compare exact transformed TT values to exact transformed
  dense quadrature on tiny `T=2` fixtures.
- Mixture approximation risk: KSC mixture Kalman/CUT4 closeness to exact
  transformed SV is statistical/approximation evidence only.  It must not be
  treated as exact equality or as a native-SV correctness proof.
- Artifact adequacy: plan, tests, implementation, result note, and Claude
  review ledger are required before promotion.

## Evidence Contract

Question:

- Can the exact transformed log-chi-square SV likelihood be evaluated by the
  scalar Zhao--Cui/fixed-design TT lane and tied to dense quadrature for
  dimensions 1, 2, and 3 through an independent-product panel construction?
- Does the exact transformed target agree with the raw native SV likelihood
  after applying the known Jacobian correction?
- How close is the KSC Gaussian-mixture Kalman/CUT4 approximation on the same
  tiny fixtures?

Primary pass/fail criteria:

- For dimensions 1, 2, and 3 and deterministic `T=2` nonzero observations,
  exact transformed dense quadrature and exact transformed Zhao--Cui/fixed-design
  TT agree on summed panel log likelihood within a declared local tolerance.
- For the same fixtures, raw native SV dense quadrature and exact transformed
  dense quadrature agree after subtracting `sum(log(abs(y)))` over all
  coordinates and times.
- Exact transformed dense quadrature is finite, per-coordinate log normalizers
  are finite, and panel sums are coordinatewise additive.

Veto diagnostics:

- any exact transformed lane uses `log(y^2+c)` with `c>0`;
- any observation contains zero in an exact transformed test;
- the KSC mixture approximation is described as exact;
- the panel Zhao--Cui lane is described as a coupled multivariate TT
  implementation;
- dimensions 2 or 3 silently call scalar model code as if coupled;
- raw SV likelihood is compared to transformed likelihood without the Jacobian;
- TT finite value is promoted without dense same-target comparison.

Explanatory diagnostics:

- KSC mixture Kalman/CUT4 gap against exact transformed dense quadrature;
- Zhao--Cui TT fit residuals and retained-filter metadata;
- per-dimension summed coordinate gaps.

What will not be concluded:

- no coupled multivariate Zhao--Cui TT implementation;
- no generalized SV/CNS estimator claim;
- no KSC importance-reweighting claim;
- no nonlinear CUT4 accuracy claim;
- no derivative, HMC, DSGE, GPU, paper-scale, or production-default readiness.

Artifacts:

- `bayesfilter/highdim/sv_mixture_cut4.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p41-exact-transformed-sv-zhaocui-ladder-result-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p41-exact-transformed-sv-zhaocui-claude-review-ledger-2026-06-07.md`

## Implementation Plan

1. Add exact transformed SV utilities:
   - coordinatewise `z=log(y^2)` transform that rejects zero observations;
   - exact log-density for \(u=\log(\epsilon^2)\):
     \[
       \log f_U(u)=\frac12u-\frac12\exp(u)-\frac12\log(2\pi).
     \]
2. Add an exact transformed scalar SV model contract compatible with existing
   scalar dense and scalar fixed-design TT value paths:
   - state \(h_t\);
   - transition \(h_t=\gamma h_{t-1}+\sigma\eta_t\);
   - observation density \(z_t-\log(\beta^2)-h_t\sim \log(\chi_1^2)\).
3. Add exact transformed dense scalar and independent-panel helpers:
   - scalar dense quadrature over the transformed target;
   - independent-panel sum over scalar lanes for dimensions 1, 2, and 3.
4. Add exact transformed Zhao--Cui/fixed-design TT independent-panel helper:
   - run the existing scalar fixed-design TT value path per coordinate;
   - sum log likelihoods;
   - record diagnostics that this is a factorized independent-panel lane, not a
     coupled multivariate TT.
5. Add raw native SV dense panel helper or test-local reference:
   - compare to exact transformed dense after the Jacobian correction
     \[
       \log p(y_{1:T}) = \log p(z_{1:T}) - \sum_{t,i}\log|y_{t,i}|.
     \]
6. Add tests for dimensions 1, 2, and 3:
   - exact transformed dense versus exact transformed Zhao--Cui TT;
   - raw native dense versus transformed dense plus Jacobian relation;
   - KSC mixture Kalman/CUT4 gap is finite and labeled approximation-only.
7. Run CPU-only focused tests and relevant guardrails.
8. Run Claude plan review before implementation and Claude code review after
   implementation, looping to convergence or max five iterations.

## Review Gates

- Plan review: `PASS_P41_PLAN_GOVERNANCE` or `BLOCKED_P41_PLAN_GOVERNANCE`.
- Code review: `PASS_P41_CODE_GOVERNANCE` or `BLOCKED_P41_CODE_GOVERNANCE`.
- Stop only for a blocker that Codex and Claude cannot resolve without a human
  target decision.
