# P29 Mass And Normalizer Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Targeted audit of squared-TT mass contractions, marginalization, normalizers, and derivative normalizer identities.

what_is_not_concluded:
- This does not prove numerical Cholesky stability.
- This does not certify all TT implementation index conventions outside the audited equations.

## Audit Table

| P27 label | role | audit finding | status |
|---|---|---|---|
| `eq:p24-m1` | square marginal expansion | Correct expansion of integral of squared product using right-interface mass matrix. | PASS_TARGETED_AUDIT |
| `eq:p24-m2` | right mass matrix definition | Dimensions: `M_{>k}` is `R_k x R_k`; positive semidefinite by Gram form. | PASS_TARGETED_AUDIT |
| `eq:p24-m3` | Cholesky/square-root representation | Correct if `M_{>k}=L L^T`. Numerical Cholesky may need jitter if semidefinite. | PASS_WITH_LIMITATION |
| `eq:p24-m4` | marginal with defensive reference | Matches Zhao--Cui Eq. (14) structure: squared marginal plus `tau lambda(x_{<=k})` divided by normalizer. | SOURCE_MATCH_TARGETED |
| `eq:p24-m5` | right-to-left mass recursion | Dimensionally correct: `H_j` maps `R_{j-1}` to `R_j`; `H_j M_{>j} H_j^T` yields `R_{j-1} x R_{j-1}`. | PASS_TARGETED_AUDIT |
| `eq:p24-m6` | basis-coefficient recursion | Index structure matches elementwise integration with basis mass matrix `B_j`. | PASS_TARGETED_AUDIT |
| `eq:p24-m7`--`eq:p24-m9` | three-coordinate example | Correct worked example; useful for implementation. | PASS_TARGETED_AUDIT |
| `eq:p24-p22-o13` and derivative normalizer equations | `Zhat=e^{-c}R+tau` and derivative | Correct if `c_t` and `tau_t` are fixed. If `c_t` changes with beta, an omitted `-dot c e^{-c}R` term would be required. P27 states fixed branch/frozen shift in derivative proof. | PASS_WITH_LIMITATION |

## Verdict

mass_normalizer_verdict: `PASS_TARGETED_AUDIT_WITH_LIMITATIONS`

The mass/normalizer equations survive targeted audit. The main caveat is numerical PSD/Cholesky handling and ensuring the derivative path freezes `c_t` and `tau_t` exactly as stated.

