# Phase 5 Subplan: `main.tex` Integration And Cleanup

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Integrate the rewritten high-dimensional block into `docs/main.tex`, repair
cross-references and bibliography wiring, and verify that the block now reads as
part of the monograph rather than as a detached digression.

## Scope

- integrate rewritten `ch34`--`ch37`,
- fix label and cross-reference drift,
- run BibTeX and rebuild the monograph,
- verify coherence with earlier sigma-point, validation, and HMC chapters.

## Chapter goal

Make the main monograph build the new high-dimensional block as the canonical
readable exposition, superseding the need to consult p47 or p50 for the primary
narrative.

## Verification

- `docs/main.tex` rebuilds successfully,
- bibliography is resolved,
- chapter cross-references are materially cleaner,
- the high-dimensional block now feels imported into the monograph rather than
  appended beside it.
