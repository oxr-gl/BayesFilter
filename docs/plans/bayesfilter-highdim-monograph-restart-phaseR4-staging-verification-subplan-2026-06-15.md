# Phase R4 Subplan: Staging-Only Verification

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Compile and review the staged p47+p50 block as a whole before any canonical
switch is considered.

## Scope

- compile the staging driver,
- repair labels, references, bibliography, and source-map consistency in staging,
- review the staged PDF for actual p47/p50 presence and not just structural
  plausibility,
- perform a whole-block integration audit on the staged surface only.

## Deliverables

- staging build result note,
- whole-block staging integration audit,
- one R4 manifest JSON,
- blocker register if needed,
- explicit token pair:
  - `PASS_R4_CUTOVER_PREFLIGHT_READY`
  - `BLOCK_R4_CUTOVER_PREFLIGHT_READY`

## Verification

Phase R4 succeeds when:
- the staging build compiles cleanly,
- the staged PDF carries the expected p47/p50 explanatory weight,
- references, labels, bibliography, and source-map links are acceptable,
- whole-block review confirms the material belongs to the monograph rather than
  merely existing as buildable text.

## Stop conditions

- block if the staged PDF still feels like a compressed digest,
- block if p47/p50 material is still visibly absent or under-carried,
- block if references/bibliography/source-map consistency remain materially
  unstable.
