# P18 Zhao--Cui True Annotation Inventory Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui code audit and paper-code crosswalk ledgers.

what_is_not_concluded:
- No claim that Sections 4 and 6 are fully annotated.
- No claim that adaptive TT-cross is globally differentiable.
- No production BayesFilter implementation claim.

## Inventory Rule

Every material source unit in Zhao--Cui Sections 1--3 and 5 must have an
explicit source-unit marker in the P18 note.  Material displayed formulas and
algorithmic math lines are `expanded` or `expanded_as_part_of_larger_derivation`.

## Source-Unit Inventory

| Source unit | Type | Source anchor | P18 note marker | Disposition | Implementation meaning |
|---|---|---|---|---|---|
| S1-overview | paragraph/definition | Section 1 opening problem description | `Source unit S1-overview` | `expanded` | Builds the first three-block target evaluator. |
| S1-Eq1--Eq2 | numbered equations | Eqs. (1)--(2) | `Source units S1-Eq1--Eq2` | `expanded` | Transition and observation density evaluators. |
| S1-Eq3 | numbered equation | Eq. (3) | `Source unit S1-Eq3`; P18 Eq. BF-3/BF-3a | `expanded` | Log joint-density sum. |
| S1-Eq4 | numbered equation | Eq. (4) | `Source unit S1-Eq4`; P18 Eq. BF-4 | `expanded` | Posterior/evidence scalar. |
| S1-Eq5--Eq8 | numbered equations | Eqs. (5)--(8) | `Source units S1-Eq5--Eq8`; P18 Eqs. BF-5--BF-8 | `expanded` | Marginal outputs: filter, parameter, path, smoothing. |
| S1 notation | definitions/displayed formulas | Section 1.4 notation, Hellinger, pushforward, pullback | Reader notation; P18 Eqs. N1--N5 | `expanded` | Coordinate groups and transform-density identities. |
| S2.1-Eq9--Eq11 | numbered equations/proof steps | Eqs. (9)--(11) | `Source units S2.1-Eq9--Eq11`; P18 Eqs. BF-9--BF-11 | `expanded` | Sequential posterior and retained filter recursion. |
| S2.2-TT-display | unnumbered displayed formulas | Functional TT definition and rank sums | `Source units S2.2-TT-display and basis expansion`; P18 TT-1--TT-3a | `expanded` | TT core arrays and evaluator. |
| S2.2-basis-family | unnumbered display/cost | Basis expansion, basis choices, complexity | `Source unit S2.2-basis-family`; P18 TT-6--TT-11 | `expanded` | Basis evaluation and rank/cost diagnostics. |
| S2.2-core-integration | unnumbered displayed formula | TT core integration | `Source unit S2.2-core-integration`; P18 TT-4--TT-5 | `expanded` | Endpoint marginalization by core contraction. |
| S2.3-Algorithm1(a) | algorithm math line/numbered equation | Algorithm 1(a), Eq. (12) | `Source unit S2.3-Algorithm1(a)`; P18 A1-1/A1-0 | `expanded` | Pointwise target evaluator. |
| S2.3-Algorithm1(b) | algorithm math line/displayed TT | Algorithm 1(b) | `Source unit S2.3-Algorithm1(b)`; P18 A1-2--A1-2d | `expanded` | TT fitting contract. |
| S2.3-Algorithm1(c) | algorithm math line/displayed formulas | Algorithm 1(c) | `Source unit S2.3-Algorithm1(c)`; P18 A1-3--A1-7 | `expanded` | Retained filter and normalizer. |
| S3.1-nonnegativity | paragraph/math claim | Section 3 nonnegativity motivation | `Source unit S3.1-nonnegativity-barrier` | `expanded` | Vetoes unsigned density approximations. |
| S3.1-Eq13-Lemma1 | numbered equation/theorem statement | Eq. (13), Lemma 1 | `Source units S3.1-Eq13 and Lemma 1`; P18 S1--S6 | `expanded` | Squared-TT density, defensive mass, Hellinger role. |
| S3.1-Proposition2 | proposition/numbered equation | Proposition 2, Eq. (14) | `Source unit S3.1-Proposition2`; P18 M1--M9 | `expanded` | Mass matrices and squared-TT marginalization. |
| S3.1-KR-ratios | displayed formulas/remark | Conditional densities, lower/upper KR, costs | `Source units S3.1-KR-ratios and Remark 3`; P18 K1--K11 | `expanded` | Conditional CDF maps and inverse samplers. |
| S3.2-Algorithm2 | algorithm/math lines | Algorithm 2, Eqs. (15)--(16) | `Source units S3.2-Algorithm2(a)--(c), Eq15--Eq16`; P18 A2-1--A2-5 | `expanded` | Nonnegative sequential filter. |
| S3.3-Algorithm3 | numbered equations/algorithm | Eqs. (20)--(23), Algorithm 3 | `Source units S3.3-Eq20--Eq23 and Algorithm3`; P18 F1--F7 | `expanded` | Forward proposal and correction weights. |
| S3.4-Algorithm4 | numbered equations/algorithm/figure claim | Eqs. (24)--(26), Figure 1, Algorithm 4 | `Source units S3.4-Eq24--Eq26, Figure 1, and Algorithm4`; P18 B1--B9 | `expanded` | Backward smoothing/path sampler and weights. |
| S5.1-general | numbered equations | Eqs. (30)--(33) | `Source units S5.1-Eq30--Eq33`; P18 P1--P5 | `expanded` | Pushforward residual and pullback density. |
| S5.2-Gaussian | paragraph/displayed formulas | Gaussian bridge and linear preconditioning | `Source unit S5.2-Gaussian-bridge`; P18 P6a--P6c | `expanded` | Whitening map and log determinant. |
| S5.3-tempering | numbered equations | Eqs. (34)--(35) | `Source unit S5.3-Eq34--Eq35`; P18 P6--P7 | `expanded` | Tempered bridge and bridge TT. |
| S5.3-density-chain | algorithm support formulas | Preconditioned density chain after Eq. (35) | `Source unit S5.3-density-chain`; P18 P7a--P7k | `expanded` | Five-density chain and normalizer checks. |
| S5.4-Algorithm5(b.1) | algorithm line/displayed formula | Algorithm 5(b.1), bridge approximation | `Source unit S5.4-Algorithm5(b.1)`; P18 P7l | `expanded` | Bridge fit evaluator, bridge TT, bridge mass contractions. |
| S5.4-Algorithm5(b.2) | algorithm line/displayed formulas | Algorithm 5(b.2), bridge KR map and bridge marginal | `Source unit S5.4-Algorithm5(b.2)`; P18 P8--P11c | `expanded` | Bridge lower map, inverse map, bridge marginal evaluator. |
| S5.4-Algorithm5(b.3) | algorithm line/displayed formulas | Algorithm 5(b.3), residual target and residual fit | `Source unit S5.4-Algorithm5(b.3)`; P18 P12--P13a | `expanded` | Residual target evaluator and residual squared-TT fit. |
| S5.4-Algorithm5(c.1) | algorithm line/displayed formulas | Algorithm 5(c.1), residual marginalization | `Source unit S5.4-Algorithm5(c.1)`; P18 P14--P15 | `expanded` | Residual marginal evaluator and conditional residual map. |
| S5.4-Algorithm5(c.2) | algorithm line/displayed formulas | Algorithm 5(c.2), retained physical-coordinate filter and smoothing map | `Source unit S5.4-Algorithm5(c.2)`; P18 P16--P18 | `expanded` | Retained physical filter evaluator and composite smoothing map. |

Decision: `P18_INVENTORY_COMPLETE_FOR_EXECUTION_DRAFT`.
