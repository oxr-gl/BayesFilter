# P29 Algorithm Provenance Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Targeted provenance audit for Zhao--Cui Algorithm 1, Algorithm 2, and Algorithm 5 against P27 annotation.

what_is_not_concluded:
- This is not a full visual audit of every source symbol in the PDF.
- This does not certify all implementation details added by P27 beyond Zhao--Cui.

## Algorithm 1

| Zhao--Cui step | source anchor | P27 anchor | status | notes |
|---|---|---|---|---|
| prior retained approximation | Section 2.3 before Algorithm 1 | P27 Section 15 intro | SOURCE_MATCH_TARGETED | P27 uses `widehat pi_{t-1}` in same role. |
| (a) nonseparable target Eq. (12) | source lines around 472--476 in extracted text | `eq:p24-a1-1` | SOURCE_MATCH_TARGETED | Same product: previous approximation, transition, likelihood. |
| approximate proportionality | source before Algorithm 1 | `eq:p24-a1-0` | SOURCE_MATCH_TARGETED | P27 expands normalization meaning. |
| (b) TT reapproximation | source Algorithm 1(b) | `eq:p24-a1-2` plus LS expansion | SOURCE_MATCH_TARGETED_WITH_ADDED_DERIVATION | P27 adds fixed-rank LS implementation view, not claimed as Zhao--Cui adaptive code. |
| (c) integration and normalizer | source Algorithm 1(c) | `eq:p24-a1-3`--`eq:p24-a1-7` | SOURCE_MATCH_TARGETED | P27 expands retained filter and marginals. |

## Algorithm 2

| Zhao--Cui step | source anchor | P27 anchor | status | notes |
|---|---|---|---|---|
| (a) target Eq. (15) | source line around 718 | P27 Section 20 | SOURCE_MATCH_TARGETED | Same nonseparable target. |
| (b) sqrt TT and Eq. (16) | source lines around 727--735 | P27 Section 20 and Sections 16--18 | SOURCE_MATCH_TARGETED | P27 explains squared TT and defensive density. |
| (c) integrate old state using Proposition 2 | source lines around 737--744 | P27 Section 20 and Section 18 | SOURCE_MATCH_TARGETED | P27 expands mass contraction. |
| lower KR for path/smoothing | source after Algorithm 2 | P27 Sections 19, 22 | SOURCE_MATCH_TARGETED_WITH_REVIEW | Dense map notation; source visual review recommended. |
| upper KR for particle proposal | source Remark 3 and forward map equations | P27 Sections 19, 21 | SOURCE_MATCH_TARGETED_WITH_REVIEW | Directional distinction present. |

## Algorithm 5

| Zhao--Cui step | source anchor | P27 anchor | status | notes |
|---|---|---|---|---|
| Eq. (30) bridge pushforward | source Section 5.1 | `eq:p24-p1` | SOURCE_MATCH_TARGETED | Correct direction. |
| Eq. (31) residual target | source Section 5.1 | `eq:p24-p2` | SOURCE_MATCH_TARGETED | Correct ratio/reference form. |
| Eq. (32) residual squared TT | source Section 5.1 | `eq:p24-p3` | SOURCE_MATCH_TARGETED | Correct. |
| Eq. (33) pullback density | source Section 5.1 | `eq:p24-p4` | SOURCE_MATCH_TARGETED | Correct. |
| (b.1) bridge approximation Eq. (35) | source Algorithm 5 | `eq:p24-p7b`, `eq:p24-p7l` | SOURCE_MATCH_TARGETED | Correct. |
| (b.2) lower map and bridge marginal | source Algorithm 5 | `eq:p24-p8`--`eq:p24-p11c` | SOURCE_MATCH_TARGETED_WITH_REVIEW | Correct structure; visual symbol audit recommended. |
| (b.3) pushforward residual fit | source Algorithm 5 | `eq:p24-p12`--`eq:p24-p13a` | SOURCE_MATCH_TARGETED | Correct. |
| (c.1) integrate residual last block | source Algorithm 5 | `eq:p24-p14`--`eq:p24-p15` | SOURCE_MATCH_TARGETED | Correct. |
| (c.2) retained physical marginal | source Algorithm 5 | `eq:p24-p16`--`eq:p24-p17` | HUMAN_REVIEW_REQUIRED | P27 expands a dense derivation; source visual check still needed. |

## Verdict

algorithm_provenance_verdict: `SOURCE_MATCH_TARGETED_WITH_ONE_HUMAN_REVIEW_ITEM`

Algorithm 1 and the main Algorithm 2/5 spine are source-aligned in targeted audit. Algorithm 5(c.2) remains the one item requiring visual human review because it is dense and central.

