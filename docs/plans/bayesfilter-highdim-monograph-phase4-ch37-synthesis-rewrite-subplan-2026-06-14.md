# Phase 4 Subplan: Rewrite `ch37` As Synthesis

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Refine `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex` as the
book-level synthesis chapter now that the integrated chapter is structurally
present.

This phase should focus on synthesis pruning and promotion-rule audit so the
chapter consumes the rewritten `ch34` and `ch35` exports rather than reopening
derivations.

## Scope

- candidate comparison,
- vetoes,
- promotion rules,
- lane-specific strengths and limits,
- deterministic Gaussian versus TT/KR lane selection logic.

The active pass should explicitly cover:
- pruning repeated derivation or pedagogy from `ch37`,
- auditing that every promotion/veto statement traces back to exported upstream
  objects,
- tightening source-risk and non-claim language,
- preserving room for bounded Phase 5 editorial cleanup without expanding the
  chapter’s technical claims.

## Chapter goal

Make `ch37` the book-level answer to:
> given the approximation families defined in the previous chapters, which lane
> is promoted under which conditions, and what are the reasons for rejection or
> acceptance?

## Verification

- `ch37` reads as synthesis, not as a fresh derivation,
- it does not repeat the pedagogy of `ch34` or `ch35`,
- it clearly states the selection logic of the high-dimensional block,
- major promotion/veto claims remain traceable to exported upstream objects and do
  not create fresh technical content by synthesis alone,
- later Phase 5 editorial cleanup may still refine wording, but must not expand
  the chapter’s technical claims.
