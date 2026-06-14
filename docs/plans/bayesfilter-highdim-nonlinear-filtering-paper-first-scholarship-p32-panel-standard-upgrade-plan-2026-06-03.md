# P32 Academic-Report Revision Plan

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This plan does not claim that P32 already satisfies the review-panel standard.
- This plan does not propose changes to P30.
- This plan does not reduce P32 to a memo, checklist, or governance artifact.
- This plan does not claim exact nonlinear posterior fidelity or superiority over alternative high-dimensional filtering methods.

## Core question

How should P32 be rewritten so that it functions as a **self-contained academic report** that answers two review-panel questions:

1. Can a former chemistry professor serving as chair understand the document, find it thorough and self-contained, and judge the proposal persuasive enough to approve the work?
2. Can an implementation engineer on the same panel, working with Claude Code but without consulting additional papers, implement the method directly from the document?

## Required standard

The revised P32 should not read like an internal process note. It should read like a serious academic report that is simultaneously:

- mathematically explicit,
- conceptually teachable,
- self-contained in notation and derivation,
- honest about approximation scope,
- and implementation-complete.

The note must therefore succeed on **two axes at once**:

### A. Chair-readability axis

A strong but non-specialist scientific reader should be able to follow:

- what high-dimensional filtering problem is being addressed;
- why exact nonlinear filtering is difficult here;
- what FixedSGQF proposes as a compromise;
- where the approximation enters;
- why that approximation may still be scientifically reasonable in some regimes;
- what the main limitations are;
- why this proposal deserves consideration alongside richer alternatives.

### B. Implementation-completeness axis

An implementation engineer should be able to recover from the document alone:

- every mathematical object carried across time;
- every transformation between coordinates;
- every moment, covariance, and update equation;
- the exact fixed sparse-grid construction;
- the same-scalar branch rules;
- the value recursion;
- the analytical gradient recursion;
- the failure exits and what they mean mathematically;
- enough concrete detail to implement the method without returning to Jia--Xin--Cheng or other external sources.

## Main diagnosis of current P32

The current P32 is mathematically substantial, but it still falls between audiences.

- It contains enough mathematics that a specialist can see the direction.
- It does **not yet lead** the chair through the proposal as a coherent scientific argument.
- It does **not yet fully guarantee** that an implementation engineer could code the method from P32 alone without reconstructing omitted choices from the source papers.

So the revision should not merely add more sections. It should make the report simultaneously more persuasive and more executable.

## Revision objective

Turn P32 into a report that does four things in order:

1. states the scientific problem and the intellectual niche of FixedSGQF;
2. explains the approximation as a deliberate mathematical choice rather than a pile of formulas;
3. derives the full value-and-gradient machinery with enough detail for direct implementation;
4. closes with a balanced scholarly judgment about when the method is credible, when it is narrow, and why it still belongs in the high-dimensional filtering discussion.

## Proposed report structure

### 1. Opening statement of the scientific problem

Begin with the problem the panel is being asked to evaluate:

- nonlinear filtering in high dimension;
- the impracticality of exact filtering;
- the need for a deterministic approximation that still yields a stable analytical gradient;
- why this is not the same goal as building a full non-Gaussian density approximation.

This opening should orient the chair before introducing machinery.

### 2. FixedSGQF in one-page conceptual form

Before detailed derivation, explain the method as a sequence of three deliberate choices:

1. carry only a Gaussian surrogate for the filtering distribution;
2. estimate the required nonlinear moments by a sparse-grid rule rather than a full tensor or Monte Carlo method;
3. freeze the branch so that the differentiated quantity is the same deterministic scalar that the value path computes.

This should make the proposal intellectually legible before the notation expands.

### 3. Exact object, approximate object, and why the distinction matters

State with full clarity:

- the exact filtering recursion;
- the Gaussian object actually carried by FixedSGQF;
- the deterministic approximate likelihood scalar that is accumulated;
- what information about the full posterior is discarded.

This is not bureaucracy; it is the scientific heart of the proposal.

### 4. Why sparse-grid Gaussian moment approximation can still be plausible

Add a mature mathematical discussion of plausibility:

- low effective interaction order;
- local or blockwise dependence patterns;
- why sparse-grid rules buy economy in those regimes;
- why this argument weakens under strong multimodality, narrow ridges, or global coupling.

This section should read like scientific judgment, not defensive caveat language.

### 5. Fully self-contained reconstruction of the value path

The value-path derivation should be complete enough that an engineer can code it from the report alone.

This means P32 must explicitly provide:

- notation table or symbol reconciliation early enough to prevent reader overload;
- state-space model and filtering recursion;
- Gaussian projection moments;
- one-dimensional quadrature ingredients;
- tensor-product and sparse-grid construction;
- duplicate-node merging rule;
- point placement into physical coordinates;
- prediction moments;
- observation moments;
- innovation covariance and cross-covariance;
- likelihood scalar contribution;
- posterior Gaussian update.

Any hidden transition from source-paper formula to implementation object should be unpacked inside P32.

### 6. Fully self-contained reconstruction of the gradient path

The gradient material must answer the implementation question directly.

P32 should therefore make explicit:

- what branch data are frozen and why;
- what remains parameter-dependent on that branch;
- the derivative of the square-root/factor branch being used;
- prediction sensitivities;
- observation sensitivities;
- innovation-score derivative;
- posterior mean and covariance sensitivities;
- the recursion that carries derivative information to the next time step.

The engineer should not need to infer missing intermediate steps from terse identities.

### 7. One compact worked example that teaches the whole report

Add a worked one-step example that is small enough to read but complete enough to teach:

- prior or carried Gaussian;
- sparse-grid cloud;
- nonlinear observation transformation;
- innovation moments;
- approximate log-likelihood increment;
- posterior Gaussian update;
- one parameter derivative through the same branch.

Its role is to prove that the report is teachable, not just formally correct.

### 8. Relation to neighboring proposals

Explain clearly where FixedSGQF sits relative to:

- EKF / local linearization;
- sigma-point and Gauss--Hermite Gaussian filters;
- particle filtering;
- Zhao--Cui squared-TT filtering.

The goal is not to declare a winner. The goal is to help the chair understand why this proposal is a legitimate lane rather than an accidental hybrid.

### 9. Scholarly conclusion

End by telling the panel what a fair reading should conclude:

- what FixedSGQF contributes;
- what it sacrifices;
- where it is strongest;
- where it should not be oversold;
- why it remains a serious high-dimensional filtering proposal.

## Concrete revision priorities

### First priority: strengthen the report’s argument

Rewrite the opening and conclusion so the note reads as a defended scientific proposal rather than an expanded technical appendix.

### Second priority: make the derivation truly self-contained

Patch any place where the current note assumes the reader will mentally import details from Jia--Xin--Cheng, sparse-grid background, or earlier BayesFilter notes.

### Third priority: add the worked example

Use the example as the bridge between chair-readability and implementation completeness.

### Fourth priority: sharpen comparative interpretation

Make sure the panel can place the method in the broader filtering landscape without needing a separate survey document.

## What to avoid in the rewrite

Do not let P32 drift into:

- project-management tone;
- software-governance tone;
- checklist-heavy prose in the body;
- implementation instructions detached from mathematical motivation;
- comparisons that overstate what FixedSGQF can preserve relative to non-Gaussian methods.

## Success criterion

The rewrite succeeds only if both statements become true.

### Chair criterion

A former chemistry professor who is mathematically serious but not inside this exact subfield can read the report and say:

- I understand what problem this method is solving.
- I understand where the approximation enters and why it may be reasonable.
- I understand the limitations without feeling the proposal has become vague.
- I find the report thorough, self-contained, and persuasive enough to approve the work for this lane.

### Engineer criterion

An implementation engineer on the panel can read the report and, with Claude Code, implement the value-and-gradient method directly from P32 without consulting the original source papers.

## Planned execution after approval

If approved, the rewrite should proceed in this order:

1. rewrite the opening motivation and conceptual spine;
2. patch the value-path exposition for full self-containedness;
3. patch the gradient-path exposition for full self-containedness;
4. add the worked example;
5. rewrite the neighboring-method comparison;
6. tighten the conclusion around what the panel should fairly conclude.
