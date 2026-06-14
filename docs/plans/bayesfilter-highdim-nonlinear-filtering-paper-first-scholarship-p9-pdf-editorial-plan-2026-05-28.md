# P9 PDF Integration And Academic Editorial Pass Plan

## Objective

Integrate the rewritten chapters into the monograph PDF and perform an
academic-style editorial pass focused on readability, references, equation
continuity, table layout, and removal of internal-audit clutter from the main
flow.

## Inputs

- Accepted P2-P8 chapter rewrites.
- `docs/main.tex`.
- `docs/references.bib`.
- `docs/source_map.yml`.

## Execution Precondition

Execution is forbidden unless P2-P8 have accepted result notes and a
post-edit source-backed chapter audit confirms that copyediting has not
introduced unsupported claims, removed assumptions, or weakened derivations.

## Work

1. Ensure `ch33`--`ch37` are included in `docs/main.tex`.
2. Build `docs/main.pdf`.
3. Check undefined citations and references.
4. Use `pdftotext` to confirm chapter titles and key section titles.
5. Review rendered page ranges for layout, table readability, equation
   continuity, orphan claims, and academic voice.
6. Move remaining audit-heavy material into compact implementation-boundary
   notes or result notes.
7. Re-run a post-edit source-backed audit after layout/copyediting and before
   page review.

## Outputs

- Updated `docs/main.pdf`.
- P9 result note.

## Stop Conditions

- Stop if LaTeX does not build.
- Stop if references or citations are unresolved in the new block.
- Stop if rendered pages are unreadable or contain internal-audit clutter.

## Verification

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
- `pdftotext docs/main.pdf - | rg "<rewritten chapter titles>"`
- `rg -n "undefined|Citation.*undefined|Reference.*undefined" docs/main.log`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- the five active chapter files only for accepted editorial repairs;
- `docs/main.tex`
- `docs/main.pdf`
- `docs/references.bib` only for checked sources consumed by the rewritten block;
- `docs/source_map.yml` only for provenance updates.

## What Must Not Be Concluded

P9 validates document integration only, not scientific correctness.
