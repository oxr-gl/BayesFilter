# P76 Phase 1 Result: Mathematical UKF Initializer Contract

metadata_date: 2026-06-18
status: PHASE1_PASSED_CLAUDE_AGREE_READY_FOR_PHASE2
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-subplan-2026-06-18.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 1 defines the UKF-informed initializer \(h_0\) for the fixed-variant
trainable squared-TT density.  It does not edit implementation code, run
training diagnostics, claim lower-gate repair, or authorize a large
mini-batch pilot.

The design intentionally closes the P75 planning mistake.  P75 tested random
initialization, calibrated constant initialization, and source-route prefit.
Those are historical failed methods.  P76 tests a different hypothesis:

\[
  (m_U,P_U)
  \longrightarrow
  \hbox{UKF-whitened local frame}
  \longrightarrow
  h_0
  \longrightarrow
  \hbox{mini-batch stochastic density training}.
\]

The UKF object remains `scout_not_truth`.  It supplies geometry only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What exact UKF-moment initializer should be implemented before mini-batch density training? |
| Comparator | P75 historical failures: random, calibrated constant, and source-route prefit. |
| Primary criterion | Define \(m_U,P_U\), the physical-to-local moment map, covariance floors, \(h_0\), the projection objective, mini-batch handoff, and audit exclusion. |
| Veto diagnostics | Source-route prefit renamed as UKF; UKF promoted to truth; missing covariance validity rule; missing local-coordinate map; no implementable projection; audit leakage; large-pilot authorization. |
| Explanatory only | UKF spectra, local guide conditioning, initializer projection residuals, later mini-batch losses, later holdout/audit residuals. |
| Not concluded | No implementation, no validation/HMC readiness, no scaling result, no source-faithfulness, no final rank/sample policy. |

## Anchors And Claim Boundary

The p50 monograph section permits a UKF only as a scout for centers, scales,
and covariance structure, and explicitly says the UKF equations are not a
correctness oracle, exact likelihood, or HMC-readiness result.  The current
code enforces this boundary through `P52_UKF_SCOUT_CLAIM =
"scout_not_truth"` and `UKFScoutResult.nonclaims`.

The implementation anchor available today is:

- `bayesfilter/highdim/ukf_scout.py`: `spatial_sir_ukf_scout(...)` returns
  `mean_path`, `covariance_path`, `scale_path`, `covariance_eigenvalues`, and
  nonclaims.
- `bayesfilter/highdim/stochastic_density_training.py`: the opt-in
  `TrainableFunctionalTT` surface represents
  \[
    \rho_\theta(z)=h_\theta(z)^2+\tau\lambda(z),
    \qquad
    q_\theta(z)=\rho_\theta(z)/Z_\theta .
  \]

This initializer is a BayesFilter fixed-variant extension.  It is not
`source_faithful` Zhao--Cui behavior.  It also is not the failed
source-route prefit from P75.

## Definition 1: UKF State Moments

For each filtering time \(s\), let
\[
  m_s^U=m_{s|s}^U,\qquad P_s^U=P_{s|s}^U
\]
denote the filtered mean and covariance in physical state coordinates
returned by the UKF scout.  The current UKF surface provides these moments as
`mean_path[s]` and `covariance_path[s]`.

For an adjacent fixed-variant target at time \(t\), write
\[
  r_t=(x_t,x_{t-1})\in\mathbb R^D,\qquad D=2m .
\]
The Phase 1 default adjacent UKF moment is
\[
  m_A^U=
  \begin{bmatrix}
    m_t^U\\
    m_{t-1}^U
  \end{bmatrix},
  \qquad
  P_A^U=
  \begin{bmatrix}
    P_t^U & 0\\
    0 & P_{t-1}^U
  \end{bmatrix}.
\]
For \(t=1\), the second block uses `mean_path[0]` and `covariance_path[0]`
from the current UKF scout result.  If either block is absent or nonfinite,
the initializer blocks.

The block-diagonal convention is a deliberate first implementation contract:
the current UKF result stores filtered marginal covariances, not a smoothed
cross-time covariance.  This loses cross-time covariance in the initializer,
but it does not change the scientific target; the subsequent mini-batch
density objective still evaluates the fixed adjacent target.  A cross-time
UKF smoother would be a later reviewed extension.

## Definition 2: Stabilized Covariance

Let
\[
  S_A^U=\frac12(P_A^U+(P_A^U)^\top).
\]
Let
\[
  S_A^U=V\operatorname{diag}(\lambda_1,\ldots,\lambda_D)V^\top
\]
be its symmetric eigendecomposition.  With UKF jitter
\(\epsilon_{\rm abs}>0\) and relative floor \(\epsilon_{\rm rel}>0\), define
\[
  \epsilon_\lambda
  =
  \max\{\epsilon_{\rm abs},\epsilon_{\rm rel}\max_i|\lambda_i|\},
  \qquad
  \bar\lambda_i=\max\{\lambda_i,\epsilon_\lambda\}.
\]
The stabilized covariance is
\[
  \bar P_A^U=V\operatorname{diag}(\bar\lambda_1,\ldots,\bar\lambda_D)V^\top .
\]

The Phase 1 defaults are inherited from the scout scale:
\[
  \epsilon_{\rm abs}=10^{-9},\qquad \epsilon_{\rm rel}=10^{-8}.
\]
The initializer blocks if any eigenvalue is nonfinite, if
\(\max_i|\lambda_i|\) is nonfinite, or if the stabilized covariance fails a
finite symmetric-positive-definite check.

## Definition 3: UKF-Whitened Local Coordinates

Let
\[
  C_U=V\operatorname{diag}(\sqrt{\bar\lambda_1},\ldots,\sqrt{\bar\lambda_D})
\]
and let \(\gamma>0\) be a frozen coverage radius.  The Phase 1 default is
\[
  \gamma=4 .
\]
Define the physical-to-local map
\[
  r=m_A^U+L_Uz,\qquad L_U=\gamma C_U,\qquad z\in\Omega=[-1,1]^D .
\]
Equivalently,
\[
  z=L_U^{-1}(r-m_A^U).
\]

If \(R\) is a Gaussian random vector with mean \(m_A^U\) and covariance
\(\bar P_A^U\), then
\[
  Z=L_U^{-1}(R-m_A^U)
\]
has covariance \(\gamma^{-2}I_D\).  Thus the UKF guide becomes isotropic and
factorized in the local coordinates.

The map never clips a physical state into the local domain.  If later
training samples map to invalid physical model states, the training target
must handle that by a reviewed target-evaluation rule or block.  Phase 1 does
not change the model support.

## Proposition 1: Local UKF Guide Factorizes

Define the truncated local UKF guide on \(\Omega\) by
\[
  q_U(z)
  =
  Z_U^{-1}
  \exp\left(-\frac{\gamma^2}{2}\|z\|_2^2\right)
  \mathbf 1_{\Omega}(z),
\]
where \(Z_U\) is the finite normalizing constant with respect to the product
mass measure used by the tensor-product basis.  Then
\[
  q_U(z)=\prod_{k=1}^D q_{U,k}(z_k)
\]
and
\[
  h_U(z):=\sqrt{q_U(z)}
  =
  \prod_{k=1}^D h_{U,k}(z_k).
\]

### Proof

The exponent separates:
\[
  \|z\|_2^2=\sum_{k=1}^D z_k^2.
\]
The domain \(\Omega=[-1,1]^D\) and the basis mass measure are products across
coordinates.  Hence the normalizing constant factors into one-dimensional
normalizers, and the exponential factors into one-dimensional exponentials.
Taking the positive square root preserves the product form.

## Definition 4: Projected Initial Square Root \(h_0\)

Let \(\{\psi_{k,\ell}\}_{\ell=0}^p\) be the one-dimensional basis on coordinate
\(k\).  Let
\[
  a_{k,\ell}
  =
  \arg\min_{a}
  \int_{-1}^1
  \left[
    h_{U,k}(z)-\sum_{\ell=0}^p a_\ell\psi_{k,\ell}(z)
  \right]^2 d\nu_k(z)
\]
denote the one-dimensional \(L^2(\nu_k)\) projection coefficients, where
\(\nu_k\) is the active one-dimensional mass/reference convention carried by
the `ProductBasis`.  In code this is implemented by deterministic
one-dimensional quadrature or the existing basis mass/projection machinery,
not by source-route target samples.

The rank-one projected square root is
\[
  h_0^{(1)}(z)
  =
  \prod_{k=1}^D
  \left(
    \sum_{\ell=0}^p a_{k,\ell}\psi_{k,\ell}(z_k)
  \right).
\]
This is stored as a tensor train by placing the projected coefficient vector
for each coordinate on the main channel.

For requested TT rank tuple \((1,R,\ldots,R,1)\), the Phase 1 rule embeds
\(h_0^{(1)}\) into channel 0 and initializes the remaining channels by the
small deterministic seeded-channel rule from P70:
`fixed_hmc_seeded_channel_paths_v1`.  The seed channels are not a new target;
they keep rank channels trainable during the later mini-batch objective.

The initializer rule name is:

`ukf_whitened_gaussian_sqrt_projection_v1`

## Proposition 2: Degree Two Is The First Curvature-Carrying Basis

Assume the one-dimensional basis contains a constant basis function and a
linear degree-one basis function that is odd about zero, as in the normalized
Legendre basis used on \([-1,1]\).  The local UKF square-root factor
\[
  h_{U,k}(z_k)\propto \exp(-\gamma^2 z_k^2/4)
\]
is even.  Therefore its projection onto the degree-one odd basis is zero.
Consequently, a degree-one UKF-whitened Gaussian projection carries no
one-dimensional curvature information beyond the constant term.  Degree
\(p\ge2\) is the first polynomial degree that can encode the Gaussian
curvature of the UKF guide.

### Proof

The product of an even function and an odd function is odd.  Its integral over
the symmetric interval \([-1,1]\) is zero under the symmetric basis mass
measure.  Thus every odd linear coefficient vanishes.  The first nonconstant
even polynomial direction is degree two.

This is a design consequence, not a validation claim.  A degree-one smoke may
still test shapes, but it is not an adequate UKF-curvature warm-start test.

## Mini-Batch Density Handoff

After \(h_0\) is built, P76 hands off to the existing trainable squared-TT
surface:
\[
  \rho_\theta(z)=h_\theta(z)^2+\tau\lambda(z),
  \qquad
  q_\theta(z)=\rho_\theta(z)/Z_\theta .
\]
The trainable parameters are initialized from the \(h_0\) cores.  Then each
mini-batch draws fresh training-eligible local points \(z_i\), evaluates the
actual fixed adjacent target through the frozen physical map
\[
  r_i=m_A^U+L_Uz_i,
\]
and forms target square-root values
\[
  y_i=\exp\{-\tfrac12(U_t(z_i)-c_t)\},
\]
or the reviewed equivalent target-value convention already used by the
stochastic density objective.  The mini-batch objective is the density
objective, not a source-route prefit objective.

Audit samples, audit lines, validation rows, and any diagnostic-only samples
are excluded from initialization, mini-batch training, stopping, and
hyperparameter selection.  They may be evaluated after a frozen result only as
explanatory or veto diagnostics under a reviewed subplan.

## Why This Is Not Source-Route Prefit

P75 source-route prefit fit \(h_\theta\) directly to source-route square-root
target values on a fixed finite cloud before density training.  That was the
method that failed.

P76 instead:

1. uses only UKF moments \((m_U,P_U)\) to define a Gaussian local guide;
2. analytically projects the guide's square root into the product basis;
3. embeds that projection into TT cores as \(h_0\);
4. trains on fresh mini-batches from the actual fixed target afterward.

No source-route target values are used to construct \(h_0\).  No P75
source-route prefit arm is repeated as a live repair ladder.

## Failure Conditions

The Phase 2 implementation surface must block if:

- the requested \(m_U\) or \(P_U\) block is absent or nonfinite;
- covariance stabilization cannot produce finite SPD \(\bar P_A^U\);
- the local affine map \(L_U\) is nonfinite or singular;
- the product basis cannot provide deterministic one-dimensional projection
  coefficients;
- the requested polynomial degree is less than 2 for a curvature-carrying UKF
  warm-start test;
- audit records enter initialization, mini-batch training, stopping, or
  selection;
- the implementation surface tries to use source-route prefit as \(h_0\).

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to Phase 2 implementation-surface planning | Satisfied by the definitions above | No Phase 1 veto identified locally | Whether current basis/projection utilities support a clean TensorFlow implementation without ad hoc NumPy | Draft and review Phase 2, then name exact code/test surfaces for Phase 3 | No implementation, no empirical success, no lower-gate repair, no validation/HMC readiness |

## Phase 2 Handoff

Phase 2 must convert this mathematical contract into an implementation surface.
It must name exact functions/classes, tests, manifests, and CPU-only checks for:

- extracting adjacent \(m_U,P_U\) from `UKFScoutResult`;
- stabilizing \(P_U\);
- building \(m_A^U,L_U,\Omega\);
- projecting \(h_U\) into product-basis TT cores;
- embedding rank-one cores into requested rank with deterministic seed paths;
- initializing `TrainableFunctionalTT`;
- preserving audit separation;
- preparing a tiny CPU-only smoke that tests the initializer before any large
  mini-batch pilot.
