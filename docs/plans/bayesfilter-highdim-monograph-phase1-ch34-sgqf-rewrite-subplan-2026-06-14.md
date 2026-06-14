# Phase 1 Subplan: Rewrite `ch34` From `p47`

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Rebuild `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex` using
`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
as the primary authored source.

## Scope

Carry over the strongest p47 material:
- standard-normal GHQ family,
- what `F` means,
- tensor labels,
- sparse-grid level,
- Smolyak combination,
- 2D and 3D merged-cloud pedagogy,
- UKF bridge,
- second-moment / matching-weights explanation,
- fixed-cloud scalar and derivative discipline.

## Chapter goal

Make `ch34` the canonical deterministic Gaussian / sparse-grid lane chapter that
is readable without needing the standalone p47 note.

## Verification

- `ch34` can be read as a self-contained chapter within the monograph;
- the SGQF lane is pedagogically and formally clearer than in the old `ch34`;
- references back to `ch33` and forward to `ch37` are explicit and natural.
