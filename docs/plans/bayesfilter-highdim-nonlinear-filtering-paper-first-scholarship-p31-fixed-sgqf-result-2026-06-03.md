# P31 Fixed-SGQF Standalone Companion Result

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- P31 does not conclude exact nonlinear posterior accuracy.
- P31 does not conclude HMC convergence, production readiness, or superiority over Zhao--Cui.
- P31 does not certify every equation by machine proof.
- P31 does not edit or integrate the thesis chapter; it creates a standalone companion note under `docs/plans`.

## Decision

decision: `P31_STANDALONE_FIXED_SGQF_COMPANION_CREATED_WITH_TARGETED_PASS_AND_POSTPATCH_CLAUDE_API_BLOCKER`

P31 produced a standalone FixedSGQF companion note and PDF.  The note presents FixedSGQF as a fixed deterministic Gaussian-projection approximate likelihood with an analytical same-scalar gradient, and compares it honestly with the Zhao--Cui squared-TT proposal.

## What Codex Inspected

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- P8/P9 ch34 source-reconstruction and fixed-SGQF gradient ledgers/results.
- Local Jia--Xin--Cheng 2012 PDF.
- Local Singh et al. 2018 adaptive sparse-grid PDF.
- P30 Zhao--Cui companion context and prior comparison framing.
- Scholarly audit policy.

## Files Created

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-source-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-gradient-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-claude-review-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-result-2026-06-03.md`

No `docs/chapters/` or production `bayesfilter/` files were edited.

## Note Contents

The standalone note contains:

- a reader-facing statement of what FixedSGQF computes and does not compute;
- a nonlinear scalar counterexample showing the Gaussian-projection limitation;
- exact filtering recursion and Gaussian projection derivation;
- Jia--Xin--Cheng sparse-grid construction in BayesFilter notation;
- a toy two-dimensional fixed-grid duplicate-merge calculation;
- fixed-SGQF value path;
- saved scalar and same-scalar contract;
- analytical gradient recursion through points, moments, innovation scalar, and posterior sensitivity propagation;
- a single boxed value-and-gradient algorithm;
- implementation contract table;
- operational finite-difference protocol;
- scalar and cloud-sensitive finite-difference traces;
- diagnostics for construction, accuracy, memory, performance, signed-weight stability, and branch validity;
- adaptive sparse-grid as offline grid design;
- comparison with Zhao--Cui squared TT.

## Claude Review History

| phase | result | Codex classification/action |
|---|---|---|
| plan review iteration 1 | `REJECT`; six findings | Codex classified all as `ACCEPT` and patched the plan to add hard same-scalar vetoes, truth-telling example, claim-to-source mapping, implementation contract, toy grid validation, and reader-facing outline. |
| execution review iteration 1 | `REJECT`; two blockers, two majors, two minors | Codex classified all as `ACCEPT` and patched the note/ledgers. |
| post-patch review attempts | API error `400 服务繁忙,请稍后再试` in three trusted attempts | Recorded as `API_BLOCKED_NO_SUBSTANTIVE_FINDINGS`; Codex independently audited the patches. |

## Codex Patch Summary After Execution Review

- Same-scalar contract now includes \(y_{1:T}\), observation preprocessing, \(m_0(\theta)\), \(P_0(\theta)\), and initial sensitivities.
- Stabilization is narrowed to symmetrize then veto; no jitter, floor, clipping, pivoting, or eigenvalue repair is differentiated in this note.
- Finite-difference protocol now has a step ladder, same-branch validity rule, relative error metric, and pass criterion.
- Added a nonlinear cloud-sensitive trace using the merged two-dimensional sparse grid and fourth moment.
- Fixed ambiguous \(C_t^-C_t^{-\top}\) notation.
- Softened HMC wording to "candidate fixed target when branch diagnostics stay stable."

## MathDevMCP Status

mathdevmcp_status: `NARROW_SUPPORT_ONLY`

Verified:
- scalar innovation-score algebra;
- scalar Kalman-gain derivative algebra;
- toy finite-difference gradient simplification;
- cloud-sensitive score value \(G=4/9\) at \(\theta=1\).

Not certified:
- full matrix calculus proof;
- source fidelity of every line;
- numerical stability or posterior accuracy.

## Validation Commands

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.tex`
- `rg -n "Citation .*undefined|Reference .*undefined|undefined citations|There were undefined|Label\\(s\\) may have changed|Rerun|No file|Package natbib Warning|Package amsmath Warning" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.log`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-standalone-note-2026-06-03.pdf /tmp/p31_pdf.txt`
- `rg -n "symmetrize-then-veto|initial distribution|preprocessing|cloud-sensitive|branch-invalid|relative error|candidate fixed target|same saved scalar" /tmp/p31_pdf.txt`
- `git diff --check`
- `git status --short docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31* docs/chapters bayesfilter`

Validation result:
- PDF builds successfully: 15 pages.
- Log scan found no undefined references, undefined citations, missing files, amsmath warnings, or rerun blockers.  The only broad scan match was the `rerunfilecheck` package banner.
- Extracted PDF text contains the patched same-scalar, branch, finite-difference, cloud-sensitive, and softened HMC language.
- `git diff --check` passed.
- Scoped git status shows only P31 files under `docs/plans/`; no chapters or production files changed in this lane.

## Remaining Gaps

- The note is a standalone first companion, not yet a 70-page Zhao--Cui-scale expansion.
- Post-patch Claude acceptance is blocked by repeated Claude API service-busy errors.
- A future P32 could expand this note into a longer paper-grade document with more numerical examples and a fuller source-by-source Jia--Xin--Cheng reconstruction.
- Integration into `ch34` should wait until the standalone note is reviewed by the user and, if desired, receives a successful post-patch Claude pass.
