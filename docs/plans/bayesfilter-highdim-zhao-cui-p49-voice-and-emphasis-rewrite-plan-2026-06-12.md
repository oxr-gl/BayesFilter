# P49 Rewrite Plan: Opening Voice, Chapter Focus, And Implementation-Interest Emphasis

**Date:** 2026-06-12  
**Base text:** `docs/plans/bayesfilter-highdim-zhao-cui-p48-monograph-reorganized-note-2026-06-12.tex`  
**Target:** `docs/plans/bayesfilter-highdim-zhao-cui-p49-voice-and-emphasis-rewrite-plan-2026-06-12.md`

## Context

P48 is a clear structural improvement over p30.  The major chapter blocks are now
visible, the derivative material has a clearer home, and the validation protocol
feels more like a culminating chapter.  However, the current document still reads
more like a carefully reorganized research dossier than like a chapter fully
written in one settled monograph voice.

The remaining problems are now mainly rhetorical:
- the opening begins too much like a technical object ledger,
- the TT toolkit chapter still tries to teach several coequal things at once,
- the coordinate/transport/preconditioning chapter remains intellectually coherent
  but rhetorically overloaded,
- the fixed-branch likelihood chapter is organized but still too inventory-heavy,
- and the implementation detail is not yet consistently staged around what is
  mathematically interesting or easy to get wrong.

The next rewrite should therefore not perform another large structural shuffle.
It should instead rewrite p48 for:
1. stronger opening voice,
2. sharper dominant question per chapter,
3. better implementation-interest emphasis,
4. and more selective scaffolding.

## Rewrite objective

Produce a new p49 Zhao--Cui note that keeps the chapter order of p48 but rewrites
its prose so that the document reads less like a reorganized notebook and more
like a chapter written from the beginning with one narrative voice.

The goal is not to reduce substance.  The goal is to improve:
- what the reader is told to care about,
- what the chapter says is difficult,
- and why each implementation detail matters mathematically.

## Main rewrite principles

### 1. Rewrite the opening chapter, not just the order
The opening must stop beginning with object inventory.  A monograph opening should
first establish:
- the scientific problem,
- the computational object chosen,
- and why that choice matters.

The “five objects” material is useful, but it should not be the first thing the
reader encounters.  It should become a later orientation device or a supporting
subsection after the opening question is fixed.

### 2. Each chapter must have one dominant question
The current chapters are improved structurally, but several still have more than
one center of gravity.  In p49, each chapter should answer one dominant question,
and the prose should constantly reinforce that question.

### 3. Do not remove implementation detail; make it narratively meaningful
Implementation prose should not read as an inventory dump.  It should tell the
reader:
- what is the runtime object,
- what decisions silently change the scalar,
- what is subtle or easy to get wrong,
- why the pseudocode is mathematically interesting.

### 4. Reduce generic scaffolding
Repeated signals like:
- “mathematical question,”
- “implementation meaning,”
- “the next step is,”
- “this section answers…”
should be used only when truly needed.

The chapter should increasingly trust its own structure to guide the reader.

## Chapter-by-chapter rewrite plan

## Chapter 1. Orientation And Scope
**Current problem:** the chapter opens with the “five objects” frame, which is too
technical and inventory-like for a monograph opening.

**Rewrite goal:** begin with the scientific problem and why this approximation
object is worth studying.

**Planned changes:**
- Replace the current first movement with an opening paragraph centered on the
  filtering problem and the chosen object.
- Move or compress the “five objects” inventory so it becomes a later orientation
  device rather than the first rhetorical move.
- Keep the object list, but let it appear after the reader knows why those objects
  matter.
- End the opening with a short statement of what the chapter sequence will do.

**Desired effect:** the reader should first feel the purpose of the note, then be
introduced to the objects.

## Chapter 2. Running Example And Notation
**Current problem:** this chapter still behaves partly like notation-plus-background
instead of like a live example chapter.

**Rewrite goal:** make the threaded nonlinear example the true center, with
notation introduced only insofar as it serves that example and the later
construction.

**Planned changes:**
- Keep the threaded nonlinear example prominent.
- Trim literature and notation commentary that is not needed immediately.
- Use the example to motivate the need for adjacent-state targets, retained
  filters, and transformed coordinates.
- Avoid letting notation accumulate independently of a concrete inferential task.

**Desired effect:** the reader should feel they are following a live object, not a
notation registry.

## Chapter 3. Exact Filtering Target And Recursive Bottleneck
**Current problem:** the problem statement is clearer than before, but some
explanatory prose still feels like it is restarting rather than intensifying the
argument.

**Rewrite goal:** show the exact bottleneck once, cleanly, and let that bottleneck
justify the TT approximation family.

**Planned changes:**
- Keep the exact filtering target, the state-space model, the marginal learning
  problems, and the recursive bottleneck.
- Tighten repeated phrases that restate “the exact recursion is hard.”
- Make the chapter end with one strong bridge sentence to the TT toolkit:
  because the exact object is inaccessible, the note now turns to the approximation
  family that will replace it.

## Chapter 4. Tensor-Train Approximation Toolkit
**Current problem:** the chapter is rich, but its purpose is still too broad.

**Rewrite goal:** make the chapter answer one central question:
> what kind of separable approximation family is powerful enough to replace the
> full tensor object, and why can its rank remain manageable?

**Planned changes:**
- Keep the TT definition and rank explanation.
- Keep the worked three-variable exponential example as the pedagogical payoff.
- Keep the rank-plausibility material, but frame it as the consequence of the TT
  construction rather than as a parallel chapter goal.
- Keep TT marginalization material, but explicitly connect it back to why filtering
  needs it.

**Desired effect:** the reader should finish the chapter knowing what a TT is,
what rank means, and why TT makes filtering plausible without feeling that the
chapter was also trying to do four other things equally.

## Chapter 5. Coordinate Systems, Conditional Maps, And Preconditioning
**Current problem:** mathematically coherent, rhetorically overloaded.

**Rewrite goal:** make the chapter answer:
> why do we need multiple coordinate systems, and how do those coordinate systems
> support the filtering construction?

**Planned changes:**
- Lead with one paragraph explaining why the same target appears in different
  coordinates.
- Explain physical, reference, preconditioned, and retained coordinates as a
  staged necessity rather than as a list.
- Keep KR maps and preconditioning, but make explicit what problem each one solves.
- Add stronger transitions between density transformation, conditional-map logic,
  and preconditioning.

**Desired effect:** the reader should feel that the coordinate chapter is solving
one conceptual problem, not presenting several detached transform technologies.

## Chapter 6. Squared-TT Filtering Object And Operational Recursion
**Current problem:** stronger than before, but still partly reads like algorithmic
annotation plus object explanation plus nonnegativity justification all competing
for center stage.

**Rewrite goal:** make the chapter answer:
> what is the actual nonnegative approximate filtering object, and how is it
> propagated through one filtering step?

**Planned changes:**
- Keep the squared-TT motivation and nonnegativity repair.
- Keep the normalizer and marginalization material.
- Keep Algorithms 1 and 2, but make clear which one advances the filtering object
  and which one supplies conditional-map structure.
- Tighten chapter transitions so the algorithms feel like necessary culminations
  rather than inserted source reconstructions.

## Chapter 7. Fixed-Branch Likelihood Construction
**Current problem:** the material is important, but it still feels like stored-field
and array-shape inventory more than a chapter with intellectual tension.

**Rewrite goal:** make the chapter answer:
> once the adaptive filtering object exists, what exactly must be frozen in order
> to define a deterministic scalar that can later be differentiated?

**Planned changes:**
- Keep the paper-vs-fixed-branch reconciliation section.
- Keep object and array-shape material, but reorder it under three internal
  subquestions:
  1. what the fixed-branch object is,
  2. what must be saved,
  3. what choices change the scalar.
- Make each implementation detail answer one of those subquestions.
- Keep pseudocode and branch instantiation, but only after those stakes are clear.

**Desired effect:** the implementation detail should feel mathematically charged,
not merely archival.

## Chapter 8. Fixed-Branch Derivative Theory
**Current problem:** much improved, but still oversized and internally multi-track.

**Rewrite goal:** make the chapter answer:
> what exactly is differentiated, and why does the fixed-branch condition make that
> derivative meaningful?

**Planned changes:**
- Keep the warmups, but reduce any local restarts that re-explain the same branch
  idea.
- Keep the fixed-branch distinction, but make each return to it deepen the idea:
  - first: structural meaning,
  - then: derivative chain meaning,
  - then: finite-difference consequence.
- Keep propositions and derivative pass, but improve transitions so the warmups feel
  cumulative rather than like separate lectures.

## Chapter 9. Validation And Diagnostics
**Current problem:** better than p30, but still somewhat protocol-heavy.

**Rewrite goal:** make validation answer:
> what evidence would persuade us that the declared approximate scalar and its
> derivative are both credible, and what evidence would show their limits?

**Planned changes:**
- Preserve the benchmark suite and test protocol.
- Reframe the chapter by evidence type rather than by list accumulation:
  1. exact-reference checks,
  2. derivative correctness,
  3. approximation-scope tests,
  4. large-scale regime diagnostics.
- Keep the benchmark details, but make the reader know why each benchmark is there.

## Chapter 10. Positioning, Limits, And Relation To Zhao--Cui
**Current problem:** better placed, but can still sound like it is re-opening the
case rather than closing it.

**Rewrite goal:** let this final chapter synthesize rather than restart.

**Planned changes:**
- Keep the Zhao--Cui relation section.
- Keep the bounded-limit language.
- Remove repeated explanations of core mechanics.
- State only:
  - what object has been defined,
  - why it is useful,
  - where its scientific and mathematical boundaries lie,
  - and how it relates to Zhao--Cui’s original adaptive formulation.

## Material to preserve explicitly from p48

These are strengths and should not be casually cut:
- the threaded nonlinear example,
- the worked TT exponential example,
- the rank-plausibility material,
- the coordinate-system explanations,
- the fixed-branch reconciliation,
- the derivative warmups,
- the benchmark suite,
- the large-scale protocol.

## Material to reduce or rewrite, not necessarily delete

- opening object-ledger prose,
- generic “mathematical question” scaffolding,
- repeated local restarts,
- inventory-style paragraphs that do not say why the detail matters,
- explanation blocks that list implementation facts without identifying the
  interesting fragility.

## Verification plan for p49

1. Create p49 from p48.
2. Rewrite the opening voice so the chapter begins with the problem and object,
   not with an object ledger.
3. Rewrite the fixed-branch likelihood and implementation-facing sections so the
   reader is told what matters and why.
4. Tighten chapter purposes without removing the valuable substance.
5. Compile p49 with `latexmk -pdf` and run BibTeX as needed.
6. Repair any references and citations introduced by the rewrite.
7. Read the new p49 front half and ask:
   - does the opening now feel authored rather than technical-ledger-driven?
   - does each chapter answer one clear question?
   - do implementation details now feel motivated and interesting?
8. Read the derivative and validation chapters and ask:
   - do they now feel cumulative rather than assembled?
   - does the ending synthesize rather than restart?

## Proposed output file

`docs/plans/bayesfilter-highdim-zhao-cui-p49-voice-and-emphasis-rewrite-2026-06-12.tex`
