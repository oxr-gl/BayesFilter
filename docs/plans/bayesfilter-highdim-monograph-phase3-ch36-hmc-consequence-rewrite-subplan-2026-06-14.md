# Phase 3 Subplan: Rewrite `ch36` As The High-Dimensional HMC Consequence Chapter

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Refine `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex` as the
high-dimensional HMC-consequence chapter now that the integrated chapter is
structurally present.

This phase should focus on consequence-discipline and citation-boundary cleanup so
`ch36` clearly imports the rewritten `ch34` and `ch35` lanes and studies their
target/HMC consequences rather than behaving as a detached research note.

## Scope

- transformed-target discipline,
- same-scalar/HMC admissibility,
- transport-preconditioned HMC implications,
- TT/KR-to-HMC bridge consequences,
- SGQF versus TT/KR implications for target design.

The active pass should explicitly cover:
- enforcing import-only behavior from `ch33`--`ch35`,
- tightening same-scalar / transformed-target / HMC-admissibility claim discipline,
- removing residual drift back into generic HMC exposition that belongs in
  earlier chapters,
- preserving room for bounded Phase 5 editorial cleanup without reopening
  technical scope.

## Chapter goal

Make `ch36` the chapter that asks:
> given the approximation families already built, what survives as an HMC target,
> and what branch or transport choices destroy that target discipline?

## Verification

- `ch36` no longer re-derives `ch34` or `ch35` material,
- instead it clearly imports their objects and studies their HMC consequences,
- it remains coherent with earlier generic HMC chapters without duplicating them,
- source/citation boundaries for same-scalar and transformed-target claims are
  explicit enough that the chapter does not overstate what the imported lanes
  prove,
- later Phase 5 editorial cleanup may still refine wording, but must not reopen
  lane construction or expand technical scope.
