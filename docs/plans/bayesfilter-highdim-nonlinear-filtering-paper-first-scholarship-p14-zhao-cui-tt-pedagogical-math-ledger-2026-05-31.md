# P14 Zhao-Cui TT Pedagogical Math Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P10/P11/P12/P13 BayesFilter Zhao-Cui artifacts.

what_is_not_concluded:
- No posterior accuracy.
- No HMC readiness.
- No global derivative of adaptive TT-cross/rank-changing code.
- No production BayesFilter implementation.

## Pedagogical Changes Relative To P13

| P14 section | Pedagogical/math control |
|---|---|
| Filtering Objects Before Tensor Notation | Starts with SSM densities, derives \(q_t\), \(Z_t\), and filter marginal before TT appears. |
| Scalar Nonlinear Filtering Example | Keeps the quadratic observation example and derives the defensive-density contribution to the next filter. |
| Tensor Trains As Low-Rank Coupling | Adds two-coordinate matrix rank factorization and three-coordinate TT factorization before functional TT notation. |
| From Square-Root Approximation To A Filter | Derives \(\sqrt q\), \(\phi^2+\tau\lambda\), normalizer, marginal, mass matrices, and TT contraction. |
| Zhao-Cui Sequential Construction | Presents the sequential recursion and conditional/KR factorization with equations before prose. |
| Adaptive vs Gradient | Introduces branch variable \(B\), adaptive scalar \(\widehat\ell(\alpha;B(\alpha))\), and fixed-branch derivative. |
| Fixed-Branch Algorithm | Gives fixed branch specification, target values, interpolation/LS alternatives, normalizer, filter, and stored numerator. |
| Proposition 2 | Split into Layers A--F before formal proposition. |

Decision:
`P14_PEDAGOGICAL_MATH_DRAFT_CREATED`
