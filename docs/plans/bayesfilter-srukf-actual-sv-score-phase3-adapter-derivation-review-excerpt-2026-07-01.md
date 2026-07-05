# Phase 3 Adapter Derivation Review Excerpt

Date: 2026-07-01

Source provenance:

- Full source path: `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- Section label: `sec:bf-hd-actual-sv-srukf-augmented-adapter`
- Current line neighborhood when excerpt was created: approximately 351--580.

Review scope:

- Review only whether this excerpt is internally consistent and boundary-safe
  as the Phase 3 actual-SV augmented-noise adapter derivation for the generic
  factor-propagating SR-UKF score contract.
- This excerpt is a review packet, not an independent source of truth.

## Boundary

The adapter is for the raw-observation Gaussian-closure surrogate scalar.  It
is not an exact actual-SV likelihood route and is not a same-target route to the
transformed actual-SV likelihood.

Forbidden admissions:

- no exact actual-SV likelihood claim;
- no same-target transformed-likelihood claim;
- no `GradientTape` score admission;
- no historical SVD/eigenderivative score admission;
- no strict-SPD principal-root derivative admission.

## Model And Parameterization

For one panel coordinate:

\[
  H_t=\gamma H_{t-1}+U_t,\qquad
  U_t\sim N(0,\sigma^2),\qquad
  Y_t=\beta \exp(H_t/2)E_t,\qquad
  E_t\sim N(0,1).
\]

The candidate score contract uses
\[
  \theta=(\theta_\gamma,\theta_\beta),\qquad
  \gamma=\Phi(\theta_\gamma),\qquad
  \beta=\exp(\theta_\beta),\qquad
  \sigma \text{ fixed}.
\]

Thus
\[
  \partial_{\theta_\gamma}\gamma=\varphi(\theta_\gamma),
  \qquad
  \partial_{\theta_\beta}\beta=\beta,
  \qquad
  \partial_{\theta_i}\sigma=0.
\]

## Three-Coordinate Augmented Variable

The default sigma-point variable is the pre-observation uncertainty variable
\[
  A_t=(H_{t-1},U_t,E_t)^\top .
\]

If
\[
  H_{t-1}\mid y_{1:t-1}\approx N(m_{t-1},c_{t-1}c_{t-1}^\top),
\]
then
\[
  A_t\mid y_{1:t-1}
  \approx
  N\!\left(
    \begin{bmatrix}m_{t-1}\\0\\0\end{bmatrix},
    C_{a,t}C_{a,t}^\top
  \right),
  \qquad
  C_{a,t}
  =
  \begin{bmatrix}
    c_{t-1} & 0 & 0\\
    0 & \sigma & 0\\
    0 & 0 & 1
  \end{bmatrix}.
\]

The key requirement is that lagged latent state, state innovation, and
observation shock are all present.

## Maps

The maps sent to the generic SR-UKF backend are
\[
  X_\theta(A_t)=\gamma H_{t-1}+U_t,
  \qquad
  Z_\theta(A_t)=\beta\exp(X_\theta(A_t)/2)E_t .
\]

Here \(Z_\theta(A_t)\) is the raw predicted observation coordinate used by the
Gaussian closure.  It is not the transformed datum \(z_t=\log(y_t^2)\).

For a placed point \(a^{(j)}=(h_-^{(j)},u^{(j)},e^{(j)})\), let
\[
  x^{(j)}=X_\theta(a^{(j)}).
\]

The pointwise derivatives are
\[
  D_aX_\theta(a^{(j)})=
  \begin{bmatrix}\gamma&1&0\end{bmatrix},
  \qquad
  \partial_{\theta_\gamma}X_\theta(a^{(j)})
  =
  \varphi(\theta_\gamma)h_-^{(j)},
  \qquad
  \partial_{\theta_\beta}X_\theta(a^{(j)})=0,
\]
\[
  D_aZ_\theta(a^{(j)})
  =
  \beta\exp(x^{(j)}/2)
  \begin{bmatrix}
    \frac12\gamma e^{(j)}&
    \frac12 e^{(j)}&
    1
  \end{bmatrix},
\]
\[
  \partial_{\theta_\gamma}Z_\theta(a^{(j)})
  =
  \frac12\beta\exp(x^{(j)}/2)e^{(j)}
  \varphi(\theta_\gamma)h_-^{(j)},
  \qquad
  \partial_{\theta_\beta}Z_\theta(a^{(j)})
  =
  \beta\exp(x^{(j)}/2)e^{(j)}.
\]

These derivatives are pointwise map derivatives only.  They do not differentiate
a principal matrix square root, an eigensystem, an SVD basis, or an autodiff
tape.

## Initial Branch

When a stationary initialization is used:

\[
  H_0\sim N\!\left(0,\frac{\sigma^2}{1-\gamma^2}\right),
  \qquad |\gamma|<1.
\]

The handoff derivatives are
\[
  \partial_{\theta_\gamma}m_0=0,\qquad
  \partial_{\theta_\beta}m_0=0,
\]
\[
  \partial_{\theta_\gamma}
  \frac{\sigma^2}{1-\gamma^2}
  =
  \frac{2\sigma^2\gamma}{(1-\gamma^2)^2}\varphi(\theta_\gamma),
  \qquad
  \partial_{\theta_\beta}
  \frac{\sigma^2}{1-\gamma^2}=0.
\]

If the factor-propagating backend consumes the scalar stationary factor
\[
  c_0=\sigma(1-\gamma^2)^{-1/2}
\]
rather than the variance, the corresponding fixed-\(\sigma\) branch derivative
is
\[
  \partial_{\theta_\gamma}c_0
  =
  \sigma\gamma(1-\gamma^2)^{-3/2}\varphi(\theta_\gamma),
  \qquad
  \partial_{\theta_\beta}c_0=0.
\]

If a nonstationary initialization is chosen, it must replace this law and these
derivatives explicitly.

## Score Handoff

Given placed points from the augmented law, the generic SR-UKF backend computes
\[
  \bar x_t,\quad \bar y_t,\quad
  P_{xx,t,\star},\quad S_{t,\star},\quad P_{xy,t,\star}
\]
from propagated pairs
\[
  (X_\theta(a_t^{(j)}),Z_\theta(a_t^{(j)})).
\]

The one-step raw Gaussian-closure surrogate contribution is
\[
  \widehat\ell_t^{\rm rawGC}(\theta)
  =
  -\frac12
  \left[
    \log(2\pi)+\log S_{t,\star}
    +(y_t-\bar y_t)^2S_{t,\star}^{-1}
  \right].
\]

Its analytical score is the specialization of the generic SR-UKF score with
\[
  v_t=y_t-\bar y_t,
\]
followed by the generic filtered-state derivative handoff.  The cumulative
surrogate score is
\[
  \partial_{\theta_i}
  \sum_{t=1}^T\widehat\ell_t^{\rm rawGC}(\theta)
  =
  \sum_{t=1}^T
  \partial_{\theta_i}
  \widehat\ell_t^{\rm rawGC}(\theta),
  \qquad i\in\{\gamma,\beta\}.
\]

This is the score of the raw actual-SV Gaussian-closure surrogate scalar, not
the score of the transformed actual-SV likelihood.

## Collapsed-Route Fence

A two-coordinate collapsed-process specialization may be used only after the
three-coordinate adapter has been audited.  Its proof obligation is the scalar
Gaussian law equivalence
\[
  (H_t^-,E_t)
  =
  (\gamma H_{t-1}+U_t,E_t)
  \sim
  N\!\left(
    \begin{bmatrix}\gamma m_{t-1}\\0\end{bmatrix},
    \begin{bmatrix}
      \gamma^2 c_{t-1}c_{t-1}^\top+\sigma^2 & 0\\
      0 & 1
    \end{bmatrix}
  \right),
\]
together with derivative equivalence for the mean and factor handoff.  A
collapsed route that cannot demonstrate this law and derivative equivalence is a
separate approximation and cannot be used as the admitted SR-UKF analytical
score route.
