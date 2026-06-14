# P7 Gaussian/Transport/Tensor Source Anchor Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P7 plan, P1R/P1S/P1T/P1U/P2R/P3/P4/P5/P6 source ledgers,
`docs/references.bib`, `ch34`, `ch35`, `ch36`, `ch37`, local source cache,
and the scholarly literature audit policy.

what_is_not_concluded: This ledger does not conclude exhaustive literature
coverage, current citation counts, venue rankings, production readiness,
posterior accuracy, HMC convergence, or source support from abstracts,
metadata, introductions, conclusions, or quarantined papers.

## Citation Placement Rule Used

P7 cites sources only where a checked construction, algorithm, theorem, or
technical object is used.  Project derivations are labeled as project
derivations and do not pretend to be source theorems.

## Anchors Used In `ch34`

| Source | Chapter use | Support class | P7 caveat |
|---|---|---|---|
| Julier--Uhlmann 1996/1997 | Unscented transform/UKF sigma-point
construction. | `PRIMARY_TECHNICAL_SUPPORT` from prior source closure. | Used
only for construction, not posterior accuracy. |
| Arasaratnam--Haykin 2009 | CKF third-degree spherical--radial construction
and square-root CKF context. | `PRIMARY_TECHNICAL_SUPPORT` | Used for CKF
moment rule, not global high-dimensional validation. |
| Jia--Xin--Cheng 2013 | High-degree CKF construction and point-count
comparisons. | `PRIMARY_TECHNICAL_SUPPORT` | Used for high-degree cubature
construction, not free global scalability. |
| Jia--Xin--Cheng 2012 | Sparse-grid quadrature nonlinear filtering
construction. | `PRIMARY_TECHNICAL_SUPPORT` | Used for source-local SGQF, not
general Smolyak theory. |
| Singh et al. 2018 | Adaptive sparse-grid Gauss--Hermite filtering. |
`PRIMARY_TECHNICAL_SUPPORT` | Adaptive branches are not ordinary smooth HMC
gradients unless smoothed or frozen. |
| `ch18_svd_sigma_point.tex` | Local derivative template for sigma/CUT point
and Gaussian innovation score derivations. | `PROJECT_DERIVATION` /
`IMPLEMENTATION-ADJACENT MONOGRAPH SUPPORT` | Does not machine-certify the new
P7 derivation. |

## Anchors Used In `ch35`

| Source | Chapter use | Support class | P7 caveat |
|---|---|---|---|
| Gordon--Salmond--Smith 1993 | Bootstrap filter/SIR baseline. |
`PRIMARY_TECHNICAL_SUPPORT` | Does not support smooth HMC gradients through
resampling. |
| Arulampalam et al. 2002 | Tutorial SIR mechanics. |
`SURVEY_OR_TUTORIAL_FOR_MECHANICS` | Used for mechanics only, not theorem-level
collapse claims. |
| Bengtsson--Bickel--Li 2008 | High-dimensional particle collapse warning. |
`PRIMARY_TECHNICAL_SUPPORT` | Project lognormal derivation is mechanism, not a
replacement theorem. |
| Snyder et al. 2008 | Log-likelihood variance/obstacles framing. |
`PRIMARY_TECHNICAL_SUPPORT` | Used for collapse mechanism and reviewer-facing
warning. |
| Parno--Marzouk 2018 | Transport-map MCMC proposal and correction context;
Sections 2--3 and adaptive Algorithm 1 per P1R source ledger. |
`PRIMARY_TECHNICAL_SUPPORT` | Used for transport correction context, not
filter validation. |
| Papamakarios et al. 2021 | Normalizing-flow density/Jacobian orientation. |
`SURVEY_CONTEXT_ONLY` | Explicitly not used as filtering theorem support. |
| Rosenblatt 1952 | Triangular conditional-CDF transformation. |
`PRIMARY_TECHNICAL_SUPPORT` | Knothe original remains uninspected. |
| Spantini--Baptista--Marzouk 2022 | Coupling techniques for nonlinear ensemble
filtering and localization. | `PRIMARY_TECHNICAL_SUPPORT` | Distinct from the
quarantined 2016 decomposable transport workshop paper. |
| Ramgraber et al. 2023 | Smoothing-side triangular transport recursions:
Sections 2--3, Proposition 1, Appendix C algorithms per P1R. |
`RECENT_EXTENSION_CONTEXT` | Not used as foundational filtering theorem. |
| Oseledets 2011 | TT format, storage, TT-SVD/rounding framework. |
`PRIMARY_TECHNICAL_SUPPORT` | Low storage requires rank stability. |
| Oseledets--Tyrtyshnikov 2010 | TT-cross interpolation/integration. |
`PRIMARY_TECHNICAL_SUPPORT` | Savostyanov maxvol specifics remain outside P7
unless separately checked. |
| Li et al. 2019 | TT/QTT nonlinear filtering via PR-DMZ/FKE route:
Propositions 4.1/4.3, Algorithms 1--2, Lemmas 5.3--5.6, Theorem 5.7 per P1R. |
`DIRECT_METHOD` | Preprint source; used for method route, not mature
industrial validation or general rank control. |
| Fox et al. 2021 | Fokker--Planck/continuity equations (1)--(7),
finite-volume propagation, Bayes update, functional TT Section 4 per P1R. |
`DIRECT_METHOD` | Used for filtering-density route under compressibility and
discretization caveats. |
| Meng et al. 2026 | Correlated-noise DMZ/Zakai SPDE and TT route:
equations (1)--(2), Algorithm 1, Theorems 4.3--4.6 and 5.7 per P1R. |
`RECENT_EXTENSION_CONTEXT` | Recent arXiv source; not used as mature
validation. |
| Zhao--Cui 2024 | TT sequential learning, squared TT, conditional KR maps:
SSM equations (1)--(9), Algorithms 1--5, Proposition 2, Proposition 4,
Theorems 7--8, Corollary 12 per P1R. | `PRIMARY_TECHNICAL_SUPPORT` | HMC
preconditioning remains a research hypothesis until scalar/Jacobian/diagnostic
gates pass. |
| Cui--Dolgov 2021 | Deep composition of tensor trains with squared inverse
Rosenblatt transports. | `DIRECT_METHOD_CONTEXT` | Supports bridge existence,
not BayesFilter backend validation. |
| Batselier--Chen--Wong 2016 | Tensor-network Kalman filtering for lifted
Volterra systems. | `DIRECT_METHOD_CONTEXT` | Not a general nonlinear filter
over original state. |
| Menzen--Kok--Batselier 2024 | TN square-root covariance caution. |
`RECENT_CAUTION_CONTEXT` | Used to motivate PSD/factor gate. |

## Quarantine And Source Gaps

- Spantini et al. 2016 "Decomposable Transport Maps for Bayesian Filtering and
  Smoothing" remains quarantined and is not used as support.
- Knothe original rearrangement source remains uninspected; Rosenblatt and
  modern transport-filtering sources are used instead.
- Stroud, Smolyak, and Genz originals are not used as theorem support in P7.
- Savostyanov maxvol-specific theory is not used beyond the
  Oseledets--Tyrtyshnikov TT-cross anchor already inspected.
