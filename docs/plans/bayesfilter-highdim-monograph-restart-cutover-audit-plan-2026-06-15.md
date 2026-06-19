# Cutover Audit Plan: Restarted High-Dimensional Monograph Block

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Define the explicit review gate that must pass before the canonical compiled book
switches to the restarted p47+p50 integration.

## Questions the cutover must answer

1. Does the staged block actually carry the p47 and p50 material, rather than
   only summarizing it?
2. Are the chapter boundaries now aligned with the intended architecture?
3. Does the staged block read as part of the monograph rather than as appended
   source-note prose?
4. Are references, bibliography, labels, and source-map / reset-memo links clean
   enough for canonical use?
5. Does the handoff from the high-dimensional block to the later HMC part make
   sense at the whole-book level?

## Required cutover evidence

### 1. Staging build evidence
- clean compile of the staging driver
- generated staging PDF
- label/reference and bibliography review

### 2. Source-fidelity evidence
- p47 lane chapters reviewed against p47 source
- p50 lane chapters reviewed against p50 source
- shared fixed-branch and validation chapters reviewed against both source bases

### 3. Whole-block integration evidence
- read-through of:
  - retained `ch33`
  - staged `ch34`
  - staged `ch35`
  - staged `ch36`
  - staged `ch37`
  - staged `ch38`
- specific judgment on import/export continuity

### 4. Whole-book boundary evidence
- handoff from `ch20` to the restarted block
- handoff from the restarted block to later HMC chapters
- no duplicated generic-HMC or generic sigma-point burden beyond what the block
  should specialize

## Cutover vetoes

Do not switch the canonical compiled book if any of the following remain true:
- staged chapters still read like transitional seeded salvage rather than source-
  truth reconstruction,
- p47 or p50 explanatory weight is still visibly absent,
- the staged block still relies on transitional compatibility assumptions that are
  known to hide unresolved architectural ambiguity,
- the staged PDF still feels like a compressed digest instead of a monograph
  treatment,
- references/bibliography/source-map consistency remain materially unstable.

## Cutover success condition

Switching the canonical compiled book is justified only when the staged block is
judged complete as a source-faithful, monograph-native, whole-book-integrated
replacement for the high-dimensional section, not merely as a buildable chapter
set.