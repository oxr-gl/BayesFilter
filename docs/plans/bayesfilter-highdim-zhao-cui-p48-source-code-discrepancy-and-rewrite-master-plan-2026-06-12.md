# P48 Zhao--Cui Monograph-Flow Rewrite Plan

**Date:** 2026-06-12  
**Base text:** `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`  
**Target:** `docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-and-rewrite-result-2026-06-09.md`

## Context

The current Zhao--Cui companion note at
`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
contains a large amount of valuable material:
- careful notation,
- threaded nonlinear examples,
- TT basics,
- rank-plausibility discussion,
- coordinate-system and KR-map explanations,
- fixed-branch likelihood specialization,
- derivative warmups and propositions,
- and a large validation protocol.

The problem is not that the note is thin.  The problem is that it currently reads
as several strong notes interleaved at once:
- a source reconstruction of Zhao--Cui,
- a TT tutorial,
- a coordinate-transform / transport tutorial,
- a fixed-branch likelihood note,
- a derivative note,
- and a validation dossier.

The user wants to keep the material and reorganize it majorly so it flows like a
chapter or sequence of monograph chapters rather than a stitched compendium.

## Main diagnosis

P30 suffers from five major readability problems:

1. **Too many openings.**
   The early sequence (`Notation And Reading Convention`, `Threaded Nonlinear
   Example`, `Reader Orientation: Five Mathematical Objects`, `What Problem Is
   Being Solved?`, `State-Space Model`) repeatedly reintroduces the chapter.

2. **Mixed genres at equal rhetorical height.**
   Monograph exposition, implementation handoff, derivative tutorial, and
   validation protocol all compete as if they were coequal main lines.

3. **Derivative and implementation material are dispersed.**
   The fixed-branch and derivative story appears before, during, and after other
   conceptual lines rather than being given one clear home.

4. **Pedagogical material is valuable but scattered.**
   TT examples, warmups, and nonlinear toy examples exist, but they do not form
   one continuous teaching arc.

5. **Validation appears as an appended ledger.**
   The validation and benchmark protocol is important, but it currently feels
   bolted on rather than like the natural culmination of the mathematical story.

## Rewrite goal

Produce a new p48 Zhao--Cui note that preserves most of p30’s substance but
reorganizes it so the reader experiences one descending monograph arc:

1. positioning and scope,
2. running example and notation,
3. exact filtering target and recursive bottleneck,
4. TT approximation machinery,
5. coordinate systems and transport,
6. squared-TT filtering object and operational recursion,
7. fixed-branch likelihood specialization,
8. fixed-branch derivative theory,
9. validation and diagnostics,
10. positioning, limits, and relation to Zhao--Cui.

## Recommended chapter architecture for p48

### Chapter 1. Orientation And Scope
**Dominant question:** what is this note trying to define, and why is that object
scientifically worth studying?

**Merge into this chapter:**
- `Reader Orientation: Five Mathematical Objects`
- the scope-setting parts of the abstract and opening framing
- a concise reading guide

**Rewrite goal:**
- one opening only,
- one dominant lane statement,
- one limitation statement,
- one map of the chapter.

The reader should leave Chapter 1 knowing:
- the exact scientific problem,
- the object chosen for study,
- and the main mathematical threads that follow.

### Chapter 2. Running Example And Notation
**Dominant question:** what small nonlinear example and notation will carry the
reader through the later construction?

**Merge into this chapter:**
- `Notation And Reading Convention`
- `Threaded Nonlinear Example Used Throughout The Note`

**Rewrite goal:**
- use the nonlinear example as the live object that motivates later formulas,
- define notation only when it serves that example,
- avoid letting notation become an independent opening chapter.

### Chapter 3. Exact Filtering Target And Recursive Bottleneck
**Dominant question:** what exact filtering object would we like to compute, and
why is it hard enough to require approximation?

**Merge into this chapter:**
- `What Problem Is Being Solved?`
- `State-Space Model And Notation Used In This Note`
- `The Four Marginal Learning Problems`
- `The Exact Recursive Bottleneck`

**Rewrite goal:**
- make the exact problem and the bottleneck visible before introducing TT
  machinery,
- avoid restarting “what problem is being solved?” several times.

### Chapter 4. Tensor-Train Approximation Toolkit
**Dominant question:** what is a TT approximation, why can it be plausible, and
how should the reader think about rank?

**Merge into this chapter:**
- `Tensor Trains From First Principles`
- `Why Moderate Tensor-Train Rank Is A Plausible Hypothesis`
- the worked TT examples such as the three-variable exponential example

**Rewrite goal:**
- keep the pedagogical TT material together,
- use the worked TT example as the chapter payoff,
- move rank plausibility to the end of the toolkit chapter rather than letting it
  interrupt the transition from filtering to coordinates.

### Chapter 5. Coordinate Systems, Conditional Maps, And Preconditioning
**Dominant question:** why does the method need several coordinate systems, and
how do KR maps and preconditioning fit into the filtering construction?

**Merge into this chapter:**
- `Coordinate Systems And Density Transformations`
- `One Observation Step Through All Coordinate Systems`
- `Conditional Densities And KR Maps From Marginal Ratios`
- `Forward Conditional Map And Particle-Filter Correction`
- `Backward Conditional Map, Path Estimation, And Smoothing`
- `Preconditioning`

**Rewrite goal:**
- make these ideas one coherent transformed-object chapter,
- explain why KR maps and preconditioning belong together rather than appearing
  as separate technical excursions.

### Chapter 6. Squared-TT Filtering Object And Operational Recursion
**Dominant question:** what is the nonnegative approximate filtering object, and
how is it propagated operationally through the filtering recursion?

**Merge into this chapter:**
- `From Bayesian Filtering To A Tensor-Train Approximation Family`
- `Why Nonnegativity Fails And Why Square-Root TT Repairs It`
- `Squared-TT Density, Defensive Reference, And Normalizer`
- `Squared-TT Marginalization And Mass Matrices`
- `Why TT Marginalization Is Cheap Once The Representation Exists`
- `Algorithm 1, Fully Annotated`
- `Algorithm 2, Fully Annotated`

**Rewrite goal:**
- keep the approximation family and operational recursion in one place,
- make Algorithm 1 and Algorithm 2 feel like the culmination of the chapter
  rather than two isolated formal modules.

### Chapter 7. Fixed-Branch Likelihood Construction
**Dominant question:** once the approximate filtering object exists, how is the
fixed-branch scalar defined and what is the actual runtime object?

**Merge into this chapter:**
- `Fixed-Branch Likelihood Specialization`
- `Fixed-Branch Objects And Array Shapes`
- `Consolidated Fixed Least-Squares Formulation`
- `One Concrete Branch, Fully Instantiated`
- `Fixed-Branch TT Filtering Recursion`

**Rewrite goal:**
- explain the fixed-branch object after the filtering object is already understood,
- focus the chapter on runtime identity, stored fields, and what is held fixed.

### Chapter 8. Fixed-Branch Derivative Theory
**Dominant question:** what does the fixed-branch derivative differentiate, and
how does its chain of dependence unfold?

**Merge into this chapter:**
- `Integrated Fixed-Branch Gradient Expansion`
- `Fixed-Branch Gradient Motivation`
- `Warmup 1` through `Warmup 5`
- `The Fixed-Branch Forward Pass`
- `Gradient Teaching Layer: What Is Differentiated`
- `The Fixed-Branch Derivative Pass`
- `Proposition 1`
- `The Story Of The Fixed-Branch Derivative`
- `Proposition 2`
- `What This Does Not Prove`
- `What Must Be Held Fixed For The Derivative`
- `Four Checklists For Reading The Derivative`

**Rewrite goal:**
- gather all derivative pedagogy and fixed-branch logic into one chapter,
- make the warmups serve the main derivative story rather than appearing as a
  second note inside the note,
- ensure each return to “what is fixed” sharpens the branch concept rather than
  merely repeating it.

### Chapter 9. Validation And Diagnostics
**Dominant question:** how do we know the object, scalar, and derivative are
behaving correctly, and what can the benchmarks actually establish?

**Merge into this chapter:**
- `Finite-Difference Diagnostic`
- `Minimal Mathematical Example`
- `Large-Scale Validation Models And Test Protocol`
- all benchmark subsections and robustness / veto sections

**Rewrite goal:**
- turn validation into a culminating evidentiary chapter,
- organize by what is being tested:
  - exact-reference correctness,
  - fixed-branch scalar correctness,
  - derivative correctness,
  - approximation-scope boundary tests,
  - large-scale regime diagnostics.

### Chapter 10. Positioning, Limits, And Relation To Zhao--Cui
**Dominant question:** where does the present construction sit relative to Zhao and
Cui, and what exact claim is the note entitled to make at the end?

**Merge into this chapter:**
- `Integrated Conclusion`
- `Relation To Zhao And Cui`
- any remaining limitation / positioning material

**Rewrite goal:**
- use the final chapter for synthesis rather than fresh exposition,
- state what the note has established, what it has not established, and how it
  relates to the source paper and to BayesFilter’s fixed-branch specialization.

## Material to keep but move late

The following should not be deleted, but should move to appendical or late-chapter
positions if they interrupt the main reading line:
- exhaustive array-shape and object-field inventories,
- duplicated algorithm summaries,
- implementation checklists that restate already-defined equations,
- large benchmark report templates,
- repeated orientation blocks.

## Material to cut or compress

- repeated generic `\paragraph{Mathematical question.}` blocks when the section
  heading already states the question,
- duplicate opening-level motivation paragraphs,
- repeated “what this does not prove” language if it adds no new consequence,
- repeated orientation scaffolding that restarts the same frame.

## Figure / example policy

Do not cut the good pedagogical examples.

Instead:
- concentrate the TT explanatory examples in the TT chapter,
- concentrate the derivative warmups in the derivative chapter,
- let the threaded nonlinear example serve as a through-line where possible,
- use examples as chapter payoffs rather than scattered interruptions.

## Verification plan for the p48 rewrite

1. Create p48 from p30.
2. Reorganize the note into the chapter sequence above.
3. Preserve most current mathematical content, especially worked examples and
   derivative details.
4. Compile p48 with `latexmk -pdf` and run BibTeX as needed.
5. Fix all label, citation, and cross-reference issues introduced by the large
   section moves.
6. Read the first half straight through and verify that it now feels like one
   chapter sequence rather than several openings and tutorial insertions.
7. Read the derivative half and verify that the fixed-branch narrative is now one
   continuous chapter rather than a scattered set of local motivations.
8. Read the validation chapter and verify that it feels like the natural test of
   the mathematical object rather than an appended protocol.

## Proposed target file

`docs/plans/bayesfilter-highdim-zhao-cui-p48-source-code-discrepancy-and-rewrite-result-2026-06-09.md`

Note: this plan is for a major monograph-style rewrite that should ultimately
produce the new p48 Zhao--Cui PDF note in the `docs/plans` directory, with a
parallel `.tex` and compiled `.pdf` target following the project’s current naming
pattern for substantive note revisions.
