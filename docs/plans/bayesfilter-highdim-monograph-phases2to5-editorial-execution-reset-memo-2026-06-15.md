# Reset memo: high-dimensional monograph phases 2--5 editorial-pass execution

## Date
2026-06-15

## Context
After the blocker-clearance and editorial-pass plan amendments, the remaining active work in the high-dimensional monograph rewrite was to execute Phases 2--5 as bounded editorial/source-discipline passes while preserving the green `docs/main.tex` build. The live goals were no longer emergency structural rescue or first-build success; they were chapter-boundary tightening, import/export discipline, source/claim discipline, and final integration/provenance closeout.

## Decision / policy
Future sessions should assume the following unless a later pass records a stronger contradiction:

1. Phases 2--5 have now been executed at the bounded editorial/source-discipline level without hitting a new LaTeX blocker.
2. The current `docs/main.tex` build remains green after those Phase 2--4 edits.
3. The main changes in this pass were import/export and non-overclaim tightening, not new mathematics or expanded implementation claims.
4. Further work on the high-dimensional block should be treated as incremental editorial refinement only unless a new source-grounded issue or build blocker appears.

## What changed
- File: `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
  - Strengthened the ending boundary section so it explicitly states what `ch36` and `ch37` may import from `ch35` and what they may not upgrade by implication.
  - This clarifies that later chapters may consume the declared defects, diagnostics, promotion gates, and source-risk boundaries, but may not silently treat TT/KR transport existence, branch-local differentiability, or covariance-compression feasibility as stronger than the checked sources support.
- File: `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
  - Strengthened the implementation-boundary section so the chapter explicitly names what it imports from `ch33`--`ch35` and what it does not re-license as exact, validated, or production-ready.
  - Clarified that `ch37` may consume only the same-scalar, Jacobian, divergence, and promotion-ladder consequences stated there.
- File: `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
  - Tightened the synthesis-contract section so it explicitly says the chapter consumes exported defects/gates rather than reopening upstream construction or strengthening source support by synthesis alone.

## Bugs / blockers resolved
- Symptom:
  - The chapter stack was build-stable, but the remaining Phase 2--4 risk was overreach: later chapters could still read as if they were implicitly upgrading upstream source support, reopening derivations, or re-licensing implementation claims.
- Root cause:
  - The integrated monograph needed sharper import/export language at the chapter boundaries even after the major rewrites and build repair were complete.
- Resolution:
  - Added explicit chapter-boundary language at the ends of `ch35`, `ch36`, and the architectural handoff section of `ch37`.
  - Rebuilt the monograph to verify that these editorial/source-discipline passes preserved a green build.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The build completed successfully after the Phase 2--4 editorial/source-discipline edits.
- `docs/main.pdf` was written successfully (327 pages).
- No new fatal LaTeX errors appeared.
- No new undefined-reference warnings appeared in the final successful pass.

## Current policy
- Treat the high-dimensional block as fully through the planned Phase 2--5 editorial execution path.
- Keep `docs/main.tex` green if any further wording-level refinements are made.
- Do not reopen the chapters for fresh technical scope unless a new source-grounded need is identified and planned explicitly.

## Known limitations / cautions
- This pass did not perform a new broad literature expansion; it tightened chapter boundaries using already-checked source support.
- The build being green does not by itself imply that every possible stylistic refinement is done.
- Any future attempt to strengthen mathematical or implementation claims should be treated as new scope, not as ordinary editorial cleanup.

## Suggested next steps
1. If desired, do a final human-facing read-through of `ch35`--`ch37` for prose smoothness only, keeping the green-build invariant.
2. Otherwise treat the high-dimensional rewrite stream as executed through its current planned phases and move on to the next user priority.
