# P27 Zhao--Cui Large-Scale Validation Result

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- Chopin and Papaspiliopoulos, "An Introduction to Sequential Monte Carlo,"
  2020.
- Gordon, Salmond, and Smith, "Novel Approach to Nonlinear/Non-Gaussian
  Bayesian State Estimation," 1993.

what_is_not_concluded:
- No benchmark was run.
- No empirical success, production readiness, exact nonlinear posterior
  accuracy, or adaptive global differentiability is claimed.
- The P27 note specifies a validation protocol and mathematical test suite.

## Outcome

P27 was created as a successor to P26.  It preserves the P26 note and adds a
large-scale validation section with explicit mathematical models, memory and
performance quantities, accuracy metrics, robustness vetoes, fixed-branch
derivative validation, and benchmark interpretation limits.

## Files Created

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-validation-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-claude-review-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-discrepancy-report-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-result-2026-06-03.md`

## Claude Review

The full-file Claude review stalled.  A bounded excerpt review over the new
validation section returned 10 findings.  Codex classified 9 as `ACCEPT` and 1
as `PARTIAL`; all accepted/partial findings were patched.  No unresolved
Codex--Claude discrepancy remains.

## Validation Commands

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`
- `rg -n "Citation .*undefined|Reference .*undefined|undefined citations|Rerun|No file|Label\\(s\\) may have changed|Font Warning" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.log`
- `git diff --check -- <P27 changed files>`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.pdf - | rg -n "Large-Scale Validation Models|This section specifies|Exact-Reference Linear Gaussian|Long-Horizon Stochastic|Spatial SIR|Predator-Prey|BayesFilter Stress Ladders|Robustness Tests|branch-stable decreasing window|does not report BayesFilter benchmark outcomes" -C 1`
- `for f in docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-*.md; do ...; done`

## Validation Status

- PDF build: passed; 103 pages.
- Undefined references/citations: none detected in final log scan.
- `git diff --check`: passed.
- PDF text check: passed; the new validation section and model subsections are present.
- Metadata fields: present in all P27 markdown artifacts.

## Remaining Caveat

The validation section is intentionally a protocol.  A future empirical P28 or
implementation evidence phase must fill the tables with measured values,
uncertainty summaries, and actual memory/runtime/accuracy results.

