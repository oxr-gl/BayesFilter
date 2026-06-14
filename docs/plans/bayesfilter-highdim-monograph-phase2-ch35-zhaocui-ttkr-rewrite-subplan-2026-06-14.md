# Phase 2 Subplan: Rewrite `ch35` From `p50`

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Rebuild `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex` using
`docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
as the primary authored source.

## Scope

Carry over the strongest p50 material:
- the stronger opening voice,
- threaded nonlinear example discipline,
- TT approximation toolkit,
- rank plausibility,
- coordinate systems and retained-object flow,
- squared-TT object and recursion,
- fixed-branch likelihood construction,
- derivative warmups and branch identity framing,
- validation framing relevant to the TT/KR lane.

## Chapter goal

Make `ch35` the canonical TT / KR / transport filtering chapter, readable as a
chapter rather than as a reorganized technical note.

## Verification

- `ch35` can stand on its own as the monograph’s non-Gaussian carried-object lane;
- the fixed-branch and implementation-facing material is staged around what is
  mathematically interesting and easy to get wrong;
- the chapter no longer reads as several interleaved notes.
