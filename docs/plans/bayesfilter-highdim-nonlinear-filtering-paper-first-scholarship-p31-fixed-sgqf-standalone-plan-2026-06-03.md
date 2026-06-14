# P31 Fixed-SGQF Standalone Proposal Plan

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This plan does not conclude that fixed SGQF approximates the exact nonlinear posterior.
- This plan does not conclude HMC convergence or production readiness.
- This plan does not edit `docs/chapters/`, production `bayesfilter/`, DPF, student-baseline, controlled-DPF, or public APIs.
- This plan does not claim that live adaptive sparse-grid selection is globally differentiable.

## Goal

Create a standalone LaTeX companion note for the fixed sparse-grid quadrature filter (FixedSGQF) and its analytical gradient, at the same explanatory standard as the Zhao--Cui companion note.  The note should later be integrable into the thesis, but P31 itself is a separate document under `docs/plans`.

## Skeptical Pre-Execution Audit

Potential failure modes checked before execution:

- treating Gaussian projection as exact posterior inference;
- treating sparse-grid polynomial exactness as nonlinear posterior accuracy;
- treating adaptive grid changes, Cholesky pivots, floors, or clipping as globally smooth;
- hiding the scalar differentiated by the analytical gradient;
- writing a software-governance artifact rather than a readable mathematical note;
- summarizing Jia--Xin--Cheng rather than reconstructing the SGQF construction;
- producing a note that cannot guide implementation of a value-and-gradient pass.

Audit decision:
- Proceed, with the controls below.  The note must say that FixedSGQF is a fixed deterministic approximate likelihood target, while Zhao--Cui squared TT is the richer non-Gaussian density approximation proposal.

## Evidence Contract

Question:
- Can a standalone note make FixedSGQF and its analytical gradient sufficiently clear for a panel reader and for later implementation work?

Primary pass criterion:
- The note reconstructs the Jia--Xin--Cheng SGQF mechanism, defines a fixed BayesFilter scalar, derives the same-scalar analytical gradient, and passes focused Claude review.

Veto diagnostics:
- any claim that FixedSGQF is exact nonlinear filtering;
- any missing definition of the fixed cloud, weights, duplicate merging, covariance factor branch, stabilization rule, or scalar;
- a gradient formula that differentiates a different scalar from the value path;
- missing finite-difference parity against the exact saved fixed scalar;
- value and gradient paths that use different clouds, duplicate-merge tolerances, factor branches, floors, clipping rules, or stabilization decisions;
- unsupported claims attributed to Jia--Xin--Cheng or Singh et al.;
- Claude `BLOCKER` or accepted `MAJOR` finding left unpatched.

Explanatory diagnostics:
- MathDevMCP checks for log-likelihood derivative algebra, covariance derivative symmetry, Kalman update derivative, and Cholesky sensitivity algebra;
- PDF build and log validation;
- PDF text extraction checks for the standalone FixedSGQF, gradient, diagnostics, validation, and comparison sections.

What will not be concluded even if the run passes:
- exact posterior accuracy;
- superiority over Zhao--Cui or particle methods;
- production performance;
- broad machine certification of every equation.

Artifact:
- P31 plan, note, PDF, source-support ledger, gradient ledger, MathDevMCP ledger, Claude review ledger, and result file under `docs/plans`.

## Planned Files

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-source-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-gradient-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-claude-review-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.tex`
- compiled PDF beside the note
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-result-2026-06-03.md`

## Standalone Note Requirements

The note must:

- use `\cite`/`\citet`/`\citep` rather than informal source names;
- avoid governance/process language in the reader-facing note;
- define the nonlinear state-space model, Gaussian projection, sparse-grid rule, fixed cloud, fixed scalar, and derivative branch before using them;
- open with a reader-facing "what this note computes and does not compute" section;
- include an early nonlinear scalar counterexample showing that accurate quadrature moments and a Gaussian projection can still miss a non-Gaussian posterior;
- reconstruct Jia--Xin--Cheng SGQF in source order: state-space model, Bayesian prediction/update, Gaussian approximation filter, Gauss--Hermite rule, sparse-grid rule, Algorithm 1 point/weight generation, exactness and point-count statements, and UKF relation;
- explicitly separate source-supported material from BayesFilter extensions;
- include a claim-to-source map tying every SGQF construction block to exact Jia--Xin--Cheng equations/theorems/Algorithm 1 or tagging it as a BayesFilter extension;
- derive the fixed SGQF value path and gradient path side by side;
- state every stored object needed for implementation;
- include an implementation-contract table listing stored object, definition, shape, time of computation, and whether it is reused in value, gradient, or both;
- include a toy fixed-grid construction check showing duplicate-node merging, signed-weight accumulation, weight totals, and branch/stabilization choices;
- require finite-difference same-scalar parity for the saved cloud and saved branch choices;
- give failure diagnostics and finite-difference checks;
- compare FixedSGQF and Zhao--Cui as complementary proposals, without overselling either.

## Reader-Facing Note Outline

1. What FixedSGQF Computes, And What It Cannot Compute.
2. Exact Filtering Recursion And Gaussian Projection.
3. One-Dimensional Gaussian Quadrature And Tensor Products.
4. Jia--Xin--Cheng Sparse-Grid Construction, Reconstructed Equation By Equation.
5. Turning The Sparse-Grid Formula Into A Fixed Cloud.
6. FixedSGQF Filtering Value Path.
7. The Saved Scalar And Same-Scalar Contract.
8. Analytical Gradient Of The Fixed Scalar.
9. Implementation Contract And Stored Objects.
10. Toy Fixed-Grid Construction Check.
11. Finite-Difference, Accuracy, Memory, And Performance Tests.
12. Relation To Adaptive Sparse Grids.
13. FixedSGQF And Zhao--Cui As Complementary High-Dimensional Proposals.

## Claude Review Protocol

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p31-fixed-sgqf-plan-review-iter1 \
  --model sonnet --effort high \
  "<focused P31 plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p31-fixed-sgqf-exec-review-iter1 \
  --model sonnet --effort high \
  "<focused P31 execution review prompt>"
```

Codex must classify every Claude finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`, patch accepted findings, and record the classifications in the review ledger.
