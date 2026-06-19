# Phase 0 Subplan: Expanded High-Dimensional Block Architecture And Import/Export Contracts

**Date:** 2026-06-15  
**Master program:** `docs/plans/bayesfilter-highdim-monograph-expansion-master-program-2026-06-15.md`

## Purpose

Define the chapter responsibilities, file strategy, and import/export logic for an
expanded high-dimensional nonlinear filtering block before any new chapter-level
rewriting begins.

## Questions to answer

1. What exact book-level question does the expanded block answer?
2. Which conceptual units are shared across p47 and p50 and therefore deserve
   shared monograph chapters rather than source-specific ownership?
3. Which current `ch33`--`ch37` files are retained, repurposed, or replaced?
4. What new chapter files should be added under `docs/chapters/`?
5. How should `docs/main.tex` be updated while preserving the current part logic?
6. What does each expanded-block chapter import from earlier monograph chapters?
7. What does each expanded-block chapter export to the next chapter and to the
   later generic HMC part?

## Deliverables

- a chapter-role map for the expanded block,
- a file map from the current `ch33`--`ch37` arrangement to the new chapter set,
- a dependency/import map to earlier chapters such as sigma-point filters,
  square-root filters, particle filters, DPF/HMC suitability, and generic HMC
  chapters,
- a statement of what `p47` and `p50` each own as authored source bases,
- a `docs/main.tex` insertion/update plan for the new block.

## Verification

The phase succeeds when the expanded high-dimensional block can be described as
one coherent multi-chapter sequence with explicit import/export logic and a
clear file strategy, rather than as a compressed summary of two source notes.