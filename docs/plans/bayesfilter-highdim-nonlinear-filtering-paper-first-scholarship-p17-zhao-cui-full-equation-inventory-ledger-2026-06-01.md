# P17 Zhao-Cui Full Equation Inventory Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit and paper-code crosswalk ledgers.
- P11--P16 Zhao-Cui derivative, implementability, and annotated reconstruction artifacts.

what_is_not_concluded:
- No claim that Section 4 theory is fully reconstructed.
- No claim that Section 6 numerical examples are replicated.
- No claim that adaptive TT-cross or rank changes are globally differentiable.
- No production BayesFilter implementation claim.

## Disposition Rule

Material displayed formulas and mathematical algorithm lines from Zhao--Cui
Sections 1--3 and 5 must be `expanded` or
`expanded_as_part_of_larger_derivation`.  `support_only` is used only for
theorem statements whose external proof is not re-proved but whose local
mathematical role is taught.

## Inventory

| Source anchor | Source role | Disposition | P17 note location | Coverage | P16 status |
|---|---|---|---|---|---|
| Sec. 1 notation: \(x_{t,<j},x_{t,>j},x_{t,\le j},x_{t,\ge j}\) | coordinate grouping for conditional maps | `expanded` | N1--N2 | derivation meaning and map role | missed |
| Sec. 1 notation: Hellinger distance | square-root density error metric | `expanded` | N3 | formula and reason for square-root TT | compressed |
| Sec. 1 notation: pushforward \(S_\#p\) | density transform | `expanded` | N4 | change-of-variable formula and implementation object | missed |
| Sec. 1 notation: pullback \(S^\#\eta\) | inverse density transform | `expanded` | N5 | change-of-variable formula and implementation object | missed |
| Eq. (1) | transition model | `expanded` | BF-1 | symbols and Markov meaning | adequate |
| Eq. (2) | observation model | `expanded` | BF-2 | symbols and conditional-independence meaning | adequate |
| Eq. (3) | joint density | `expanded` | BF-3 | chain-rule derivation | adequate |
| Eq. (4) | posterior/evidence | `expanded` | BF-4 | evidence integral and posterior | adequate |
| Eqs. (5)--(8) | filtering, parameter, path, smoothing marginals | `expanded` | BF-5--BF-8 | all as marginalization tasks | adequate |
| Eq. (9) | recursive posterior | `expanded` | BF-9 | Bayes-rule derivation | adequate |
| Eq. (10) | adjacent-state posterior | `expanded` | BF-10 | integration over old path | adequate |
| Eq. (11) | next parameter-state filter | `expanded` | BF-11 | marginalization bottleneck | adequate |
| Sec. 2.2 TT summation with endpoint ranks | functional TT definition | `expanded` | TT-1, TT-1a, TT-2 | matrix product plus source index form | compressed |
| Sec. 2.2 basis expansion \(H_k=\sum_j\phi A_k\) | core coefficient definition | `expanded` | TT-3 | coefficient axes and implementation storage | compressed |
| Sec. 2.2 split \(L_\rho R_\rho\) | rank meaning across a split | `expanded_as_part_of_larger_derivation` | TT-2a | rank interpretation | missed |
| Sec. 2.2 core integration | TT marginalization | `expanded` | TT-4--TT-5 | core integral formula | adequate |
| Sec. 2.2 complexity \(O(DpR^2)\), \(O(DpR^3)\) | TT fitting cost | `expanded` | TT-10--TT-11 | cost and diagnostic caveat | missed |
| Sec. 2.3 approximate proportionality | unnormalized storage convention | `expanded` | A1-0 | normalization-after-contraction meaning | missed |
| Algorithm 1(a), Eq. (12) | nonseparable target | `expanded` | A1-1 | target evaluator | adequate |
| Algorithm 1(b) displayed TT over \((x_t,\theta,x_{t-1})\) | separable reapproximation | `expanded` | A1-2--A1-2d | source TT plus implementable ALS view | compressed |
| Algorithm 1(c) old-state integration | retained filter | `expanded` | A1-3--A1-4, A1-7 | retained evaluator for next step | compressed |
| Algorithm 1(c) normalizer | evidence-like contraction | `expanded` | A1-5 | complete TT contraction | adequate |
| Algorithm 1 marginals | parameter/filter densities | `expanded` | A1-6 | distinct outputs from same TT | missed |
| Sec. 3 square-root approximation | nonnegativity | `expanded` | S1--S3 | defensive density and support ratio | adequate |
| Lemma 1 | square-root/Hellinger error | `support_only` | S4--S6 | statement and interpretation; proof remains external to Cui--Dolgov | compressed |
| Proposition 2/Eq. (14) | squared-TT marginal | `expanded` | M1--M6 | mass matrix derivation | adequate |
| Three-coordinate marginal example | pedagogical expansion | `expanded_as_part_of_larger_derivation` | M7--M9 | concrete mass recursion | new |
| Conditional density ratios | KR construction | `expanded` | K1--K4 | lower conditional CDFs | adequate |
| Proposition 4 | lower map sampling proof | `expanded` | K5 and B1--B2 | triangular Jacobian proof and conditional role | adequate |
| Remark 3 / upper map | reverse-order KR map | `expanded` | K6--K8 | upper conditional construction | compressed |
| Sec. 3.1 map costs | conditional-map complexity | `expanded` | K9--K11 | preprocessing and per-sample costs | missed |
| Algorithm 2, Eqs. (15)--(16) | squared-TT sequential approximation | `expanded` | A2-1--A2-5 | target, square-root fit, defensive density, normalizer, retained filter | adequate |
| Eq. (17) | full lower KR map block structure | `expanded_as_part_of_larger_derivation` | K4, B1--B2, P14 | map structure taught by conditional blocks | compressed |
| Eq. (18) | lower conditional CDF | `expanded` | K2--K3, B1 | ratio and integral | adequate |
| Eq. (19) | lower conditional map for \(x_{t-1}\) | `expanded` | B1--B2 | backward sampler | adequate |
| Eq. (20) | upper conditional map for \(x_t\) | `expanded` | K6--K8, F1--F2 | forward proposal | compressed |
| Eq. (21) | upper inverse-map sample | `expanded` | F2 | sampling formula | adequate |
| Eq. (22) | proposal density | `expanded` | F3 | full proposal density | adequate |
| Eq. (23) | forward correction weight | `expanded` | F4--F6 | ratio and normalized weights | compressed |
| Algorithm 3 | particle filter | `expanded` | F1--F7 | proposal, weighting, ESS diagnostic | compressed |
| Eq. (24) | backward inverse-map sample | `expanded` | B2 | smoothing sample step | adequate |
| Eq. (25) | approximate path factorization | `expanded` | B3 | backward density product | adequate |
| Markov identity for smoothing | exact path factorization reason | `expanded` | B4, B7 | conditional-independence explanation | missed |
| Eq. (26) | backward correction weight | `expanded` | B5--B6 | ratio and normalized weights | compressed |
| Algorithm 4 | path estimation/smoothing | `expanded` | B2--B6 | backward recursion and weights | compressed |
| Sec. 3.4 endpoint vs middle marginalization costs | variable ordering reason | `expanded` | B8--B9 | cost and ordering explanation | missed |
| Eq. (30) | preconditioning KR map | `expanded` | P1 | pushforward bridge identity | adequate |
| Eq. (31) | preconditioned residual target | `expanded` | P2 | ratio derivation | adequate |
| Eq. (32) | squared-TT residual | `expanded` | P3 | defensive residual density | adequate |
| Eq. (33) | pullback approximation and normalizer | `expanded` | P4--P5 | density pullback and normalizer invariance | adequate |
| Sec. 5.2 Gaussian bridge | linear preconditioner | `expanded` | P6a--P6c | Cholesky whitening and log determinant | missed |
| Eq. (34) | tempering bridge | `expanded` | P6 | powered factors | adequate |
| Eq. (35) | bridge squared-TT approximation | `expanded` | P7 | bridge density approximation | adequate |
| Nonlinear bridge \(R_t,D,T_t\) composition | reference-to-uniform map | `expanded` | P8--P13 | composition and residual target | missed |
| Sec. 5.4 lower triangular maps | preconditioned marginalization | `expanded` | P14--P17 | Algorithm 5(c.2) retained marginal | compressed |
| Final lower conditional composite map | preconditioned smoothing map | `expanded` | P18 | last-block composite conditional | missed |
| Algorithm 5 | preconditioned replacements | `expanded` | P8--P18 | line-by-line mathematical effect | compressed |
| BayesFilter fixed branch | branch-local derivative extension | `expanded` | C1--C11, FB1--FB5, G1--G8 | normalized approximate filter and same-scalar derivative | P16 scaffold retained and corrected |

## Completeness Decision

`P17_INVENTORY_COMPLETE_FOR_SECTIONS_1_3_5_DRAFT`

The inventory found substantial P16 compression and misses, especially in
notation, pushforward/pullback formulas, TT source summation, proportionality,
map costs, particle/path weight normalization, variable-ordering costs, and
Section 5 preconditioning composition.

