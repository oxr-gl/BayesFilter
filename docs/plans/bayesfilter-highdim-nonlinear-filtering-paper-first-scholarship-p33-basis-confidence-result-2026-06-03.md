# P33 Basis-Choice Confidence Result

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

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
- P33 does not prove a universal optimal-basis theorem.
- P33 does not certify empirical accuracy.
- P33 does not differentiate the adaptive Zhao--Cui algorithm.
- P33 does not claim absolute novelty for neural-operator basis learning.

## Status

status: `P33_BASIS_CONFIDENCE_ACCEPTED_AFTER_EXECUTION_REVIEW_ITERATION_3`

P33 expands the P30 Zhao--Cui companion note with a basis-choice defense aimed
at the panel objection that tensor-train function approximation depends too
heavily on an unexplained basis.  The patch adds a mathematical specification
for basis selection rather than a prose reassurance.

Post-acceptance extension: after the accepted P33 package, the note was further
expanded to answer the reviewer question about whether basis selection is a
neural-operator-style nonlinear basis problem.  The added section states that
the analogy is correct, but that the HMC-compatible proposal is to train a
parameter-conditioned basis map offline, evaluate it at the approximate MAP,
and freeze the resulting basis for posterior exploration.

## What Changed In P30

The target document now contains:

- `Basis Families, Selection, And Diagnostic Equations`, a readable preview
  explaining why basis degree, TT rank, coordinate map, reference measure, and
  diagnostics are separate choices.
- `A Complete Basis-Choice Specification In Equations`, with the approximation
  design tuple \(\mathfrak D\), pullback-to-reference-measure equations, exact
  squared-TT regression target, core evaluation, least-squares row, vectorized
  ridge normal equation, mass contractions, normalizer and marginal formulas,
  quadrature residuals, projection-scope proof, basis-family taxonomy,
  deterministic basis/rank ladder, bad-basis failure taxonomy, learned-basis
  freeze boundary, and frozen-versus-moving-basis derivative equations.
- A reader-facing `Eleven Basis-Choice Questions` table with separate decisive
  equation anchors and diagnostics.
- `Relation To Neural-Operator Basis Learning`, which distinguishes fixed
  features from learned bases, first explains functions versus operators for a
  chair-facing reader, defines a parameter-conditioned basis map, gives the
  MAP-frozen HMC scalar and gradient, writes a finite-dimensional
  raw-library/mixing-matrix parameterization, and states posterior-cloud
  validation checks before using the learned basis.
- A closing subsection, `Why The Basis Choice Is A Controlled Approximation`,
  that states the basis is an approximation assumption, compared and rejected
  by diagnostics, not asserted as universally optimal.

## Claude Review History

- Plan review iteration 1 stalled and was terminated; it was not counted as
  convergence.
- Plan review iteration 2 returned blocker/major findings.  Codex classified
  all material findings as `ACCEPT` except one `PARTIAL` about allowed files,
  then patched the plan.
- Plan review iteration 3 conditionally approved with coherence blockers.
  Codex classified all findings as `ACCEPT` and patched the plan/note.
- Execution review iteration 1 returned blockers on this result ledger and
  the source ledger, plus wording/coherence findings in the main note.  Codex
  classified all findings as `ACCEPT` and patched the P30 note, P33 plan
  anchor, source ledger, and this result ledger.
- Execution review iteration 2 returned `REJECT` only because this result
  ledger and the Claude review ledger still contained stale pending status
  text.  Claude explicitly stated this was a package-level reject, not a
  math-content reject, and that the substantive basis section was strong
  enough.  Codex classified both findings as `ACCEPT` and patched the stale
  ledger sections.
- Execution review iteration 3 returned `ACCEPT`, confirming the iteration-2
  package-state findings were closed and that the result ledger did not
  overclaim final acceptance before the review.

## Codex Audit Classification Summary

- `ACCEPT`: all plan-review iteration-2 material findings, all plan-review
  iteration-3 findings, all execution-review iteration-1 findings, and both
  execution-review iteration-2 stale-ledger findings.  Execution-review
  iteration 3 had no patch-requiring findings beyond updating this final
  status after acceptance.
- `PARTIAL`: one plan-review iteration-2 allowed-file finding; allowed writes
  existed, but Codex strengthened validation and PDF-text anchor requirements.
- `DISPUTE`: none.
- `CLARIFY`: none.

## MathDevMCP Status

Recorded in
`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-basis-confidence-mathdevmcp-ledger-2026-06-03.md`.

- \(\frac{d}{d\beta}\log Z=\dot Z/Z\): `MCP_VERIFIED` after scalarization.
- Scalar square-mass derivative: `MCP_VERIFIED` for scalar constant-mass case.
- Scalar quotient/linear-solve derivative form: `MCP_VERIFIED`.
- Functional notation checks: `MCP_TOOL_LIMIT`.
- Projection monotonicity for nested spaces: `MCP_UNVERIFIED`.

## Validation Status

completed:

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
  succeeded after disabling microtype font expansion; after the
  neural-operator extension, the built PDF has 126 pages.
- LaTeX log scan with `rg -n "undefined|Undefined|Citation.*undefined|Rerun|may have changed|missing file|No file|Fatal|Emergency stop|LaTeX Error|Package natbib Warning" ...log`
  found no undefined references, undefined citations, missing files, fatal
  errors, or rerun blockers after the final pass.  The only match was the
  package name `rerunfilecheck`.
- `pdftotext` confirmed all required anchors:
  `A Complete Basis-Choice Specification In Equations`,
  `The Approximation Design Tuple`,
  `Basis Functions Inside Tensor-Train Cores`,
  `Mass Matrices, Normalizers, And Marginals`,
  `What Optimal Basis Can And Cannot Mean`,
  `Basis-Family Taxonomy`,
  `Deterministic Basis And Rank Ladder`,
  `How A Bad Basis Fails`,
  `Learned Bases And The Freeze Boundary`,
  `Frozen-Basis And Moving-Basis Gradients`,
  `Relation To Neural-Operator Basis Learning`,
  `Eleven Basis-Choice Questions`, and
  `Why The Basis Choice Is A Controlled Approximation`.
- Scoped `git diff --check` over the P30 note and P33 ledgers passed.
- Scoped `git status --short` showed only the allowed P30 note/PDF and P33
  plan/source/result/review/MathDevMCP ledgers in this P33 slice.  The broader
  repository remains dirty with unrelated files, which were not touched.

## Remaining Limitations

- P33 does not prove a universal optimal-basis theorem.
- P33 does not provide empirical accuracy evidence; it specifies diagnostics
  and acceptance criteria that must be run for each actual filtering problem.
- The neural-operator section is a methodological extension and does not claim
  that a trained basis map has already been learned or validated.
- MathDevMCP checked only narrow algebraic identities.  Projection monotonicity
  and the full tensor contraction proof remain human/project derivations.
- Claude execution review iteration 2 was a package-level `REJECT` before this
  final stale-ledger patch, but the reviewer explicitly stated the substantive
  math note was strong enough and identified no math-content blocker.
