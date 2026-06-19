# Phase R5 Subplan: Canonical Cutover

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Switch the canonical compiled book to the restarted p47+p50 integration only
after all staging gates pass.

## Scope

- execute the final cutover from staging surface to canonical compiled surface,
- update canonical include paths only after explicit approval gates pass,
- retire the non-canonical state to historical/salvage status,
- record the cutover result and remaining non-claims.

## Deliverables

- cutover result note,
- final cutover manifest JSON,
- canonical switch record,
- explicit token pair:
  - `PASS_R5_RESTART_LAUNCH_AUTHORIZED`
  - `BLOCK_R5_RESTART_LAUNCH_AUTHORIZED`

## Verification

Phase R5 succeeds when:
- all prior restart gates pass,
- the staged block is approved as source-faithful and monograph-native,
- canonical include paths are updated only at the end,
- the newly canonical compiled book builds cleanly after cutover.

## Stop conditions

- block if any R4 issue remains unresolved,
- block if canonical and staging surfaces are still ambiguous,
- block if the staged block has not yet passed a whole-block cutover audit.
