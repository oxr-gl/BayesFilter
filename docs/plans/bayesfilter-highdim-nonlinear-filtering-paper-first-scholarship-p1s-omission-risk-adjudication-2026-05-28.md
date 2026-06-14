# P1S Omission-Risk Adjudication

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: P1R seed set plus P1S promoted blocker candidates.

what_is_not_concluded: see section "What Is Not Concluded".

## Purpose

This register adjudicates the P1R `PROMOTED_BLOCKER` rows.  Metadata status
does not close scholarly blockers.  A blocker is closed only by checked
technical anchors, explicit scope deferral, source block, quarantine, or a
decision that the item is not in the rewrite scope.

## Adjudication Rows

| p1r_source_row_or_topic | p1r_risk | severity | p1s_evidence | closure_basis | technical_anchor_reference | adjudication | reviewer_answer | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Oseledets 2011 tensor-train decomposition / TT-SVD | TT storage/rank/rounding needs original TT format | High | Local SIAM PDF indexed and OpenAlex DOI metadata checked | `PRIMARY_ANCHOR` | Oseledets 2011 Definition of TT format; Theorems 2.1/2.2; Corollary 2.4; Algorithms 1--2; complexity sections | `CLOSED` | We can cite and derive TT storage/SVD/rounding from Oseledets directly. | Use in Ch35 before TT filtering claims. |
| TT-cross/maxvol foundations | Need primary cross approximation and maxvol sources | High | Public PDF attempt failed; checked seed papers only use TT-cross source-locally | `SOURCE_BLOCKED` | `SOURCE_BLOCKED_NO_PRIMARY_ANCHOR` | `REMAINS_SOURCE_BLOCKED` | TT-cross will not be proved from primary sources unless PDF is supplied. | Manual placement or keep as blocker. |
| Zakai/Duncan/Mortensen/Kushner--Stratonovich filtering foundations | Need primary or standard derivation anchors for filtering equations | High | van Handel lecture notes indexed with Ch. 7.2 propositions | `STANDARD_MONOGRAPH_ANCHOR` | van Handel Proposition 7.2.6; Proposition 7.2.8; Proposition 7.2.9; Zakai PDE discussion | `CLOSED` | We have a standard derivation anchor, but not original historical priority papers. | Use standard anchor; cite originals only after checking if needed. |
| Robust/pathwise DMZ | Need robust/pathwise transformation source | High | No primary robust DMZ source obtained; TT papers checked only source-locally | `SOURCE_BLOCKED` | `SOURCE_BLOCKED_NO_PRIMARY_ANCHOR` | `REMAINS_SOURCE_BLOCKED` | Robust/pathwise DMZ remains a blocker for full derivation. | Keep source-local or request source. |
| Smolyak 1963 sparse-grid formula | Need actual sparse-grid construction | High | No primary Smolyak full text; Jia 2012 source-local formula checked | `EXPLICIT_SCOPE_DEFERRAL` | Jia 2012 equations (26)--(29), Theorem 3.1, Algorithm 1 | `DEFER_TO_CHAPTER_REWRITE` | Ch34 can explain SGQF as Jia's method; broad Smolyak derivation remains out of scope unless source obtained. | Write source-local SGQF derivation or obtain Smolyak. |
| Genz/Stroud cubature rules | Need cubature exactness foundations | Medium | No primary full text; Jia 2013 source-local high-degree rules checked | `EXPLICIT_SCOPE_DEFERRAL` | Jia 2013 Definition 3.1; Theorem 3.1; Proposition 3.1; rules (40)--(46); Proposition 3.2 | `DEFER_TO_CHAPTER_REWRITE` | Ch34 can derive high-degree CKF from Jia; broader cubature history remains scoped. | Avoid independent Stroud/Genz claims. |
| Arasaratnam--Haykin CKF | Need primary CKF baseline | High | Public source attempt failed SSL certificate verification; no local full text | `SOURCE_BLOCKED` | `SOURCE_BLOCKED_NO_PRIMARY_ANCHOR` | `REMAINS_SOURCE_BLOCKED` | CKF cannot be fully derived from primary paper in the rewrite unless user supplies it. | Manual PDF requested if CKF derivation is required. |
| Julier--Uhlmann UT/UKF | Need sigma-point claim support | Medium | Julier--Uhlmann 1997 local PDF indexed | `PRIMARY_ANCHOR` | consistency Eq. 6; Taylor expansion around Eq. 7; sigma points around Eq. 12; transformed mean/covariance formulas; UKF prediction/update boxes | `CLOSED` | UT/UKF baseline can be cited from Julier--Uhlmann. | Use for baseline only; scaled variants need separate source. |
| Ito--Xiong / Gaussian approximation filters | Need Gaussian approximation filter foundation | Medium | No primary Ito--Xiong source obtained; Jia source-local Gaussian equations checked | `EXPLICIT_SCOPE_DEFERRAL` | Jia 2012 equations (1)--(25); Jia 2013 equations (1)--(15) | `DEFER_TO_CHAPTER_REWRITE` | The rewrite can stay source-local to Jia's Gaussian approximation filter setup. | Avoid independent Ito--Xiong derivation. |
| Reich ensemble transform and EnKF/localization | Need transport ensemble baseline | High | Reich 2013 PDF indexed; EnKF/localization general sources not inspected | `PRIMARY_ANCHOR` | Reich Sections 2--4; optimal transport formulation; Theorem 3.2; high-dimensional caveat in conclusion | `CLOSED` for Reich; `DEFER_TO_CHAPTER_REWRITE` for EnKF/localization | Reich closes ETPF baseline; EnKF/localization remains scoped unless chapter expands it. | Use Reich and checked Spantini localization appendix; do not claim broad EnKF survey. |
| Villani/Peyre--Cuturi OT | Need OT definitions/context | Medium | No full technical OT monograph text inspected; Peyre--Cuturi download is HTML landing page only | `EXPLICIT_SCOPE_DEFERRAL` | checked modern transport sources from P1R and Reich 2013 source-local OT formulation | `DEFER_TO_CHAPTER_REWRITE` | Use source-local transport definitions unless deriving OT theory. | Inspect full OT monograph if theorem-level OT claims are needed. |
| Rosenblatt/Knothe rearrangement | Need triangular/KR foundations | High | No primary Rosenblatt/Knothe source; Zhao--Cui/DIRT/Spantini source-local triangular transport checked in P1R | `EXPLICIT_SCOPE_DEFERRAL` | Zhao--Cui conditional KR construction; Cui--Dolgov inverse Rosenblatt propositions/algorithms; Spantini triangular map algorithms | `DEFER_TO_CHAPTER_REWRITE` | Use modern checked transport-map sources; do not claim historical KR theorem support. | Obtain primary/standard KR source for a formal theorem. |
| Gordon/Doucet/Arulampalam/Chopin SMC foundations | Need particle-filter baseline support | Medium | Arulampalam PDF indexed; Gordon original blocked; Doucet/Chopin bibliography exists but full technical source not checked | `PRIMARY_ANCHOR` for tutorial mechanics; `EXPLICIT_SCOPE_DEFERRAL` for monographs/original | Arulampalam SIS Algorithm 1, resampling Algorithm 2, generic PF Algorithm 3, SIR Algorithm 4, degeneracy discussion | `CLOSED` for baseline terminology; `DEFER_TO_CHAPTER_REWRITE` for historical/original detail | Baseline PF definitions are supported; original bootstrap priority and monograph depth remain optional. | Use Arulampalam for baseline; avoid over-detailed historical claims. |
| Bengtsson--Bickel--Li and Snyder high-dimensional PF collapse | Need technical support for collapse warnings | High | Snyder exact OpenAlex metadata found; full text blocked; Bengtsson full text not obtained | `SOURCE_BLOCKED` | `SOURCE_BLOCKED_NO_PRIMARY_ANCHOR` | `REMAINS_SOURCE_BLOCKED` | High-dimensional PF collapse remains a blocker for theorem-level statements. | User/manual PDF needed before strong collapse derivation. |
| Neal/Hoffman--Gelman/Betancourt HMC foundations | Need HMC mechanics and diagnostics | High | Neal, Hoffman--Gelman, Betancourt PDFs indexed; NUTS metadata checked | `PRIMARY_ANCHOR`/`STANDARD_MONOGRAPH_ANCHOR` | Neal Sections 5.2--5.4; Hoffman--Gelman Algorithms 1--6; Betancourt Sections 3--5 and divergence discussion | `CLOSED` | HMC mechanics, NUTS reference role, and diagnostic caution are supported. | Use with no convergence/production claims. |
| Girolami--Calderhead RMHMC | Need geometry-aware competitor | Medium | Public source attempt failed; no local full text | `SOURCE_BLOCKED` | `SOURCE_BLOCKED_NO_PRIMARY_ANCHOR` | `REMAINS_SOURCE_BLOCKED` | RMHMC cannot be derived or compared in detail. | Request/manual PDF before detailed comparison. |
| Recent citing works of all seed papers | Need forward snowball coverage | High | OpenAlex forward rows completed for several exact seed records; explicit blocked/failed/search-only rows added for remaining seeds and promoted blockers | `EXPLICIT_SCOPE_DEFERRAL` | P1S snowball ledger forward rows and per-seed completion matrix with query strings/dates/sentinels | `DEFER_TO_CHAPTER_REWRITE` | Forward coverage remains an active reviewer-risk blocker for any later comprehensive-survey or rewrite-readiness claim. It is not closed by P1S. | Inspect high-risk candidates and complete exact forward queries before final chapter audit or comprehensive-survey language. |
| Spantini et al. 2016 decomposable transport workshop | User reported retracted | High | Quarantine retained | `QUARANTINED` | user quarantine report 2026-05-28; no support allowed | `QUARANTINED` | The paper is excluded and cannot support claims. | Use non-quarantined Spantini/Ramgraber/Zhao--Cui sources. |

## Top Remaining Reviewer Risks

- TT-cross/maxvol primary foundations.
- Robust/pathwise DMZ transformations.
- Arasaratnam--Haykin CKF primary paper.
- High-dimensional PF collapse papers by Bengtsson--Bickel--Li and Snyder et
  al.
- RMHMC primary paper.
- Broad Smolyak/Stroud/Genz sparse-grid/cubature foundations if Ch34 wants
  derivations beyond Jia.
- Forward-snowball candidates surfaced by OpenAlex, especially transport
  filtering follow-ups and high-dimensional geoscience PF review, before a
  final "comprehensive survey" claim.

## What Is Not Concluded

This register does not make the chapters scholarly or review-ready.  It
identifies which P1R risks were closed, scoped, quarantined, or remain blocked.
