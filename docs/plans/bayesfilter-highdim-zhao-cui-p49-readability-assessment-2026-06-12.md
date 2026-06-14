# P49 Readability Assessment

**Target:** `docs/plans/bayesfilter-highdim-zhao-cui-p49-voice-and-emphasis-rewrite-2026-06-12.tex`

Reading p49 as a mathematically literate academic from a neighboring field, I
would say the document is now clearly stronger than p48, but it still does not
fully read like a settled monograph chapter.  The most important difference is
that the opening voice is better and the note now announces more clearly what it
is trying to define.  However, the later chapters still carry too much of the
internal-note voice of the original p30 material.

## What improved in p49

1. **The opening now sounds like a chapter opening rather than an object ledger.**
   The earlier p48 opening began too quickly with the five-object inventory.
   P49 instead foregrounds the scientific problem, the chosen computational
   object, and the purpose of the note before introducing later technical layers.
   This is a real improvement.

2. **The note now states more clearly what the reader should care about.**
   The new opening tells the reader that the central issue is the identity of the
   mathematical object being carried, normalized, differentiated, and validated.
   That gives the chapter a stronger center.

3. **The fixed-branch likelihood chapter now better signals why the implementation
   material matters.**
   The reframing around runtime object identity, scalar-changing choices, and
   hidden implementation fragility makes the implementation material easier to
   justify intellectually.

4. **The conclusion reads more like synthesis and less like another restart.**
   This helps the chapter close more naturally.

## What still feels weak

### 1. The “Running Example And Notation” chapter still carries too much reference and notation burden
The chapter remains useful, but it still feels partly like notation-plus-background
rather than like a live narrative chapter.  The threaded example is helpful, yet
it competes with a large amount of literature and symbol setup.  A neighboring-
field reader still has to work hard to tell what is indispensable immediately and
what could have arrived later.

### 2. The TT toolkit chapter is still somewhat too broad in purpose
The TT chapter teaches several good things at once:
- what TT form is,
- how split ranks work,
- why moderate rank may be plausible,
- how the worked exponential example functions,
- and why marginalization is cheap.
All of that is valuable, but the chapter still lacks a completely sharp single
payoff.  It reads more like a toolkit dossier than a chapter with one decisive
question.

### 3. The coordinate / KR / preconditioning chapter is still rhetorically heavy
The material is mathematically coherent, but it is still a long technical tunnel.
A reader can see why the chapter exists, but it remains hard to sustain momentum
through it.  It still feels like several transform-oriented subchapters compressed
into one.

### 4. The fixed-branch likelihood chapter is improved, but still somewhat ledger-like
The chapter now tells the reader why the implementation details matter, which is
an important improvement.  But many subsections still unfold as inventories of
stored objects, array shapes, and branch components.  A reader can follow them,
but they do not yet always feel driven by one dominant mathematical tension.

### 5. The derivative chapter is better motivated, but still oversized
The derivative chapter remains long and internally multi-track: motivation,
warmups, forward pass, teaching layer, derivative pass, propositions, and
checklists all remain.  The grouping is better than in p30, but it still reads
as a carefully assembled derivative notebook rather than as one calm chapter arc.

## Main diagnosis

P49 is now strong enough that the remaining weakness is no longer global
structure.  The remaining weakness is **chapter interior discipline**.

That means:
- each major chapter still has slightly too many local goals,
- internal subsections still sometimes compete with each other,
- and the note still retains too much of the voice of an internal technical
  dossier even when the chapter order is now much better.

## Recommendation

The next pass should not do another large reordering.  It should instead target:
1. chapter-level singularity of purpose,
2. lighter notation burden in the early running-example chapter,
3. a more sharply focused TT toolkit chapter,
4. a more selective treatment of implementation substructure,
5. and a smaller, more integrated derivative chapter.

In short: p49 is closer to a true monograph chapter than p48, but it still needs
one more pass that rewrites **within chapters**, not between chapters.
