# Phase R2 Subplan: Staging Surface Creation

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Create the separate staging integration surface so the restarted p47+p50 block
can be rebuilt and reviewed without touching the canonical compiled surface.

## Scope

- create the staging driver file under `docs/`,
- define which chapter files belong to the staged candidate block,
- verify that the staging build can compile independently,
- ensure canonical `docs/main.tex` is no longer the migration surface.

## Deliverables

- staging driver file,
- file-touch manifest for the staging surface,
- one R2 result note,
- one R2 manifest JSON,
- explicit token pair:
  - `PASS_R2_CUTOVER_WRITESET_FROZEN`
  - `BLOCK_R2_CUTOVER_WRITESET_FROZEN`

## Verification

Phase R2 succeeds when:
- the separate staging driver exists,
- it is explicit which chapter files it includes,
- the staging surface can be compiled and reviewed independently,
- canonical and staging surfaces are no longer conflated.

## Stop conditions

- block if migration work still requires direct use of canonical `docs/main.tex`,
- block if the staging surface cannot be defined without ambiguity about active
  chapter ownership,
- block if the staging driver introduces canonical/baseline confusion rather than
  reducing it.
