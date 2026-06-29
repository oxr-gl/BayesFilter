# actual-SV single-target corrected derivation note

metadata_date: 2026-06-29
status: DRAFT_REVIEW_READY
artifact_type: derivation_note
scope: corrected actual-SV single-target argument
source_files:
- bayesfilter/highdim/sv_mixture_cut4.py
- docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex
- docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex
- docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex
- docs/plans/bayesfilter-actual-sv-single-target-lane-reset-memo-2026-06-28.md
- docs/plans/bayesfilter-actual-sv-single-target-lane-correction-plan-2026-06-28.md
mathdevmcp_support:
- MathDevMCP derive-step
- MathDevMCP check-proof-obligation
- MathDevMCP search-latex
- MathDevMCP audit-derivation-v2-label
- MathDevMCP typed-obligation-label

what_is_not_concluded:
- No exact raw actual-SV likelihood quadrature claim.
- No claim that the augmented-noise Gaussian-closure route is equal to the transformed exact-target route.
- No coupled multivariate Zhao--Cui TT claim.
- No generalized SV/CNS estimator claim.
- No scalability or HMC-admission claim.
- No blanket machine-certified proof claim from MathDevMCP.

## Objective

This note derives the corrected single-target statement for the actual stochastic-
volatility (SV) work in BayesFilter.  The governing correction is that there is
one transformed actual-SV likelihood target, and any admissible numerical route
must approximate that same scalar.  The note also shows where the previous
augmented-noise Gaussian-closure route changes the scalar and therefore does not
belong to the same target family.

## Evidence contract

| Item | Statement |
| --- | --- |
| Question | What is the exact transformed actual-SV target, and which current BayesFilter routes approximate that same scalar? |
| Primary claim | The dense exact-transformed reference, the direct-likelihood Fixed-SGQF route, and the factorized scalar Zhao--Cui TT route are same-target computations for the transformed actual-SV likelihood. |
| Critical contrast | The augmented-noise Gaussian-closure route accumulates a Gaussian innovation scalar based on predictive moments and therefore changes the scalar. |
| Veto diagnostic | Any step that replaces the exact transformed observation law by a different observation-density construction is not same-target evidence for the transformed actual-SV likelihood. |
| Explanatory-only diagnostics | MathDevMCP step checks and typed-obligation audits help document assumptions and unresolved obligations, but they do not replace the derivation itself. |
| Artifact | This markdown note is the durable derivation artifact for the corrected single-target statement. |

## Source and provenance ledger

| ID | Source | Role in derivation |
| --- | --- | --- |
| SRC1 | `bayesfilter/highdim/sv_mixture_cut4.py:199-218` | Exact transformed observation law and target manifest string. |
| SRC2 | `bayesfilter/highdim/sv_mixture_cut4.py:408-442` | Exact `log(y^2)` transform, exact log-chi-square log density, and Jacobian helper. |
| SRC3 | `bayesfilter/highdim/sv_mixture_cut4.py:445-572` | Dense exact-transformed scalar reference and independent-panel aggregation. |
| SRC4 | `bayesfilter/highdim/sv_mixture_cut4.py:575-680` | Same-target direct-likelihood Fixed-SGQF route. |
| SRC5 | `bayesfilter/highdim/sv_mixture_cut4.py:683-748` | Gradient wrapper labels for the same-target direct-likelihood route. |
| SRC6 | `bayesfilter/highdim/sv_mixture_cut4.py:751-969` | Augmented-noise Gaussian-closure route and its non-claims. |
| SRC7 | `bayesfilter/highdim/sv_mixture_cut4.py:1063-1113` | Factorized scalar Zhao--Cui TT same-target comparator. |
| SRC8 | `bayesfilter/highdim/sv_mixture_cut4.py:2771-2818` | Augmented state-space observation map used in the Gaussian-closure route. |
| SRC9 | `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex` | Generic Gaussian innovation scalar form exported by the Gaussian-projection route. |
| SRC10 | `docs/plans/bayesfilter-actual-sv-single-target-lane-reset-memo-2026-06-28.md` | Governing reset policy: one target, previous Lane-B framing wrong. |

## Model and notation

We use the scalar stochastic-volatility observation equation
\[
  y_t = \beta e^{h_t/2} \varepsilon_t,
  \qquad
  \varepsilon_t \sim \mathcal N(0,1),
\]
with \(\beta>0\).  The latent state \(h_t\) evolves according to the declared
SV transition law; for stationary initializations the code also assumes
\(|\gamma|<1\) and \(\sigma>0\).

Define the transformed observation
\[
  z_t = \log(y_t^2).
\]
Because the transform uses \(\log(y_t^2)\), the exact transformed route requires
nonzero finite observations; this is enforced in the code path that constructs
`exact_transformed_sv_observations` (SRC2).

Let the one-step transformed exact-target normalizer be
\[
  Z_t(\theta)
  =
  \int g_\theta(z_t\mid h_t)\,p_\theta(h_t\mid z_{1:t-1})\,dh_t,
\]
and let the cumulative transformed likelihood target be
\[
  \ell_T(\theta)=\sum_{t=1}^T \log Z_t(\theta).
\]
This is the single target considered in this note.

## Proposition A

Title:
`Exact transformed actual-SV observation law is log-chi-square`

Assumptions:
- \(\beta>0\);
- \(y_t\neq 0\) so that \(\log(y_t^2)\) is defined;
- observation equation \(y_t = \beta e^{h_t/2}\varepsilon_t\) with \(\varepsilon_t\sim\mathcal N(0,1)\).

Derivation:
\[
  y_t^2 = \beta^2 e^{h_t} \varepsilon_t^2.
\]
Taking logs on both sides gives
\[
  \log(y_t^2)=\log(\beta^2)+h_t+\log(\varepsilon_t^2).
\]
Therefore, with \(z_t=\log(y_t^2)\),
\[
  z_t-\log(\beta^2)-h_t = \log(\varepsilon_t^2).
\]
Since \(\varepsilon_t\sim\mathcal N(0,1)\), the random variable
\(\varepsilon_t^2\) is \(\chi_1^2\)-distributed, so the transformed observation
noise is exactly
\[
  \log(\varepsilon_t^2) \sim \log(\chi_1^2).
\]
Hence the exact transformed observation density is
\[
  g_\theta(z_t\mid h_t)
  =
  p_{\log\chi_1^2}\!\left(z_t-\log(\beta^2)-h_t\right).
\]
This is exactly the contract implemented by `ExactTransformedSVSSM` (SRC1), whose
manifest target string is
`z_t=log(y_t^2), z_t-log(beta^2)-h_t ~ log(chi_square_1)`.

Proof obligations:
- factorization of \(y_t^2\): proved by squaring the observation equation;
- transformed identity for \(z_t\): proved by direct logarithm algebra;
- log-chi-square law: proved from \(\varepsilon_t\sim\mathcal N(0,1)\).

Status:
`PROJECT_DERIVATION_HUMAN_WRITTEN_CODE_ALIGNED`

## Proposition B

Title:
`Dense reference and direct Fixed-SGQF route are same-target computations`

Assumptions:
- Proposition A assumptions;
- the predictive state approximation supplies a declared predictive law for \(h_t\);
- quadrature rules and weights are finite and well defined on the declared branch.

Derivation:

The dense exact-transformed scalar reference (SRC3) constructs the transformed
observations first, then for each time step evaluates
\[
  \log g_\theta(z_t\mid h_t)
\]
at latent-state grid points and accumulates the resulting log normalizer.
Operationally, the code path is:
1. build \(z_t=\log(y_t^2)\);
2. evaluate `model.observation_log_density(theta, x_grid, z_t, t)`;
3. update the dense log density by adding that observation log density;
4. compute the one-step log normalizer by weighted log-sum-exp.

The direct Fixed-SGQF route (SRC4) follows the same target logic with a sparse
quadrature cloud.  At each time step and coordinate it:
1. propagates the predictive latent cloud to `predicted_points`;
2. evaluates the exact transformed observation log density
   \(\log g_\theta(z_t\mid h_t)\) at those points;
3. computes
   \[
     \log \widehat Z_t^{\rm SGQF}
     =
     \log\sum_r w_r\exp\{\log g_\theta(z_t\mid h_t^{(r)})\};
   \]
4. normalizes the weights by that same \(\widehat Z_t^{\rm SGQF}\);
5. carries the filtered posterior moments forward.

The SGQF route is therefore a same-target computation because its one-step value
path is direct likelihood reweighting of the transformed exact observation law,
not Gaussian observation closure.  The route is approximate because the predictive
integral is approximated numerically, but the scalar being approximated is the
same transformed actual-SV normalizer from Proposition A.

Proof obligations:
- dense route uses the exact transformed observation law: source-supported by SRC3;
- SGQF route uses the exact transformed observation law: source-supported by SRC4;
- both routes accumulate one-step transformed normalizers: source-supported by SRC3 and SRC4;
- therefore both are same-target approximations to \(\ell_T(\theta)\): proved by code-path alignment to the same \(g_\theta(z_t\mid h_t)\).

Status:
`PROJECT_DERIVATION_HUMAN_REVIEWED_SOURCE_ALIGNED`

## Proposition C

Title:
`Factorized scalar Zhao--Cui TT route is a same-target comparator`

Assumptions:
- Proposition A assumptions;
- independent-panel factorization used by the current wrapper;
- fixed-design TT value path consumes the declared model and transformed observations as given.

Derivation:

The current Zhao--Cui wrapper (SRC7) first computes
\[
  z_t = \log(y_t^2)
\]
through the same `exact_transformed_sv_observations` helper used by the dense and
Fixed-SGQF routes.  For each coordinate it then constructs an
`ExactTransformedSVSSM` model and passes the transformed data to
`scalar_nonlinear_fixed_design_tt_value_path`.  The wrapper returns per-step log
normalizers and sums them across coordinates.

Thus the present Zhao--Cui comparator is same-target in exactly the sense needed
here: it is another numerical route to the coordinatewise exact transformed
actual-SV likelihood, not a different observation model.  Its current non-claims
matter: the wrapper is not a coupled multivariate Zhao--Cui implementation and it
makes no generalized-SV/CNS or scalability claim.  Those boundaries do not alter
the target identity; they only limit the scope of what the comparator represents.

Proof obligations:
- transformed observations shared with the dense and SGQF routes: source-supported by SRC2 and SRC7;
- model object is `ExactTransformedSVSSM`: source-supported by SRC7;
- returned target string is `factorized coordinatewise exact transformed SV`: source-supported by SRC7;
- therefore the current Zhao--Cui wrapper is same-target for the transformed coordinatewise likelihood: proved by wrapper construction.

Status:
`PROJECT_DERIVATION_HUMAN_REVIEWED_SOURCE_ALIGNED`

## Proposition D

Title:
`Augmented-noise Gaussian-closure route changes the accumulated scalar`

Assumptions:
- actual-SV augmented route uses the current two-dimensional augmented cloud implementation;
- Gaussian innovation scalar is assembled from predictive observation moments and an innovation covariance;
- observation variance floor is positive on the declared branch.

Derivation:

The augmented-noise route (SRC6, SRC8) does not begin from the transformed exact
observation law of Proposition A.  Instead, it constructs a two-dimensional state
containing the latent coordinate and an explicit observation-noise coordinate, and
uses the raw observation map
\[
  y_t = \beta e^{h_t/2}\varepsilon_t.
\]
In code, the observation function is
\[
  (h_t,\varepsilon_t)
  \longmapsto
  \beta e^{h_t/2}\varepsilon_t.
\]
The filter then pushes the augmented cloud through that raw observation map and
forms predictive observation moments such as \(\bar z_t\) and \(S_t\).  The
accumulated one-step scalar is the Gaussian innovation log likelihood
\[
  \widehat\ell_t^{\rm FSGQ}
  =
  -\frac12\left\{\log\det S_t + v_t^\top S_t^{-1} v_t + n_y\log(2\pi)\right\},
  \qquad
  v_t = y_t - \bar z_t,
\]
which is the generic Gaussian-projection scalar documented in the SGQF chapter
(SRC9).

This scalar differs from the transformed exact-target scalar of Proposition A in
two decisive ways:
1. it is assembled from predictive observation moments of the augmented raw map,
   rather than by evaluating the exact transformed observation density
   \(g_\theta(z_t\mid h_t)\) at latent-state nodes;
2. it requires an innovation covariance and positive observation variance floor,
   which are ingredients of a Gaussian innovation model, not of the exact
   transformed log-chi-square observation law.

Therefore the augmented-noise route is not a same-target approximation to
\(\ell_T(\theta)\).  It is a different declared approximate scalar.  That is why
its own diagnostics explicitly say
`raw actual SV augmented-noise Gaussian-closure approximate likelihood` and list
non-claims including `not exact transformed same-target admission` and
`not direct actual-SV likelihood quadrature` (SRC6).

Proof obligations:
- augmented state-space observation map is raw and multiplicative: source-supported by SRC8;
- accumulated scalar is Gaussian innovation log likelihood: source-supported by SRC6 and SRC9;
- transformed exact observation density is not evaluated in this route: source-supported by contrast between SRC1/SRC4 and SRC6/SRC8;
- therefore the scalar changes: proved by value-path comparison.

Status:
`PROJECT_DERIVATION_HUMAN_REVIEWED_WITH_EXPLICIT_NON_EQUIVALENCE`

## Claim-status ledger

| Claim | Status | Basis |
| --- | --- | --- |
| Exact transformed observation law is log-chi-square | Proved in note | Direct algebra + SRC1/SRC2 |
| Dense exact-transformed route is same-target | Source-aligned and proved by value-path reading | SRC3 |
| Direct Fixed-SGQF route is same-target | Source-aligned and proved by direct-likelihood reweighting structure | SRC4/SRC5 |
| Current Zhao--Cui wrapper is same-target | Source-aligned | SRC7 |
| Augmented-noise Gaussian-closure route is same-target | Rejected | SRC6/SRC8/SRC9 |
| Augmented-noise Gaussian-closure route defines a different declared scalar | Source-aligned and proved by value-path comparison | SRC6/SRC8/SRC9 |

## What is not concluded

- This note does not prove a corrected same-target augmented-noise route exists.
- This note does not prove any equality between transformed and raw-route scalar
  values after Jacobian adjustment or any other correction.
- This note does not certify the current score implementations beyond the target
  alignment stated in the corresponding wrappers.
- This note does not establish multivariate Zhao--Cui TT, KSC importance
  reweighting, or generalized SV/CNS inference claims.

## MathDevMCP checkpoints and audit boundary

The note used MathDevMCP in a provenance-first support role, not as a final proof
oracle.

| Checkpoint | Tool | Outcome | Interpretation |
| --- | --- | --- | --- |
| CP1 | `derive-step` on `z_t=log(y_t^2)` to `z_t=log(beta^2)+h_t+log(epsilon_t^2)` | `mismatch` | Expected limitation: the tool does not infer the hidden observation-equation substitution automatically. The algebra is therefore written explicitly in Proposition A instead of being machine-certified. |
| CP2 | `check-proof-obligation` on the same identity with the observation equation as an assumption | `inconclusive` | Expected encoding limitation: the backend rejected the expression syntax. This is recorded as a tooling boundary, not as evidence against the identity. |
| CP3 | `search-latex 'Gaussian innovation log likelihood'` | located `eq:p31-fsgq-loglik` and related SGQF innovation-score references | Confirms the generic Gaussian-projection scalar form used to explain the augmented route. |
| CP4 | `audit-derivation-v2-label eq:p31-fsgq-loglik --summary-only` | `unverified` with missing-shape / backend limitations | Useful boundary evidence: the SGQF Gaussian innovation equation requires explicit shape and positive-definite assumptions, which are stated in Proposition D rather than hidden. |
| CP5 | `typed-obligation-label prop:p31-innovation-score` | `ready_for_backend` | Confirms that the Gaussian innovation score proposition carries typed obligations and should be treated as a bounded, assumption-dependent scalar statement. |

Decision:
`WRITE_THIS_NOTE_AS_THE_DERIVATION_ARTIFACT_FOR_THE_CORRECTED_SINGLE_TARGET_ARGUMENT`
