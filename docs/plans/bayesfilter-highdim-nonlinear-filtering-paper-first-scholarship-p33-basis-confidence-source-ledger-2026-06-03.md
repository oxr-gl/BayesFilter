# P33 Basis-Choice Confidence Source Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Oseledets and Tyrtyshnikov, "TT-cross Approximation for Multidimensional Arrays," Linear Algebra and its Applications 2010.
- Trefethen, *Approximation Theory and Approximation Practice*.
- Ghanem and Spanos, *Stochastic Finite Elements: A Spectral Approach*.
- Xiu and Karniadakis, "The Wiener--Askey Polynomial Chaos for Stochastic Differential Equations."
- Daubechies, *Ten Lectures on Wavelets*.
- Mallat, *A Wavelet Tour of Signal Processing*.
- Aharon, Elad, and Bruckstein, "K-SVD."
- Bachmayr, Cohen, and Dahmen, "Parametric PDEs: Sparse or Low-Rank Approximations?"
- Lu, Jin, Pang, Zhang, and Karniadakis, "Learning Nonlinear Operators via DeepONet Based on the Universal Approximation Theorem of Operators."
- Li et al., "Fourier Neural Operator for Parametric Partial Differential Equations."
- Kovachki et al., "Neural Operator: Learning Maps Between Function Spaces with Applications to PDEs."

what_is_not_concluded:
- This ledger does not certify that the P33 basis protocol is empirically optimal.
- This ledger does not prove high-dimensional filtering accuracy.
- This ledger does not claim broad source-complete coverage of approximation theory.
- This ledger does not claim absolute novelty for neural-operator basis learning; it records a scoped MAP-frozen use in this TT filtering contract.

## Source Support Scope

| source | classification | P33 use | forbidden claim |
|---|---|---|---|
| Zhao and Cui 2024 | DIRECT_METHOD | Functional TT, squared-TT filtering, basis families in the Zhao--Cui implementation context. | Does not prove BayesFilter's fixed-basis ladder or fixed-branch derivative. |
| Oseledets 2011 | FOUNDATIONAL | Tensor-train format, ranks, storage, contractions. | Does not choose a best function basis. |
| Oseledets and Tyrtyshnikov 2010 | FOUNDATIONAL | Cross approximation context and adaptive index selection background. | Does not justify differentiability of adaptive TT-cross. |
| Trefethen 2019 | FOUNDATIONAL_BACKGROUND | Smooth bounded-domain approximation by polynomial-type bases; approximation-space framing. | Does not certify any posterior approximation. |
| Ghanem and Spanos 1991 | FOUNDATIONAL_BACKGROUND | Polynomial chaos as a stochastic spectral approximation family. | Does not imply polynomial chaos is optimal for all filtering targets. |
| Xiu and Karniadakis 2002 | FOUNDATIONAL_BACKGROUND | Wiener--Askey/polynomial-chaos matching to reference distributions. | Does not make Hermite the universal default. |
| Daubechies 1992 and Mallat 2009 | FOUNDATIONAL_BACKGROUND | Wavelets/local multiscale bases for localized structure. | Does not require wavelets in P30. |
| Aharon--Elad--Bruckstein 2006 | BACKGROUND_METHOD | Learned dictionaries as a possible pilot-basis route. | Does not support differentiating through adaptive basis retraining. |
| Bachmayr--Cohen--Dahmen 2018 | BACKGROUND_CONTEXT | Sparse versus low-rank approximation framing. | Does not prove a rank bound for the sequential filtering posterior. |
| Lu et al. 2021, Li et al. 2021, Kovachki et al. 2023 | BACKGROUND_METHOD | Neural-operator/operator-learning context for learning parameter-conditioned maps between approximation objects. | Does not prove that the MAP-frozen neural basis is novel, optimal, or accurate for filtering. |

## P33 Claim Support Mapping

| P33 claim or derivation | P30 location | support type | source / evidence | limitation |
|---|---|---|---|---|
| The basis choice is part of a full approximation design including coordinate map, reference measure, basis family, degree, rank, fit/holdout points, weights, ridge, and sweep budget. | `A Complete Basis-Choice Specification In Equations`, \(\eqref{eq:p33-design-tuple}\)--\(\eqref{eq:p33-design-table}\) | project derivation and method specification | Zhao--Cui use functional TT bases and ranks; Oseledets provides TT format background. | This is a BayesFilter specification, not a theorem from Zhao--Cui. |
| Physical densities must be pulled back to basis coordinates and the declared reference measure before fitting. | \(\eqref{eq:p33-pullback-leb}\)--\(\eqref{eq:p33-pullback-nu}\) | project derivation | Change-of-variables algebra in the note. | Does not certify any specific coordinate map is optimal. |
| TT core evaluation and least-squares rows follow from holding all other cores fixed. | `Basis Functions Inside Tensor-Train Cores`, \(\eqref{eq:p33-core-eval}\)--\(\eqref{eq:p33-ls-linear}\) | project derivation grounded in TT representation | Zhao--Cui functional TT setup; Oseledets TT decomposition. | Does not certify adaptive TT-cross pivot choices. |
| The ridge normal equations are the first-order condition of the local weighted least-squares problem. | \(\eqref{eq:p33-ridge-objective}\)--\(\eqref{eq:p33-normal-equation}\) | project derivation; narrow algebra check in MathDevMCP ledger for related solve derivative | Standard least-squares calculus. | Does not guarantee global minimization of the alternating TT objective. |
| Squared-TT mass contractions use one-dimensional basis mass matrices and therefore depend on the basis/measure pair. | `Mass Matrices, Normalizers, And Marginals`, \(\eqref{eq:p33-mass-matrix}\)--\(\eqref{eq:p33-retained-normalized}\) | project derivation grounded in squared-TT construction | Zhao--Cui squared-TT density idea; Oseledets TT contraction background. | Full tensor contraction proof is human-reviewed, not machine-certified in full generality. |
| Quadrature exactness must be stated with the declared basis/measure pair. | \(\eqref{eq:p33-quadrature-mass}\)--\(\eqref{eq:p33-quadrature-aggregate}\) | project derivation and standard quadrature fact | Legendre/Gauss exactness statement used as a concrete example. | Does not claim Gauss--Legendre is universal. |
| "Optimal basis" means best approximation inside a declared space, not a universal basis theorem. | `What Optimal Basis Can And Cannot Mean`, \(\eqref{eq:p33-design-error}\)--\(\eqref{eq:p33-empirical-norms}\) | project derivation; approximation-theory background | Trefethen; Bachmayr--Cohen--Dahmen for approximation-space framing. | Projection monotonicity is not machine-certified by MathDevMCP due to infinite-dimensional/set notation limits. |
| Basis-family choices are matching heuristics tied to support, reference measure, and regularity. | `Basis-Family Taxonomy`, taxonomy table and \(\eqref{eq:p33-orthogonality-triplet}\) | scoped literature background | Trefethen; Ghanem--Spanos; Xiu--Karniadakis; Daubechies; Mallat; Aharon--Elad--Bruckstein. | These sources support candidate-family reasoning, not posterior accuracy for this model. |
| Confidence comes from a deterministic ladder and veto diagnostics, not from choosing one named basis ex ante. | `Deterministic Basis And Rank Ladder`, \(\eqref{eq:p33-ladder}\)--\(\eqref{eq:p33-no-candidate}\) | project method specification | Derived from the panel concern and numerical-method discipline. | Thresholds still require empirical calibration for a given run. |
| Basis insufficiency, rank insufficiency, and coordinate-map/preconditioner failure can be separated by enrichment tests. | `How A Bad Basis Fails`, \(\eqref{eq:p33-bad-basis-traces}\)--\(\eqref{eq:p33-discrimination-ladder}\) | project diagnostic specification | TT rank/basis separation follows from the representation structure. | The tests diagnose failure modes; they do not prove success when all diagnostics pass. |
| Learned bases are optional and must be frozen before fixed-branch differentiation. | `Learned Bases And The Freeze Boundary`, \(\eqref{eq:p33-raw-library}\)--\(\eqref{eq:p33-learned-artifact}\) | scoped method extension | Aharon--Elad--Bruckstein supports learned dictionary background. | Does not support differentiating through adaptive basis retraining. |
| A neural operator can be used as an offline parameter-conditioned basis proposal, evaluated at the MAP and frozen for HMC. | `Relation To Neural-Operator Basis Learning`, \(\eqref{eq:p33-neural-basis-map}\)--\(\eqref{eq:p33-map-cloud-marginal}\) | scoped method extension and project derivation | Lu et al., Li et al., and Kovachki et al. support operator-learning context; project equations define the MAP-frozen TT filtering contract. | Does not claim the neural operator replaces the filter; does not use a data-dependent basis during HMC; does not prove empirical success without MAP-cloud diagnostics. |
| Frozen-basis gradients omit \(\dot\psi\) and \(\dot M\); moving-basis gradients require those additional terms. | `Frozen-Basis And Moving-Basis Gradients`, \(\eqref{eq:p33-frozen-hdot}\)--\(\eqref{eq:p33-moving-square-derivative}\) | project derivation; narrow scalar mass derivative checked in MathDevMCP ledger | Product-rule algebra. | The note's fixed-branch derivative intentionally does not cover moving-basis adaptation. |
