# Reset-Safe Runbook: High-Dimensional Monograph P47+P50 Reintegration Restart

**Date:** 2026-06-15  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Purpose

Provide a visible, gated runbook for restarting the p47+p50 monograph
integration without confusing the staging build with the canonical compiled book.

## Hard rule

The canonical compiled book may not switch to the restarted p47+p50 block until
all cutover gates in this runbook pass.

## Surface definitions

### Canonical compiled surface
- `docs/main.tex`
- frozen during restart
- may be inspected and cited as current baseline
- may not be used as the migration surface for unfinished p47+p50 integration

### Staging integration surface
- a separate driver file under `docs/` created in Phase R2
- hosts the restarted high-dimensional integration candidate
- all chapter replacement, label repair, and whole-block review happen here first

## Gates

### Gate G0 — Baseline lock
Pass when:
- the current active state is explicitly demoted to non-canonical,
- source truth, salvage, and canonical compiled baseline are clearly classified.

Block if:
- any plan still treats the current expanded block as accepted canon.

### Gate G1 — Planning spine
Pass when:
- restart master program exists,
- runbook exists,
- chapter crosswalk exists,
- cutover audit plan exists.

Block if:
- any execution starts before these artifacts exist.

### Gate G2 — Staging surface established
Pass when:
- the separate staging driver exists,
- it is clear which files it includes,
- canonical compiled surface remains untouched.

Block if:
- migration work still edits the canonical include path directly.

### Gate G3 — Source-truth integration
Pass when:
- p47 and p50 content has been reintegrated into the target chapters in the
  staging surface,
- salvage files are only mined, not treated as final authority.

Block if:
- a staging chapter is still visibly driven by salvage architecture rather than
  source truth.

### Gate G4 — Staging verification
Pass when:
- the staging build compiles cleanly,
- labels, bibliography, and references are acceptable,
- whole-block review confirms the material is truly present rather than implied.

Block if:
- the staged PDF still reads as a compressed digest or an unfinished migration.

### Gate G5 — Canonical cutover
Pass when:
- all prior gates pass,
- a final cutover audit approves switching the canonical compiled surface.

Block if:
- any unresolved ambiguity remains about target completeness or source fidelity.

## Phase order

1. R0 baseline lock
2. R1 planning spine
3. R2 staging surface creation
4. R3 source-truth integration in staging
5. R4 staging-only verification
6. R5 canonical cutover

## Deliverable

A restart workflow in which the canonical book remains frozen while the new
p47+p50 integration is rebuilt and reviewed in staging, then switched only after
explicit approval gates pass.