# P1U Claim-Support Update

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T plus P1U newly supplied local PDFs.

what_is_not_concluded: see section "What Is Not Concluded".

## Claim-Support Rows

| planned_rewrite_claim | support_class | checked_support | allowed_use | blocker_or_limit |
| --- | --- | --- | --- | --- |
| TT-cross gives a source-local interpolation formula for low TT-rank tensors and a black-box integration strategy whose complexity is rank dependent. | `PRIMARY_TECHNICAL_SUPPORT` | Oseledets--Tyrtyshnikov 2010 Theorem 3.1, Algorithms 2--3, Section 4 integration examples. | Ch35/Ch37 TT-cross substrate exposition. | Rank boundedness and BayesFilter filtering validity remain unproved. |
| Savostyanov maxvol/quasioptimality is an important but unavailable stronger source. | `SOURCE_GAP_BLOCKER` | Supplied Savostyanov-named PDF is misidentified. | Omission/source blocker only. | No Savostyanov-specific theorem support. |
| PR-DMZ can be motivated as a pathwise/multiplicative transformation of nonlinear filtering equations. | `PRIMARY_TECHNICAL_SUPPORT` | Davis 1980 multiplicative functional setup and generator theorem; Yau--Yau 2000/2008 robust DMZ equations. | Ch33 pathwise robust filtering foundations. | Must state assumptions; no BayesFilter implementation claim. |
| Yau--Yau offline/online memoryless algorithms solve PR-DMZ through observation-frozen Kolmogorov equations under their hypotheses. | `PRIMARY_TECHNICAL_SUPPORT` | Yau--Yau 2000 Proposition 3.1 and convergence theorems; Yau--Yau 2008 Proposition 2.1, Theorems A/B/C, appendices. | Ch33/Ch35 PDE-filtering algorithms and proof sketches. | Avoid "all engineering problems" overclaim. |
| Recent PR-DMZ/QTT work links higher-order weighted Sobolev regularity to sparse FTT/QTT approximation and QTT error estimates. | `PRIMARY_TECHNICAL_SUPPORT` | Meng--Wang--Yau--Zhang 2025 Theorems 3.3, 3.10, 4.1, 4.11 and Algorithms 1--2. | Ch35 recent TT-PDE filtering exposition, with an explicit arXiv preprint/version caveat. | Preprint status does not support peer-reviewed theorem-finality; no NAWM/BayesFilter validation. |
| Rosenblatt transformation maps an absolutely continuous multivariate distribution to independent uniforms by a triangular conditional-CDF transform. | `PRIMARY_TECHNICAL_SUPPORT` | Rosenblatt 1952 construction and proof. | Ch35/Ch36 triangular/KR transport foundations. | Knothe original remains blocked. |
| Stroud's book is a standard catalogue of multiple-integration formulas. | `SURVEY_CONTEXT_ONLY` | Mathematics of Computation review of Stroud book. | Historical context only if needed. | No formula/theorem support. |
| Sparse-grid and high-degree cubature filtering can be explained source-locally from checked filtering papers. | `PRIMARY_TECHNICAL_SUPPORT` | Jia 2012 SGQF; Jia 2013 high-degree CKF; Arasaratnam--Haykin 2009 CKF; Julier--Uhlmann 1997 UKF. | Ch34 method derivations and algorithms. | Do not claim independent Smolyak/Genz/Stroud theorem support. |
| High-dimensional particle collapse is a real failure mode under stated assumptions. | `PRIMARY_TECHNICAL_SUPPORT` | Bengtsson--Bickel--Li 2008; Snyder et al. 2008; Gordon 1993 with OCR caveat; Arulampalam 2002. | Ch33/Ch35 degeneracy propositions and diagnostics. | Do not claim all PFs fail or structured proposals cannot help. |
| RMHMC is a geometry-aware competitor with nonseparable Hamiltonian and metric-derivative burdens. | `PRIMARY_TECHNICAL_SUPPORT` | Girolami--Calderhead 2011 local PDF from P1T. | Ch36 comparison and algorithmic burden discussion. | No convergence/NAWM success claim. |

## Replacement-Path Anchor Detail

P1U authorizes only the following replacement paths:

- Smolyak-original gap: Jia 2012 equations (26)--(29), Theorem 3.1, Algorithm 1,
  and Propositions 3.1--3.2 support SGQF source-local sparse-grid filtering
  prose.  They do not support a historical Smolyak theorem.
- Genz/Stroud-original gap: Arasaratnam--Haykin 2009 equations (21)--(33) and
  Appendix algorithms, Jia 2013 Definition 3.1, Theorem 3.1, Propositions
  3.1--3.2, and rules (40)--(46) support filtering-specific cubature prose.
  The Stroud review supplies context only.
- Knothe-original gap: Rosenblatt 1952 supports the conditional-CDF triangular
  transformation to independent uniforms; Spantini--Baptista--Marzouk 2022
  Sections 3.2--3.7, Algorithms 1--3, and Appendices A--B support
  source-local triangular-map filtering algorithms; Zhao--Cui 2024 Lemma 1,
  Propositions 2/4/5/6/9/11, Theorems 7--8, and Corollary 12 support
  conditional KR constructions in the TT sequential-learning setting;
  Cui--Dolgov 2021 Propositions 1--7, Theorems 1/3/4, and Algorithms 1--4
  support inverse Rosenblatt TT transport outside filtering.  None of these
  supports original Knothe priority/proof.
- Original DMZ historical gap: van Handel Chapter 7.2 supports standard Zakai
  and Kushner--Stratonovich equations; Davis 1980 supports a multiplicative
  functional/pathwise transformation; Yau--Yau 2000/2008 support robust-DMZ
  memoryless algorithms under their hypotheses.  None of these supports
  unchecked original-priority claims for Duncan, Mortensen, or Zakai.

## What Is Not Concluded

No chapter is yet rewritten or accepted.  No claim in this ledger is a
BayesFilter validation claim.  Citation counts, venue metadata, file names, and
abstracts are not theorem support.
