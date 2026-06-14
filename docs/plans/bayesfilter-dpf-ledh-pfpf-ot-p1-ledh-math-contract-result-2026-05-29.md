# P1 Result: LEDH Math Contract

Date: 2026-05-29

## Decision

`P1_LEDH_MATH_CONTRACT_ACCEPTED`

## Contract

For ancestor `x_{t-1}`, pre-flow proposal `x0 ~ q0`, transition mean
`m_prior = A x_{t-1}`, transition covariance `Q`, observation `y`, local
observation map `h`, Jacobian `H = Dh(x0)`, and observation covariance `R`, the
finite-step local Gaussian closure uses:

- residual `r = y - h(x0)` with fixture-specific angle wrapping;
- pseudo-observation `z = H x0 + r`;
- posterior precision `Q^{-1} + H' R^{-1} H`;
- posterior mean `m_post = P_post (Q^{-1} m_prior + H' R^{-1} z)`;
- frozen local-affine map `x1 = m_post + L_post L_prior^{-1}(x0 - m_prior)`;
- forward log determinant `log |det(L_post L_prior^{-1})|`.

The nonlinear range-bearing use is a local proposal mechanism only; it is not
an exact nonlinear filter identity.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| wrong default architecture | pass | Contract supports LEDH-PF-PF proposal correction. |
| bootstrap-proposal overclaim | pass | Bootstrap proposal appears only as comparator/q0 seed path. |
| OT-resampling overclaim | pass | OT is not part of the proposal density correction. |
| missing stop conditions | pass | Singular covariance, missing Jacobian, missing log-det, or nonlinear exactness overclaim block. |
| hidden production/monograph drift | pass | Artifact only; no production or monograph edits. |
| contamination | pass | No vendored/student/highdim authority used. |

## What Is Not Concluded

No continuous-time EDH ODE exactness, nonlinear correctness, posterior
correctness, HMC readiness, production readiness, NAWM-scale readiness, or
monograph claim.
