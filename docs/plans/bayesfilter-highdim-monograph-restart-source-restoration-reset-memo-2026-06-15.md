# Reset memo: restart the high-dimensional monograph integration from staging after premature cutover

## Date
2026-06-15

## Context
This session attempted to repair the high-dimensional monograph block, then expand it, then restart the p47+p50 integration safely in staging. The restart-safe governance and staging split were created, and the staging chapter set was rewritten from source truth enough to support an R4 review. However, the later canonical cutover was still premature. The current canonical expanded block compiles, but it does not yet carry enough of the useful explanatory burden of p47 and especially p50 to be trusted as the finished monograph integration.

The key failure was not just local prose quality. It was that architectural plausibility and clean builds were allowed to stand in for full source-fidelity sufficiency. In practice, the current canonical chapters still compress too much of the source material — especially the p50 operational middle: coordinate-system walkthroughs, retained-object flow, fixed-branch scalar construction, derivative mechanics, and validation depth.

## Decision / policy
Future sessions should assume the following unless a later memo explicitly supersedes it:

1. The current canonical expanded high-dimensional block is **not accepted as final**.
2. The most trustworthy work surface is the **staging surface**, not the current canonical compiled book.
3. Source truth remains:
   - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
   - `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
4. The next work should be **source-restoration**, not more architecture invention.
5. The strongest remaining source-fidelity gap is on the **p50 side**, especially:
   - staging `ch36` (retained-object / TT / KR lane),
   - then likely staging `ch35` if the p47 pedagogy is still too compressed.
6. No future canonical switch should happen until:
   - source-restoration is done,
   - a fresh whole-block review passes,
   - and the staged block no longer feels thinner than p47/p50 in explanatory burden.

## What changed in this session
- A restart-safe planning spine was created under `docs/plans`:
  - restart master program,
  - runbook,
  - chapter crosswalk,
  - cutover audit plan,
  - restart phase subplans,
  - restart reset memos.
- A staging driver was created:
  - `docs/main_highdim_restart_staging.tex`
- A staging chapter directory was created:
  - `docs/chapters_restart_staging/`
- Source-truth rewrites were performed in staging for:
  - `ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - `ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - `ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - `ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - `ch38_highdim_validation_defect_calculus_and_promotion.tex`
- A canonical cutover was then performed, but this memo records that the cutover should not be treated as acceptance.

## Why the cutover is now considered premature
- p47 is partly under-carried, but still mostly recognizable in chapter form.
- p50 remains materially under-carried in the current canonical book.
- The current canonical chapters do not yet fully replace the need to read p50 for:
  - retained-object mechanics,
  - coordinate-system flow,
  - branch-frozen recomputation logic,
  - fixed-branch derivative burden,
  - richer validation depth.
- The correct judgment criterion should have been “does the new monograph carry the useful source explanation?”, not merely “does it compile cleanly and fit the chapter map?”.

## Current trusted surfaces

### Source truth
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

### Preferred active work surface
- `docs/main_highdim_restart_staging.tex`
- `docs/chapters_restart_staging/`

### Do not trust as final answer
- current canonical expanded chapter files under `docs/chapters/ch34`--`ch38`
- current canonical `docs/main.pdf`

These may still be useful as salvage or comparison, but they should not be treated as the completed monograph integration.

## Known limitations / cautions
- This session’s history is now too complex and self-contradictory to continue safely without a clean restart.
- Delayed audit results referred to multiple obsolete topologies during the session, which further increased context confusion.
- A new session should not inherit informal assumptions from this one beyond what is written in this memo and the restart artifacts under `docs/plans`.

## Suggested next steps
1. Start a fresh session.
2. In that new session, treat this memo as the active reset baseline.
3. Resume from the staging surface only:
   - `docs/main_highdim_restart_staging.tex`
   - `docs/chapters_restart_staging/`
4. First task in the new session:
   - audit staging `ch36` against p50 specifically for missing explanatory burden,
   - then restore that burden before any new cutover discussion.
5. Only after the p50 source-restoration pass, reconsider whether staged `ch35` also needs restoration of p47 pedagogy.
6. Do not attempt canonical cutover again until a new whole-block review says the staged block actually replaces the need to read p47 and p50.
