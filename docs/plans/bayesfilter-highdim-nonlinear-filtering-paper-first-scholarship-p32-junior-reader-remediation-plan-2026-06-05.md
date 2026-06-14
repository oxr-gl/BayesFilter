# P32 Junior-Reader Remediation Plan

metadata_date: 2026-06-05

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

what_is_not_concluded:
- This plan does not lower the mathematical standard of the note.
- This plan does not replace the panel-facing or implementation-facing remediation plans; it supplements them for a junior lab-reader audience.
- This plan does not assume the workers are mathematically weak; it assumes they are early-stage researchers who still need clearer conceptual staging.

## Purpose

This plan is for adapting P32 so that it can be given to workers in the lab who are mostly first-year PhD students in scientific subjects. The goal is not to simplify the mathematics away, but to make the note more teachable and more executable for readers who are mathematically capable but still new to nonlinear filtering, Gaussian closures, and branch-conditioned differentiation.

The current note is now much stronger for senior readers, but a junior scientific reader may still struggle with:

1. distinguishing the three layers of approximation;
2. understanding what is standard filtering theory versus what is specific to FixedSGQF and BayesFilter;
3. understanding what a branch means operationally;
4. following the general gradient derivation without constantly reconstructing the dependency chain;
5. extracting a stable implementation path from the document without overloading on notation.

## Reader model

This plan assumes the target reader:
- is a first-year PhD student in a science subject;
- is comfortable with calculus, linear algebra, and basic probability;
- is not yet fluent in nonlinear filtering literature;
- can implement mathematical procedures if the conceptual layers are clearly separated;
- benefits from explicit “what to retain” summaries, worked examples, and clear boundaries between standard theory and project-specific design choices.

## Remediation goals

After this pass, a junior reader should be able to answer:

1. What is the exact object in Bayesian filtering and what surrogate object does FixedSGQF carry instead?
2. What are the three distinct approximations being made, and what does each one cost?
3. What parts of the note are standard filtering theory, what parts come from Jia--Xin--Cheng, and what parts are BayesFilter-specific design choices?
4. What exactly is a branch, and why does same-branch consistency matter for gradients and finite differences?
5. How does the gradient section break into understandable stages?
6. What sequence of objects should I implement first if I am coding this in the lab?

## Workstream 1 — Separate standard theory, source reconstruction, and project-specific design

### Problem
A junior reader may not know what is generic Bayesian filtering, what is from the SGQF literature, and what is local to this report.

### Required changes
Add one short orienting subsection early in the report, likely after “What This Note Computes” or near the start of the formal development, titled something like:
- `What Is Standard, What Is Source Reconstruction, And What Is FixedSGQF-Specific?`

This subsection should explicitly separate three layers:

1. **Standard filtering theory**
   - exact Bayesian prediction/update recursion,
   - Gaussian projection update once moments are given.
2. **Source reconstruction from Jia--Xin--Cheng**
   - one-dimensional Gaussian quadrature,
   - tensor-product rules,
   - sparse-grid / Smolyak cloud construction.
3. **BayesFilter-specific design choices**
   - fixed scalar definition,
   - branch identity contract,
   - same-scalar finite-difference logic,
   - selected deterministic Cholesky derivative convention.

### Done criterion
A junior reader can say which pieces are textbook-like, which are literature-derived, and which are local design decisions.

## Workstream 2 — Make the approximation layers impossible to confuse

### Problem
Junior readers may still blur together Gaussian projection, sparse-grid moment approximation, and fixed-branch differentiation.

### Required changes
Add a dedicated short subsection or boxed summary titled something like:
- `The Three Approximations, Separated`

It should list and explain distinctly:

1. **Gaussian carried-state approximation**
   - replaces the full filtering law with \((m_t,P_t)\).
2. **Sparse-grid moment approximation**
   - approximates the moments needed to define that Gaussian surrogate.
3. **Fixed-branch derivative restriction**
   - fixes the computational path so the derivative refers to the same scalar that the value path computes.

Each item should include:
- what exact object is replaced,
- what new object is computed instead,
- and what kind of limitation enters at that layer.

### Done criterion
A junior reader can explain the three approximations separately instead of treating them as one bundle.

## Workstream 3 — Add an explicit “what is a branch?” teaching subsection

### Problem
The formal branch contract is now explicit, but the intuitive meaning of “branch” is still hard for junior readers to internalize.

### Required changes
Add one short subsection, likely near Section 12, titled something like:
- `What The Branch Means In Practice`

This subsection should explain in plain mathematical language:
- the branch is the fixed structural computational route,
- not the numerical values themselves;
- changing cloud structure, merge policy, factorization family, or veto path means changing the scalar being differentiated;
- same-branch finite differences are meaningful because they compare values of the same declared computational target.

A very small example should be included, e.g.:
- same cloud + same Cholesky branch + different \(\theta\) = same branch;
- changed active grid or different factorization outcome = different branch.

### Done criterion
A junior reader can explain branch consistency without resorting only to the formal tuple notation.

## Workstream 4 — Add a “how to read Section 13” preface

### Problem
Section 13 remains one of the hardest parts of the report for junior readers.

### Required changes
Before the main derivative subsections, add one short reading guide titled something like:
- `How To Read The Gradient Section`

This guide should tell the reader:
1. what is the current-score part;
2. what is the next-step propagation part;
3. in what order to understand the subsections;
4. what can be skipped on a first pass and returned to later.

This is not a replacement for the derivation. It is a reading strategy scaffold.

### Done criterion
A junior reader can enter Section 13 with a map rather than only a wall of symbols.

## Workstream 5 — Add “what to retain” recap lines in the hardest places

### Problem
Even when a subsection is readable locally, a junior reader may not know what the key takeaway is before moving on.

### Required changes
At the end of the hardest derivative subsections, add one short recap line beginning with something like:
- `What to retain from this subsection is ...`

Priority subsections:
- Square-Root Branch,
- Prediction Sensitivities,
- Observation Sensitivities,
- Innovation Score,
- Posterior Sensitivity Propagation.

Each recap should say:
- what new object was produced,
- whether it is needed for current score, propagation, or both.

### Done criterion
A junior reader can summarize each derivative stage before continuing to the next one.

## Workstream 6 — Add an explicit “implementation order for lab workers” subsection

### Problem
The report is now implementation-complete, but a junior reader may still not know where to start when coding.

### Required changes
Add a short subsection titled something like:
- `Implementation Order For A First Prototype`

This subsection should recommend a staged build order for lab workers:

1. implement one-dimensional rule and sparse-grid cloud construction;
2. verify duplicate merge and weights on toy examples;
3. implement value path only;
4. verify the worked numeric oracle;
5. implement branch checks and failure returns;
6. implement factor derivative and predictive sensitivities;
7. implement observation sensitivities and score;
8. implement posterior sensitivity propagation;
9. verify same-scalar finite differences.

### Done criterion
A junior engineer or scientist can begin implementation without guessing what to code first.

## Workstream 7 — Preserve the worked example as the main teaching anchor

### Problem
The worked example is one of the most helpful parts of the note for junior readers. It should be used more systematically as the anchor for the general machinery.

### Required changes
Cross-reference the worked example from:
- the approximation-layer discussion,
- the branch explanation,
- the gradient reading guide,
- and the hardest derivative subsections.

This should make the example function not just as one section, but as the recurring concrete anchor for the rest of the report.

### Done criterion
A junior reader can always return to the worked example when the general notation becomes too abstract.

## Success criteria

This plan succeeds if, after execution:

1. a first-year PhD student in a scientific field can distinguish standard theory, source reconstruction, and FixedSGQF-specific design choices;
2. the three approximations are clearly separable in the reader’s mind;
3. the meaning of branch consistency becomes intuitive rather than only formal;
4. Section 13 becomes significantly easier to enter and follow;
5. a lab worker can see a plausible implementation order from the note itself.
