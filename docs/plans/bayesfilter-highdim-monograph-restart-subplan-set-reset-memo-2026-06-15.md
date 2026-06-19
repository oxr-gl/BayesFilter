# Reset memo: detailed restart phase subplan set created

## Date
2026-06-15

## Context
The restart-safe p47+p50 monograph reintegration plan spine had already been
created, but the new restart master program still lacked detailed phase subplans
comparable in granularity to the older workflows. Since the user explicitly asked
whether the master program had detailed per-phase subplans, the next safe step was
to create that full subplan set before any further restart execution continued.

## Decision / policy
Future sessions should assume the following unless a later restart program
supersedes it:

1. The restart workflow now has a full detailed phase subplan set for phases
   R0--R5.
2. The restart phases are now executable as a governed sequence rather than just a
   high-level master program.
3. The canonical compiled book still may not switch early; the new subplans all
   preserve that rule.
4. The next restart execution step should follow the R-phase spine, not the older
   rewrite/expansion phase subplans.

## What changed
Created the following detailed restart phase subplans:
- `docs/plans/bayesfilter-highdim-monograph-restart-phaseR0-baseline-lock-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-highdim-monograph-restart-phaseR1-planning-spine-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-highdim-monograph-restart-phaseR2-staging-surface-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-highdim-monograph-restart-phaseR3-staging-reintegration-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-highdim-monograph-restart-phaseR4-staging-verification-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-highdim-monograph-restart-phaseR5-canonical-cutover-subplan-2026-06-15.md`

## Bugs / blockers resolved
- Symptom:
  - The restart master program existed, but did not yet have chaptered detailed
    subplans for each restart phase.
- Root cause:
  - The restart workflow had been established at the governance level before the
    per-phase subplan layer was filled in.
- Resolution:
  - Added a dedicated subplan file for each restart phase, each with purpose,
    scope, deliverables, verification, and stop conditions.

## Verification already run
- The full R0--R5 subplan set now exists under `docs/plans`.
- Each subplan preserves the staging-vs-canonical distinction and the no-early-
  cutover rule.

## Current policy
- Continue the restart using the R-phase subplan set.
- Treat the older rewrite/expansion phase subplans as superseded for restart
  execution control.
- The next meaningful restart step is to begin execution under the new R-phase
  spine, starting from the already-created staging surface.

## Known limitations / cautions
- The restart spine is now complete, but the from-scratch p47+p50 reintegration in
  staging has not yet begun under this reset-safe framework.
- The current active expanded block remains non-canonical under the restart policy
  until the later cutover phases pass.

## Suggested next steps
1. Start restart execution from the R2/R3 staging surface and reintegration plan.
2. Keep recording one result/reset artifact per meaningful restart step.
3. Do not touch canonical cutover until the staged block completes and R4 passes.
