# Phase R0 Subplan: Baseline Lock And Demotion

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Declare the current active expanded state non-canonical, freeze the canonical
compiled baseline conceptually, and record that neither the current compressed
nor current expanded chapter sets are trusted as the final answer.

## Scope

- classify:
  - canonical compiled baseline,
  - source truth,
  - salvage-only chapter/material sets,
  - historical plan artifacts,
- state the hard rule that the active canonical compiled book may not switch early,
- define the pass/block token for restart governance.

## Deliverables

- one R0 result note,
- one R0 manifest JSON describing baseline/source/salvage sets,
- explicit token pair:
  - `PASS_R0_RESTART_GOVERNANCE`
  - `BLOCK_R0_RESTART_GOVERNANCE`

## Verification

Phase R0 succeeds when:
- the current state is explicitly demoted from accepted canon,
- the source manuscripts are clearly identified as the authored source truth,
- the canonical compiled baseline is clearly separated from salvage material,
- the restart hard rule against early cutover is written plainly.

## Stop conditions

- block if any artifact still treats the current expanded block as accepted canon,
- block if source truth, salvage, and compiled baseline cannot be distinguished
  cleanly,
- block if R0 cannot be written without changing the chapter-count target again.
