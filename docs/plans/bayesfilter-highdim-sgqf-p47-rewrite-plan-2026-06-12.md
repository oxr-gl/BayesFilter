# P47 Rewrite Plan: Focus-Preserving Monograph Rewrite From P44

**Date:** 2026-06-12  
**Base text:** `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p44-fixed-sgqf-expanded-companion-note-monograph-flow-rewritten-2026-06-12.tex`  
**Target:** `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`

## Context

P44 is currently the most content-complete and intellectually useful version of
the SGQF companion note.  It already contains many of the right ingredients:
- a clearer opening,
- stronger low-dimensional construction,
- explicit GHQ family clarification,
- what `F` means,
- tensor labels,
- sparse-grid level and Smolyak clarification,
- the UKF bridge,
- low-level cloud diagrams,
- implementation-facing detail,
- same-scalar and derivative material,
- and verification structure.

The user’s criticism of p45 and p46 is correct: those rewrites over-corrected.
They treated the problem too much as one of excess detail and repetition, and in
doing so removed or flattened material from p44 that was actually valuable.  The
next rewrite should therefore **not** be a compression-first rewrite.  It should
be a **focus-preserving rewrite**.

The real remaining problem is this:
- the chapter still does not always tell the reader what the **main line** is,
- what the **interesting difficulty** is,
- what they should **pay attention to at each stage**,
- and why the implementation-facing detail is mathematically interesting rather
  than merely technical.

So the goal of p47 is to keep most of p44’s substance while rewriting the prose,
transitions, and chapter emphasis so that:
- repeated ideas deepen rather than restart,
- useful detail is preserved,
- implementation material becomes narratively meaningful,
- and the whole document reads more like one authored monograph chapter than a
  reorganized dossier.

## Core rewrite principles

### 1. Preserve substance from p44
This rewrite should start from the assumption that p44 contains many useful
things that must remain:
- explanatory clarifications,
- UKF/SGQF weight discussion,
- detailed implementation-facing points,
- branch / scalar identity emphasis,
- figures that carry the pedagogical load,
- worked examples that expose the real mathematical subtleties.

The rewrite should therefore prefer **reframing** and **restaging** over cutting.

### 2. Repetition should deepen, not flatten
Repetition is not automatically bad.

Keep a repeated concept if the later occurrence adds a new layer of meaning.
Examples:
- first occurrence: one carried Gaussian surrogate,
- later occurrence: consequence for what moment structure is retained,
- later occurrence: consequence for what the scalar means,
- later occurrence: consequence for branch identity and same-scalar derivatives.

Cut only those repetitions that merely restate the same sentence without adding a
new implication.

### 3. Do not demote implementation detail; make it intelligible and interesting
Implementation detail is not the problem.  Unfocused implementation detail is the
problem.

In p47, implementation-facing sections should be rewritten so that the reader
knows:
1. what the runtime object actually is,
2. what decision points silently change the scalar,
3. what is genuinely subtle or easy to get wrong,
4. why the pseudocode matters mathematically.

The aim is that the implementation chapter should feel revealing, not dutiful.

### 4. Every chapter should answer one dominant question
The chapter sequence should not merely “contain material.”  Each chapter should
have one dominant purpose.

## Proposed chapter logic for p47

### Chapter 1. Introduction And Scope
**Dominant question:** what object is this note trying to define, and why is that
object scientifically worth studying?

**Keep from p44:**
- the high-dimensional filtering tension,
- the fixed SGQF lane,
- the exact-object vs carried-surrogate distinction,
- the bounded limitation statement.

**Rewrite goal:**
- preserve the content, but make the opening feel less like a compact defense note
  and more like a chapter beginning with one governing question.
- keep the reading guide, but phrase it as one chapter map rather than multiple
  meta-signals.

**Specific rewrite moves:**
- keep the first paragraph almost intact;
- keep the limitation paragraph;
- reduce local meta-commentary like “this note serves two roles” unless it helps
  the chapter identity;
- replace any “how to read” mini-resets with one closing overview paragraph.

### Chapter 2. Exact Filtering And Gaussian Projection
**Dominant question:** what exact object would we like to compute, and what is the
first narrowing that FixedSGQF imposes?

**Keep from p44:**
- state-space recursion,
- Gaussian projection equations,
- affine projection proposition,
- connection back to the Jia–Xin–Cheng Gaussian approximation block.

**Rewrite goal:**
- make the transition from introduction to formal foundation smoother,
- ensure the object-map table feels like support rather than a separate restart,
- emphasize why the exact recursion and Gaussian projection matter for what comes
  next.

**Specific rewrite moves:**
- add one stronger bridge sentence into the chapter;
- trim repeated reminders of what exactness is not;
- keep the object map, but introduce it more lightly and make clear why each
  object will matter later.

### Chapter 3. Low-Dimensional Construction Of FixedSGQF
**Dominant question:** how is the sparse-grid cloud built, and what geometric and
algebraic ideas make it understandable?

This should remain the main pedagogical engine of the note.

**Keep from p44:**
- scalar nonlinear moment setup,
- 2D tensor-product growth example,
- standard-normal GHQ family explanation,
- what `F` means,
- tensor labels,
- sparse-grid level,
- Smolyak combination,
- 2D merged cloud,
- 3D preview,
- UKF relation,
- final-weight discussion,
- all three pedagogical figures.

**Rewrite goal:**
- preserve these sections, but make them read as one staircase rather than several
  explanatory rooms.

**Specific rewrite moves:**
- keep the current order but tighten transitions so each subsection naturally
  forces the next one:
  1. one nonlinear Gaussian moment,
  2. tensor-product growth,
  3. one-dimensional rule family,
  4. tensor labels,
  5. sparse-grid level,
  6. Smolyak coefficients,
  7. merged clouds,
  8. UKF relation.
- remove local “reader should think...” type scaffolding unless the sentence is
  doing real interpretive work.
- explicitly frame the UKF comparison as the payoff to the cloud-construction
  story, not as a side excursion.
- preserve the weight-matching derivation, because it is one of the most
  intellectually clarifying parts of the note.

### Chapter 4. Fixed Cloud As The Computational Object
**Dominant question:** once the sparse-grid construction is complete, what exact
object is later reused in value and gradient evaluation?

**Keep from p44:**
- merged node dictionary,
- fixed cloud `\mathcal C_{b,L}`,
- merge tolerance, pruning, ordering conventions,
- cloud-construction convention.

**Rewrite goal:**
- separate the pedagogical cloud-building story from the formal statement of what
  the runtime object actually is.

**Specific rewrite moves:**
- pull together the formal “this is the stored object” material into a more
  clearly signposted chapter or major subsection;
- emphasize that the implementation does not store a symbolic Smolyak rule, but a
  merged, ordered cloud;
- use repeated mention of the cloud only when adding consequence (e.g. same cloud
  for value path, same cloud for gradient path, same cloud identity for finite
  differences).

### Chapter 5. Filtering Value Path And Worked Example
**Dominant question:** once the cloud is fixed, what deterministic scalar is being
computed?

**Keep from p44:**
- value recursion,
- one-step numeric oracle,
- scalar worked example.

**Rewrite goal:**
- let the chapter feel like one clean value story rather than value plus contract
  reminders plus side oracles.

**Specific rewrite moves:**
- keep the worked one-step example immediately after the value recursion;
- make the worked example explicitly answer: what does the cloud do to the scalar
  in practice?
- cut any branch-language repetition that does not yet add a new consequence.

### Chapter 6. Implementation Chapter
**Dominant question:** what does the algorithm actually store and preserve, and
what details matter enough to silently change the mathematical object?

This is the biggest rewrite opportunity.

**Keep from p44:**
- implementation contracts,
- branch identity,
- algorithm summaries,
- end-to-end ordering,
- inventories.

**Rewrite goal:**
- do not demote this material,
- but stage it so the reader knows what is interesting.

**Proposed internal order:**
1. **What the runtime object is**
   - fixed cloud,
   - weights,
   - ordering,
   - branch record,
   - merge conventions.
2. **What choices change the scalar**
   - level,
   - merge tolerance,
   - ordering,
   - zero-weight pruning,
   - factor family,
   - veto policy.
3. **What is easy to get wrong**
   - same level but different merge policy,
   - same cloud but different factor convention,
   - symbolic rule vs merged cloud,
   - signed weights and branch identity.
4. **Then pseudocode and algorithm summaries**
   - now the reader knows why each step matters.

**Desired effect:**
The implementation material should now feel like the chapter where the note tells
us where the real mathematical fragility lives.

### Chapter 7. Same-Scalar Branch Contract And Analytical Gradient
**Dominant question:** what does it mean to differentiate the same declared scalar,
and how does that discipline propagate through the recursion?

**Keep from p44:**
- branch tuple,
- fixed scalar,
- derivative chain,
- square-root branch,
- innovation score,
- posterior sensitivity propagation,
- boxed algorithm.

**Rewrite goal:**
- preserve the mathematics,
- but ensure each return to the branch idea adds a new consequence rather than
  restating the same warning.

**Specific rewrite moves:**
- first occurrence: define branch identity structurally,
- second occurrence: explain derivative correctness consequence,
- third occurrence: explain finite-difference consequence,
- remove flat restatements of “same scalar” that add no new layer.

### Chapter 8. Verification And Validation
**Dominant question:** how do we know that the value and derivative are correct,
and how do we know what the lane can and cannot represent?

**Keep from p44:**
- FD checks,
- toy traces,
- test-model hierarchy,
- validation report template.

**Rewrite goal:**
- organize this chapter by the kind of question being tested, not only by the
  testing instrument.

**Proposed internal structure:**
1. exact-collapse / reference correctness,
2. scalar-value correctness,
3. same-scalar gradient correctness,
4. cloud-sensitivity and approximation-boundary checks.

### Chapter 9. Positioning And Conclusion
**Dominant question:** where does this lane sit among neighboring proposals, and
what claim is the chapter finally entitled to make?

**Keep from p44:**
- neighboring-method comparison,
- conclusion.

**Rewrite goal:**
- use the comparison chapter for synthesis rather than fresh exposition,
- let the conclusion state only:
  - what object was defined,
  - why it is useful,
  - what scientific boundary remains.

**Specific rewrite moves:**
- remove any trace of “pitching the lane” again,
- refer back to the earlier UKF chapter rather than redoing that discussion,
- end with one crisp bounded judgment.

## Material to preserve explicitly from p44

These should be treated as valuable assets, not likely deletion targets:
- the UKF cloud comparison and its diagrams,
- the second-moment / matching-weights derivation,
- the explanation that low-level clouds can coincide geometrically while the
  constructions differ,
- the branch-identity and scalar-identity emphasis,
- the object-level explanation of the fixed cloud,
- the worked examples that show where interesting difficulty actually lives.

## Material to cut or flatten only if it does not deepen anything

- repeated lane identity statements,
- repeated “what this note does not claim” language when it is literally the same
  limitation restated,
- repeated “how to read this section” scaffolding,
- repeated object inventories that do not sharpen the next chapter.

## Verification plan for executing p47

1. Create p47 from p44, not from p45 or p46.
2. Rewrite chapter by chapter according to the dominant-question structure above.
3. Preserve current diagrams unless one no longer serves the revised flow.
4. Compile with `latexmk -pdf` and run BibTeX as needed.
5. Repair all labels, references, and bibliography issues.
6. Read the chapter straight through and check:
   - do repeated ideas deepen rather than restart?
   - does the implementation material now feel motivated?
   - does each chapter clearly tell the reader what matters and why?
7. Confirm the note now reads like one authored chapter with a clear main line,
   while still preserving the substance that made p44 useful.

## Proposed output file

`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
