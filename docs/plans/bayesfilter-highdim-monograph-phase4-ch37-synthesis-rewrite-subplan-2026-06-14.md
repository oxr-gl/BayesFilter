# Phase 4 Subplan: Rewrite `ch37` As Synthesis

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Rebuild `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex` so it
functions as a true synthesis chapter using the rewritten `ch34` and `ch35` as
its inputs.

## Scope

- candidate comparison,
- vetoes,
- promotion rules,
- lane-specific strengths and limits,
- deterministic Gaussian versus TT/KR lane selection logic.

## Chapter goal

Make `ch37` the book-level answer to:
> given the approximation families defined in the previous chapters, which lane
> is promoted under which conditions, and what are the reasons for rejection or
> acceptance?

## Verification

- `ch37` reads as synthesis, not as a fresh derivation,
- it does not repeat the pedagogy of `ch34` or `ch35`,
- and it clearly states the selection logic of the high-dimensional block.
