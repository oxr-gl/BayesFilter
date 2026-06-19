# Phase R3 Subplan: From-Scratch P47+P50 Reintegration In Staging

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Rebuild the target high-dimensional block in the staging surface from p47/p50
source truth, using both the old compressed and current expanded chapter sets as
salvage-only inputs.

## Scope

- migrate p47/p50 into the target destination chapters named in the crosswalk,
- use salvage chapter files only for equations, tables, wording fragments, and
  previously repaired boundary/claim text,
- preserve the staged build after each migration step,
- keep chapter-by-chapter migration and review entirely in the staging surface.

## Deliverables

- one result note per meaningful migration step,
- one R3 manifest JSON tracking the staged chapter state,
- chapter-by-chapter source-allocation notes as needed,
- explicit token pair:
  - `PASS_R3_EXECUTION_RUNBOOK_READY`
  - `BLOCK_R3_EXECUTION_RUNBOOK_READY`

## Verification

Phase R3 succeeds when:
- p47 and p50 material are materially present in the staged destination chapters,
- salvage architecture is no longer dictating chapter roles,
- the staged build remains green after each migration step,
- the destination chapters no longer read as mere digests of the source notes.

## Stop conditions

- block if a staged chapter still visibly follows salvage architecture instead of
  source truth,
- block if the staged build breaks and the failure obscures chapter-role judgment,
- block if the migration still depends on treating the staging surface as already
  canonical.
