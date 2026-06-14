# P32 Subplan B — Value-Path Implementation Completeness

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md)

what_is_not_concluded:
- This subplan does not yet complete the gradient-path derivation.
- This subplan does not claim that the current P32 value path is incorrect; it claims only that it is not yet fully self-contained for implementation.
- This subplan does not replace the need for a worked example.

## Goal

Patch the value-path sections of P32 so that an implementation engineer can reconstruct the full FixedSGQF filtering recursion from the report alone.

## P32 sections to touch

Primary targets in the current note:

- `What This Note Computes`;
- `State-Space Model And Exact Filtering Recursion`;
- `Gaussian Projection From Moments`;
- `One-Dimensional Gaussian Quadrature And Tensor Products`;
- `Sparse-Grid Rule Reconstructed In Source Order`;
- `A Toy Fixed Grid With Duplicate Merging`;
- `FixedSGQF Filtering Value Path`;
- `Implementation Contract`;
- `End-To-End Mathematical Algorithm`.

## Expansion guardrail

This subplan must expand the value-path sections of the LaTeX report with missing formulas, contracts, and algorithm detail. It must not satisfy implementation completeness by replacing derivations with shorter paraphrase.

## Concrete edits to make

### 1. Add a symbol-and-object reconciliation block early in the value path

Before the main derivation becomes dense, insert a compact table or structured list that fixes:

- `\xi^{(r)}`: standard Gaussian quadrature nodes;
- `w^{(r)}`: associated weights after sparse-grid assembly and duplicate merge;
- `x^{(r)}`: physical state points under the carried Gaussian;
- `a^{(r)}`: transition images or predicted state points;
- `z^{(r)}`: observation images;
- `m_t^-`, `P_t^-`, `m_t`, `P_t`;
- `\bar z_t`, `S_t`, `C_{xz,t}`, `K_t`, `v_t`, `\ellhat_t`.

The purpose is to stop notation drift between conceptual coordinates and implementation objects.

### 2. Make the prediction path completely explicit

The report must say exactly how the predictive Gaussian is formed.

That includes:

- whether additive transition noise enters by analytic covariance addition, by state augmentation, or by another stated route;
- the exact sparse-grid sums used for predictive mean and covariance;
- the shape of each predictive object;
- whether covariance symmetrization is assumed after finite-precision accumulation;
- what positive-definiteness requirement is imposed before proceeding.

If the note currently leaves any of these implicit, add them.

### 3. Make the observation-moment path completely explicit

In `FixedSGQF Filtering Value Path`, the report must provide the exact implementation sequence:

1. place the cloud in physical coordinates;
2. evaluate the transition map;
3. evaluate the observation map;
4. compute the approximate observation mean `\bar z_t`;
5. compute the innovation covariance `S_t`;
6. compute the cross-covariance `C_{xz,t}`;
7. form `v_t`, `K_t`, `m_t`, `P_t`, and `\ellhat_t`.

Each line should state whether it is an expectation, a weighted finite sum, a linear algebra solve, or a branch check.

### 4. Expand the sparse-grid assembly into an implementation-level recipe

The current sparse-grid reconstruction should be made precise enough to code.

Add explicit statements for:

- how the multi-index set is enumerated;
- how Smolyak coefficients are attached;
- how tensor-product nodes are mapped into one merged cloud;
- how duplicate nodes are identified and combined;
- what ordering, if any, is assumed for the merged cloud;
- what exact weight object is stored after merging.

If P32 already gives the mathematics, this subplan requires turning it into a sequence that an engineer can implement without guessing ordering or merging semantics.

### 5. Turn the toy duplicate-node section into a coding bridge

The current toy grid should not remain purely illustrative.

Add to it:

- a short algorithmic explanation of the duplicate-merge operation;
- a statement of the final stored node/weight dictionary;
- a sentence explaining why the merged cloud is the object reused by the value and gradient paths.

### 6. Expand the implementation contract for the value path

The current `Implementation Contract` section should explicitly list, for the value path alone:

- required inputs at each time step;
- saved branch data;
- required matrix shapes;
- branch-failure conditions;
- exact outputs passed to the next step.

In particular, the engineer should know whether the next step receives only `(m_t, P_t)` or also saved cloud/factor information.

### 7. Upgrade the end-to-end algorithm into a true implementation recipe

The `End-To-End Mathematical Algorithm` should become a numbered step sequence that an engineer can translate nearly line-for-line into code.

It should separate:

- one-time setup: sparse-grid construction and merge;
- per-time-step prediction;
- per-time-step observation update;
- scalar accumulation;
- branch validity checks;
- state carried forward.

The algorithm should also explicitly state the order in which linear algebra operations occur.

### 8. Add a notation and formula inventory hook

The value-path sections must participate in the report-wide notation/formula inventory required by the master program.

For the value path specifically, the inventory must point the reader to:

- the symbol-and-dimension table;
- the predictive-moment equations;
- the observation-moment equations;
- the update equations;
- the scalar increment definition;
- the value-path algorithm block;
- the value-path branch checks and numerical conventions.

This hook is required so an implementation engineer can find the full value recursion without hunting through the report.

## Mandatory implementation deliverables from this subplan

The value-path rewrite is not complete unless P32 contains all of the following:

1. **A notation and dimension table** for the main value-path objects.
2. **An explicit step input/output contract** that states what enters and leaves one filtering step.
3. **All value-path formulas** for predictive moments, observation moments, update quantities, and scalar increment.
4. **A sparse-grid construction recipe** detailed enough to code without Jia--Xin--Cheng open beside the report.
5. **A value-path algorithm block** in implementation order.
6. **An explicit numerical convention paragraph** stating factorization choice, solve-vs-invert convention, and positive-definiteness/failure behavior.
7. **A value-path inventory entry** that maps the value recursion formulas, algorithm block, and branch checks to exact report locations.

If any of these seven items is absent, the engineer criterion is not met for the value path.

## Specific hidden gaps this subplan must eliminate

This subplan is successful only if P32 no longer requires the engineer to infer:

- how additive noise enters the predictive moments;
- whether observation moments use predicted-state or pre-noise states;
- how the merged sparse-grid cloud is stored and reused;
- what exact object is inverted or factorized in the innovation step;
- what exactly is propagated to the next time step.

## Engineer-facing success test

After this rewrite, an engineer should be able to sit with only P32 and write:

- sparse-grid cloud construction;
- prediction/update loops;
- likelihood accumulation;
- branch checks for the value path.

No return to Jia--Xin--Cheng should be required for missing implementation semantics.

## Risks to guard against

- Do not bury the implementation details inside long prose paragraphs.
- Do not rely on “similarly” or “analogously” where an explicit formula is needed.
- Do not let the algorithm section disagree with earlier derivation notation.
- Do not overcomplicate the value path with derivative details that belong in Subplan C.

## Block review gate

After the value-path block is drafted, it must be reviewed by the opposite agent family before any gradient-path drafting begins.

The review must check:

- whether every carried object, moment, and update quantity is defined before use;
- whether the sparse-grid assembly and duplicate-merge semantics are implementable without outside sources;
- whether the algorithm block matches the derivation notation exactly;
- whether the value-path inventory entry is present and accurate;
- whether the block expanded the LaTeX report rather than replacing derivations with prose compression.

Only after that review passes should the rewrite proceed to Subplan C.

## Done criterion

This subplan is complete only if the value recursion is reconstructible from P32 alone, with explicit notation, formulas, algorithm order, and numerical conventions, and without hidden bridges from source-paper formulas to code objects.
