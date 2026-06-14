# P29 KR And Preconditioning Jacobian Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Targeted audit of P27 KR conditional maps and preconditioning coordinate-transform equations.
- Focus on Jacobian direction, invertibility, conditional ratios, and source alignment with Zhao--Cui Sections 3 and 5.

what_is_not_concluded:
- This does not prove global invertibility of all numerical KR maps.
- This does not certify every root-finding or CDF implementation detail.

## KR Map Audit

| P27 label | role | audit finding | status |
|---|---|---|---|
| `eq:p24-k1` | chain rule and conditional density ratio | Correct if denominators are positive; matches Zhao--Cui conditional-density construction after Proposition 2. | PASS_TARGETED_AUDIT |
| `eq:p24-k2`--`eq:p24-k4` | lower KR CDF map | Correct lower triangular form. Domain lower bound is `-infty` in the generic formula; finite intervals later use `a_k`. | PASS_WITH_LIMITATION |
| `eq:p24-k5`, `eq:p26-kr-teach-6` | determinant product | Correct triangular Jacobian identity: diagonal entries are conditional densities, product is joint density. | PASS_TARGETED_AUDIT |
| `eq:p24-p23-kr2-3` | two-dimensional conditional | Correct if first marginal is positive. | PASS_TARGETED_AUDIT |
| `eq:p24-p23-kr2-8d`--`eq:p24-p23-kr2-8e` | TT mass to conditional evaluator | Correct cancellation of global normalizer; denominator is unnormalized marginal `n_1(r_1)`. | PASS_TARGETED_AUDIT |
| `eq:p24-k6`--`eq:p24-k8` | upper/reverse KR | Correct reverse-order analogue; implementation must record direction. | PASS_WITH_LIMITATION |

## Preconditioning Audit

| P27 label | role | audit finding | status |
|---|---|---|---|
| `eq:p24-p1` | Zhao--Cui Eq. (30), bridge pushforward | Correct pushforward direction: density at inverse times inverse-Jacobian determinant. | SOURCE_MATCH_TARGETED |
| `eq:p24-p2` | Zhao--Cui Eq. (31), residual target | Correct derivation using bridge pushforward proportional to reference density. Requires bridge positivity. | SOURCE_MATCH_TARGETED |
| `eq:p24-p4` | Zhao--Cui Eq. (33), pullback to physical density | Correct unnormalized pullback form when `T_t` was built from the bridge. | SOURCE_MATCH_TARGETED |
| `eq:p24-p5` | normalizer invariance | Correct change-of-variables identity if `T_t` is bijective on the relevant domain. | PASS_WITH_LIMITATION |
| `eq:p24-p23-prec4`--`eq:p24-p23-prec6` | before/after flattening derivation | Correct; includes bridge normalizing constant `Z_rho`, so proportional constants are visible. | PASS_TARGETED_AUDIT |
| `eq:p26-prec-teach-7` | two-Jacobian teaching identity | Directionally correct as a teaching identity, but approximation sign should not be read as exact unless residual approximation is exact. | PASS_WITH_LIMITATION |
| `eq:p24-p16c`--`eq:p24-p17` | Algorithm 5(c.2) marginal pullback | The middle conditional-Jacobian explanation is plausible and matches Algorithm 5(c.2) structure. Because this is the densest transform in P27, visual source review is still required. | HUMAN_REVIEW_REQUIRED |

## Verdict

kr_preconditioning_verdict: `PASS_TARGETED_AUDIT_WITH_ONE_HUMAN_REVIEW_ITEM`

The main Jacobian directions are correct in targeted audit. The remaining high-risk item is the dense Algorithm 5(c.2) marginal pullback derivation; it should receive visual human review before final submission.

