# Neural OT teaching-note pedagogical deepening plan

Date: 2026-06-24

metadata_date: 2026-06-24

## Context

The current teaching note already exists at:
- `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex`
- compiled PDF: `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.pdf`

The note has already moved beyond a short survey and now has a solid chaptered
skeleton, stronger notation discipline, and substantially better equation
coverage.  However, the current state still does **not** meet the intended user
standard.

The standard for the next pass is explicit:
1. the note should read like lecture notes for first-year PhD students,
   especially engineering students with weak real-analysis or PDE background;
2. for the core papers, the note should be detailed enough that a strong Claude
   session could implement a first-pass algorithm from the note without
   reopening the original paper;
3. the note should close expository gaps in the original papers rather than only
   summarize them.

This plan is for the next document pass only.  It does **not** broaden the
paper shelf, reopen the recent-candidate ranking, or change BayesFilter’s
scientific priorities.

## Question

What exact rewrite sequence should bring the current neural-OT teaching note
from “substantially improved but still too dense” to “pedagogically usable and
implementation-bearing” for the current seminar goal?

## Scope

### In scope
- Full pedagogical audit of the current `.tex` note.
- Explicit triage of which sections still fail the first-year-PhD /
  implementation-bearing bar.
- Targeted deepening of the weakest sections while preserving the current
  chapter structure.
- More prerequisite explanation where PDE, function-space, or theorem-heavy
  material currently moves too fast.
- Stronger theorem-to-algorithm bridges where the current note states claims but
  does not yet carry the reader into executable steps.
- Recompile and verify the PDF after revisions.

### Out of scope
- Adding new papers to the shelf.
- Re-running the full ranking/reread pipeline from the 2026-06-22 note unless a
  section is found to rely on an unchecked claim.
- Replacing Part II frontier material with an appendix.
- Cosmetic-only changes as the primary fix.
- New BayesFilter code implementation work.

## Evidence Contract

### Document-design question
Can the current note be revised so that the weakest sections match the standard
already approached by the strongest Wang and Al-Jarrah sections?

### Exact baseline
The baseline is the current note source:
- `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex`

The comparison standard is the current user-approved direction recorded in:
- `docs/plans/neural-ot-teaching-note-reset-memo-2026-06-24.md`

### Primary promotion criterion
The revision pass succeeds only if the revised note:
1. preserves the current coverage and Part I / Part II structure,
2. reduces pedagogical density in the weakest sections,
3. makes the learned object / objective / practical optimization loop explicit
   for each core method,
4. makes frontier sections legible enough that a strong first-year PhD student
   can understand what problem is being solved and why the machinery is needed,
5. and compiles successfully.

### Veto diagnostics
- Sections still require the reader to infer what object is learned.
- Sections still state objectives without explaining where they come from.
- Sections still jump from theorem statements to implementation claims without an
  intermediate bridge.
- A core-method section still fails the “Claude could implement a first pass from
  the note alone” test.
- Revisions compile poorly or introduce broken references.

### Explanatory-only diagnostics
- Raw page count increase.
- Number of added displayed equations by itself.
- Added summary boxes or formatting devices by themselves.
- Apparent completeness of paper coverage by itself.

### What will not be concluded even if this pass succeeds
- That the represented methods are scientifically validated for BayesFilter.
- That frontier papers are now easy in an absolute sense.
- That every theorem-heavy paper can be made implementation-ready without any
  source rereading.
- That the note has become a substitute for all primary-source consultation in
  future research decisions.

### Artifact
- Plan: `docs/plans/neural-ot-teaching-note-pedagogical-deepening-plan-2026-06-24.md`
- Main deliverable to revise:
  `docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex`
- Supporting handoff reference:
  `docs/plans/neural-ot-teaching-note-reset-memo-2026-06-24.md`

## Skeptical Audit Before Execution

Status: `PASSED_WITH_GUARDS`

Main risks and guards:
1. **Wrong job definition** — guard by treating this as pedagogical deepening,
   not literature expansion.
2. **Cosmetic fixes mistaken for substantive improvement** — guard by requiring
   explicit theorem-to-algorithm and object/objective/optimization explanations,
   not just better formatting.
3. **Strong sections over-rewritten while weak sections remain weak** — guard by
   auditing the full note first and prioritizing the weakest sections.
4. **Frontier material demoted implicitly by compression** — guard by preserving
   Part II and adding scaffolding rather than exile to an appendix.
5. **Implementation-bar overclaim** — guard by using an explicit section-level
   test: could a strong Claude session implement a first pass from the note
   alone?
6. **Unverified mathematical claims** — guard by rereading local note text before
   revision and checking primary-source support where a section appears to rest
   on a claim not yet justified in the note.

## Current hypotheses about the weakest areas

These are working hypotheses from the reset memo and section map, not final
findings.  The first audit pass must confirm or revise them.

Likely weak areas:
- `Hosseini, Hsu, and Taghvaei (2025)` section:
  function-space / conditional-law bridge may still be too compressed.
- `Advanced directions and compressed shelf` chapter:
  frontier material likely still moves too quickly for the target audience.
- theorem-heavy bridges in the conditional transport chapter:
  some sections may still state the mathematics more cleanly than they explain
  the practical algorithm.
- any section where implementation loops are less explicit than in the Wang and
  Al-Jarrah chapters.

Likely stronger anchors to preserve and imitate:
- `Wang et al. (2025)` section.
- `Al-Jarrah et al. (2025)` section.
- primer examples when they are already carrying the intended intuition.

## Work sequence

### Step 1 — full pedagogical audit of the current note
Read the current `.tex` note in full and score each major section against the
seminar standard.

For each core or frontier section, answer explicitly:
1. What object is learned?
2. Why does the objective take this form?
3. What is optimized in practice?
4. What is done at deployment/inference time?
5. Could a strong first-year PhD student explain the section back?
6. Could Claude implement a first pass from the note alone?

Produce a triage table with labels such as:
- `strong_enough_as_is`
- `needs_pedagogical_scaffolding`
- `needs_algorithmic_bridge`
- `needs_both`

### Step 2 — identify the minimum necessary rewrite set
Select only the sections that materially fail the standard.

Priority rule:
1. first repair remaining core-anchor gaps in `Makkuva`, `Hosseini`, and `UNOT`,
   because those sections still carry the implementation-bearing burden;
2. then repair shorter comparison sections that remain inside the core narrative,
   such as `Bunne`, when they currently interrupt the teaching flow;
3. then repair compressed Part II shelf sections by adding the minimum scaffolding
   needed for legibility;
4. then do local structural cleanup when it removes confusion without broadening
   scope.

Do **not** broaden scope by rewriting already-strong sections unless a local
consistency or structural fix requires it.

### Step 3 — deepen weak sections using a role-appropriate rewrite pattern
For core-anchor sections that are supposed to be implementation-bearing (for this
pass: `Makkuva`, `Hosseini`, `UNOT`), rewrite toward the full pattern:
1. one plain-language paragraph naming the mathematical problem,
2. one paragraph naming the learned object,
3. one derivation or structured explanation of the objective,
4. one theorem-to-algorithm bridge,
5. one explicit training loop,
6. one explicit deployment/inference loop,
7. one BayesFilter-fit paragraph explaining what transfers and what does not.

For shorter comparison or frontier-shelf sections, use a lighter pattern instead:
1. name the object class,
2. state the new mathematical or computational burden,
3. say what the section teaches the student,
4. state explicitly whether the section is implementation-bearing or only a
   comparison marker,
5. explain BayesFilter relevance without pretending the section is a full
   algorithm manual.

When prerequisite ideas are heavy (PDE, function spaces, continuity equation,
conditional laws), insert a slower local staircase before returning to the full
notation.

### Step 4 — make frontier chapters readable without demoting them
Preserve Part II as frontier/research-direction material, but add scaffolding:
- remind the reader what object class each paper belongs to,
- say what mathematical burden is new relative to earlier chapters,
- separate “what the paper proves/claims” from “what would still be needed for a
  BayesFilter implementation,”
- explain why the frontier section is still in the seminar.

### Step 5 — tighten cross-chapter consistency
After local rewrites, do one pass for:
- notation consistency,
- repeated definitions of learned objects,
- consistent use of training/deployment terminology,
- avoiding contradictions between primer, core-method chapters, and frontier
  summary chapters.

### Step 6 — compile and verify
Rebuild the PDF and check for:
- successful compilation,
- no broken references,
- no accidental sectioning damage,
- no newly introduced notation gaps visible in the compiled output.

## Section-level acceptance test

A revised section passes only if all of the following are true:
- it states the learned object unambiguously;
- it explains why the objective has the stated form;
- it says what is optimized in practice;
- it distinguishes theorem / approximation / implementation burden;
- it includes enough algorithmic detail for a strong Claude session to sketch a
  first implementation;
- it is slower and more legible than the current version for the target student.

## Deliverable structure to preserve

Keep the current broad structure:
- primer,
- static-map / OT-ICNN cautionary chapter,
- conditional posterior transport chapter,
- retained-teacher acceleration chapter,
- advanced/frontier chapter,
- final synthesis chapter.

Do not collapse frontier sections into footnotes or appendices merely to improve
surface readability.

Structural cleanup is allowed when it removes a genuine pedagogical defect without
changing the broad chapter architecture.  In particular, duplicated recap sections,
misplaced summaries, or local ordering glitches may be repaired if the audit shows
that they break lecture-note flow.

## Planned commands

Audit / heading checks as needed:
```bash
cd /home/chakwong/BayesFilter
rg -n '^\\(chapter|section|subsection)\{' docs/plans/bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex
```

Compile verification:
```bash
cd /home/chakwong/BayesFilter/docs/plans
latexmk -pdf -interaction=nonstopmode -halt-on-error bayesfilter-neural-ot-recent-candidate-comparison-note-2026-06-22.tex
```

If parse artifacts are needed again:
```bash
cd /home/chakwong/research-assistant
scripts/ra-dev parse-pdf --pdf <paper.pdf>
```

## Success criterion for this pass

This pass is successful if it ends with:
1. a written audit of which sections are weak and why,
2. targeted rewrites of only those sections,
3. clearer theorem-to-algorithm bridges in the remaining weak chapters,
4. stronger implementation-bearing exposition for the core methods,
5. a more teachable frontier chapter without demoting it,
6. and a successfully compiled PDF.

## What would change the next step

- If the audit shows that only a few sections remain weak, proceed directly to
  targeted rewriting.
- If the audit shows that the current organization itself causes the density,
  revise local ordering inside chapters while preserving the global Part I / Part
  II structure.
- If a section cannot be repaired without checking a primary-source derivation,
  pause and do the smallest focused source reread needed for that section only.
- If compilation or local consistency regress after the rewrite, fix those before
  any further expansion.

## What is not being changed by this plan

This plan does not change the shortlist of neural-OT families, does not declare
any method BayesFilter-ready by exposition alone, and does not replace the need
for later research or implementation artifacts.  It only defines the explicit
rewrite program for bringing the current teaching note up to the intended
pedagogical and implementation-bearing standard.
