# P28 Source-Fidelity Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Source-fidelity audit against Zhao--Cui Sections 1--3 and 5.
- Dependency escalation for appendices and cited external results when P27 relies on them.

what_is_not_concluded:
- PDF text extraction does not replace visual page-by-page inspection of the source paper.
- This ledger does not certify equations from Zhao--Cui Sections 4, 6, or the appendices except where explicitly noted.

## Source Artifact

- local_pdf: `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`
- extracted_text: `/tmp/zhao_cui_paper.txt`
- extraction_status: `AVAILABLE_BUT_DISPLAY_STRUCTURE_IMPERFECT`

## Numbered Equation Spine Checked

| Zhao--Cui item | paper location from extracted text | P27 location | status | notes |
|---|---:|---|---|---|
| Eqs. (1)--(2): state and observation densities | lines 42, 56 | P27 Sections 5 and 7 | EXPANDED | State-space model and conditional-independence notation reconstructed. |
| Eq. (3): full joint density | line 95 | P27 Section 5 | EXPANDED | Product factorization derived. |
| Eq. (4): posterior/evidence | line 103 | P27 Section 5 | EXPANDED | Bayes numerator/normalizer explained. |
| Eqs. (5)--(8): filtering, parameter, path, smoothing marginals | lines 111, 120, 124, 130 | P27 Section 6 | EXPANDED | Treated as marginalization problems. |
| Eqs. (9)--(11): recursive bottleneck | lines 311, 322, 335 | P27 Section 7 | EXPANDED | Derived by Bayes rule and integration. |
| Eq. (12): TT approximation target | line 476 | P27 Section 15 | EXPANDED | Algorithm 1 annotation present. |
| Eq. (13): squared TT approximation | line 546 | P27 Sections 16--17 | EXPANDED | Defensive density and shift discussed. |
| Lemma 1 | lines 573--590 | P27 Section 17 | SUPPORT_ONLY | P27 cites and explains; does not reprove Cui--Dolgov theorem. Acceptable if not presented as project proof. |
| Proposition 2 / Eq. (14): mass marginalization | lines 594--619 | P27 Section 18 | EXPANDED | Mass-matrix contraction reconstructed. Requires deep algebra/dimension review. |
| Algorithm 2 | lines 711--744 | P27 Section 20 | EXPANDED | Annotated, but final submission should visually compare every algorithm line. |
| Eqs. (15)--(16): squared sequential target | lines 718, 735 | P27 Section 20 | EXPANDED | Present in annotation. |
| Eqs. (17)--(20): KR maps / conditionals | lines 797, 802, 823, 885 | P27 Sections 19, 21, 22 | EXPANDED | KR construction is high-risk; chair-reader ledger still flags teachability risk. |
| Eqs. (21)--(23): particle proposal/correction | lines 929, 945, 965 | P27 Section 21 | EXPANDED | Proposal and correction weights reconstructed. |
| Eqs. (24)--(26): backward path/smoothing | lines 1089, 1103, 1262 | P27 Section 22 | EXPANDED | Present; needs visual source-line confirmation. |
| Eqs. (27)--(29): error propagation | lines 1371, 1396, 1407 | P27 Section 23 | SUPPORT_ONLY | P27 states what these prove and do not prove. Deep proof not central to fixed-branch derivative. |
| Eqs. (30)--(33): preconditioning identities | lines 1780, 1798, 1813, 1847 | P27 Section 24 | EXPANDED | Pullback/pushforward normalizer invariance included. |
| Eqs. (34)--(35): bridging/preconditioned density | lines 1945, 1957 | P27 Section 24 | EXPANDED | Tempering/bridge expanded. |
| Algorithm 5 | lines 2019--2035 | P27 Section 24 | EXPANDED | Annotated; final submission should compare every step visually. |

## Dependency Escalations

| issue id | dependency | why escalated | status |
|---|---|---|---|
| P28-I009 | Cui and Dolgov theorem behind Zhao--Cui Lemma 1 and Proposition 2 | P27 uses squared-TT error and mass-marginalization claims. | HUMAN_REVIEW_REQUIRED_NOT_REPROVED |
| P28-I010 | Zhao--Cui Appendix lemmas for error propagation | P27 explains Section 4 limitations and large-scale claims. | SUPPORT_ONLY_NOT_SUBMISSION_BLOCKER unless the note claims full propagation theorem. |
| P28-I011 | Spantini/Rosenblatt transport references | P27 motivates KR maps and triangular transport. | HUMAN_REVIEW_REQUIRED for broad transport optimality claims; local Jacobian identity checked separately. |

## Verdict

source_fidelity_verdict: `NOT_READY_FOR_FLAWLESS_CLAIM`

P27 appears to reconstruct the main displayed spine of Zhao--Cui Sections 1--3 and 5, but this P28 pass relied partly on extracted text and targeted matching.  A final claim that every Zhao--Cui source equation is faithfully annotated requires a visual page-by-page source audit, especially Algorithm 2, Algorithm 5, Proposition 2, and KR-conditionals.
