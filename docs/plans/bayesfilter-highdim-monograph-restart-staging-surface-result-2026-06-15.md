# Reset memo: restart staging surface isolated from canonical chapter copies

## Date
2026-06-15

## Context
The restart-safe planning spine had already been created, along with an initial
staging driver. However, the first staging driver still directly included the
same expanded chapter files that were also serving as the current compiled
expanded block. That meant the staging-vs-canonical distinction existed in
planning, but not yet in the actual writable chapter surface. The next safe step
was therefore to isolate the staging surface by copying the current expanded
chapters into a separate staging-only directory and rewiring the staging driver to
compile those copies.

## Decision / policy
Future sessions should assume the following unless a later restart artifact
supersedes it:

1. The restart staging surface is now physically isolated from the current active
   expanded chapter files.
2. The canonical compiled surface and the staging integration surface are now
   distinct both conceptually and in file paths.
3. Restart reintegration work should proceed inside `docs/chapters_restart_staging/`,
   not inside the canonical compiled include path.
4. The staging build already compiles in this isolated form, so future source-
   truth migration can proceed there without further canonical ambiguity.

## What changed
- Directory created:
  - `docs/chapters_restart_staging/`
- Copied into staging-only form:
  - `ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - `ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - `ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - `ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - `ch38_highdim_validation_defect_calculus_and_promotion.tex`
- File updated:
  - `docs/main_highdim_restart_staging.tex`
  - The staging driver now inputs the chapter files from
    `docs/chapters_restart_staging/` rather than from the canonical expanded
    chapter path.

## Bugs / blockers resolved
- Symptom:
  - The restart staging surface was still conceptually separate but not file-
    isolated, so future migration work could still blur staging and canonical
    chapter state.
- Root cause:
  - The first staging driver reused the same chapter files already being used by
    the current compiled expanded block.
- Resolution:
  - Created a physically separate chapter directory for the staging surface and
    rewired the staging driver to use it.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- The isolated staging driver rebuilt successfully.
- `docs/main_highdim_restart_staging.pdf` was written successfully (279 pages).
- No fatal LaTeX errors occurred.
- The remaining undefined-reference warnings are inherited whole-book issues
  outside the high-dimensional restart scope and do not reflect a failure of the
  staging isolation step itself.

## Current policy
- All restart reintegration work should now happen in:
  - `docs/chapters_restart_staging/`
- Do not treat edits to those files as edits to the canonical compiled surface.
- Preserve the current canonical compiled baseline while the staging surface is
  rebuilt from p47/p50 source truth.

## Known limitations / cautions
- The staging chapter copies currently inherit the same transitional content as
  the expanded chapter set at the moment they were copied.
- The source-truth reintegration restart has not yet begun inside the staging
  copies; only the safe execution surface is now established.
- The staging build still reports pre-existing whole-book reference warnings that
  are outside the specific high-dimensional restart scope.

## Suggested next steps
1. Begin the actual from-scratch p47+p50 reintegration in
   `docs/chapters_restart_staging/` according to the restart crosswalk.
2. Keep compiling `main_highdim_restart_staging.tex` as the review surface.
3. Do not consider canonical cutover until the staged block is judged complete by
   the restart cutover audit plan.
