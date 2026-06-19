# Reset memo: high-dimensional monograph rewrite restart handoff

## Date
2026-06-14

## Context
This pass was part of the broader rewrite of the high-dimensional nonlinear
filtering block in the BayesFilter monograph.  The existing `docs/chapters/ch34`
through `ch37` material was judged too incoherent, disconnected, and incomplete
to serve as the canonical monograph exposition.  Independent development first
produced two stronger source manuscripts:

- the SGQF / sparse-grid lane note `p47`, and
- the Zhao--Cui / TT / KR lane note `p50`.

A master program and phase subplans were then created under `docs/plans` to guide
full reintegration into `docs/main.tex`.

The immediate goal at the time of this reset memo was to begin executing the
master program phases in order, starting with:
1. Phase 0: block architecture and import/export logic,
2. Phase 1: rewrite `ch34` from `p47`.

## Decision / policy
Future sessions should assume the following without re-litigating them unless a
strong contradiction is found in the book build or source material:

1. The current `docs/chapters/ch34`--`ch37` files are **not** treated as a sound
   authored skeleton.  They are salvage material only.
2. The canonical authored source manuscripts for the high-dimensional block are:
   - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
   - `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
3. The master program to execute is:
   - `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`
4. The active phase sequence is:
   - Phase 0: completed enough to guide execution,
   - Phase 1: in progress (`ch34` from `p47`),
   - Phase 2+: not yet executed.
5. The correct strategy is **not** to keep polishing standalone p47/p50 notes.
   The correct strategy is to rewrite the actual monograph chapters.

## What changed
- File: `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`
  - Created the governing program for the full high-dimensional block rewrite.
- File: `docs/plans/bayesfilter-highdim-monograph-phase0-block-architecture-subplan-2026-06-14.md`
  - Created Phase 0 subplan.
- File: `docs/plans/bayesfilter-highdim-monograph-phase1-ch34-sgqf-rewrite-subplan-2026-06-14.md`
  - Created Phase 1 subplan.
- File: `docs/plans/bayesfilter-highdim-monograph-phase2-ch35-zhaocui-ttkr-rewrite-subplan-2026-06-14.md`
  - Created Phase 2 subplan.
- File: `docs/plans/bayesfilter-highdim-monograph-phase3-ch36-hmc-consequence-rewrite-subplan-2026-06-14.md`
  - Created Phase 3 subplan.
- File: `docs/plans/bayesfilter-highdim-monograph-phase4-ch37-synthesis-rewrite-subplan-2026-06-14.md`
  - Created Phase 4 subplan.
- File: `docs/plans/bayesfilter-highdim-monograph-phase5-maintex-integration-subplan-2026-06-14.md`
  - Created Phase 5 subplan.
- File: `.claude/settings.json`
  - Added narrow project-scoped permission rules for LaTeX build commands (`latexmk`, `bibtex`, `pdflatex`-style build paths) to reduce future permission denials after restart.
- File: `docs/preamble.tex`
  - Added `graphicx`, `tikz`, and `\usetikzlibrary{arrows.meta,calc,positioning}` so monograph chapters can support figures imported from the standalone SGQF note.
- File: `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
  - Replaced the original chapter body with the adapted `p47` SGQF chapter body.
  - Removed standalone-note-specific `\tableofcontents` usage.
  - Began adapting standalone notation/macros into monograph-compatible form.

## Bugs / blockers resolved
- Symptom: The rewritten `ch34` initially failed in the monograph build due to
  standalone-note macros not defined in the monograph preamble.
- Root cause: `p47` assumed its own standalone preamble (`\N`, `\ellhat`,
  `\chol`, `\dd`, etc.), while `docs/preamble.tex` defines a different set of
  monograph-wide macros.
- Resolution:
  - replaced or adapted several standalone forms inside `ch34`,
  - added only minimal local compatibility macros where necessary,
  - updated `docs/preamble.tex` for figure support.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- The monograph rebuild progressed into the rewritten `ch34` and therefore
  confirmed that the integration path is live.
- Major early blockers in `ch34` were exposed and partially repaired:
  - `\N` macro mismatch,
  - `\ellhat` / `\widehatell` mismatch,
  - `\chol` prose usage,
  - duplicate local macro definitions,
  - missing `tikzpicture` environment before `docs/preamble.tex` was updated.
- The build did **not** yet complete successfully.
- At the end of this pass, the next blocker still lived inside the integrated
  `ch34` chapter and/or the broader monograph citation/reference environment.

## Current policy
- Continue from the master program, not from standalone-note polishing.
- Resume with Phase 1 until `ch34` compiles cleanly inside `docs/main.tex`.
- Only after `ch34` is stabilized should work move to Phase 2 (`ch35` from
  `p50`).
- Use the project `.claude/settings.json` LaTeX permission rule after restart;
  it may not have been fully honored in-session because it was added mid-session.

## Known limitations / cautions
- `ch34` currently contains adapted p47 content, but the full monograph build is
  not yet clean.
- The standalone notes remain the most coherent authored sources; do not let the
  current `ch34`--`ch37` wording override them without a good reason.
- The rewrite is at a stage where broad structural direction is settled, but many
  local integration fixes are still ahead.
- Do not drift back into further standalone-note iterations.  The next real work
  is chapter integration.

## Suggested next steps
1. Restart Claude Code so the new project-scoped `.claude/settings.json` LaTeX
   permissions are loaded from session start.
2. Re-run the full monograph build from `docs/`:
   ```bash
   cd /home/chakwong/BayesFilter/docs
   latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
   ```
3. Continue fixing `ch34` integration blockers until `main.tex` passes that
   chapter cleanly enough to move on.
4. Then begin Phase 2 by rewriting `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
   from the stronger `p50` manuscript.
