# P43 Monograph-Flow Rewrite Plan

**Date:** 2026-06-12  
**Target:** `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p43-fixed-sgqf-expanded-companion-note-monograph-reorganized-2026-06-10.tex`

## Context

P43 is materially better than p42, but it still reads as a reorganized composite rather than as a chapter written in one voice from the beginning. The user wants the note to read like a chapter or chapter-like companion in the monograph tradition of `docs/main.tex`, not like a patched explainer or a question-flow teaching note.

The problem is now mainly **rhetorical structure**, not missing content. The note already contains many of the right clarifications:
- standard-normal GHQ family,
- what `F` means,
- tensor labels,
- sparse-grid level,
- Smolyak combination,
- UKF comparison,
- low-dimensional diagrams.

What remains weak is the flow between those pieces and their integration into one monograph-style argument.

## Diagnosis: why p43 still feels stop-and-go

1. **Repeated thesis restarts.** The note repeatedly reintroduces the same claims in slightly different language:
   - exact target vs carried Gaussian surrogate,
   - fixed cloud / fixed branch / same-scalar gradient,
   - “deterministic, auditable, reproducible,”
   - “not exact nonlinear filtering.”
   These ideas should each have one authoritative home.

2. **Mixed rhetorical genres.** P43 still shifts between:
   - monograph exposition,
   - review-defense language,
   - implementation-contract language,
   - beginner teaching inserts.
   A chapter can contain all four, but not at the same narrative altitude.

3. **Pedagogy is scattered instead of gathered.** Toy cases, cloud construction, UKF analogy, and interaction examples are useful, but currently appear as inserted modules rather than one pedagogical chapter.

4. **Implementation and inventory material competes with exposition.** Contracts, formula inventories, boxed summaries, and end-to-end algorithms interrupt the reading line instead of supporting it from the margin or appendix.

5. **Transitions are weak.** Sections often restart the frame instead of deepening the previous step.

## Rewrite objective

Preserve almost all of p43’s mathematical content, but rewrite the chapter so it reads as one descending arc:

1. introduction and scope,
2. exact filtering and Gaussian-projection foundation,
3. pedagogical low-dimensional construction,
4. formal sparse-grid rule and fixed cloud,
5. filtering value recursion,
6. same-scalar branch contract and analytical gradient,
7. verification and validation,
8. method positioning,
9. conclusion,
10. appendix-like technical detail.

## Recommended section architecture for p44

### Chapter 1. Introduction And Scope
Merge and compress the current opening material into one unified introduction with four subsections:
1. problem setting and selected lane,
2. exact object versus carried surrogate,
3. approximation hierarchy,
4. reading guide and contribution summary.

**Rule:** say the lane once, say the main limitation once, and do not restart the thesis later unless a section needs a narrow reminder.

### Chapter 2. Exact Filtering And Gaussian Projection
Keep together:
- state-space model and exact recursion,
- Gaussian projection from moments.

This chapter should establish:
- what the exact recursion would require,
- what Gaussian projection keeps instead,
- why moment computation becomes the bottleneck.

### Chapter 3. Low-Dimensional Construction Of FixedSGQF
Gather all early pedagogy into one integrated construction chapter:
1. why quadrature appears,
2. one-dimensional GHQ family,
3. what `F` means,
4. tensor labels and tensor-product rules,
5. sparse-grid level and active tensor rules,
6. Smolyak coefficients and signed combination,
7. merged 2D and 3D clouds,
8. UKF relation and low-level weight coincidence,
9. diagrams.

This should be the main teaching chapter of the note.

### Chapter 4. Formal Sparse-Grid Rule And Fixed Cloud
After the pedagogical chapter, return to formal notation and define the fixed computational object cleanly:
- sparse-grid formula,
- merged node dictionary,
- fixed cloud `\mathcal C_{b,L}`,
- deterministic merge / zero-weight / sorting conventions.

The chapter should answer: *what exact object does the later recursion consume?*

### Chapter 5. Filtering Value Path And Worked Example
Keep together:
- filtering value recursion,
- one-step worked numeric oracle.

The worked example should immediately follow the value recursion so the chapter closes with a concrete check.

### Chapter 6. Same-Scalar Branch Contract And Analytical Gradient
Keep together:
- saved scalar and branch identity,
- factor derivative convention,
- gradient dependency chain,
- posterior sensitivity propagation,
- boxed algorithm.

The boxed algorithm should conclude the chapter, not compete with the chapter as a separate top-level object.

### Chapter 7. Verification And Validation
Merge:
- finite-difference same-scalar check,
- diagnostics / accuracy / test-model sections.

Organize by verification ledger:
- engineering correctness,
- scalar-value correctness,
- same-scalar gradient parity,
- approximation-scope checks.

### Chapter 8. Positioning Against Neighboring Methods
Keep the neighboring-method discussion, but shorten it and make it a true positioning chapter. The UKF comparison here should be only a short cross-reference back to the pedagogical chapter, not a re-explanation.

### Chapter 9. Conclusion
Keep the conclusion, but make it a true closeout rather than another partial restart of the opening thesis.

### Appendices / Late Technical Material
Move or compress toward the end:
- implementation contracts,
- formula inventories,
- notation inventories,
- source maps,
- duplicate algorithm summaries.

## Figure placement plan

### Figure 1. 2D tensor-rule build-up to merged SGQF cloud
**Home:** Low-Dimensional Construction chapter, immediately after the first duplicate-merge explanation.

### Figure 2. SGQF cloud versus canonical UKF-style sigma-point sketch
**Home:** same chapter, inside the UKF relation subsection, immediately after the explanation of why the cloud looks familiar.

### Figure 3. 3D axis coverage versus full tensor / corner coverage
**Home:** same chapter, with the three-dimensional interaction discussion.

**Editorial rule:** each figure should live exactly where the prose asks the reader to picture the next step.

## What to compress or move out of the main line

Reduce or relocate:
- repeated lane/limitation statements,
- repeated audience-setting language,
- duplicate roadmaps,
- multiple formula inventories,
- repeated algorithm summaries,
- review-facing rhetoric that interrupts the mathematics,
- implementation-contract detail that is better read as appendix support.

## Writing rules for the rewrite

1. Each section should answer **one main chapter question**.
2. Do not re-explain a concept in full if it already has a clear home earlier.
3. Keep beginner clarifications, but integrate them into monograph prose rather than isolating them as stand-alone teaching modules.
4. Use fewer micro-`\paragraph{...}` interruptions when a smooth subsection arc would do.
5. Move from:
   - object,
   - to construction,
   - to recursion,
   - to derivative,
   - to verification,
   - to positioning.

## Verification plan

1. Rewrite the front half of p43 into the section architecture above.
2. Keep the UKF bridge and all three diagrams inside the low-dimensional construction chapter.
3. Compile the resulting p44 note with `latexmk -pdf`.
4. Fix all label, package, citation, and figure-placement issues.
5. Read the first half of the note in order and confirm it now feels like one monograph chapter arc:
   - motivation,
   - GHQ family,
   - tensor labels,
   - sparse-grid level,
   - Smolyak,
   - merged clouds,
   - UKF relation.
6. Confirm that later chapters descend clearly from theory to construction to algorithm to verification to positioning.
7. Confirm that the note still preserves source-safe claims:
   - SGQF is not “basically UKF,”
   - sparse-grid level is not simply a UKF spread parameter,
   - Smolyak is not mere point deletion.

## Deliverable

Create a new successor note, tentatively:

`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p44-fixed-sgqf-expanded-companion-note-monograph-flow-rewritten-2026-06-12.tex`

with the above chapter-like architecture.
