# Reset memo: monograph rewrite editorial-pass transition

## Date
2026-06-15

## Context
The high-dimensional monograph rewrite master program and phase subplans were originally written in a pre-stability state where the dominant concern was clearing `ch34` integration blockers and reaching a successful `docs/main.tex` build. After the 2026-06-15 blocker-clearance pass, that build now succeeds and the immediate `\chol`/cross-reference issues are resolved. The next ambiguity was governance: the plan stack still read as if Phases 2--4 were pre-build rewrites and Phase 5 was mainly “make the monograph build,” which risked blocking or second-guessing the editorial/source-discipline work that should follow.

## Decision / policy
Future sessions should assume the following unless a later plan supersedes it:

1. The high-dimensional block is now in **editorial/provenance execution mode**, not blocker-repair mode.
2. Phase 1 (`ch34`) is a completed prerequisite / maintenance baseline, not the live gate.
3. Phases 2--4 are now explicitly authorized as **bounded editorial/source-discipline passes** over the existing integrated chapters:
   - `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
   - `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
   - `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
4. Phase 5 now means **preserve the green `docs/main.tex` build while editorial, bibliography, cross-reference, provenance, and chapter-boundary cleanup proceeds**.
5. These editorial passes may tighten prose, chapter flow, source-risk language, claim boundaries, and import/export clarity, but they must **not** introduce new mathematics, new implementation claims, or weakened Zhao--Cui source-anchor discipline.

## What changed
- File: `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`
  - Added post-blocker status noting that `docs/main.tex` now builds and that Phase 1 is a completed prerequisite.
  - Reframed Phases 2--4 from open-ended rewrites into editorial/source-discipline, consequence-discipline, and synthesis-pruning passes over structurally present chapters.
  - Reframed Phase 5 from a one-time build gate into a maintained-green-build editorial/provenance closeout.
  - Added an explicit governing rule authorizing one bounded post-build editorial/source-discipline pass across `ch34`--`ch37`.
  - Expanded verification criteria so build stability plus disciplined editorial cleanup are both part of program success.
- File: `docs/plans/bayesfilter-highdim-monograph-phase2-ch35-zhaocui-ttkr-rewrite-subplan-2026-06-14.md`
  - Recast the phase as refinement of the existing `ch35` chapter.
  - Added explicit scope for source-anchor audit, claim-discipline tightening, chapter-flow cleanup, and downstream import/export cleanup.
  - Added verification language preserving later Phase 5 wording cleanup without technical-scope expansion.
- File: `docs/plans/bayesfilter-highdim-monograph-phase3-ch36-hmc-consequence-rewrite-subplan-2026-06-14.md`
  - Recast the phase as a consequence-discipline and citation-boundary pass over the existing integrated `ch36`.
  - Added explicit scope for import-only behavior, same-scalar / transformed-target claim discipline, and pruning of generic-HMC drift.
- File: `docs/plans/bayesfilter-highdim-monograph-phase4-ch37-synthesis-rewrite-subplan-2026-06-14.md`
  - Recast the phase as synthesis pruning and promotion-rule audit over the existing integrated `ch37`.
  - Added explicit scope for pruning repetition, tracing promotion/veto statements to upstream exports, and tightening source-risk / non-claim language.
- File: `docs/plans/bayesfilter-highdim-monograph-phase5-maintex-integration-subplan-2026-06-14.md`
  - Recast Phase 5 around maintaining the green monograph build while editorial/provenance cleanup runs.
  - Expanded scope and verification to include source-risk, non-claim, chapter-boundary, and provenance/reset-memo/source-map closeout.
- File: `docs/plans/bayesfilter-highdim-main-monograph-integration-plan-2026-06-14.md`
  - Updated the recommended order so execution resumes from the Phase 2 editorial pass rather than from `ch34` rescue.
  - Updated build verification to require preserving a green build throughout the remaining passes.

## Bugs / blockers resolved
- Symptom:
  - The governing plan stack no longer matched the actual repository state after the build was repaired.
- Root cause:
  - The plans were still written in a pre-stability frame where blocker repair and first successful build were the dominant milestones.
- Resolution:
  - Amended the governing plan artifacts so they now explicitly authorize bounded editorial/source-discipline passes after build stability and make the green build a maintained invariant.

## Verification already run
```bash
# Read back amended plan artifacts for authority and phase order
# (master program, phase 2-5 subplans, and integration plan)
```

Observed:
- The master program now explicitly says the `ch34` blocker is cleared, `docs/main.tex` builds, and active execution resumes with Phases 2--5 editorial/source-discipline work.
- Phase 2 now explicitly authorizes a p50/Zhao--Cui source-anchor and claim-discipline pass on the existing `ch35`.
- Phase 3 now explicitly authorizes an import-only consequence-discipline pass on the existing `ch36`.
- Phase 4 now explicitly authorizes synthesis pruning and promotion-rule audit on the existing `ch37`.
- Phase 5 now explicitly authorizes maintaining the green build while editorial/provenance closeout proceeds.
- The integration plan’s recommended order now starts from the editorial-pass sequence rather than `ch34` rescue.

## Current policy
- Resume execution at **Phase 2 editorial/source-discipline review of `ch35`**.
- After each chapter pass, rerun the monograph build to preserve the green-build invariant.
- Treat build success as necessary but not sufficient; chapter-role, source-faithfulness, and synthesis discipline remain required gates.

## Known limitations / cautions
- The plan amendments authorize the remaining work but do not themselves complete the editorial passes.
- `ch35`, `ch36`, and `ch37` still need actual section-by-section review against their source manuscripts and phase goals.
- If a future pass discovers that an editorial change requires true new mathematical content, that should trigger a new planning decision rather than being smuggled in under the editorial-pass authority.

## Suggested next steps
1. Start the Phase 2 editorial/source-discipline pass on `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex` against the p50 source note and Zhao--Cui source-anchor rules.
2. Rebuild `docs/main.tex` after that pass.
3. Then continue Phase 3 (`ch36`) and Phase 4 (`ch37`) under the amended plan stack.
