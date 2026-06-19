# Reset memo: expanded high-dimensional block migration step 1 (new Chapter 34 normalization)

## Date
2026-06-15

## Context
After activating the expanded high-dimensional architecture and creating an explicit execution plan, the first migration step was to normalize the new `ch34` into a true deterministic Gaussian / point-rule foundations chapter. The seeded file had been copied from the front of the old compressed `ch34`, so it still read too much like a whole-lane or imported-note chapter rather than the new shared deterministic entry point that should prepare the reader for the sparse-grid specialization in the next chapter.

## Decision / policy
Future sessions should assume the following unless a later migration step replaces it:

1. The new `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex` is now the active deterministic Gaussian / point-rule foundations chapter in the expanded block.
2. Its role is narrower than the old compressed `ch34` role:
   - deterministic Gaussian carried object,
   - Gaussian projection,
   - point-rule family language,
   - bridge into sparse-grid specialization.
3. Low-dimensional cloud construction, sparse-grid mechanics, filtering value path, and the fixed-cloud scalar now belong conceptually to new `ch35`, not to new `ch34`.
4. The monograph build remains green after this first migration step.

## What changed
- File: `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - Rewrote the opening to frame the chapter as the shared deterministic Gaussian entry point rather than the whole fixed sparse-grid lane.
  - Replaced direct sparse-grid-lane wording with language about deterministic Gaussian carried objects and point-rule foundations.
  - Reframed the import/export logic so the chapter explicitly imports from `ch33` and exports to new `ch35`.
  - Renamed the object-map subsection from report-wide language to chapter-local deterministic-Gaussian language.
  - Replaced remaining “this note/report” wording in the touched front matter with chapter-language.
  - Added an explicit bridge paragraph at the Jia--Xin--Cheng Gaussian approximation block interface explaining that the sparse-grid specialization begins in the next chapter at the expectation-to-cloud replacement step.

## Bugs / blockers resolved
- Symptom:
  - The new `ch34` still read like a transplanted whole-lane chapter instead of the first method chapter in the expanded architecture.
- Root cause:
  - The file was seeded directly from the front of the old compressed `ch34`, which still bundled Gaussian foundations together with sparse-grid lane identity.
- Resolution:
  - Narrowed the framing and role statements so the chapter now serves as a deterministic Gaussian / point-rule foundation chapter rather than the full sparse-grid method chapter.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuilt successfully after the `ch34` normalization pass.
- `docs/main.pdf` was written successfully (304 pages).
- No new fatal LaTeX errors appeared.
- No new undefined-reference warnings appeared in the final successful pass.

## Current policy
- Continue the migration according to the execution plan, with `new ch35` now the next active chapter to normalize into the true sparse-grid / fixed-cloud method chapter.
- Preserve the green build after each chapter migration step.
- Do not let `new ch34` regrow sparse-grid-heavy content that now belongs in `new ch35`.

## Known limitations / cautions
- `new ch34` is only normalized in its front/shared deterministic portion so far; it has not yet undergone a full style/label cleanup across every inherited section.
- The deeper substantive migration still lies ahead in `new ch35` and `new ch36`, where the seeded content remains closer to the old compressed chapters.

## Suggested next steps
1. Normalize `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex` into the true p47 sparse-grid method chapter.
2. Rebuild `docs/main.tex` after that pass.
3. Continue then to `new ch36` for the p50 retained-object lane migration.
