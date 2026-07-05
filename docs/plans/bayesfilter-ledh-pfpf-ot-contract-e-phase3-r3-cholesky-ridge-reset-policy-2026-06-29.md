# Phase R3 Policy Design: Cholesky-Ridge Contract E Reset

Date: 2026-06-29

Status: `DRAFT_FOR_REVIEW`

R3 subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-reset-blocker-resolution-subplan-2026-06-29.md`

## Objective

Resolve the R2 eigensystem blocker by replacing the reset-map material
factorization with a square-root Cholesky-gauge route.  The goal is to avoid
manual differentiation of eigenvectors and hard retained-rank branches.  This
does not by itself implement the full manual likelihood reverse scan or unblock
material Phase 3.

## Skeptical Plan Audit

The plan is allowed only as a local reset-policy repair.  It must not claim the
old support-exact Contract E algebra after adding a full-rank ridge.  The
primary evidence is local reset-fixture behavior and static route inspection,
not Kalman agreement, full-filter FD, or production gradient correctness.  If
the Cholesky ridge creates large covariance residuals or nonfinite factors, the
result is a tuning or contract failure, not evidence that the original
eigensystem route was correct.

## Proposed Reset Factorization

Let \(\Sigma_w\) be the weighted target covariance, \(\Sigma_+\) the covariance
of the positive first-stage cloud, and \(G=\operatorname{sym}(\Sigma_w-\Sigma_+)\).
Use a single state-scale ridge
\[
  \lambda
  =
  \max\!\left\{
    \lambda_{\rm abs},
    \lambda_{\rm rel}\frac{\operatorname{tr}(\Sigma_w)}{d_x}
  \right\}.
\]
The user-facing parameters are `--chol-ridge-rel` and `--chol-ridge-abs`.

The residual stage uses a strictly positive ridge selected by
\[
  \lambda_0
  =
  \max\!\left\{
    \lambda_{\rm abs},
    \lambda_{\rm rel}\frac{\operatorname{tr}(\Sigma_w)}{d_x}
  \right\},
  \qquad \lambda_{\rm abs}>0.
\]
The implementation must use an escalation-or-stop rule: try
\(\lambda_k=\lambda_0\gamma^k\) for a fixed \(\gamma>1\) until the Cholesky
factors below are finite and have positive diagonal entries, or stop with a
diagnostic failure after a bounded number of attempts.  It must record the
final \(\lambda_k\) actually used.  A collapsed trace is therefore not allowed
to produce a zero ridge.

The residual stage uses
\[
  B_\lambda=\sqrt{\rho}\operatorname{chol}(G+\lambda I),
  \qquad
  \widetilde Y=Y^+ + B_\lambda \Xi .
\]
The affine restoration stage uses
\[
  L_w=\operatorname{chol}(\Sigma_w+\lambda I),
  \qquad
  L_{\tilde{}}=\operatorname{chol}(\widetilde\Sigma+\lambda I),
  \qquad
  A_\lambda=L_wL_{\tilde{}}^{-1}.
\]
The particle map is the explicitly recentered map
\[
  Y^\star
  =
  \mu_w\mathbf 1^\top
  +
  A_\lambda(\widetilde Y-\bar{\widetilde Y}\mathbf 1^\top).
\]
Thus the equal-weight mean is \(\mu_w\) by construction.  For the covariance,
\[
  A_\lambda(\widetilde\Sigma+\lambda I)A_\lambda^\top
  =
  \Sigma_w+\lambda I.
\]
The realized covariance after applying \(A_\lambda\) to the unridged cloud is
only approximately \(\Sigma_w\), with residual
\[
  A_\lambda\widetilde\Sigma A_\lambda^\top-\Sigma_w
  =
  \lambda(I-A_\lambda A_\lambda^\top).
\]

## Lambda Policy

The relative ridge is scale-aware and the absolute ridge is a hard numerical
floor.  The caller must tune these explicitly.  A valid run must record both
requested values, the escalation multiplier, the maximum attempts, the final
ridge actually used, and the resulting covariance residual and conditioning
proxy.  Failure modes:

- too small: Cholesky can produce nonfinite factors or enormous whitening;
- too large: the reset becomes a biased ridged covariance contract rather than
  the intended covariance-restoration approximation;
- bad scale: constrained or transformed models can receive artificial
  full-state noise from \(\lambda I\).

## Required Implementation Changes

- Add `contract_e_reset_tf.py` with local reset helpers and a Cholesky-ridge
  reset function.
- Add `--contract-e-reset-factorization` with choices `cholesky-ridge` and
  `eigh-support`; keep `eigh-support` as the default until broader evidence
  promotes the new route.
- Add `--chol-ridge-rel`, `--chol-ridge-abs`, `--chol-ridge-escalation`, and
  `--chol-ridge-max-attempts`, validate them, and record them in Phase 2 and
  Phase 3 manifests along with the realized maximum ridge used.
- Keep the material Phase 3 blocker in place.
- Add local CPU-only reset tests with `CUDA_VISIBLE_DEVICES=-1`.
- Add static tests that the Cholesky-ridge helper does not use
  `tf.linalg.eigh`, `GradientTape`, Jacobian, or `ForwardAccumulator`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Contract E reset avoid the unstable eigensystem factorization using an explicit Cholesky ridge? |
| Baseline/comparator | Local tiny reset fixture and static source inspection. |
| Primary pass criterion | Cholesky-ridge reset returns finite particles, mean residual is small, covariance residual is reported, and the helper contains no hidden eigensystem/autodiff fallback. |
| Veto diagnostics | Nonfinite Cholesky factors/output, missing lambda manifest fields, hidden `tf.linalg.eigh` in Cholesky helper, hidden `GradientTape`/Jacobian/ForwardAccumulator, or removal of the material blocker. |
| Explanatory only | Full-filter smoke, covariance residual magnitude, Cholesky diagonal conditioning proxy. |
| Not concluded | Full manual reverse-scan implementation, exact unridged covariance restoration, LGSSM gradient correctness, SIR/SV validity, HMC readiness, or production readiness. |

## Stop Conditions

Stop if Claude review rejects the policy, if the Cholesky route cannot be
implemented without hidden eigensystem/autodiff fallbacks, if local reset tests
produce nonfinite output, or if any artifact weakens the material Phase 3
blocker.
