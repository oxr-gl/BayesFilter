# Reset memo: p47+p50 monograph integration restart

## Date
2026-06-15

## Context
The expanded high-dimensional block was made buildable and then improved through
multiple architecture and chapter-role rewrites.  However, the user correctly
judged that the active compiled book had switched too early into a partially
migrated replacement state: the book compiled, but large parts of the p47 and
especially p50 explanatory burden were still missing or redistributed in ways
that were not yet trustworthy as canonical monograph integration.

The safest recovery is therefore a restart in governance, not another local
patch.  The current state is treated as failed/non-canonical, and the p47+p50
integration is restarted from source truth with an explicit rule that the
canonical compiled book may not switch until the new integration is complete and
passes a staged review gate.

## Decision / policy
Future sessions should assume the following unless a later program supersedes it:

1. The current active expanded block is not trusted as the canonical p47+p50
   integration.
2. The current active compiled book surface is frozen conceptually as baseline,
   not as acceptance proof.
3. p47 and p50 are the authored source truth for the restart:
   - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
   - `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
4. Both the old compressed block and the current expanded block are salvage-only
   inputs until the restart completes.
5. A separate staging integration surface must be used before any future
   canonical cutover.
6. The canonical compiled book may not switch to the restarted integration until
   the staged block is complete, compiles cleanly, and passes a whole-block
   cutover audit.

## What changed
- File: `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`
  - Created the new governing restart master program.
- File: `docs/plans/bayesfilter-highdim-monograph-restart-runbook-2026-06-15.md`
  - Created the gated reset-safe runbook.
- File: `docs/plans/bayesfilter-highdim-monograph-restart-chapter-crosswalk-2026-06-15.md`
  - Created the source-truth chapter crosswalk.
- File: `docs/plans/bayesfilter-highdim-monograph-restart-cutover-audit-plan-2026-06-15.md`
  - Created the explicit cutover audit plan.

## Bugs / blockers resolved
- Symptom:
  - The active compiled book had become a partially migrated expanded block that
    was buildable but not trusted.
- Root cause:
  - The canonical compiled surface switched before the source-material migration
    was actually complete.
- Resolution:
  - Reframed the problem as a restart, froze the current state conceptually, and
    rewrote the governing plan spine around source truth, salvage layers, staging
    integration, and explicit cutover gates.

## Verification already run
- The new reset master program, runbook, chapter crosswalk, and cutover audit
  plan have all been created.
- Their shared rule is explicit: do not switch the canonical compiled book early.

## Current policy
- Do not treat the active expanded block as accepted canon.
- Do not begin the restarted p47+p50 integration inside the canonical compiled
  surface.
- The next execution step is to define the separate staging driver file and only
  then begin the from-scratch reintegration on that surface.

## Known limitations / cautions
- The restart governance is now in place, but the staging surface itself has not
  yet been created.
- No new source migration should begin until that staging-vs-canonical split is
  made explicit in the actual build surface.

## Suggested next steps
1. Create the separate staging driver file under `docs/`.
2. Define exactly which chapter files the staging driver will compile.
3. Only then begin the from-scratch p47+p50 reintegration using the new restart
   program and chapter crosswalk.
