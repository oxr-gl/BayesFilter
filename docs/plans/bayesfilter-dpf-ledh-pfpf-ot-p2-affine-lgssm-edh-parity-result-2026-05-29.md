# P2 Result: Affine LGSSM EDH Parity

Date: 2026-05-29

## Decision

`P2_AFFINE_LGSSM_EDH_PARITY_ACCEPTED`

## Result

The LGSSM fixture uses linear observation matrix `C`, so the LEDH local
linearization is exactly the model observation matrix.  The implemented
finite-step local Gaussian map therefore uses the same one-step Gaussian
conditioning objects as the Kalman reference for the local proposal step:
`Q`, `R`, `A`, `C`, prior mean, posterior mean/covariance, and
`log |det(L_post L_prior^{-1})|`.

P8 validates this contract in the integrated runner by recording finite
corrected weights, finite frozen local-affine log-dets, finite singular values,
and Kalman-comparator smoke metrics.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | LGSSM fixture and Kalman reference are current TF/TFP files. |
| wrong baseline | pass | Kalman is exact only for this LGSSM. |
| proxy overclaim | pass | Parity is one-step local Gaussian/affine evidence, not full scientific validation. |
| missing stop conditions | pass | Cholesky/log-det/finiteness failures veto. |
| drift/contamination | pass | No production, monograph, vendored, or high-dimensional lane edits. |

## What Is Not Concluded

No nonlinear filter correctness, HMC readiness, posterior correctness,
production readiness, NAWM-scale readiness, or monograph claim.
