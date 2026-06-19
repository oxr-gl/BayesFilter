# Phase 2 Subplan: Rewrite `ch35` From `p50`

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Refine the existing `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
using `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
as the primary authored source base.

This phase now treats `ch35` as an already-formed monograph chapter that needs a
bounded editorial and source-discipline pass rather than a blank-sheet rewrite.

## Scope

Carry over and discipline the strongest p50 material already present or still
needed in `ch35`:
- the stronger opening voice,
- threaded nonlinear example discipline,
- TT approximation toolkit,
- rank plausibility,
- coordinate systems and retained-object flow,
- squared-TT object and recursion,
- fixed-branch likelihood construction,
- derivative warmups and branch identity framing,
- validation framing relevant to the TT/KR lane.

The active pass should explicitly cover:
- source-anchor audit against p50 and Zhao--Cui source-faithfulness rules,
- claim-discipline tightening for TT/KR/fixed-branch statements,
- chapter-flow cleanup so the lane reads as one monograph chapter,
- import/export cleanup for downstream `ch36` and `ch37` use.

## Chapter goal

Make `ch35` the canonical TT / KR / transport filtering chapter, readable as a
chapter rather than as a reorganized technical note, with source-faithfulness and
claim boundaries explicit enough for later HMC-consequence and synthesis use.

## Verification

- `ch35` can stand on its own as the monograph’s non-Gaussian carried-object lane;
- the fixed-branch and implementation-facing material is staged around what is
  mathematically interesting and easy to get wrong;
- the chapter no longer reads as several interleaved notes;
- every source-faithfulness claim needed for the Zhao--Cui lane is auditable from
  the cited paper/source basis rather than implied by prose alone;
- later Phase 5 editorial cleanup may still refine wording, but must not expand
  the technical scope or weaken the source-anchor discipline.
