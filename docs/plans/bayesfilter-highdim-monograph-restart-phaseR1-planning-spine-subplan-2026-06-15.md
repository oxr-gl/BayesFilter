# Phase R1 Subplan: Reset Planning Spine

**Date:** 2026-06-15  
**Restart program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Create the restart control layer that supersedes the old execution assumptions:
master program, runbook, chapter crosswalk, cutover audit plan, and reset memo.

## Scope

- define the governing restart spine,
- define surface distinctions,
- define cutover gates,
- define how old subplans are wrapped rather than reused as restart governance.

## Deliverables

- restart master program,
- reset-safe runbook,
- chapter crosswalk ledger,
- cutover audit plan,
- reset memo,
- one R1 result note,
- one R1 manifest JSON,
- explicit token pair:
  - `PASS_R1_CHAPTER_CROSSWALK_FROZEN`
  - `BLOCK_R1_CHAPTER_CROSSWALK_FROZEN`

## Verification

Phase R1 succeeds when:
- all core restart-control artifacts exist,
- chapter crosswalk defines what each destination chapter should own from p47/p50,
- the cutover plan forbids early canonical switching,
- later execution can proceed without ambiguity about what is trusted.

## Stop conditions

- block if any execution starts before the control-layer artifacts exist,
- block if the crosswalk still leaves source ownership ambiguous across chapters,
- block if the new spine cannot clearly supersede the old execution logic.
