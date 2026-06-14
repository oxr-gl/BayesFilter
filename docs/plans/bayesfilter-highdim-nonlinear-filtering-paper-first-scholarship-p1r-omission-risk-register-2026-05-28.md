# P1R Omitted-Paper And Reviewer-Risk Register

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: paper-first source set and backward snowball candidates.

what_is_not_concluded: see section "What Is Not Concluded".

Field mapping: table columns `promotion_rule_status` and
`blocking_disposition` implement the P1R snowball promotion rule.

## Purpose

This register records papers and topics a skeptical academic/industrial panel
may expect.  Some are already cited in existing chapters or `docs/references.bib`,
but P1R marks them as risks unless their primary technical sections have been
checked for the specific future claim.

## Reviewer-Risk Rows

| Candidate/topic | Why it arose | Classification | Source status | Expected hostile-review question | promotion_rule_status | blocking_disposition | Severity | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Oseledets 2011 tensor-train decomposition / TT-SVD | Repeated in TT filtering, TT sampling, TN Kalman, TT rank sources | `FOUNDATIONAL` | Not checked in P1R | "How can you discuss TT storage/ranks/rounding without citing the original TT format?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect original TT decomposition paper before deriving TT storage/rank propositions. |
| TT-cross and maxvol foundations: Oseledets--Tyrtyshnikov, Goreinov lines | TT sampling, DIRT, Fokker--Planck TT-cross | `FOUNDATIONAL` | Not checked in P1R | "Where is the source for cross approximation and sample-complexity/rank behavior?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect primary TT-cross/maxvol references or keep as source-gap blocker. |
| Zakai, Duncan, Mortensen, Kushner--Stratonovich nonlinear filtering foundations | TT/DMZ sources rely on these equations | `FOUNDATIONAL` | Not checked in P1R | "Are the filtering SPDE/DMZ equations derived from primary filtering theory or copied from secondary papers?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect primary or standard monograph sources before full foundations derivation. |
| Robust DMZ/pathwise filtering references used by Li--Wang--Yau--Zhang | Li et al. convergence section imports robust DMZ propositions | `FOUNDATIONAL` | Not checked in P1R | "What exactly is robust/pathwise in the DMZ transformation?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect the cited robust DMZ source before reproducing transformation. |
| Smolyak 1963 sparse-grid formula | Jia 2012 and adaptive SGHF rely on Smolyak construction | `FOUNDATIONAL` | Not checked in P1R | "Where is the actual sparse-grid construction from?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect Smolyak or a primary/standard numerical-analysis source. |
| Genz spherical rules, Stroud cubature, Mysovskikh/Cools cubature tables | Jia 2013 high-degree CKF derives spherical-radial rules from them | `FOUNDATIONAL` | Not checked in P1R | "Are the cubature rules and exactness claims grounded in primary cubature literature?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | Medium | Inspect at least Genz 2003 and Stroud before full cubature derivation. |
| Arasaratnam--Haykin CKF and Arasaratnam--Haykin--Hurd continuous-discrete CKF | Jia 2012/2013 comparisons; current chapters mention CKF | `DIRECT_METHOD` | Not checked in P1R, likely in references | "Why discuss high-degree CKF without deriving baseline CKF?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect CKF primary papers for baseline and point-rule comparison. |
| Julier--Uhlmann UT/UKF and van der Merwe sigma-point thesis | Existing references and Jia 2012 UKF-subset theorem | `FOUNDATIONAL` | Present in `docs/references.bib`; not technically checked in P1R | "Are sigma-point claims derived or just cited?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | Medium | Recheck technical sections before theorem/proposition prose. |
| Ito--Xiong Gaussian filters; Gauss--Hermite quadrature filtering | Jia 2012/2013 rely on Gaussian approximation filter forms | `FOUNDATIONAL` | Not checked in P1R | "Where is the Gaussian approximation filter baseline from?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | Medium | Inspect for Ch34 baseline derivations. |
| Reich ensemble transform particle filter and EnKF/localization literature | Transport-map filtering related work | `DIRECT_METHOD`/`FOUNDATIONAL` | Reich 2013 present in `docs/references.bib`; not technically checked in P1R | "Why is ensemble transport discussed without Reich/EnKF localization foundations?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect Reich and a small EnKF/localization foundation set. |
| Villani optimal transport; Peyre--Cuturi computational OT | Transport filtering relies on OT/couplings | `FOUNDATIONAL` | Present in `docs/references.bib`; not checked in P1R | "Are OT definitions being used precisely?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | Medium | Use as definitions/context; avoid theorem-level transport claims unless checked. |
| Rosenblatt and Knothe rearrangement foundations | Zhao--Cui, DIRT, transport maps | `FOUNDATIONAL` | Rosenblatt appears in TT sampling references; not checked in P1R | "Where do the triangular/KR map definitions come from?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect primary or standard transport-map sources. |
| Gordon, Doucet, Arulampalam, Chopin SMC foundations | Particle filter baseline and degeneracy contrast | `FOUNDATIONAL` | Several present in `docs/references.bib`; not rechecked in P1R | "Are particle-filter baselines and correction claims fair?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | Medium | Recheck if particle filter section remains in rewrite. |
| Bengtsson--Bickel--Li and Snyder et al. high-dimensional particle filter collapse | Current chapters cite high-dimensional PF collapse | `FOUNDATIONAL`/`COMPETITOR` | Present in `docs/references.bib`; not rechecked in P1R | "Is the high-dimensional degeneracy warning technically faithful?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Inspect technical claims before using collapse statements. |
| Neal HMC, Hoffman--Gelman NUTS, Betancourt HMC diagnostics | HMC chapter and NeuTra context | `FOUNDATIONAL` | Present in `docs/references.bib`; not rechecked in P1R | "Are HMC diagnostic claims grounded in HMC literature?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | High | Recheck technical sections before HMC derivations. |
| Girolami--Calderhead RMHMC | Geometry-aware HMC comparison | `COMPETITOR` | Present in `docs/references.bib`; not rechecked in P1R | "Why discuss geometry-aware acceleration without RMHMC?" | `PROMOTED_BLOCKER` | `PARTIAL_READY_BLOCKER` | Medium | Inspect before comparing transport-preconditioning and geometry-aware HMC. |
| Normalizing flows survey and transport-map theory beyond Parno--Marzouk | NeuTra/transport bridge | `SURVEY_OR_TUTORIAL`/`BACKGROUND` | Some present in `docs/references.bib`; not fully checked | "Are neural transports being oversold as filtering methods?" | `NOT_PROMOTED` | `ACCEPTABLE_OMISSION` unless Ch36 expands flows | Medium | Cite for context only; do not use as theorem support. |
| Spantini et al. 2016 decomposable transport workshop | Required in earlier pillar list but user reported retraction | `RETRACTED_OR_QUARANTINED` | Quarantined | "Why are you citing a retracted workshop paper?" | `QUARANTINED` | `QUARANTINED` | High | Do not cite as support; replace with checked non-quarantined sources. |
| Recent citing works of all seed papers | Forward snowballing policy | `SOURCE_BLOCKED` | No approved metadata query | "What recent follow-up invalidates or supersedes this source?" | `PROMOTED_BLOCKER` for final-complete-survey claim | `PARTIAL_READY_BLOCKER` | High | Run approved metadata-intake pass before claiming comprehensive survey coverage. |

## Reviewer-Facing Coverage Table

| Method family | Coverage status after P1R | Remaining risk |
| --- | --- | --- |
| Direct TT nonlinear filtering | Seed papers locally indexed, including correlated-noise recent paper. | TT foundations and classical DMZ/Zakai foundations remain promoted blockers for full derivations. |
| Tensor-network Kalman and square-root tensor filtering | TNKF and TNSRKF locally indexed. | Classical square-root Kalman and TT/TNm foundations need primary-source anchors. |
| Low-rank tensor UKF/observation compression | NeuroImage paper now locally indexed. | Only domain-specific support; do not generalize. |
| Transport-map filtering/smoothing | Main non-quarantined transport filtering/smoothing sources locally indexed. | OT/KR/Reich/EnKF-localization foundations need checking; decomposable workshop paper quarantined. |
| Sparse-grid and high-degree cubature filtering | Jia 2012/2013 and adaptive SGHF locally indexed. | Smolyak, Genz/Stroud, CKF/UKF/GHQ foundations need checking before full derivations. |
| Transport-preconditioned MCMC/HMC/NeuTra | Parno--Marzouk, NeuTra, DIRT locally indexed. | HMC/RMHMC/NUTS foundations need checking; no BayesFilter HMC conclusion. |
| TT sampling/rank/integration substrate | TT sampling, rank bounds, Fokker--Planck TT-cross, tensor-network integration locally indexed. | TT-cross/TT-SVD foundations and non-Gaussian rank limits need careful exposition. |

## What Is Not Concluded

This register does not mean omitted papers are wrong or irrelevant.  It records
what a skeptical panel may ask about.  Because several `PROMOTED_BLOCKER` rows
remain uninspected, P1R cannot honestly return `READY_FOR_CHAPTER_REWRITE`
without qualification.
