# P11 Zhao-Cui TT Derivation Ledger

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports."
- Zhao-Cui companion code audit snapshot at `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

what_is_not_concluded:
- No complete analytical derivative for the adaptive stochastic companion code.
- No HMC readiness.
- No production BayesFilter implementation.
- No posterior accuracy or paper-figure replication.
- No default-method recommendation.

## Source And Code Anchors

Paper anchors:
- Algorithm 1 constructs the nonseparable density
  \(q_t(x_t,\theta,x_{t-1})=\widehat\pi(x_{t-1},\theta\mid y_{1:t-1})
  f(x_t\mid x_{t-1},\theta)g(y_t\mid x_t,\theta)\), then integrates its TT
  approximation to obtain a normalizing constant.
- Equation (13) gives the squared-TT defensive approximation
  \(\widehat\pi(x)=\phi(x)^2+\tau\lambda(x)\) and
  \(\widehat z=\int\widehat\pi(x)\,dx\).
- Algorithm 2 applies the squared-TT construction to sequential filtering.
- Section 4.1 states that the exact normalizer \(z_t\) is the evidence and
  explains the two-step approximation \(q_t\rightarrow\widehat\pi_t\).

Code anchors:
- `models/full_sol.m`: `sol.logmarginal_likelihood = sol.logmarginal_likelihood + log(sirt.z) - const`.
- `deep-tensor.dev/src/SIRT.m`: `potential_to_density` maps potential values
  to square-root density values for SIRT.
- `deep-tensor.dev/src/@TTSIRT/TTSIRT.m`: `approx = TTFun(func, arg, opt, 'var', var)`.
- `deep-tensor.dev/src/@TTSIRT/marginalise.m`: repeated mass-weighted QR
  contractions compute `obj.fun_z`; `obj.z = obj.fun_z + obj.tau`.

## Derivation Decision

The LaTeX note derives a complete fixed-branch derivative of
\[
  \widehat\ell_T^{\rm TT}(\alpha)
  =
  \sum_t\{\log\widehat z_t(\alpha)-c_t(\alpha)\}.
\]

The derivation uses \(\alpha\) for external differentiation parameters and
\(\vartheta\) for Zhao-Cui's learned parameter coordinate.  This avoids
confusing the filtering posterior coordinate with the parameter being
differentiated by HMC or an outer optimizer.

## Fixed-Branch Assumptions

The derivative requires fixed:
- basis and domain maps;
- variable ordering;
- TT ranks;
- interpolation/cross points;
- ALS sweep count and selected local solves;
- random/debug samples;
- truncation decisions;
- QR/SVD sign and active-subspace branches;
- defensive term policy;
- preconditioner branch;
- selected minimizer for the stabilizing constant \(c_t\).

If these change, the note classifies the derivative as branch-local rather than
an ordinary same-scalar gradient.

## Main Formula

If
\[
  \phi_t(r)=G_{t,1}(r_1)\cdots G_{t,D}(r_D)
\]
and \(R_{t,0}\) is the direct mass-matrix contraction of \(\phi_t^2\), then
\[
  \partial_i\widehat\ell_T^{\rm TT}
  =
  \sum_t
  \left[
  \frac{\partial_i R_{t,0}+\partial_i\tau_t}
       {R_{t,0}+\tau_t}
  -
  \partial_i c_t
  \right].
\]

The differentiated contraction is computed recursively:
\[
\partial_i R_{k-1}
 =
 \sum_{a,b}M_k[a,b]\{
 \partial_i C_{k,a}R_kC_{k,b}^\top
 +C_{k,a}\partial_iR_kC_{k,b}^\top
 +C_{k,a}R_k\partial_iC_{k,b}^\top
 \}.
\]

## Unclosed Implementation Obligations

The note intentionally leaves the following as future implementation work:
- deriving core sensitivities for the exact fixed TT-cross/ALS branch chosen in
  a BayesFilter prototype;
- matching the derivative scalar to either the direct mass contraction or the
  companion code's QR contraction;
- finite-difference checking under frozen branches;
- deciding whether \(c_t\) is differentiated or fixed numerically and naming
  the scalar accordingly.

Decision:
`FIXED_BRANCH_ANALYTICAL_DERIVATIVE_DERIVED_ADAPTIVE_CODE_NOT_DERIVED`
