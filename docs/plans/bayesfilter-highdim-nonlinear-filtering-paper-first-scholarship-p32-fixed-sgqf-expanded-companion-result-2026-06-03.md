# P32 FixedSGQF Expanded Companion Result

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- P32 does not conclude exact nonlinear posterior accuracy.
- P32 does not conclude HMC convergence, production readiness, or superiority over Zhao--Cui.
- P32 does not certify every equation by machine proof.
- P32 does not integrate into `docs/chapters/`; it creates a standalone companion note under `docs/plans`.
- P32 does not claim Claude acceptance because Claude Code review was API-blocked.

## Decision

decision: `P32_EXPANDED_FIXED_SGQF_COMPANION_CREATED_LOCAL_TARGETED_PASS_CLAUDE_API_BLOCKED`

P32 produced a 24-page standalone FixedSGQF companion note and PDF.  It expands P31 rather than replacing it: the LaTeX source grew from 1049 to 1776 lines, and the PDF grew from 15 to 24 pages.

## What Codex Inspected

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- P8/P9 ch34 source and gradient ledgers.
- P31 FixedSGQF note, result, source, gradient, MathDevMCP, and Claude review ledgers.
- Local Jia--Xin--Cheng 2012 PDF via `pdftotext`.
- Local Singh et al. 2018 adaptive sparse-grid PDF via `pdftotext`.
- P17--P30 Zhao--Cui context through prior ledgers and comparison requirements.
- Scholarly literature audit skill and policy.

## How P32 Expands P31

Added:

- approximation hierarchy and coordinate walk;
- moderate-rank/sparse-grid plausibility explanation using low-order interaction structure;
- source-order reconstruction of Jia--Xin--Cheng index sets, Smolyak coefficients, univariate moment matching, cloud dictionary, exactness scope, point-count meaning, nestedness, and UKF relation;
- explicit bridge from Jia--Xin--Cheng Gaussian approximation formulas to the BayesFilter moment equations;
- deterministic level ladder before declaring FixedSGQF design failure;
- one-page story of the derivative before the formal equations;
- input/output/invariant/failure contract;
- default diagnostic constants;
- end-to-end mathematical algorithm with branch exits;
- large-scale validation models A--F and report template.

## Claude Review History

| phase | attempt | result | Codex classification |
|---|---:|---|---|
| plan review | 1 | API error `400 服务繁忙,请稍后再试` | `CLARIFY` |
| plan review | 2 | API error `400 服务繁忙,请稍后再试` | `CLARIFY` |
| execution review | 1 | API error `400 服务繁忙,请稍后再试` | `CLARIFY` |
| execution review | 2 | API error `400 服务繁忙,请稍后再试` | `CLARIFY` |

Claude returned no substantive findings.  Codex therefore cannot claim Claude plan acceptance, Claude execution acceptance, or Claude chemistry-persona satisfaction.

## Codex Audit Classifications Summary

- `CLARIFY`: 4 Claude API-blocked attempts.
- `ACCEPT`: none, because no substantive Claude findings returned.
- `PARTIAL`: none.
- `DISPUTE`: none.

Codex performed an independent skeptical plan audit before execution and a hostile self-review after drafting.

## MathDevMCP Status

mathdevmcp_status: `NARROW_SUPPORT_ONLY_WITH_TOOL_LIMITS`

- `MCP_VERIFIED`: scalar finite-difference arithmetic \(G=1/2\) and cloud-sensitive bracket arithmetic.
- `MCP_TOOL_LIMIT`: parser could not encode broader derivative obligations for \(\log\det\), \(v^\top S^{-1}v\), \(C S^{-1}\), or covariance-update analogues.
- `MCP_UNVERIFIED`: full Cholesky branch identity in matrix form.

No broad machine certification is claimed.

## Files Created

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-source-support-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-gradient-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-validation-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-mathdevmcp-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-claude-review-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-discrepancy-report-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-result-2026-06-03.md`

No `docs/chapters/` or production `bayesfilter/` files were edited.

## PDF Build Status

pdf_status: `BUILT`

The P32 PDF builds successfully with `latexmk`; final PDF length is 24 pages.

## Validation Commands Run

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex`
- `rg -n "Citation .*undefined|Reference .*undefined|undefined citations|There were undefined|Label\\(s\\) may have changed|Rerun|No file|Package natbib Warning|Package amsmath Warning|Missing|LaTeX Error" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.log`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.pdf /tmp/p32_fixed_sgqf.txt`
- `rg -n "Approximation Hierarchy|Sparse-Grid Rule Reconstructed In Source Order|The Story Of The Derivative|End-To-End Mathematical Algorithm|Model A|Model D|Relation To Zhao|same-scalar|Jia|Singh|Zhao" /tmp/p32_fixed_sgqf.txt`
- `rg -n "governance|artifact|ledger|review gate|Claude|Codex|policy|execute|production|public API|student|controlled|DPF|HMC label|exported" /tmp/p32_fixed_sgqf.txt`
- `git diff --check`
- `git status --short docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf* docs/chapters bayesfilter`
- metadata scan for `metadata_date`, `seed_papers`, and `what_is_not_concluded`.

Validation result:

- `git diff --check` passed.
- final LaTeX log scan found no undefined references/citations, missing files, rerun blockers, or amsmath warnings; only the `rerunfilecheck` package banner matched the broad `Rerun` scan.
- PDF text contains the required expanded sections.
- reader-facing process/governance terms were cleaned; remaining "policy" uses are ordinary mathematical branch/preprocessing policy.
- scoped git status shows only new P32 files under `docs/plans/`.

## Remaining Gaps

- Claude plan and execution reviews are API-blocked, so external hostile review is not complete.
- The note is much stronger than P31 but still 24 pages, not a 70-page treatment.
- Matrix derivative identities are project-derived and human-reviewed by Codex, not machine-certified.
- The validation models are mathematical specifications; no implementation or benchmark results are produced in P32.
- The chemistry-chair readability is improved but not independently confirmed by Claude due to API failure.

## Chemistry Persona Status

chemistry_persona_status: `CODEX_SELF_REVIEW_POSITIVE_CLAUDE_UNAVAILABLE`

Codex estimates that the chair can now follow the broad method and why it is plausible: the note explains the approximation hierarchy, coordinate walk, low-order interaction motivation, source-order sparse-grid construction, Gaussian projection limitation, and validation tests.  The hardest remaining teach-back items are the Cholesky derivative and posterior sensitivity propagation.

## Probability Estimate

Estimated probability that P32 passes a skeptical mixed numerical/chemistry panel as a standalone FixedSGQF proposal note:

- `0.72` if judged as a standalone mathematical companion and proposal specification.
- `0.55` if the panel expects near-complete implementation-level proof of every matrix derivative and empirical validation results.

The main discount is not the source reconstruction; it is the missing successful Claude review and the fact that P32 specifies tests rather than running them.
