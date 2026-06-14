# P50 Rewrite Plan: Chapter Interior Discipline And Selective Emphasis

**Date:** 2026-06-12  
**Base text:** `docs/plans/bayesfilter-highdim-zhao-cui-p49-voice-and-emphasis-rewrite-2026-06-12.tex`  
**Target:** `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

## Context

P49 is better than p48 in two important ways: the opening has a clearer chapter
voice, and the fixed-branch likelihood chapter better signals why its
implementation details matter.  However, the note still does not yet feel like a
fully settled monograph chapter.  The remaining problem is no longer large-scale
structure.  The remaining problem is **chapter interior discipline**.

The current version still has several chapters that try to do too many things at
once:
- the opening still becomes technical too quickly,
- the running example chapter still carries too much notation and background at
  once,
- the TT toolkit chapter still has several coequal payoffs,
- the coordinate / transport / preconditioning chapter remains rhetorically
  overloaded,
- and the derivative chapter remains too large and multi-track for one calm
  narrative arc.

The p50 rewrite should therefore keep p49’s chapter order and most of its
content, but sharpen the internal purpose of each chapter and reduce the feeling
that each chapter is also trying to be a mini-compendium.

## Core rewrite goals

### 1. Keep the global order from p49
The chapter sequence is already strong enough.  Do not do another major
reordering.

### 2. Give each chapter one dominant payoff
Every chapter should leave the reader with one main gain.  If a chapter contains
several useful materials, one of them should clearly govern the others.

### 3. Lighten the early notation burden
The running-example chapter should define only what is needed when it is needed.
Notation should serve the example rather than surrounding it.

### 4. Make implementation material interesting, not merely explicit
The implementation-facing chapters should focus on:
- what the runtime object is,
- what silently changes the scalar,
- what is easy to get wrong,
- why the algorithms are mathematically delicate.

### 5. Trim local scaffolding
Cut or reduce phrases that re-announce what the chapter is doing when the chapter
structure is already clear.

## Chapter-specific plan

## Chapter 1. Orientation And Scope
**Current issue:** improved from p48, but still slightly dense for an opening.

**Rewrite goal:** make the opening read as a problem-and-object chapter opening,
not a compressed technical setup.

**Planned changes:**
- keep the first two paragraphs largely intact,
- shorten the “guiding question” paragraph so it reads less like a meta-outline,
- make the “what the reader should focus on” block shorter and less list-like,
- keep the limitation paragraph, but remove any sentence that feels like it is
  already anticipating late-stage defense language.

**Desired payoff:** the reader should leave the opening with one strong memory:
this note studies a TT-based filtering object and its fixed-branch scalar/gradient
specialization.

## Chapter 2. Running Example And Notation
**Current issue:** this chapter still behaves like notation-plus-background instead
of like an example-driven entry into the method.

**Rewrite goal:** let the threaded nonlinear example govern the notation, not the
other way around.

**Planned changes:**
- move the threaded nonlinear example earlier within the chapter’s emphasis,
- compress notation explanations that can be delayed until later chapters,
- shorten literature framing so it does not interrupt the example,
- use the example to motivate why adjacent-state targets, retained filters, and
  transformed coordinates matter.

**Desired payoff:** the reader should feel that the notation is serving one live
example rather than that the example is buried inside a notation chapter.

## Chapter 3. Exact Filtering Target And Recursive Bottleneck
**Current issue:** conceptually strong, but still slightly overexplained.

**Rewrite goal:** make the exact bottleneck feel like one clean forcing argument
for why approximation is needed.

**Planned changes:**
- keep the exact target and recursion material,
- tighten repeated restatements of the filtering problem,
- end the chapter with a cleaner bridge into the TT toolkit: because exact
  recursion is inaccessible, the next step is to choose the approximation family.

**Desired payoff:** the reader should clearly understand why TT approximation is
being introduced.

## Chapter 4. Tensor-Train Approximation Toolkit
**Current issue:** too many coequal chapter purposes.

**Rewrite goal:** define one central payoff:
> what is the TT approximation family, and why can it plausibly replace the full
> tensor object in structured problems?

**Planned changes:**
- keep the TT definition,
- keep the rank interpretation,
- keep the fully worked exponential example,
- keep the rank-plausibility discussion,
- but explicitly subordinate the marginalization and least-squares details to the
  main TT-family explanation.

**Desired payoff:** by the end of the chapter, the reader should feel they now
understand what TT form is and why rank is the main structural diagnostic.

## Chapter 5. Coordinate Systems, Conditional Maps, And Preconditioning
**Current issue:** still mathematically coherent but rhetorically heavy.

**Rewrite goal:** make the chapter answer one central question:
> why does the same filtering object need to be seen in several coordinate systems,
> and what does each coordinate system buy us?

**Planned changes:**
- state the physical / reference / retained / preconditioned coordinate roles more
  explicitly at the start,
- compress repeated density-identity restatements,
- make KR maps and preconditioning each answer a specific need,
- reduce the sense that several transform technologies are being introduced in
  parallel.

**Desired payoff:** the reader should feel that every new coordinate system solves
one concrete obstacle rather than merely adding symbolic machinery.

## Chapter 6. Squared-TT Filtering Object And Operational Recursion
**Current issue:** better than before, but still partly split between object
justification and algorithm commentary.

**Rewrite goal:** keep the chapter’s center on the nonnegative approximate
filtering object and its operational recursion.

**Planned changes:**
- keep squared-density repair, normalizer, marginalization, and Algorithms 1–2,
- sharpen the transitions so that each algorithm feels like a necessary stage in
  the operational recursion,
- reduce any leftover side-commentary that restarts the approximation-family
  discussion.

**Desired payoff:** the reader should see one clear forward movement from TT
object to squared-TT object to normalized retained filter.

## Chapter 7. Fixed-Branch Likelihood Construction
**Current issue:** improved, but still too often reads as stored-field inventory.

**Rewrite goal:** make the chapter read as the answer to:
> what exactly must be frozen in order for the scalar to be one mathematical
> object rather than a changing algorithmic procedure?

**Planned changes:**
- keep reconciliation with paper objects,
- keep object and array-shape details,
- but foreground the interesting fragility:
  - what choices silently change the scalar,
  - why stored arrays matter,
  - why fixed least-squares replaces adaptive TT-cross here,
  - why branch identity is mathematically consequential.
- reduce inventory-style lists where no mathematical consequence is attached.

**Desired payoff:** the reader should understand the implementation object as a
mathematical identity, not merely a software structure.

## Chapter 8. Fixed-Branch Derivative Theory
**Current issue:** still too large and internally multi-track.

**Rewrite goal:** give the derivative chapter one calmer internal spine.

**Planned changes:**
- keep all the warmups and propositions,
- but make the warmups more explicitly cumulative,
- reduce local re-motivation once the fixed-branch derivative goal is established,
- treat the “what must be held fixed” material as the chapter’s late payoff rather
  than as another partial restart,
- keep the checklists only if they genuinely help the chapter close, rather than
  reopening the derivative story.

**Desired payoff:** the chapter should feel like one slow derivative ascent rather
than several derivative notes placed adjacently.

## Chapter 9. Validation And Diagnostics
**Current issue:** stronger than before, but still somewhat protocol-heavy.

**Rewrite goal:** keep the benchmark detail, but make the evidentiary structure
more apparent.

**Planned changes:**
- frame the chapter around what each test is trying to establish,
- keep the benchmark suite,
- reduce ledger-style listing where possible,
- make the final “what each benchmark can and cannot establish” subsection the
  explicit interpretive payoff.

**Desired payoff:** the reader should feel the validation chapter is a scientific
argument about evidence, not only a benchmark registry.

## Chapter 10. Positioning, Limits, And Relation To Zhao And Cui
**Current issue:** already improved, but still needs to sound purely synthetic.

**Rewrite goal:** ensure the ending is only about:
- what object has been defined,
- what it is useful for,
- what its limits are,
- how it relates back to Zhao and Cui.

**Planned changes:**
- do not re-explain chapter mechanics,
- keep the relation-to-source section,
- let the chapter sound like a bounded closing judgment.

## Material to preserve from p49

These are strengths and should remain unless a local rewrite clearly improves them:
- stronger opening voice,
- threaded nonlinear example,
- worked TT exponential example,
- coordinate-system explanations,
- fixed-branch reconciliation,
- derivative warmups,
- benchmark suite,
- source-safe relation to Zhao and Cui.

## Material to trim or rewrite more selectively

- front-loaded notation that can be deferred,
- generic “mathematical question” scaffolding,
- chapter openings that announce too many coequal purposes,
- inventory paragraphs that do not yet say why the details matter,
- repeated motivation sentences that do not deepen the concept.

## Verification plan for p50

1. Create p50 from p49.
2. Rewrite chapter interiors using the goals above.
3. Keep the current chapter order.
4. Compile p50 with `latexmk -pdf` and run BibTeX as needed.
5. Fix any remaining references or bibliography issues.
6. Read the opening and running-example chapters straight through and check that
   the note now starts from a problem and an example rather than from a notation
   burden.
7. Read the TT, coordinate, and fixed-branch chapters straight through and check
   that each now has one more clearly dominant payoff.
8. Read the derivative and validation chapters and check that they feel cumulative
   rather than multi-track.

## Proposed output file

`docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
