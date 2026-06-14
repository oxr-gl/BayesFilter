# P3 Result: Nonlinear Local Linearization

Date: 2026-05-29

## Decision

`P3_RANGE_BEARING_LOCAL_LINEARIZATION_ACCEPTED`

## Result

The range-bearing fixture uses analytic TF/TFP Jacobian
`range_bearing_jacobian_tf` for `[sqrt(px^2 + py^2), atan2(py, px)]` with
angle residual wrapping from the existing fixture.  The local closure is used
only as a proposal mechanism.  UKF remains approximate and proxy-only.

The P9 integrated run records finite local Jacobian singular values and
range-bearing proxy diagnostics:

- median LEDH state RMSE to UKF: `0.07742171157461389`;
- median LEDH latent position RMSE: `0.08208559692155928`;
- median LEDH observation proxy RMSE: `0.1141841886622492`;
- min LEDH Jacobian singular value: `0.643116090267122`.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| wrong baseline | pass | UKF is approximate, not ground truth. |
| proxy overclaim | pass | RMSE rows are proxy diagnostics only. |
| missing stop conditions | pass | Near-origin/Jacobian/finiteness failures veto. |
| OT overclaim | pass | Sinkhorn is resampling component only. |
| drift/contamination | pass | No production, monograph, vendored, or high-dimensional lane edits. |

## What Is Not Concluded

No UKF ground truth, nonlinear posterior correctness, production readiness, HMC
readiness, NAWM-scale readiness, or monograph claim.
