# P1R Backward And Forward Snowball Ledger

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: all non-quarantined paper-first seed papers in
`.local_sources/highdim_nonlinear_filtering/`; Spantini et al. 2016 is listed
only as quarantined.

what_is_not_concluded: see section "What Is Not Concluded".

Forward field mapping: every seed uses `forward_snowball_query_status`,
`query_source`, `query_scope`, and `query_date`; because no live metadata query
was approved, these fields carry blocked values rather than citing-work lists.

## Policy

Backward snowballing inspects related-work, literature-survey, introduction,
comparison, and reference-list sections of seed papers and classifies relevant
references.  P1R did not run live forward-snowball metadata queries; therefore
every seed records the explicit blocked fields:

- `forward_snowball_query_status`: `FORWARD_SNOWBALL_BLOCKED_NO_APPROVED_METADATA_QUERY`
- `query_source`: `QUERY_SOURCE_BLOCKED`
- `query_scope`: `QUERY_SCOPE_BLOCKED`
- `query_date`: `QUERY_DATE_N/A`

Forward snowballing remains a blocker for a final "complete literature" claim.

## Backward Snowball Coverage By Family

| Seed family | Inspected sections | Relevant backward references/classes | Immediate action |
| --- | --- | --- | --- |
| TT/DMZ nonlinear filtering: Li--Wang--Yau--Zhang and Meng--Yau--Zhang | Introductions, DMZ/FKE preliminaries, convergence sections, references | Zakai 1969 (`FOUNDATIONAL`), Duncan-Mortensen-Zakai/robust DMZ line (`FOUNDATIONAL`), particle filtering references (`COMPETITOR`), finite-difference/PDE solvers (`BACKGROUND`), Oseledets/Tyrtyshnikov TT literature (`FOUNDATIONAL`), TT-rounding/TT-cross references (`DIRECT_METHOD`), Kloeden--Platen stochastic numerics (`FOUNDATIONAL_FOR_CORRELATED_NOISE`) | Inspect foundational nonlinear filtering and TT decomposition references before writing foundations. Keep correlated-noise claims source-local unless primary stochastic-numerics support is checked. |
| Zhao--Cui TT sequential learning | Introduction and Related Work Section 1.2; algorithm/error-analysis cross references; references | Cappe et al. and Kantas et al. SSM/SMC references (`FOUNDATIONAL`), Cui--Dolgov DIRT and squared TT (`DIRECT_METHOD`), Spantini transport-map theory (`FOUNDATIONAL`), SMC2/particle methods (`COMPETITOR`), Griebel--Harbrecht approximation theory (`FOUNDATIONAL_FOR_ERROR_BOUNDS`) | Promote SSM/SMC foundations and transport-map theory to omission-risk register if not already covered. Cite Zhao--Cui for TT-KR filtering only after assumptions are stated. |
| Functional TT grid filtering | Introduction and references in accepted manuscript | Kalman/filtering foundations (`FOUNDATIONAL`), grid filtering/finite-volume PDE literature (`DIRECT_METHOD`/`BACKGROUND`), Fokker--Planck/continuity-equation numerics (`FOUNDATIONAL`), Dolgov TT methods (`FOUNDATIONAL`) | Use as bridge between Bayes-optimal continuous-discrete filtering and TT representation; inspect numerical PDE foundations for derivations if foundations chapter uses them. |
| Tensor-network Kalman and square-root tensor filtering | Introductions, tensor preliminaries, implementation sections, references | Kalman 1960 and square-root/Potter filters (`FOUNDATIONAL`), Oseledets TT decomposition and tensor-network theory (`FOUNDATIONAL`), prior TNKF papers (`DIRECT_METHOD`), GP regression references (`BACKGROUND`), PSD/rounding warnings (`DIRECT_METHOD`) | Promote classical Kalman/square-root filtering and TT decomposition to omission-risk register; restrict TNSRKF to square-root PSD lesson, not nonlinear filtering. |
| Low-rank tensor UKF tractography | Introduction, methods Sections 2.1--2.4, discussion, references | Basser/Mori diffusion MRI tractography (`BACKGROUND`), Malcolm et al. UKF tractography (`DIRECT_METHOD_FOR_DOMAIN`), Ankele et al. constrained higher-order tensor fODFs (`DIRECT_METHOD_FOR_DOMAIN`), spatial regularization and tractography benchmark references (`EMPIRICAL_EXAMPLE`) | Cite only as domain-specific observation-compression example. Do not promote diffusion MRI references into main nonlinear-filtering foundations unless tractography analogy is retained. |
| Transport-map filtering/smoothing | Spantini--Baptista--Marzouk Related work Section 1.1; ensemble transport smoothing Introduction and transport basics | Villani optimal transport (`FOUNDATIONAL`), Marzouk/Parno transport maps (`FOUNDATIONAL`), Reich ensemble transform (`DIRECT_METHOD`), feedback particle filter (`COMPETITOR`), EnKF/LETKF/localization data-assimilation references (`FOUNDATIONAL_OR_COMPETITOR`), Rosenblatt/Knothe rearrangements (`FOUNDATIONAL`), multivariate rank histogram filter (`COMPETITOR`) | Promote Villani/Reich/Rosenblatt/Knothe/EnKF-localization references to omission-risk register. Quarantine Spantini et al. 2016 decomposable workshop paper. |
| Sparse-grid and cubature competitors | Jia 2012/2013 Introductions, theory sections, references; adaptive SGHF introduction/references | Smolyak 1963 (`FOUNDATIONAL`), Heiss--Winschel sparse-grid integration (`FOUNDATIONAL`), Arasaratnam--Haykin CKF (`DIRECT_METHOD`), Ito--Xiong Gaussian filters (`FOUNDATIONAL`), Julier--Uhlmann UT (`FOUNDATIONAL`), Genz spherical rules (`FOUNDATIONAL_FOR_HIGH_DEGREE`), Stroud cubature (`FOUNDATIONAL`), Arulampalam/Doucet particle filters (`COMPETITOR`) | Promote Smolyak, Genz/Stroud, Arasaratnam--Haykin, Ito--Xiong, and Julier--Uhlmann to omission-risk register if missing or not checked. |
| Transport-preconditioned MCMC/HMC | Parno--Marzouk Sections 1--5 and references; NeuTra related work Section 3; DIRT related work Section 1.2 | Neal/Hoffman--Gelman HMC/NUTS (`FOUNDATIONAL`), Girolami--Calderhead RMHMC (`COMPETITOR`), Marzouk transport-map theory (`FOUNDATIONAL`), normalizing flows (`COMPETITOR_CONTEXT`), Rosenblatt transport (`FOUNDATIONAL`), MCMC proposal/correction literature (`FOUNDATIONAL`) | Keep HMC acceleration as substrate only. Promote RMHMC and transport-map foundations as omission risks if not in chapters. |
| TT sampling/rank/PDE/integration substrate | TT sampling introduction/references; TT rank bounds introduction/references; Fokker--Planck related works; tensor-network integration references | Oseledets 2011 TT (`FOUNDATIONAL`), TT-cross/maxvol (`FOUNDATIONAL`), Grasedyck--Kressner--Tobler low-rank tensor survey (`SURVEY_OR_TUTORIAL`), Dolgov TT sampling (`DIRECT_METHOD`), Gaussian rank-bound references (`DIRECT_METHOD`), tensor-network integration/regression references (`BACKGROUND`) | Promote Oseledets/TT-cross and low-rank tensor survey to omission-risk register; use surveys for orientation only, not theorem support. |

## Seed-Level Forward Snowball Status

All seed rows share:

- `forward_snowball_query_status`: `FORWARD_SNOWBALL_BLOCKED_NO_APPROVED_METADATA_QUERY`
- `query_source`: `QUERY_SOURCE_BLOCKED`
- `query_scope`: `QUERY_SCOPE_BLOCKED`
- `query_date`: `QUERY_DATE_N/A`
- `highly_cited_citing_works`: `BLOCKED_NO_APPROVED_METADATA_QUERY`
- `recent_citing_works`: `BLOCKED_NO_APPROVED_METADATA_QUERY`
- `followups_or_corrections`: `BLOCKED_NO_APPROVED_METADATA_QUERY`
- `forward_action`: request a separate approved metadata-intake pass if the
  final survey must claim high-confidence forward coverage.

This applies to the non-quarantined seed papers by Li--Wang--Yau--Zhang,
Zhao--Cui, Fox--Dolgov--Morrison--Molteno, Meng--Yau--Zhang,
Batselier--Chen--Wong, Menzen--Kok--Batselier, Gruen--Groeschel--Schultz,
Spantini--Baptista--Marzouk, Ramgraber--Baptista--McLaughlin--Marzouk,
Jia--Xin--Cheng 2012, Jia--Xin--Cheng 2013, Singh--Radhakrishnan--Bhaumik--Date,
Parno--Marzouk, Hoffman et al., Cui--Dolgov, Dolgov et al., TT rank bounds,
Fokker--Planck TT-cross, and Cassel.

## Quarantined Snowball Entry

- Spantini et al. 2016, "Decomposable Transport Maps for Bayesian Filtering
  and Smoothing": `RETRACTED_OR_QUARANTINED`.  It does not enter backward or
  forward support.  Later transport-map exposition must cite checked
  non-quarantined transport filtering/smoothing sources.

## Promotion Candidates From Backward Snowballing

These candidates are high enough risk that chapter rewrite should either inspect
them or carry explicit omission/blocker text:

- Oseledets 2011 tensor-train decomposition and TT-SVD:
  `FOUNDATIONAL`; `PROMOTED_BLOCKER` until primary anchors are checked.
- TT-cross/maxvol references, including Oseledets--Tyrtyshnikov and Goreinov
  lines: `FOUNDATIONAL`; `PROMOTED_BLOCKER`.
- Zakai/Duncan/Mortensen nonlinear filtering foundations and robust DMZ
  references: `FOUNDATIONAL`; `PROMOTED_BLOCKER`.
- Smolyak 1963 sparse-grid quadrature and Genz/Stroud cubature rules:
  `FOUNDATIONAL`; `PROMOTED_BLOCKER`.
- Arasaratnam--Haykin CKF and Julier--Uhlmann UKF/UT:
  `FOUNDATIONAL`; partially present in `docs/references.bib`, but primary
  technical anchors need checking before derivation-heavy rewrite.
- Reich ensemble transform and EnKF/localization references:
  `DIRECT_METHOD`/`FOUNDATIONAL`; `PROMOTED_BLOCKER` for transport-map chapter
  if local source anchors are not checked.
- Rosenblatt/Knothe rearrangement foundations:
  `FOUNDATIONAL`; `PROMOTED_BLOCKER` for TT-KR/transport synthesis.
- Neal HMC, Hoffman--Gelman NUTS, Girolami--Calderhead RMHMC:
  `FOUNDATIONAL`/`COMPETITOR`; partially present in `docs/references.bib`, but
  HMC chapter must check technical sections rather than relying on memory.
- Particle filter degeneracy foundations: Gordon, Doucet, Arulampalam,
  Bengtsson/Bickel/Li, Snyder et al.:
  `FOUNDATIONAL`/`COMPETITOR`; already cited in current chapters but should be
  rechecked for any high-dimensional degeneracy claims.

## What Is Not Concluded

This ledger does not establish complete backward or forward coverage.  It does
not say every cited reference in every seed paper should be cited.  It records
the relevant candidates that a skeptical panel is likely to expect and marks
forward-snowballing as blocked pending an approved metadata pass.
