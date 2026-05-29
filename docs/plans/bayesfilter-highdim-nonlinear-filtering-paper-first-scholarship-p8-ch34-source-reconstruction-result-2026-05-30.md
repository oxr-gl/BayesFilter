# P8 Ch34 Source-Reconstruction Result

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: P8 plan, rewritten `ch34`, P8 source/gradient/anchor/MCP/Claude
ledgers, Julier--Uhlmann 1997, Arasaratnam--Haykin 2009, Jia--Xin--Cheng 2012,
Jia--Xin--Cheng 2013, Singh et al. 2018, `ch18_svd_sigma_point.tex`, and the
scholarly literature audit policy.

what_is_not_concluded: This result does not conclude posterior accuracy, HMC
convergence, production readiness, NAWM readiness, GPU/XLA readiness, default
readiness, exhaustive cubature/sparse-grid literature coverage, or
machine-certified proof validity.

## Current Decision

`P8_CH34_SOURCE_RECONSTRUCTION_COMPLETE_WITH_LIMITS`.

## Execution Summary

`ch34` was rewritten as a source-by-source reconstruction chapter with the
requested structure:

1. What This Chapter Computes
2. Gaussian Moment Projection
3. EKF and Second-Order Taylor Filters
4. Julier-Uhlmann Unscented Transform / UKF
5. Arasaratnam-Haykin Cubature Kalman Filter
6. Jia-Xin-Cheng High-Degree CKF
7. Tensor-Product Gauss-Hermite Filtering
8. Jia-Xin-Cheng Sparse-Grid Quadrature Filter
9. Adaptive Sparse-Grid Gauss-Hermite Filter
10. Approximate Likelihood and Analytical Gradient
11. Limitations of These Methods

The old audit-style "Methodological Boundary And Sources" section was removed.
Limitations now appear as human-facing mathematical reasons for failure.

## Source Reconstruction

- Julier--Uhlmann 1997: UT sigma points and transformed mean/covariance
  reconstructed from Eq. 12--14.
- Arasaratnam--Haykin 2009: CKF third-degree spherical--radial point rule,
  update role, and cost caveat reconstructed from the local full text.
- Jia--Xin--Cheng 2013: high-degree CKF degree definition, fifth-degree rule,
  point-count growth, and negative-weight caveat reconstructed source-locally.
- Jia--Xin--Cheng 2012: tensor-product GHQ and SGQF construction reconstructed
  from source-local equations/theorems/algorithm.
- Singh et al. 2018: ASGHF admissible-index/error-indicator/tolerance mechanics
  reconstructed with preprint scope caveat.

## Gradient Summary

The chapter derives the approximate Gaussian innovation scalar
\[
  \widehat\ell_t
  =
  -\frac12\{\log\det S_t+v_t^\top S_t^{-1}v_t+n_y\log(2\pi)\},
  \qquad S_tw_t=v_t,
\]
and the score
\[
  \partial_i\widehat\ell_t
  =
  -\frac12[
    \tr(S_t^{-1}\dot S_t^{(i)})
    +2\dot v_t^{(i)\top}w_t
    -w_t^\top\dot S_t^{(i)}w_t].
  \]
It also derives fixed-rule \(\dot\chi,\dot z,\dot{\bar z},\dot S,\dot v\).
This is the derivative of the declared approximate scalar only.

## PDF And Validation Result

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex`
  completed and produced `docs/main.pdf`.
- `git diff --check` passed.
- `docs/main.log` contains no undefined citation/reference/rerun blockers under
  the targeted scan.  The only `Rerun` occurrence found by the broad scan was
  the loaded `rerunfilecheck` package banner.
- `pdftotext docs/main.pdf -` contains the new P8 chapter sections:
  "What This Chapter Computes", "Gaussian Moment Projection",
  "Extended Kalman Filter", "Unscented Transform", "Cubature Kalman Filter",
  "High-Degree Cubature", "Tensor-Product Gauss-Hermite",
  "Sparse-Grid Quadrature", "Adaptive Sparse-Grid",
  "Approximate Likelihood and Analytical Gradient", and
  "Limitations of These Methods".
- `.local_sources/` and `.localsource/` remain untracked and unstaged.
- No files were staged.  The P8 intentional write set is `ch34`, `docs/main.pdf`,
  and P8 ch34 plan/result/ledger files.  The broader worktree still contains
  unrelated dirty files from prior lanes, which were not edited for this P8
  pass.

## Claude Execution Review Iteration 1

Claude returned `REJECT`.  Codex agreed with the actionable issues and repaired
them:

- headings now spell out acronyms before abbreviations;
- method sections now include explicit exact-versus-approximate and
  method-local limitation paragraphs;
- the gradient contract now states that fixed weights/offsets are required
  unless derivative terms for the rule are included;
- the HMC table is tied directly to \(\widehat\ell_t\);
- the stale boundary label was removed;
- non-policy support-class names were normalized in the source-anchor ledger.

## Claude Execution Review Iteration 2

Claude returned `REJECT`.  Codex agreed that the remaining issues were
artifact-consistency and same-scalar wording repairs, not substantive chapter
reconstruction blockers.  Repairs applied:

- the source-reconstruction ledger now uses `PROJECT_DERIVATION` for the `ch18`
  derivative-pattern row instead of an extra non-policy class;
- the HMC table now names the declared scalar \(\widehat\ell_t\) in the EKF and
  iterated-EKF row labels/reasons;
- this result note records the iteration-2 outcome instead of stale pending
  text.

## Claude Execution Review Iteration 3

Claude returned `REJECT`.  Codex agreed that the only blocker was stale
current-decision text in this result note: it still said iteration 3 was pending
after iteration 3 had run.  Repair applied:

- the current-decision field now records
  `ITER3_REJECTED_ARTIFACT_CONSISTENCY_REPAIRED_PENDING_ITER4_AND_PDF_VALIDATION`;
- pending work now names iteration 4, not iteration 3.

## Claude Execution Review Iteration 4

Claude returned `ACCEPT`.  Residual limits from Claude:

- PDF build/citation rendering validation was not part of Claude's review;
- broad mathematical certification was not claimed;
- remaining source-history limits are recorded in the omission-risk register.

Codex subsequently performed PDF and validation checks listed above.  The
remaining limits are scholarly/layout limits, not P8 execution blockers.
