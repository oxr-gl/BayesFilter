# P70 Phase 3 Result: UKF-Guided Branch-Builder Design

metadata_date: 2026-06-16
status: PHASE3_PASSED_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 3 designs the fixed branch-builder map \(G_t\).  It does not implement
the map, edit p50, or run diagnostics.  The design is scoped to the current
P70 author-SIR lane, where the adjacent fitting block has dimension
\(D=2m=36\) and no unknown static parameter block is present.  A future
parameter-learning block would require a separate reviewed extension.

The design goal is:

> Use the UKF only to freeze localization and design choices, then fit the
> actual Zhao--Cui adjacent target on the frozen branch.

This is stronger than fitting only at one chosen \(\beta\).  For HMC use, the
branch choices are frozen, while the fixed fitting rule remains a deterministic
map of the target values \(y_j(\beta)\) to fitted cores
\(\phi_t^B(\cdot;\beta)\).

## Source And Claim Boundary

| Operation | Classification | Direct anchors | Consequence |
| --- | --- | --- | --- |
| Adjacent filtering target and marginalization over the old state | `source_faithful` mathematical route | Zhao--Cui Eqs. (9)--(11), Algorithm 1/Eq. (12) | The target being fitted remains the adjacent source-route target, not a UKF Gaussian surrogate. |
| Squared square-root TT density and defensive term | `source_faithful` mathematical route | Zhao--Cui Eq. (13), Algorithm 2, Eq. (15), Eq. (16) | The fixed branch keeps \(\phi_t^2+\tau_t\lambda_t\). |
| Squared-TT marginalization and normalizer contractions | `source_faithful` mathematical route | Zhao--Cui Proposition 2/Eq. (14), Section 3.2 | Normalizer and retained-density contractions stay on the squared-TT route. |
| Author SIR benchmark dimensions and solver route | author-source anchored route component, fixed by BayesFilter for replay | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`, `:39-56` | Establishes \(d=0,m=18,T=20\), source sample count/options, and use of `full_sol`; does not establish UKF guidance. |
| Author pushed-sample recursion and TTSIRT construction | author-source anchored route component, fixed by BayesFilter for replay | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`, `:46-70`, `:84-124` | Establishes propagated samples, weighted localization, sample splitting, TTSIRT construction, and log-normalizer update; does not make deterministic replay source-faithful. |
| Author weighted localization rule | author-source anchored route component, fixed by BayesFilter for replay | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47` | Establishes weighted mean/covariance, Cholesky regularization, optional quantile stretch, and expansion; does not establish UKF scale selection. |
| Deterministic seeds, frozen design rows, fixed rank, fixed basis, fixed sweep policy, and replayable branch identity | `fixed_hmc_adaptation` | p50 Definition `def:p50-fixed-branch`; p50 Proposition `prop:p50-fixed-adaptive-relation`; current manifest route `fitting.py:573-608` | These choices define a differentiable approximate scalar but are not adaptive Zhao--Cui parity. |
| UKF-guided center, scale, covariance orientation, and design support | `fixed_hmc_adaptation`; not source-faithful | p50 UKF scout section, Eqs. `eq:p52-ukf-pred-mean`--`eq:p52-ukf-update`; `ukf_scout.py:13-22`, `ukf_scout.py:140-267` | The UKF is a scout and preflight mechanism only.  It is not correctness evidence, rank truth, or HMC readiness evidence. |

## Branch-Builder Definition

Let \(\mathcal U_t\) denote the UKF scout record at time \(t\), containing
\((m_{s|s}^{U},P_{s|s}^{U})\) for \(s\le t\), finite scale summaries, covariance
spectra, and the `scout_not_truth` nonclaim.  Let \(\mathcal S_t\) denote the
source-route pushed sample record obtained from the previous retained object and
the current observation, using the Zhao--Cui adjacent target.  A retained object
is the previously stored fixed-branch approximation and its retained samples.
For the current d18 author-SIR lane, write the physical adjacent variable as
\[
  r_t=(x_t,x_{t-1})\in\mathbb R^{2m}.
\]

The P70 branch builder is a deterministic map
\[
  G_t(\mathcal U_t,\mathcal S_t,\theta_G)
  =
  (\mu_t,L_t,\Omega_t,\mathcal D_t,c_t,\mathcal M_t),
\]
where \(\theta_G\) is a recorded table of branch-builder hyperparameters and
\(\mathcal M_t\) is the branch-builder manifest payload.

### Localization

The following branch-builder hyperparameters are frozen before any fitting or
diagnostic output is observed:
\[
\begin{gathered}
  \epsilon_{\rm scale}=10^{-8},\quad
  \epsilon_{\rm corr}=10^{-12},\quad
  \epsilon_{\rm cov}=10^{-10},\\
  \alpha_C=0.25,\quad
  \gamma_t=4,\quad
  \rho_N=0.50,\quad
  \rho_W=0.50.
\end{gathered}
\]
The value \(\gamma_t=4\) is a fixed-HMC counterpart of the source expansion
factor used in the current author-SIR route; it is not tuned from repaired
diagnostics.

The center is the adjacent UKF scout center
\[
  \mu_t
  =
  \begin{bmatrix}
    m_{t|t}^{U}\\
    m_{t-1|t-1}^{U}
  \end{bmatrix}.
\]
For \(t=1\), the second block uses the UKF-filtered or initial distribution
recorded for time \(0\).  The branch is blocked if either required scout block
is absent or nonfinite.

Let \(D_t^U\) be the diagonal matrix of UKF marginal scales for
\((x_t,x_{t-1})\), floored by a predeclared \(\epsilon_{\rm scale}>0\).  Let
\widehat C_t^{S}\) be a source-sample correlation surrogate computed from the
finite pushed adjacent source rows in \(\mathcal S_t\).  The construction is:

1. keep only columns \(r_i\) with finite coordinates and finite positive
   source weights;
2. normalize the kept weights to \(\omega_i\);
3. compute the weighted source mean \(\bar r^S=\sum_i\omega_i r_i\);
4. compute the weighted covariance
   \(S_0^S=\sum_i\omega_i(r_i-\bar r^S)(r_i-\bar r^S)^\top\), and symmetrize it
   by \(S^S=(S_0^S+(S_0^S)^\top)/2\);
5. let \(d_k^S=\sqrt{\max(S^S_{kk},0)}\) and
   \(D_\epsilon^S=\operatorname{diag}(\max\{d_k^S,\epsilon_{\rm corr}\})\);
6. set
   \[
      \widehat C_t^S
      =
      (D_\epsilon^S)^{-1}S^S(D_\epsilon^S)^{-1}.
   \]

If the finite kept row count is less than two or the weighted effective sample
size is less than
\[
  E_{\rm corr,min}=\max\{4,\lceil 0.10\,N_{\rm finite}\rceil\},
\]
then \(\widehat C_t^S\) is set to \(I\) and the manifest records
`source_correlation_fallback_identity`.  Near-zero source variance in a
coordinate is handled by the \(\epsilon_{\rm corr}\) denominator floor; UKF
marginal scales still determine that coordinate's physical scale.

With predeclared correlation shrinkage
\[
  C_t^{B}=(1-\alpha_C)\widehat C_t^{S}+\alpha_C I,
  \qquad 0<\alpha_C\le 1.
\]
The branch covariance used for localization is
\[
  \Sigma_t^B
  =
  D_t^U C_t^B D_t^U+\epsilon_{\rm cov} I.
\]
The affine factor is
\[
  L_t=\gamma_t\,\operatorname{chol}(\Sigma_t^B),
\]
where \(\epsilon_{\rm cov}>0\) and \(\gamma_t>0\) are the frozen values above.
With finite inputs, positive floors, \(\alpha_C>0\), and
\(\epsilon_{\rm cov}>0\), this matrix is required to be symmetric positive
definite.  If a numerical check of symmetry, finiteness, or positive
definiteness fails, the branch blocks as `branch_covariance_invalid`; such a
block is an invalid-input or implementation-consistency blocker, not an
expected scientific diagnostic.  This hybrid keeps UKF scale guidance while
retaining source-sample correlation information for the adjacent block when
that information is well-defined.  It is a fixed-HMC adaptation, not a
source-faithful Zhao--Cui operation.

The local domain is
\[
  \Omega_t=[-1,1]^D,\qquad T_t(z)=\mu_t+L_tz.
\]
No design row is clipped into \(\Omega_t\).

### Coverage Gate

Let \(I_{\rm finite}\) be the finite kept source-row index set after the
filtering above, and let
\[
  z_i=L_t^{-1}(r_i-\mu_t),\qquad i\in I_{\rm finite}.
\]
The in-domain index set is
\[
  I_{\rm in}
  =
  \{i\in I_{\rm finite}:\max_{1\le k\le D}|z_{i,k}|\le 1\}.
\]
The counting convention is unresampled physical source rows; no multiplicity is
introduced by resampling.  Let
\[
  F_N=\frac{|I_{\rm in}|}{|I_{\rm finite}|},\qquad
  F_W=\sum_{i\in I_{\rm in}}\omega_i,\qquad
  N_{\rm in,min}=\max\{4,\lceil D/4\rceil\}.
\]
The branch-builder coverage gate is
\[
  |I_{\rm in}|\ge N_{\rm in,min},\qquad
  F_N\ge\rho_N,\qquad
  F_W\ge\rho_W.
\]
Failure of any of these three inequalities blocks the branch as
`branch_local_domain_coverage_failed`.  This is a branch-builder admissibility
gate.  It is separate from the Phase 4 row-adequacy and fitting-design gates.

### Design Measure

The design measure is finite and positive:
\[
  \mathcal D_t
  =
  \sum_{j=1}^{m_t}w_j\delta_{z_j}.
\]
The P70 default uses weighted raw pushed source rows, not resampled rows.  The
primary design rows are
\[
  z_j=L_t^{-1}(r_j-\mu_t),
  \qquad j\in I_{\rm in},
\]
from the unresampled pushed adjacent source samples \(r_j\).  Their weights are
the renormalized source weights on \(I_{\rm in}\):
\[
  w_j=\omega_j\Big/\sum_{i\in I_{\rm in}}\omega_i.
\]
Thus row multiplicity and row weights are not both used to encode the same
source weights.  A separate deterministic-resampling mode is not part of the
Phase 3 default; adding one would require a later reviewed design row that
states whether multiplicity or explicit weights carry the source weights.  Any
design row must evaluate the true adjacent target at that row and must be
classified as `fixed_hmc_adaptation` unless it exactly matches cited source
behavior.

### Shift

For a branch-creation parameter \(\beta_\star\), define the local negative
log-density
\[
  U_t(z;\beta)
  =
  \ell_t(\mu_t+L_tz;\beta)-\log|\det L_t|,
\]
where \(\ell_t\) is the negative log of the exact adjacent target from
Zhao--Cui Eqs. (9)--(12).  The frozen shift is
\[
  c_t=\min_{z_j\in\operatorname{supp}\mathcal D_t} U_t(z_j;\beta_\star).
\]
For later likelihood evaluations at \(\beta\), the same \(c_t\) is reused:
\[
  y_j(\beta)
  =
  \exp\left[-\frac{1}{2}\{U_t(z_j;\beta)-c_t\}\right].
\]
Recomputing \(c_t\), \(\mu_t\), \(L_t\), \(\Omega_t\), \(\mathcal D_t\), ranks,
or sweep policy at a new \(\beta\) defines a different branch.

### Fitting Scalar

Given the fixed branch choices, the fitting rule \(\mathcal A_t\) returns
\[
  \phi_t^B(\cdot;\beta)
  =
  \mathcal A_t\bigl(y(\beta),\mathcal D_t,\mathcal V_t,\mathcal R_t\bigr).
\]
Here \(\mathcal V_t\) is the finite tensor-train approximation space,
\(\mathcal R_t\) is the declared rank tuple, \(\tau_t\) is the defensive mass on
the shifted scale, \(\lambda_t\) is the defensive reference density on
\(\Omega_t\), and \(\zeta_t^B\) is the shifted normalizer.
Thus the fitted cores are allowed to vary with \(\beta\) through the fixed
linear algebra of \(\mathcal A_t\).  What is frozen is the branch, not merely
the fitted coefficients at \(\beta_\star\).  The shifted density and log
increment remain
\[
  q_t^{B,\mathrm{sh}}(z;\beta)
  =
  \phi_t^B(z;\beta)^2+\tau_t\lambda_t(z),
  \qquad
  \log\overline Z_t^B(\beta)=\log\zeta_t^B(\beta)-c_t.
\]

## Branch Identity Payload

The branch-builder manifest \(\mathcal M_t\) must record at least:

- target id, time index, observation prefix hash, previous retained hash;
- UKF scout claim class `scout_not_truth`, scout config, scout result hash, and
  nonclaims;
- \(\mu_t\), \(L_t\), \(\Omega_t\), dimension \(D\), determinant and condition
  diagnostics;
- source pushed-sample hash, source row count, finite-row count, weighted ESS,
  source-correlation fallback status, coverage count, coverage fractions
  \(F_N,F_W\), in-domain row count, row-weight hash, and design-measure hash;
- covariance rule:
  `ukf_scale_source_correlation_shrinkage`, \(\epsilon_{\rm scale}\),
  \(\epsilon_{\rm corr}\), \(E_{\rm corr,min}\), \(\alpha_C\),
  \(\epsilon_{\rm cov}\), and \(\gamma_t\);
- coverage rule:
  \(N_{\rm in,min}\), \(\rho_N\), \(\rho_W\), and
  `branch_local_domain_coverage_failed`;
- shift rule, \(\beta_\star\) identity, \(c_t\), and target-value scale
  summaries at branch creation;
- fitting-space placeholders to be filled by Phase 4:
  basis, rank tuple, initialization rule, sweep count, sweep order, ridge,
  channel-activity thresholds, normalizer/holdout/replay thresholds;
- governance classification for every operation;
- nonclaims:
  UKF is not truth; no filtering correctness; no exact likelihood; no HMC
  readiness; no adaptive Zhao--Cui parity; no rank/degree validation.

## Required Phase 4 Obligations

Phase 4 must design the fitting rule \(\mathcal A_t\) and admissibility
predicates against this branch builder.  It must address:

1. Nondegenerate initialization.  Constant-path initialization is allowed as a
   positive baseline component, but Phase 4 must add a reviewed rule that gives
   declared nonfirst rank channels nonzero initial paths or otherwise proves
   why the chosen multi-sweep rule can activate them.
2. Sweep policy.  The source-route helper's current one-sweep forward pass is
   the baseline, not the P70 target.  Phase 4 must declare sweep count, sweep
   order, stopping rule, and whether reverse or alternating sweeps are used.
3. Channel activity.  Phase 4 must define predicates on fitted cores or on a
   gauge-aware equivalent, with thresholds frozen before Phase 5 implementation
   and Phase 6 diagnostics.
4. Normalizer and diagnostic stability.  Phase 4 must define finite/bounded
   predicates for \(\zeta_t^B\), \(\log\overline Z_t^B\), holdout residuals,
   replay residuals, and condition diagnostics.  Fit residual alone is not a
   promotion criterion.
5. Implementation scope for Phase 5.  Phase 4 must name the exact code surfaces
   that may be edited and the tests that must be added.

Phase 3 has frozen the branch-builder coverage predicate above.  It has not
settled the later fitting predicates.  Phase 4 must still supply exact
channel-activity, normalizer, holdout, replay, condition-number, and
row-adequacy thresholds before any implementation or repaired diagnostic run.

## Stop Conditions Produced By This Phase

Phase 4 should stop rather than design around a silent assumption if:

- the UKF scout record is missing or nonfinite;
- pushed source samples cannot produce finite adjacent rows;
- the UKF/source hybrid covariance fails the finite/symmetric/positive-definite
  consistency check after the declared floors and shrinkage;
- branch coverage fails the frozen local-domain predicate;
- source-governance classification would require calling UKF guidance
  `source_faithful`;
- Phase 4 cannot freeze channel-activity thresholds without seeing repaired
  diagnostics.

Claude returned `VERDICT: AGREE` after the Phase 3 R1 repairs.  The agreed
design freezes branch-builder coverage and row/weight conventions, keeps the
UKF/source covariance hybrid as `fixed_hmc_adaptation`, and hands later fitting
predicates to Phase 4 without claiming they are already settled.

## Not Concluded

- No implementation was changed.
- No p50 prose was edited.
- No diagnostic or ladder was run.
- No Phase 5 code surface is authorized until Phase 4 passes.
- No Phase 6/7 diagnostic execution is authorized.
- No claim is made that the proposed branch builder fixes rank-channel
  collapse, stabilizes degree-2 normalizers, validates d18, scales to d50/d100,
  or is HMC-ready.
