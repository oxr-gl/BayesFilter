# P10 Zhao-Cui TT Filtering Scalar Ledger

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui JMLR 2024.
- Companion code `models/full_sol.m`, `@TTSIRT/marginalise.m`, `AbstractIRT.m`.

what_is_not_concluded:
- No exact likelihood claim.
- No HMC target readiness claim.
- No posterior accuracy claim.
- No complete BayesFilter scalar implementation claim.

## Paper Scalar

The exact recursion uses the conditional evidence
\[
  p(y_t\mid y_{1:t-1})
\]
in equations (9)--(10).  The joint posterior normalizer at time \(t\) is
identified in Section 4.1 as
\[
  z_t
  =
  \int \pi_t(x_t,\theta,x_{t-1})\,dx_t\,d\theta\,dx_{t-1},
\]
and the paper states that this is the evidence \(p(y_{1:t})\).

Algorithm 1 defines a TT approximation to the unnormalized joint density and
computes a normalizing constant
\[
  c_t
  =
  \int \widehat\pi_t(x_t,\theta,x_{t-1}\mid y_{1:t})
      \,dx_t\,d\theta\,dx_{t-1}.
\]

Algorithm 2 uses the squared-TT approximation
\[
  \widehat\pi_t(x_t,\theta,x_{t-1}\mid y_{1:t})
  =
  \phi_t(x_t,\theta,x_{t-1})^2
  +
  \tau_t\lambda(x_t)\lambda(\theta)\lambda(x_{t-1}),
\]
with normalizer
\[
  \widehat z_t
  =
  \int \widehat\pi_t(x_t,\theta,x_{t-1}\mid y_{1:t})
      \,dx_t\,d\theta\,dx_{t-1}.
\]

## Code Scalar

In `models/full_sol.m`, `reapprox` builds `sirt = TTSIRT(...)`, and then
updates:
\[
  \texttt{sol.logmarginal\_likelihood}
  \leftarrow
  \texttt{sol.logmarginal\_likelihood}
  +
  \log(\texttt{sirt.z})-\texttt{const}.
\]

In `@TTSIRT/marginalise.m`, the squared-TT normalizer is computed through
successive marginalization and stored as:
\[
  \texttt{obj.z}=\texttt{obj.fun\_z}+\texttt{obj.tau}.
\]

The scalar is therefore identifiable as a declared approximate evidence-like
quantity built from the squared-TT normalizer and the stabilizing constant shift
used in the code.

## BayesFilter Notation

The conservative BayesFilter scalar is:
\[
  \widehat\ell_T^{\rm TT}(\theta)
  =
  \sum_{t=1}^T \log \widehat Z_t^{\rm TT}(\theta),
\]
where \(\widehat Z_t^{\rm TT}\) is the normalizer of the fixed-branch
squared-TT approximation to
\[
  \widehat q_t(x_t,\theta,x_{t-1})
  =
  \widehat\pi_{t-1}(x_{t-1},\theta)
  f_\theta(x_t\mid x_{t-1})
  g_\theta(y_t\mid x_t).
\]

The word "fixed-branch" is essential.  It means fixed basis/domain, fixed
variable order, fixed rank pattern, fixed interpolation/cross points, fixed
rounding decisions, fixed defensive term, fixed preconditioner branch, and
fixed smooth model maps.  If any of those change with \(\theta\), the ordinary
gradient is at best branch-local.

## Decision

`FILTERING_SCALAR_IDENTIFIED_AS_APPROXIMATE_FIXED_BRANCH_CANDIDATE`

This is enough to promote Zhao-Cui as a high-dimensional filtering candidate.
It is not enough to claim HMC readiness or an implemented analytical gradient
without the additional fixed-branch derivative machinery.
