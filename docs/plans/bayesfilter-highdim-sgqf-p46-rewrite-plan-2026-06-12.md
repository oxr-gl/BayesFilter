# P46 Rewrite Plan: Focus, Deepening, And Structured Implementation Flow

**Date:** 2026-06-12  
**Target:** `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p46-fixed-sgqf-expanded-companion-note-focus-deepened-2026-06-12.tex`

## Context

P45 is materially better than p44.  The opening is clearer, the low-dimensional
construction chapter is more coherent, and the UKF bridge now lives closer to the
cloud-construction material.  However, the note still reads like a strong internal
research chapter draft rather than a fully natural monograph chapter.

The remaining problem is **not** lack of explanation.  The problem is now one of
**focus, deepening, and rhetorical hierarchy**:
- too many ideas still appear at the same level of prominence,
- the prose still contains residual scaffolding language,
- implementation material is still not fully staged around what is genuinely
  interesting or easy to get wrong,
- and some repeated ideas are repeated flatly rather than deepened.

The goal of p46 is therefore not to add much new content.  It is to rewrite p45
so that:
- repeated material either disappears or returns only when it deepens the idea,
- implementation detail is concentrated into a motivated chapter rather than
  scattered forward references,
- pseudocode and contracts arrive only after the reader knows what matters and
  why,
- the note tells the reader what to pay attention to at each stage.

## Editorial principles for p46

### 1. Remove flat repetition, keep cumulative repetition
Not all repetition is bad.

- **Bad repetition:** saying the same thing again with no new consequence.
- **Good repetition:** returning to the same concept later, but now explaining a
  deeper consequence of it.

For p46, repetition is allowed only when it sharpens the meaning.  For example:
- first appearance: one carried Gaussian surrogate,
- later consequence: why this cannot preserve multimodality,
- later consequence: why the same-scalar contract is narrower than exact
  likelihood evaluation.

If a repeated paragraph adds no new consequence, cut it.

### 2. Reduce scaffolding phrases
P45 still contains too many framing phrases like:
- “the next step is,”
- “the reader should think of,”
- “the point is,”
- “it is worth stating slowly,”
- “this is the place where many readers first get lost.”

Some such phrases are useful, but too many make the chapter sound guided rather
than authored.  In p46, keep only the ones that actually prevent a genuine
misreading.

### 3. Do not demote implementation detail; stage it better
Implementation detail is not the problem.  Unfocused implementation detail is the
problem.

The implementation-related material should be reorganized so it answers three
clear questions:
1. what is the runtime object,
2. what is easy to misunderstand or easy to get wrong,
3. what conventions actually change the scalar.

Only after those questions are answered should contracts and pseudocode appear.

### 4. Make each chapter answer one dominant question
Each chapter in p46 should have one main job:
- foundation chapter: what exact object is being approximated?
- construction chapter: how is the sparse-grid cloud built and what intuition
  should the reader carry?
- value chapter: once the cloud is fixed, what scalar is computed?
- implementation chapter: what object is actually stored and what decisions
  matter?
- gradient chapter: what does it mean to differentiate the same scalar?
- verification chapter: how do we know the value and gradient are the same-scalar
  objects?
- positioning chapter: where does this lane sit among neighboring methods?

## Rewrite goals by chapter

## Chapter 1. Introduction And Scope
### Current problem
The opening is much better than before, but it still does a bit too much at once:
- lane definition,
- audience statement,
- limitation statement,
- reading guide,
- hierarchy statement.

### Rewrite goal
Make the introduction feel less like a compact grant-defense memo and more like a
chapter opening.

### Planned changes
- Keep the first paragraph on the high-dimensional filtering tension.
- Keep the lane statement.
- Keep the limitation statement.
- Shorten or soften meta-writing such as “the note therefore serves two roles...”
  unless it contributes directly to the chapter’s scientific identity.
- Reduce explicit “how to read this note” language and fold it into one closing
  paragraph rather than several distinct signals.

### Desired effect
The opening should tell the reader:
- what the scientific problem is,
- what this chapter chooses to compute,
- what it does not claim,
without sounding like a defense brief.

## Chapter 2. Exact Filtering And Gaussian Projection
### Current problem
This chapter is mathematically correct but still arrives abruptly after the
opening.  The object-map table is useful, but it still has documentation energy.

### Rewrite goal
Smooth the transition from chapter-level motivation into formal foundation.

### Planned changes
- Add one stronger transition sentence from the introduction into the exact
  filtering chapter.
- Keep the exact filtering equations and Gaussian projection equations.
- Compress the object-map language so the table is presented as support rather
  than as a second beginning.
- Remove any phrases that repeat the chapter’s main point without deepening it.

### Desired effect
The formal foundation should feel like the natural first technical descent, not a
fresh note starting over.

## Chapter 3. Low-Dimensional Construction Of FixedSGQF
### Current problem
This is currently the strongest part of the note, but still slightly over-signaled
and locally over-explained.

### Rewrite goal
Preserve the construction pedagogy, but make it read like one chapter written in
one voice.

### Planned changes
- Keep the scalar nonlinear moment, the 2D tensor-product picture, GHQ family,
  tensor labels, sparse-grid level, Smolyak combination, merged clouds, and UKF
  bridge.
- Reduce the number of local “what this means” restarts.
- Make the progression more continuous:
  1. one-dimensional Gaussian rule,
  2. tensor-product lift,
  3. why the tensor rule becomes too large,
  4. how sparse-grid level chooses active tensor rules,
  5. how Smolyak recombines them,
  6. what the merged cloud looks like,
  7. why UKF can look similar at low level.
- Keep the UKF comparison in this chapter, but ensure it follows naturally from
  the cloud examples rather than feeling like a separate inserted note.
- Keep the weight-matching derivation, but present it as the payoff to the UKF
  comparison, not as a self-standing theorem.

### Desired effect
The reader should feel they are climbing one staircase, not entering several
adjacent rooms.

## Chapter 4. Formal Sparse-Grid Rule And Fixed Cloud
### Current problem
Some of the fixed-cloud meaning is still split between construction material and
later implementation material.

### Rewrite goal
Make this chapter the definitive home of the answer to:
> what exact mathematical object is later stored and reused?

### Planned changes
- Keep the formal Smolyak rule, merged-node dictionary, and fixed cloud
  `\mathcal C_{b,L}` together.
- Add a slightly stronger statement that this is the actual computational object,
  not a symbolic rule or raw tensor family.
- Remove later repetition of the same point unless it adds a new implementation
  consequence.

### Desired effect
The chapter should pin down the runtime mathematical object once and for all.

## Chapter 5. Filtering Value Path
### Current problem
The value chapter is generally fine, but the worked example and the chapter-level
focus can be sharpened.

### Rewrite goal
Make this chapter answer one question clearly:
> once the cloud is fixed, what scalar does the filter compute?

### Planned changes
- Keep the value recursion and the one-step oracle.
- Trim any wording that repeats branch philosophy if the branch contract is not
  yet the direct subject.
- Ensure the worked example is framed as a concrete realization of the chapter’s
  central scalar rather than as an independent teaching interlude.

## Chapter 6. Implementation Chapter
### Current problem
This is the most important structural change in p46.

Right now implementation-related material is scattered across:
- object tables,
- merge conventions,
- cloud definitions,
- branch identities,
- contracts,
- algorithms,
- appendix material.

This makes the implementation detail feel both overexposed and unfocused.

### Rewrite goal
Concentrate implementation-facing material into one coherent implementation
chapter or chapter-like block that tells the reader what is interesting and what
can go wrong.

### Planned internal order
#### A. What the runtime object is
- fixed cloud,
- stored weights,
- ordering,
- merge rule,
- factor convention,
- veto conventions.

#### B. What decisions change the scalar
Explicitly list the structural choices that are part of the scalar identity.

#### C. What is easy to get wrong
Examples:
- treating the cloud as symbolic instead of merged,
- assuming “same level” means “same scalar,”
- changing merge/order/factor policies silently,
- forgetting that signed weights are part of the object.

#### D. Then show pseudocode / algorithm summaries
Only after A–C have made the stakes visible.

### Desired effect
The implementation material should feel like a mathematically interesting chapter
about object identity and correctness, not like a technical dump.

## Chapter 7. Same-Scalar Branch Contract And Analytical Gradient
### Current problem
The mathematics is strong, but the branch philosophy is still repeated in a way
that sometimes feels defensive.

### Rewrite goal
Let the same-scalar idea deepen rather than repeat.

### Planned changes
- Keep the full branch tuple and derivative chain.
- Rephrase repeated branch warnings so each recurrence adds a new consequence:
  - first: structural identity of the scalar,
  - later: consequence for derivative correctness,
  - later: consequence for finite differences.
- Remove flat reiterations of “same scalar” where they do not sharpen meaning.

### Desired effect
The reader should feel the branch idea becoming more precise, not merely being
restated.

## Chapter 8. Verification And Validation
### Current problem
Good material, but still somewhat ledger-like.

### Rewrite goal
Make the verification chapter feel like the natural scientific test of the
preceding mathematical claims.

### Planned changes
- Organize the chapter explicitly by what is being checked:
  1. exact-collapse / reference correctness,
  2. value correctness,
  3. same-scalar gradient correctness,
  4. approximation-scope boundary tests.
- Keep the FD check, but treat it as one component of this larger verification
  story.
- Reduce repeated reminders of what the chapter is for if the ordering already
  makes that clear.

## Chapter 9. Positioning And Conclusion
### Current problem
The conclusion and positioning chapters still risk sounding like a restatement of
opening claims.

### Rewrite goal
Make the ending feel like synthesis rather than re-introduction.

### Planned changes
- Keep the neighboring-methods chapter concise.
- Refer back to earlier UKF discussion instead of re-explaining it.
- Let the conclusion state only:
  - what object was successfully defined,
  - what it is useful for,
  - where its scientific boundary lies.
- Remove any tone that sounds like pitching the lane all over again.

## Material to cut or compress

### Cut or compress aggressively
- flat repetition of lane identity,
- repeated “what this note does not claim” statements,
- repeated “how to read this section” guidance,
- repeated object inventories once the same object has a clear home,
- duplicate algorithm summaries when one final algorithm is enough,
- phrases that explain the same subtlety more than once without adding a new
  consequence.

### Keep, but deepen when repeated
- exact object vs carried surrogate,
- fixed cloud identity,
- same-scalar branch,
- UKF similarity vs constructional difference,
- low sparse-grid level as a deliberate interaction-order compromise.

## Verification plan for p46

1. Create `p46` from `p45`.
2. Rewrite the opening chapters and implementation flow according to the chapter
   goals above.
3. Preserve all current diagrams unless one clearly no longer serves the revised
   flow.
4. Compile with `latexmk -pdf` and run BibTeX as needed.
5. Fix references, bibliography, and figure placement.
6. Read the front half straight through and ask:
   - do I always know what the current chapter is trying to teach?
   - do repeated ideas deepen rather than restart?
   - do the implementation sections tell me what is interesting and easy to get
     wrong?
7. Read the later chapters and ask:
   - does the derivative chapter sharpen the branch idea rather than repeat it?
   - does the verification chapter test the mathematical claims rather than
     merely list diagnostics?
8. Confirm the chapter now reads more like one authored monograph chapter than a
   reorganized research dossier.

## Proposed output file

`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p46-fixed-sgqf-expanded-companion-note-focus-deepened-2026-06-12.tex`
