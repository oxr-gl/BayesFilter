# Phase 5 Subplan: `main.tex` Integration And Cleanup

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Preserve a green `docs/main.tex` build while the rewritten high-dimensional block
receives its final editorial, provenance, and integration closeout.

This phase should repair cross-references and bibliography wiring created or
exposed by those editorial passes and verify that the block now reads as part of
the monograph rather than as a detached digression.

## Scope

- maintain a green `docs/main.tex` build while rewritten `ch34`--`ch37` receive
  bounded editorial/source-discipline passes,
- fix label and cross-reference drift,
- run BibTeX and rebuild the monograph as needed,
- verify coherence with earlier sigma-point, validation, and HMC chapters,
- normalize source-risk, non-claim, and chapter-boundary language across the
  high-dimensional block,
- perform provenance/reset-memo/source-map closeout where relevant.

## Chapter goal

Make the main monograph maintain the new high-dimensional block as the canonical
readable exposition, superseding the need to consult p47 or p50 for the primary
narrative, while preserving build stability through the final editorial/provenance
closeout.

## Verification

- `docs/main.tex` remains green after the editorial/source-discipline passes,
- bibliography is resolved,
- chapter cross-references are materially cleaner,
- the high-dimensional block now feels imported into the monograph rather than
  appended beside it,
- chapter-boundary, source-risk, and non-claim language is normalized across the
  block,
- no new technical claims were introduced during editorial cleanup.
