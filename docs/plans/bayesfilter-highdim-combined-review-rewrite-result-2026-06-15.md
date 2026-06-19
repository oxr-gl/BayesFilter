# Reset memo: combined internal-plus-Codex rewrite pass for the high-dimensional block

## Date
2026-06-15

## Context
After the monograph rewrite reached a green build, a careful internal audit of the high-dimensional block and an independent Codex review were run against `docs/main.tex` and `docs/chapters/ch33`--`ch37`. Both reviews agreed on the highest-risk issues: a structural `\appendix` bug in `ch34`, lingering standalone-note voice in `ch34`, inconsistent export/import structure across `ch34`--`ch37`, over-generic UKF comparison formulas in `ch34`, an inconsistent same-scalar branch contract in `ch34`, an overstated one-dimensional rule requirement in `ch34`, overcompressed pseudo-marginal / exact-correction language in `ch36`/`ch37`, and an overstated particle-count proposition in `ch37`.

## Decision / policy
Future sessions should assume the following unless a later pass explicitly revises it:

1. The combined internal/Codex rewrite pass accepted the structural and claim-discipline concerns as real and addressed them directly.
2. The local `\appendix` in `ch34` was a true document bug and has been removed.
3. The `ch34` deterministic-rule comparison should now be read as allowing separate mean and covariance weights, so scaled UKF is no longer falsely collapsed into a one-weight template.
4. The `ch34` same-scalar branch contract now freezes the initial-condition policy rather than parameter-dependent realized initial values.
5. The `ch36` and `ch37` HMC language now distinguishes declared approximate scalar targets from separately defined exact-target correction schemes; ordinary approximate-filter HMC is not described as exact-target HMC by pseudo-marginal citation alone.
6. The `ch37` particle-count claim has been softened from theorem-like necessity to a heuristic/industrial-warning statement.

## What changed
- File: `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
  - Rewrote the opening to speak as a monograph chapter rather than a standalone note and added explicit import/export framing to `ch33`, `ch35`, and `ch37`.
  - Fixed the repeated/malformed factor-convention and “level” prose defects.
  - Generalized the deterministic Gaussian-surrogate comparison formulas to allow distinct mean and covariance/cross-covariance weights, with explicit note that scaled UKF requires that distinction.
  - Rewrote the saved-branch tuple so it freezes initial-condition policy rather than parameter-dependent numerical initial values.
  - Corrected the input-contract one-dimensional rule range from `\{I_\ell\}_{\ell=1}^{L+b-1}` to `\{I_\ell\}_{\ell=1}^{L}` in line with the active-band definition.
  - Replaced the old conclusion/appendix split with a chapter conclusion followed by a new `Defects Passed To Synthesis` export section; removed the local `\appendix` and kept the former appendix-style material as ordinary chapter sections.
  - Replaced several residual “report/note” references with chapter-local language in the touched sections.
- File: `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
  - Narrowed the exact-target HMC contract language so approximate-filter HMC is described as targeting the declared approximate scalar unless a separately defined exact-target extended-state correction scheme is given.
  - Reworded the same point in the plain-English explanation and approximate-filter gradient section.
  - Added explicit forward reference that broader sampler/transport policy lives in later HMC chapters, keeping `ch36` in its high-dimensional consequence role rather than a second general HMC foundations chapter.
- File: `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
  - Rewrote the HMC defect paragraph so pseudo-marginal or particle-MCMC logic is treated as relevant only when a separately defined exact-target correction scheme is actually part of the algorithm.
  - Softened `Log-weight variance defect` into `Log-weight variance warning` and changed its proof language from theorem-strength necessity to heuristic/industrial-warning language.
  - Softened the Gaussian observation illustration so it claims only exponential order in `d/R^2`, not an exact theorem-grade scale factor.

## Bugs / blockers resolved
- Symptom:
  - The high-dimensional block had no build blocker, but it still contained one true structural document bug and multiple places where the prose or mathematical contract was stronger than the formulas/citations justified.
- Root cause:
  - `ch34` still carried imported-note structure and terminology, and `ch36`/`ch37` compressed some distinctions between exact-target, approximate-target, and pseudo-marginal/extended-state logic too aggressively.
- Resolution:
  - Applied a bounded rewrite across `ch34`, `ch36`, and `ch37` that combined the internal audit with Codex's independent review, accepting the overlapping findings and incorporating the broader ones only where they fit the monograph’s current architecture.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after the combined-review rewrite.
- `docs/main.pdf` was written successfully (329 pages).
- No new fatal LaTeX errors appeared.
- No new undefined-reference warnings appeared in the final successful pass.

## Current policy
- Treat the high-dimensional block as materially safer structurally and mathematically than before the combined review pass.
- If future refinements are made, preserve the new distinctions between:
  - approximate scalar targets vs exact-target correction schemes,
  - one-weight point rules vs scaled-UKF-style separate mean/covariance weights,
  - frozen branch-defining policy vs recomputed parameter-dependent numerical values.
- Further edits should be incremental unless a new source-grounded issue is discovered.

## Known limitations / cautions
- This pass did not perform a large-scale monograph reordering, so `ch36` still remains in the high-dimensional filtering block rather than being physically moved into the later HMC part.
- `ch34` is still substantially longer than neighboring chapters even after the structural cleanup; the present pass made it safer and more coherent but did not fully resize the chapter.
- Some proposition-style material in `ch37` still functions more as monograph derivation / industrial contract than as source-backed formal theorem; this is now better signaled, but not fully relabeled.

## Suggested next steps
1. If desired, run one final prose-smoothing pass on `ch34` to reduce remaining “chapter vs report” residue outside the sections touched here.
2. Otherwise treat the combined internal-plus-Codex rewrite pass as complete and move on to the next priority with the green monograph build preserved.
