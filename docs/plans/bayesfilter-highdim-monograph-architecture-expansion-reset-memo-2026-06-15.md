# Reset memo: high-dimensional monograph architecture expansion transition

## Date
2026-06-15

## Context
The high-dimensional monograph rewrite stream had already gone through blocker
repair, editorial/source-discipline cleanup, and combined internal/Codex audit.
Those passes improved correctness and build stability, but they also made clear
that the deeper problem was architectural compression: `p47` and `p50` together
were being forced into too few chapter slots, which produced a monograph block
that still felt like a summarized digest of the source notes rather than a
holistic monograph treatment.

The user then made the decisive architectural call: the source material should
spread across multiple chapter files, roughly 4--5 chapters after the shared
foundations chapter, and the monograph should synthesize the two documents rather
than assign them one-to-one chapter ownership.

## Decision / policy
Future sessions should assume the following unless a later plan explicitly
replaces it:

1. The current compressed `ch33`--`ch37` target architecture is obsolete.
2. The program is now in **architecture-expansion mode**, not local cleanup mode.
3. The correct implementation strategy is **Option B**: add multiple new chapter
   files rather than continue trying to force the source material into the current
   `ch34`--`ch37` files.
4. The preferred architectural target is:
   - retained `ch33` foundation,
   - then five post-foundation chapters:
     1. deterministic Gaussian / point-rule foundations,
     2. sparse-grid quadrature and fixed-cloud scalar,
     3. low-rank TT/KR retained-object methods,
     4. fixed-branch approximate likelihoods and same-scalar gradients,
     5. validation / defect calculus / promotion.
5. A sixth chapter is allowed if the validation/synthesis material proves too
   large, but the default planning target remains the 5-chapter post-foundation
   block.
6. The enlarged block should remain at the end of `\part{Nonlinear Filtering}`
   and should hand off to the later generic HMC part rather than moving wholesale
   into it.

## What changed
- File: `docs/plans/bayesfilter-highdim-monograph-expansion-master-program-2026-06-15.md`
  - Created the new governing expansion master program.
  - Replaced the compressed `ch33`--`ch37` target architecture with a larger,
    synthesized block architecture.
  - Declared Option B (new chapter files) as the active file strategy.
- File: `docs/plans/bayesfilter-highdim-monograph-expansion-phase0-architecture-subplan-2026-06-15.md`
  - Created the Phase 0 architecture subplan for the expansion stream.
  - Defined the architecture/file/import-export questions that must be settled
    before implementation.
- File: `docs/plans/bayesfilter-highdim-monograph-expansion-integration-plan-2026-06-15.md`
  - Created the integration plan for the expanded block.
  - Defined the proposed new chapter-file map and the implementation order.

## Bugs / blockers resolved
- Symptom:
  - Even after structural cleanup and build success, the high-dimensional block
    still read like a compressed or butchered summary of `p47` and `p50`.
- Root cause:
  - The architecture itself was too small for the explanatory and methodological
    scope of the source manuscripts.
- Resolution:
  - Abandoned the compressed rewrite target and replaced it with an explicit
    architecture-expansion program built around shared-structure chapters plus
    method-specific chapters.

## Verification already run
```bash
# Read-only architecture audit and source-structure mapping
# followed by plan creation for the expanded block
```

Observed:
- The source manuscripts naturally support five conceptual units after the shared
  foundations chapter.
- The current monograph part structure can host the expanded block without moving
  it outside `\part{Nonlinear Filtering}`.
- The main planning risk is no longer “can we make the current chapters better?”
  but “can we now rewrite the governing plans and file strategy before touching
  chapter text?”

## Current policy
- Do not continue the old `ch34`--`ch37` rewrite phases as if they were still the
  target architecture.
- The next implementation work should begin by deciding the concrete new chapter
  filenames and updating `docs/main.tex` accordingly.
- The current `ch34`--`ch37` files remain salvage material and local reference,
  not the fixed destination.

## Known limitations / cautions
- The new plan establishes the right architectural target but does not yet create
  the new chapter files.
- Chapter numbering/file naming inside `docs/chapters/` still needs a concrete
  implementation decision before text migration begins.
- Any aggressive global renumbering outside the high-dimensional block is still
  out of scope unless later approved explicitly.

## Suggested next steps
1. Decide the exact new chapter filenames and `docs/main.tex` insertion order.
2. Create the new chapter files under `docs/chapters/` and migrate the source
   material according to the expansion program.
3. Only after the expanded file structure exists begin the full chapter-by-chapter
   rewrite execution.
