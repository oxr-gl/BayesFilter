# P1R Claim-Support Ledger

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: paper-first source set indexed in P1R.

what_is_not_concluded: see section "What Is Not Concluded".

## Purpose

This ledger maps planned literature claims to checked primary technical anchors
or blockers.  It is a pre-rewrite contract, not final chapter prose.

## Claim Rows

| Claim for future rewrite | Intended chapter | Support class | Checked support anchors | Limits and reviewer risk |
| --- | --- | --- | --- | --- |
| Checked modern seed papers state the prediction/update or PDE filtering formulations they use for their own algorithms. | Ch33 foundations | `PRIMARY_TECHNICAL_SUPPORT` | Jia 2012 equations (1)--(4), Li--Wang--Yau--Zhang model/DMZ discussion, Fox et al. Fokker--Planck/continuous-discrete setup, Meng--Yau--Zhang correlated-noise DMZ/Zakai SPDE. | Supports source-local exposition of those papers' setups, not a standalone derivation of classical nonlinear filtering theory. |
| A self-contained foundations chapter must derive or cite primary classical nonlinear-filtering results for Zakai/Duncan/Mortensen, Kushner--Stratonovich, and robust DMZ transformations. | Ch33 foundations | `SOURCE_GAP_BLOCKER` | Promoted by TT/DMZ seed papers and snowball ledger; primary classical anchors not checked in P1R. | Rewrite must inspect classical foundations or keep explicit source-gap language. |
| TT/QTT PDE methods can approximate discretized nonlinear filtering density evolution when the discretized operators/densities have controlled TT ranks and the PDE assumptions hold. | Ch35 or TT chapter | `PRIMARY_TECHNICAL_SUPPORT` | Li--Wang--Yau--Zhang Propositions 4.1/4.3, Algorithms 1--2, Lemmas 5.3--5.6, Theorem 5.7; Meng--Yau--Zhang Algorithm 1, Theorems 4.3--4.6, 5.7. | Does not imply rank control for NAWM, arbitrary likelihoods, or BayesFilter implementation. |
| TT sequential state/parameter learning with conditional KR maps is a direct bridge between TT density approximation and transport-style posterior operations in SSMs. | Ch35/Ch37 synthesis | `PRIMARY_TECHNICAL_SUPPORT` | Zhao--Cui SSM equations (1)--(9), Algorithms 1--5, Proposition 2, Proposition 4, Theorems 7--8, Corollary 12. | Requires stating TT approximation, nonnegativity, boundedness/error assumptions. Does not prove NeuTra/HMC readiness. |
| Functional TT grid filtering is a Bayes-optimal grid-filtering route that replaces naive density arrays by TT representations but remains compressibility/discretization dependent. | Ch35 | `PRIMARY_TECHNICAL_SUPPORT` | Fox--Dolgov--Morrison--Molteno DOI/front matter; Fokker--Planck/continuity equations (1)--(7); finite-volume and functional TT sections. | Does not support general scalability without rank/mesh evidence. |
| Tensor-network Kalman filtering compresses lifted linear/Kalman recursions, while square-root tensor Kalman formulations address PSD loss from naive covariance rounding. | Ch35/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Batselier--Chen--Wong Sections 3--4 and Lemmas 1--3; Menzen--Kok--Batselier equations (1)--(9), TNSRKF Section 4, Algorithms 1--2, Lemmas 5 and 7. | Applies to lifted Volterra/online GP settings in sources; not a proof for nonlinear SSM filtering. |
| Low-rank tensor UKF tractography is a domain-specific example of compressing nonlinear observation geometry before/inside a UKF-style recursion. | Ch35 or Ch34 example | `PRIMARY_TECHNICAL_SUPPORT` | Gruen--Groeschel--Schultz equations (1)--(20), Sections 2.1--2.4, experiments and Table 1. | Supports only the diffusion MRI tractography example; must not be generalized to DSGE, BayesFilter, or broad high-dimensional filtering. |
| Sparse-grid quadrature filtering and high-degree cubature are natural high-order Gaussian competitors with polynomial point growth for fixed level/degree, but not a general cure for high-dimensional nonlinear filtering. | Ch34 | `PRIMARY_TECHNICAL_SUPPORT` | Jia 2012 SGQF Theorem 3.1, Algorithm 1, Theorem 3.2, Proposition 3.1; Jia 2013 Definition 3.1, Theorem 3.1, Proposition 3.1, Proposition 3.2; Singh et al. adaptive index-set/tolerance sections. | "Polynomial" requires fixed level/degree and may still be large; sources assume Gaussian approximation/additive-noise settings. |
| Transport-map ensemble filtering/smoothing provides deterministic or stochastic prior-to-posterior maps, often triangular/localized, and offers a high-dimensional non-Gaussian research pillar. | Ch35/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Spantini--Baptista--Marzouk Algorithms 1--3, Related work Section 1.1, Remarks 1--7; Ramgraber et al. Sections 2--3, Proposition 1, Algorithms in appendix. | No BayesFilter backend or NAWM validation. Map-estimation, localization, ensemble size, and residual diagnostics remain required. |
| Transport-map accelerated MCMC and NeuTra motivate geometry-aware acceleration for difficult posterior geometries. | Ch36/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Parno--Marzouk map proposals and adaptive Algorithm 1; Hoffman et al. NeuTra transformed target/Jacobian and experiments. | Does not support HMC convergence, BayesFilter NeuTra, or production HMC. |
| Any BayesFilter-specific HMC target/correction claim must be derived in project notation and checked against HMC foundations. | Ch36/Ch37 | `PROJECT_DERIVATION` | Future chapter derivation required; Neal/Hoffman/Gelman/Betancourt anchors in existing bibliography need rechecking for foundations. | P1R does not supply BayesFilter HMC target validation. |
| Deep inverse Rosenblatt transports and TT sampling form a plausible substrate for transport-preconditioned inference and density/proposal design. | Ch36/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Cui--Dolgov related work, Propositions 1--7, Theorems 1/3/4, Algorithms 1--4; Dolgov TT sampling Algorithms 1--2 and Lemmas 1--2. | Does not support filtering correctness unless composed with checked filtering sources and downstream diagnostics. |
| TT rank bounds for Gaussian densities provide conditions under which TT compression is plausible and warn against assuming rank remains small for arbitrary densities. | Ch35/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | TT rank bounds Theorems 2.3--2.8, Theorem 3.1, Lemmas 3.3--3.7, Bayesian filtering Section 5. | Supports Gaussian/structured precision discussion, not non-Gaussian rank guarantees. |
| Fokker--Planck TT-cross and tensor-network integration are numerical substrates for PDE evolution and high-dimensional integration, not filtering validation by themselves. | Ch35/Ch37 | `PRIMARY_TECHNICAL_SUPPORT` | Fokker--Planck TT-cross Algorithms 1--5 and examples; Cassel equations (1)--(9), TT-X construction, Tables 1--2. | Supports substrate discussion only; cannot support filtering-specific correction/update or posterior accuracy claims. |
| Spantini et al. 2016 decomposable transport workshop paper supports decomposable transports for filtering/smoothing. | None | `QUARANTINED` | User report: retracted on 2026-05-28. | Forbidden as support. Any decomposable/triangular transport claim must use non-quarantined sources. |

## Claim-Support Gaps Before Rewrite

- Classical nonlinear filtering foundations need checked primary anchors for
  Zakai/Duncan/Mortensen, Kushner--Stratonovich, and robust DMZ if the
  foundations chapter gives full derivations.
- Tensor-train foundations need checked primary anchors for Oseledets TT-SVD and
  TT-cross/maxvol if the chapter derives storage, rounding, or cross algorithms.
- Transport-map foundations need checked primary anchors for Rosenblatt/Knothe
  and optimal transport theory if the synthesis gives proposition/proof style
  statements.
- HMC foundations need rechecking of Neal, Hoffman--Gelman, Betancourt, and
  Girolami--Calderhead anchors before deriving diagnostics or RMHMC comparisons.

## What Is Not Concluded

No claim in this ledger establishes chapter review-readiness.  The ledger only
identifies where future claims can be sourced and where source blockers remain.
It does not validate BayesFilter code, posterior accuracy, tensor scaling,
HMC convergence, GPU/XLA readiness, or NAWM readiness.
