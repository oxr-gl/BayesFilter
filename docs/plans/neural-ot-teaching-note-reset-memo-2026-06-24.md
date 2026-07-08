# Reset memo: neural OT teaching-note rewrite handoff

## Date
2026-06-24

## Context
This memo is for a fresh agent resuming work on the standalone teaching note:

- `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex`
- compiled PDF: `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.pdf`

The work has already moved far beyond a short survey note.  The current document
has chapters, consistent notation, much better equation coverage, and deeper
reconstructions of several key papers.  However, the user correctly judged that
it still does **not** fully meet the intended standard.

The target standard is now explicit:
- this should read like **lecture notes for first-year PhD students**, especially
  engineering students without strong real-analysis or PDE background;
- for the core papers, the note should be detailed enough that **a strong Claude
  session could implement the algorithm from the note without reopening the
  original paper**;
- the document should **plug the expository gaps in the original papers**, not just
  summarize them.

A clean handoff is useful now because the conversation context became large and the
thread started to drift.

## Current deliverable state
Primary file:
- `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex`

Current document structure:
- primer chapter,
- OT-ICNN / Makkuva chapter,
- conditional posterior transport chapter,
- retained-teacher acceleration chapter,
- advanced directions / frontier chapter,
- final synthesis chapter.

The PDF currently compiles successfully.

## What has already been improved
Compared with the early survey version, the note now has:
- chaptered structure,
- much more consistent notation,
- many more retained displayed equations,
- stronger derivational explanations,
- a clearer distinction among learned objects:
  - retained teacher,
  - direct map,
  - conditional posterior map,
  - dynamic path,
  - measure operator,
- a primer with a weighted-particle example and a conditional Gaussian toy model.

Core-paper improvements already made:
- **Makkuva / OT-ICNN**:
  - better Brenier / convex-potential explanation,
  - explicit correction that BayesFilter did not faithfully reproduce the paper.
- **Wang (2025)**:
  - strongest current chapter,
  - has block-triangular derivation,
  - change-of-variables to NLL derivation,
  - dynamic/control interpretation,
  - implementation-style training/deployment loops.
- **Al-Jarrah (2025)**:
  - much stronger conditional-law explanation,
  - max--min interpretation,
  - implementation-style training/deployment loops.
- **Hosseini (2025)**:
  - much better finite-dimensional bridge to function-space conditional OT,
  - theorem-vs-approximation distinction clearer,
  - implementation route outlined.
- **Meta OT / UNOT**:
  - now treated as retained-teacher implementation routes rather than loose survey
    items,
  - have input/objective/training/deployment descriptions.
- **GeONet (2024)**:
  - improved conceptual staircase from Benamou--Brenier objective to continuity
    equation, Lagrangian, KKT system, and operator-learning residuals,
  - implementation-style training/deployment outline added.

## What is still wrong
The user and students still find the note too dense.  The remaining weakness is
**not** mainly missing equations.  It is that too many sections still move too
quickly for first-year students.

Main remaining issues:
1. **Pedagogical density is still too high.**
   The note often asks the reader to decode notation, follow derivations, and infer
   implementation details all at once.

2. **Some chapters still do not fully meet the “Claude could implement this” bar.**
   Wang and Al-Jarrah are the closest.  Other chapters are improved but still not
   equally implementation-bearing.

3. **Frontier material is still hard to digest.**
   We deliberately kept frontier papers in the main document rather than an
   appendix, because the seminar is supposed to expose students to open research
   directions.  That was the right call, but those chapters still need more
   scaffolding.

4. **The note is still trying to do many jobs at once.**
   It is a comparison, a reconstruction, a teaching note, and an implementation
   manual.  The remaining work is to make those layers feel organized rather than
   compressed together.

## Important user decisions that should not be re-litigated
These were established explicitly in the conversation and should be preserved:

- The note should **not** demote frontier papers such as Hosseini, GeONet,
  Chen--Liu, neighboring direct-map variants, and boundary papers to a mere
  appendix.  They are part of the seminar because the frontier itself matters.
- Part II should be treated as **frontier and research-direction material**, not as
  “unimportant leftovers.”
- The user prefers **slower mathematics with more background**, because many
  engineering students have weak formal preparation in real analysis and PDE.
- The right standard is not “readable survey.”  It is “lecture note that could
  guide implementation.”
- Tiny add-ons like takeaway boxes are not the main fix.  The real fix is to
  **close mathematical and algorithmic gaps**.

## Temporary parse artifacts
The note has repeatedly relied on research-assistant parse outputs under:
- `/tmp/ra_neural_ot_parses/`

These files are temporary.  A fresh agent should verify they still exist.
If they are missing, rerun the parse pipeline on the local shelf:
- source PDFs are under `/.localsource/neural_operator2/`
- prior commands used `~/research-assistant/scripts/ra-dev parse-pdf --pdf <paper>`

If the parse directory is gone, regenerating it is justified before further note
work.

## Recommended next step for a fresh agent
Do **not** broaden the shelf or add more papers.

Instead, perform a targeted pedagogical audit of the current note and then rewrite
only the weakest remaining sections with the same standard already applied to Wang
and Al-Jarrah.

Concretely, a fresh agent should:
1. read the current `.tex` note in full,
2. identify which sections still fail the standard:
   - first-year PhD teaching note,
   - implementation-bearing for core methods,
3. keep Part I / Part II structure,
4. deepen the weakest remaining sections rather than expanding coverage,
5. recompile and verify.

Most likely remaining weak areas:
- frontier chapter pacing,
- theorem-to-algorithm bridges,
- explicit implementation steps in the still weaker core sections,
- prerequisite explanations for PDE- or function-space-heavy material.

## Suggested working rule for the next agent
For each core or frontier paper section, ask:
- Could a strong first-year PhD student explain what object is learned?
- Could they explain why the objective has that form?
- Could they say what is optimized in practice?
- Could Claude implement a first pass of the algorithm from the note alone?

If any answer is “no,” the section still needs work.

## Verification already passing
Current note compiles successfully with:
```bash
cd /home/chakwong/BayesFilter/docs/plans
latexmk -pdf -interaction=nonstopmode -halt-on-error bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex
```

## Bottom line
The note is substantially improved and now has a solid skeleton.  The next agent
should treat this as a **pedagogical deepening and implementation-readiness pass**,
not as a literature-expansion pass.
