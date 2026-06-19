# Reset memo: high-dimensional monograph rewrite blocker clearance and integration gate

## Date
2026-06-15

## Context
The active governing program remained `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`, with the user asking to fix the active monograph LaTeX blocker and continue the remaining phases unless a blocker was hit. At the start of this pass, the LaTeX toolchain itself was usable in-session, but the integrated monograph build stopped inside `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex` on an undefined standalone-note macro `\chol` carried over from the p47 lane. The execution goal for this pass was to restore forward progress on the actual monograph chapters rather than reopening detached standalone-note work.

## Decision / policy
Future sessions should assume the following unless a stronger contradiction appears in a later build or source audit:

1. The immediate LaTeX blocker was a real source-integration error, not a compiler-permission problem.
2. For the rewritten high-dimensional monograph block, standalone-note notation should be normalized to monograph chapter notation locally before adding new global aliases to `docs/preamble.tex`.
3. The current integrated `ch35`, `ch36`, and `ch37` can be advanced from the monograph side without reopening standalone macro-compatibility work: a targeted scan found no surviving p47/p50-style alias family (`\N`, `\vecop`, `\sgq`, `\chol`, `\ellhat`, `\widehatell`, `\bfone`) in those chapters.
4. The build now passes `docs/main.tex`; the next work should be editorial/source-discipline review against the phase goals rather than emergency blocker repair.

## What changed
- File: `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
  - Replaced the failing `\chol` notation in the one-step predictive-factor example with the chapter’s declared covariance-factor map notation (`C(P)`), so the example now matches the monograph’s square-root-factor language.
  - Rewrote the derivative-lane prose to refer to factor identities `P_t=C_tC_t^\top` / `P_t^-=C_t^-(C_t^-)^\top` on the declared branch rather than the undefined standalone macro `\chol(\cdot)`.
  - Replaced the saved-branch record description `C(P)=\chol(P)` with monograph-consistent lower-triangular covariance-factor wording.
- File: `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
  - Repaired stale cross-chapter references from `eq:bf-hd-gq-loglik` / `eq:bf-hd-gq-score` to the live `ch34` labels `eq:p31-fsgq-loglik` and `eq:p31-score`.

## Bugs / blockers resolved
- Symptom:
  - `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` stopped in `ch34` with `! Undefined control sequence.` at the equation using `\chol(P_1^-)`.
- Root cause:
  - The integrated monograph chapter still contained a p47 standalone macro transplant even though `docs/preamble.tex` does not define `\chol` and the chapter’s own later sections already used the monograph’s explicit factor-branch language.
- Resolution:
  - Normalized the local `\chol` references in `ch34` to the existing monograph factor notation instead of adding a new global preamble alias.
  - Rebuilt the monograph and then repaired the next downstream issue: stale `ch36` references to renamed Gaussian/quadrature labels.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

grep -nE '\\(N|vecop|sgq|chol|ellhat|widehatell|bfone)\b' docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex
grep -nE '\\(N|dd|vecop|sgq|chol|ellhat|widehatell|bfone)\b' /home/chakwong/BayesFilter/docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex
grep -nE '\\(N|dd|vecop|sgq|chol|ellhat|widehatell|bfone)\b' /home/chakwong/BayesFilter/docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex
grep -nE '\\(N|dd|vecop|sgq|chol|ellhat|widehatell|bfone)\b' /home/chakwong/BayesFilter/docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex
```

Observed:
- The first rebuild moved past the prior `\chol` failure and produced `main.pdf`.
- A downstream label drift remained in `ch36`: references to `eq:bf-hd-gq-loglik` and `eq:bf-hd-gq-score` were unresolved because `ch34` now exposes `eq:p31-fsgq-loglik` and `eq:p31-score`.
- After fixing those `ch36` references, a second `latexmk` rebuild completed successfully and wrote `docs/main.pdf` (327 pages).
- The targeted alias scan found no surviving p47/p50-style macro family in `ch35`, `ch36`, or `ch37`.
- No undefined citations remained in the final successful build pass.

## Current policy
- Treat the high-dimensional block as build-stable enough to continue with editorial and source-discipline work.
- Keep normalizing standalone notation locally inside affected chapters instead of broadening `docs/preamble.tex` unless repeated multi-chapter evidence justifies a shared alias.
- Use the successful `docs/main.tex` rebuild as the Phase 5 integration gate for this blocker-clearing pass, not as proof that every chapter is finished editorially.

## Known limitations / cautions
- This pass focused on blocker removal and label repair, not a full line-by-line editorial audit of `ch35` against p50 or of `ch37` against the synthesis subplan.
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex` still contains local compatibility aliases such as `\widehatell` and `\dd`; they are now defined locally and no longer block the build, but future normalization passes may still decide to reduce them further.
- A successful LaTeX build does not by itself establish that the rewritten exposition is mathematically or pedagogically complete; it only clears the current integration gate.

## Suggested next steps
1. Audit `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex` section-by-section against `docs/plans/bayesfilter-highdim-monograph-phase2-ch35-zhaocui-ttkr-rewrite-subplan-2026-06-14.md` and the p50 source note, focusing on opening voice, threaded running example, fixed-branch likelihood construction, and validation framing.
2. Perform the same chapter-role audit for `ch36` and `ch37` against their phase subplans now that the build is stable.
3. If future chapter rewrites rename exported equations again, repair cross-chapter references immediately and rebuild `docs/main.tex` before continuing.
