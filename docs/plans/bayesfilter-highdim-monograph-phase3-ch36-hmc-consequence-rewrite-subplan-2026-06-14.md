# Phase 3 Subplan: Rewrite `ch36` As The High-Dimensional HMC Consequence Chapter

**Date:** 2026-06-14  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Purpose

Rebuild `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex` so it clearly
imports the rewritten `ch34` and `ch35` lanes and studies their target/HMC
consequences rather than behaving as a detached research note.

## Scope

- transformed-target discipline,
- same-scalar/HMC admissibility,
- transport-preconditioned HMC implications,
- TT/KR-to-HMC bridge consequences,
- SGQF versus TT/KR implications for target design.

## Chapter goal

Make `ch36` the chapter that asks:
> given the approximation families already built, what survives as an HMC target,
> and what branch or transport choices destroy that target discipline?

## Verification

- `ch36` no longer re-derives `ch34` or `ch35` material,
- instead it clearly imports their objects and studies their HMC consequences,
- it remains coherent with earlier generic HMC chapters without duplicating them.
