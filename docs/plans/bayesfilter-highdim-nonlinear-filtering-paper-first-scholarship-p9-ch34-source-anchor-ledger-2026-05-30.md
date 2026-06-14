# P9 Ch34 Source Anchor Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Rewritten `ch34`, P9 plan, P8 source-anchor ledger,
Jia--Xin--Cheng 2012, Jia--Xin--Cheng 2013, Singh et al. 2018,
Julier--Uhlmann 1997, Arasaratnam--Haykin 2009, and the scholarly literature
audit policy.

what_is_not_concluded: This ledger does not conclude exhaustive literature
coverage, posterior accuracy, HMC convergence, production readiness, or broad
method validation.  Source-scope boundaries are not treated as P9
implementability blockers unless a construction used in the chapter lacks a
checked anchor or project derivation.

## Source Anchors

| P9 construction or claim | Chapter anchor | Support class | Source/project anchor |
|---|---|---|---|
| Tensor-product GHQF as conventional baseline. | Section `bf-hd-tensor-product-ghq` | `PRIMARY_TECHNICAL_SUPPORT` plus notation translation | Jia--Xin--Cheng 2012 Section 2.2.1. |
| One-dimensional GHQ exactness degree and construction context. | GHQF one-dimensional rule paragraph | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Section 2.2.1. |
| GHQF prediction/update recursion in BayesFilter notation. | Algorithm `bf-hd-ghqf-step` | `PROJECT_DERIVATION` | Gaussian projection derivation plus GHQ rule. |
| SGQF source-local sparse-grid formula. | Eq. `bf-hd-sgqf-smolyak` | `PRIMARY_TECHNICAL_SUPPORT` with notation translation | Jia--Xin--Cheng 2012 Eq. 26--29. |
| SGQF exactness/construction algorithm/UKF relation. | Fixed SGQF section | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Theorem 3.1, Algorithm 1, Theorem 3.2. |
| Fixed sparse-grid default univariate level policy \(s_\ell=2\ell-1\). | Eq. `bf-hd-sgqf-level-policy` | `PRIMARY_TECHNICAL_SUPPORT` plus project implementation choice | Jia--Xin--Cheng 2012 Section 3.2 discusses \(2\ell-1\) symmetric points; P9 fixes standard-normal GHQ as default. |
| Fixed sparse-grid duplicate-node dictionary and filter step. | Algorithms `bf-hd-construct-fixed-sgq`, `bf-hd-fixed-sgqf-step` | `PROJECT_DERIVATION` from source formula | Implementation expansion of Jia--Xin--Cheng construction. |
| ASGHF admissible index/error indicator/adaptive selection. | Section `bf-hd-asghf`, Algorithm `bf-hd-select-asghf` | `PRIMARY_TECHNICAL_SUPPORT` with notation translation | Singh et al. 2018 Section 3. |
| ASGHF pilot integrand and frozen node/weight assembly. | Eq. `bf-hd-asghf-pilot-integrand`; Algorithm `bf-hd-assemble-frozen-asghf` | `PROJECT_DERIVATION` from source ASGHF mechanics | Project implementation convention to make Singh et al.'s adaptive rule reproducible for filtering moments. |
| Fixed-SGQF analytical gradient recursion. | Section `bf-hd-fixed-sgqf-gradient` | `PROJECT_DERIVATION` | Local derivation patterned after `ch18`; not a claim from Jia/Singh. |
| HMC admissibility labels. | HMC table and method-local labels | `PROJECT_DERIVATION` | Same-scalar contract and branch-smoothness reasoning. |

## Citation Placement

P9 cites the technical sources where their checked constructions enter:
Jia--Xin--Cheng 2012 at GHQF/SGQF construction and SGQF exactness/algorithm;
Singh et al. 2018 at ASGHF adaptive mechanics; earlier P8 citations for
Julier--Uhlmann, Arasaratnam--Haykin, and Jia--Xin--Cheng 2013 remain local to
their method sections.
