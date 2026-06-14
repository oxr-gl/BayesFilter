# P33 Basis-Choice Confidence Plan

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Oseledets and Tyrtyshnikov, "TT-cross Approximation for Multidimensional Arrays," Linear Algebra and its Applications 2010.
- Trefethen, *Approximation Theory and Approximation Practice*, extended edition.
- Ghanem and Spanos, *Stochastic Finite Elements: A Spectral Approach*.
- Xiu and Karniadakis, "The Wiener--Askey Polynomial Chaos for Stochastic Differential Equations."
- Daubechies, *Ten Lectures on Wavelets*.
- Mallat, *A Wavelet Tour of Signal Processing*.
- Aharon, Elad, and Bruckstein, "K-SVD."
- Bachmayr, Cohen, and Dahmen, "Parametric PDEs: Sparse or Low-Rank Approximations?"

what_is_not_concluded:
- P33 will not prove that any basis family is universally optimal.
- P33 will not prove a global TT rank bound for arbitrary nonlinear filtering posteriors.
- P33 will not certify empirical performance; it will specify mathematical diagnostics and validation criteria.
- P33 will not differentiate the adaptive Zhao--Cui algorithm; it will distinguish fixed-branch gradients from moving-basis/adaptive derivatives.

## Skeptical Plan Audit

status: `PASSED_WITH_GUARDRAILS`

Potential failure modes checked before execution:

- Wrong baseline: comparing basis families only by storage count would not answer the panel.  P33 must compare by approximation, integral, conditioning, and downstream diagnostics.
- Proxy metrics: training residual alone must not become the promotion criterion.  Holdout residual, evidence stability, marginal projection, conditioning, rank saturation, and finite-difference parity must be stated as veto checks.
- Hidden assumptions: the note must define domain map, reference measure, basis family, degree, ranks, fitting points, weights, ridge, and sweep budget together.
- Stale context: P30 already has a basis section; P33 must expand it, not replace it or summarize it.
- Unsupported claims: claims about Legendre, Hermite, wavelets, learned bases, and sparse/low-rank approximation must be scoped as background unless the note proves the claim in project notation.
- Commands and artifacts: the output must be the patched P30 note/PDF plus P33 ledgers; a patch without a PDF build and PDF-text confirmation is not sufficient.

## Objective

Address the panel objection that the Zhao--Cui TT method appears to depend on an unsupported choice of basis functions.  The note must make basis choice a declared, derived, auditable, rejectable part of the numerical method.

## Required P30 Additions

Add multiple substantial sections under the existing basis discussion.  The sections should be mathematical first and explanatory second.  They must avoid governance language in the main note.

### Section A: The Approximation Design Tuple

Define
\[
  \mathfrak D
  =
  (\Psi,\nu,\omega_{1:D},T,\mathcal B_{1:D},p_{1:D},R_{0:D},
   Z_{\rm fit},Z_{\rm hold},W_{\rm fit},W_{\rm hold},\rho,S_{\max})
\]
and explain every component.  Derive how a physical density is pulled to the basis coordinate and reference measure.

### Section B: Basis Functions Inside TT Cores

Derive
\[
  H_k(z_k)=\sum_{\ell=0}^{p_k-1} C_k[:,\ell,:]\psi_{k,\ell}(z_k)
\]
and then derive the full TT value at a point.  Include the vectorization convention and the exact least-squares row
\[
  A_{j,k}[a,\ell,b]=L_{j,k}[a]\psi_{k,\ell}(z_k^{(j)})R_{j,k}[b].
\]
Prove that the core update is a ridge least-squares normal equation.

Explicitly state tensor shapes and index conventions:
- \(C_k\in\mathbb R^{R_{k-1}\times p_k\times R_k}\);
- \(L_{j,k}\in\mathbb R^{1\times R_{k-1}}\);
- \(R_{j,k}\in\mathbb R^{R_k\times1}\);
- \(A_k\in\mathbb R^{N_{\rm fit}\times R_{k-1}p_kR_k}\);
- use one displayed vectorization map and state whether displayed summation indices are 0-based or 1-based.

### Section C: Mass Matrices, Normalization, And Marginalization

Derive one-dimensional mass matrices:
\[
  M_k[\ell,m]=\int \psi_{k,\ell}(z)\psi_{k,m}(z)\,\omega_k(z)\,dz.
\]
Show explicitly how a non-identity mass matrix enters squared-TT contractions.  Prove the contraction recursion and show how evidence and marginals depend on the chosen basis/mass pair.

Also add quadrature/discretization details.  If \(M_k\) or a diagnostic integral is computed by quadrature, define the quadrature rule, exactness assumption for polynomial bases when applicable, quadrature residual, and aliasing check.  The note must state that inaccurate mass/evidence quadrature can make a good basis look bad or a bad basis look good.

### Section D: What "Optimal Basis" Can Mean

Define the ideal projection error for a fixed measure:
\[
  E_{\mathcal H}(h)=\inf_{\widehat h\in\mathcal T_{\mathcal H}}\|h-\widehat h\|_{L^2(\nu)}.
\]
Prove elementary statements that are within scope:
- orthogonal projection is best within a fixed linear space;
- a richer nested space cannot have larger best-approximation error;
- this does not imply a universal basis across targets, measures, coordinates, or ranks.

Define the residual norms used in the actual fitting protocol:
\[
  \|v\|_{W_{\rm fit}}^2=v^\top W_{\rm fit}v,\qquad
  \|v\|_{W_{\rm hold}}^2=v^\top W_{\rm hold}v.
\]
State that these are empirical weighted norms, not identical to the ideal \(L^2(\nu)\) norm unless the sampling/quadrature design supports that approximation.

### Section E: Basis Family Taxonomy With Matching Conditions

Give a mathematical taxonomy:
- Legendre/Chebyshev for bounded smooth coordinates;
- Hermite/polynomial chaos for Gaussian/reference-measure coordinates;
- Fourier for periodic coordinates;
- piecewise polynomial/splines/wavelets for local sharp features;
- learned dictionary/reduced basis for repeated model classes.

Every entry must state:
- support/measure;
- regularity assumption;
- mass matrix behavior;
- expected failure mode.

Prepend a scope statement: these are heuristic matching rules from approximation literature and simple measure/regularity arguments, not theorem-level guarantees for nonlinear filtering posteriors.  Explicitly warn that orthogonality and conditioning depend on the pulled-back measure and coordinate map, not only the named basis family.

### Section F: Deterministic Basis-Degree And Rank Ladder

Define candidate families and ladders:
\[
  \mathcal L =
  \{(\mathcal B^{(q)},p^{(q)},R^{(q)})\}_{q=1}^Q.
\]
State that confidence comes from comparing candidate families/ladders under common diagnostics, not from asserting one family ex ante.
Derive pass/fail criteria using:
- training residual;
- holdout residual;
- residual ratio/overfit diagnostic;
- evidence stability;
- marginal projection checks;
- conditioning;
- coefficient perturbation stability;
- rank saturation;
- finite-difference derivative parity when gradients are claimed.

Add a deterministic selection rule:
- candidate ordering;
- veto precedence;
- tie-breaks;
- whether \(\rho\) is fixed or laddered;
- the normal matrix whose condition number is monitored;
- the exact record saved for the winning \((\mathcal B,p,R,\rho)\).

### Section G: How A Bad Basis Fails

Provide a failure taxonomy:
- high degree but low holdout accuracy;
- good point fit but unstable integrals;
- evidence changes under enrichment;
- marginal inconsistency;
- ill-conditioned normal equations;
- rank saturation caused by unresolved one-coordinate features;
- derivative mismatch caused by unfrozen/moving basis.

Add a discrimination test between basis insufficiency and TT-rank insufficiency:
- enrich basis at fixed ranks;
- increase ranks at fixed basis;
- change preconditioner/coordinate map;
- compare which action reduces holdout residual, evidence drift, and marginal error.

### Section H: Learned Or Trained Bases

Derive a pilot basis-training problem using a raw library:
\[
  \psi_{k,\ell}^{U}(z)=\sum_m U_{k,m\ell}\varphi_{k,m}(z).
\]
State the pilot objective, orthonormalization/Gram step, and how the learned basis is frozen before fixed-branch filtering.  Explain why training the basis as \(\beta\) changes changes the scalar and requires extra derivative terms.

Define the learned-basis freeze boundary: basis learning stops after pilot fitting and orthonormalization; the frozen artifact contains raw library, learned coefficient matrices, mass matrices, domain/reference measure, training data identifier, seed, and acceptance diagnostics.  All downstream derivatives condition on that artifact.

### Section I: Frozen-Basis Versus Moving-Basis Gradients

Derive
\[
  \dot H_k =
  \sum_\ell \dot C_k[:,\ell,:]\psi_{k,\ell}
\]
for a frozen basis and
\[
  \dot H_k =
  \sum_\ell \dot C_k[:,\ell,:]\psi_{k,\ell}
  +\sum_\ell C_k[:,\ell,:]\dot\psi_{k,\ell}
\]
for a moving basis.  Propagate the moving-basis term into the least-squares row, mass matrix, and normalizer.  State clearly that P30's fixed-branch derivative uses the frozen-basis scalar.

### Section J: Eleven Basis-Choice Questions And Where Each Is Answered

Add a reader-facing checklist mapping each of the 11 issues to the new sections and diagnostics:

1. Why basis choice matters mathematically.
2. Full approximation design tuple.
3. Basis inside TT core evaluation and least-squares rows.
4. Mass matrices, normalization, marginalization, and squared-TT contractions.
5. Meaning and limits of optimal basis.
6. Basis-family taxonomy and matching conditions.
7. Deterministic basis-degree/rank ladder.
8. Residual, evidence, marginal, conditioning, stability, and derivative diagnostics.
9. How a bad basis fails and is rejected.
10. Learned/trained bases and their limits.
11. Frozen-basis versus moving-basis gradients.

For each item, state: question, where answered, decisive equations, and pass/fail diagnostic.

### Section K: Why This Is Not An Arbitrary Basis Gamble

Add a short concluding subsection in the P30 note answering why the method is not an arbitrary basis gamble.  The answer must state that basis choice is a modeling/approximation assumption, declared before fitting, compared against alternatives, audited by diagnostics, frozen before fixed-branch differentiation, and rejected when diagnostics fail.

## MathDevMCP Scope

Use MathDevMCP only for narrow identities:

- orthonormal mass identity for simple basis examples where feasible;
- normal-equation derivative:
  \[
  N g=d \Rightarrow N\dot g=\dot d-\dot N g;
  \]
- square contraction derivative:
  \[
  \frac{d}{d\beta}(C^\top M C)=\dot C^\top M C+C^\top M\dot C+C^\top \dot M C;
  \]
- normalizer quotient/log derivative:
  \[
  \frac{d}{d\beta}\log Z=\dot Z/Z;
  \]
- projection error monotonicity for nested spaces if feasible.

Record `MCP_VERIFIED`, `MCP_UNVERIFIED`, `MCP_INCONCLUSIVE`, or `MCP_TOOL_LIMIT`.

## Claude Plan Review

Run Claude plan review before execution.  Max 5 rounds.  Claude must review as:

1. hostile numerical analyst;
2. implementation engineer;
3. skeptical panel chair without tensor-train background.

Claude must answer:

- Does this plan address all 11 basis-choice issues?
- Would the resulting note be self-contained and confidence-building if executed?
- Are any required mathematical derivations missing?
- Are any claims over-scoped or under-supported?
- What exact changes are required before execution?

Codex must classify every finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`.

## Execution Review

After patching P30, run Claude execution review with the same personas, max 5 rounds.  Claude must inspect the actual patched file and answer:

- Is the basis-choice defense now self-contained?
- Are all mathematical claims either proved or properly scoped/cited?
- Would the panel still see basis choice as an unsupported weak point?
- What exact additions are still required?

Codex must classify every finding and patch accepted/partial findings.

## Validation

Run:

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- log scan for undefined references/citations, missing files, and rerun blockers;
- `pdftotext` confirmation for all 11 issues;
- `git diff --check`;
- scoped `git status`.

## Acceptance Criteria

P33 passes only if:

- P30 contains multiple substantial basis-confidence sections;
- the note derives core evaluation, least-squares rows, mass contractions, diagnostics, learned-basis formulation, and frozen-versus-moving-basis derivative terms;
- the note states no universal basis optimum is claimed;
- literature claims are cited with `\cite` and scoped;
- Claude execution review has no unresolved blocker or major finding accepted by Codex;
- PDF builds cleanly and extracted PDF text contains the expanded sections;
- only allowed files changed.

Allowed changed files for P33:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p33-*`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- compiled P30 PDF/log/auxiliary artifacts beside the note
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-source-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-result-2026-06-03.md`
- `docs/references.bib` only if necessary citations are missing.

PDF-text validation anchors must include:
- `The Approximation Design Tuple`
- `Basis Functions Inside Tensor-Train Cores`
- `Mass Matrices, Normalizers, And Marginals`
- `What Optimal Basis Can And Cannot Mean`
- `Basis-Family Taxonomy`
- `Deterministic Basis And Rank Ladder`
- `How A Bad Basis Fails`
- `Learned Bases And The Freeze Boundary`
- `Frozen-Basis And Moving-Basis Gradients`
- `Eleven Basis-Choice Questions`
- `Why The Basis Choice Is A Controlled Approximation`

## Plan Review Iteration 3 Tightening

Claude's third plan review found the plan substantively complete but required
six coherence controls before execution.  P33 therefore also requires:

1. Reconcile the earlier P30 basis-defense subsection with the P33 audited
   design tuple, so \(\mathcal H\) and \(\mathfrak D\) do not coexist as two
   competing frameworks.
2. State the exact scalar fitted in the local regression: the row equations fit
   samples of the pulled-back square-root target under the declared measure.
3. Give a concrete quadrature exactness example, including the Legendre
   degree/mass threshold and an aliasing criterion.
4. State deterministic fallback behavior when no candidate passes, and clarify
   that finite-difference derivative parity is a veto when gradients are
   reported or used.
5. Mark learned bases as optional/non-default unless a concrete accepted pilot
   basis exists.
6. Add notation harmonization and off-by-one vectorization range checks.
