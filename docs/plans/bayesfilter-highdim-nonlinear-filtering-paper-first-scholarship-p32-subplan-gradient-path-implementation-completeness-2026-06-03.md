# P32 Subplan C — Gradient-Path Implementation Completeness

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md)

what_is_not_concluded:
- This subplan does not claim differentiability of adaptive branch changes.
- This subplan does not replace the need for the value-path subplan.
- This subplan does not certify every matrix derivative by machine proof.

## Goal

Patch the gradient-path sections of P32 so that the fixed-branch analytical gradient can be implemented from the report alone.

## P32 sections to touch

Primary targets in the current note:

- `The Saved Scalar And Same-Scalar Contract`;
- `Analytical Gradient Of The Fixed Scalar`;
- `One Boxed Mathematical Algorithm`;
- `Implementation Contract`;
- `End-To-End Mathematical Algorithm`;
- `Finite-Difference Same-Scalar Check`.

## Expansion guardrail

This subplan must expand the gradient-path sections of the LaTeX report with explicit derivative machinery, branch semantics, and implementation ordering. It must not compress these sections into high-level summaries.

## Concrete edits to make

### 1. Define the frozen branch data exactly

The note must explicitly define the branch object `B_t` or its equivalent.

It should state whether the fixed branch includes:

- sparse-grid level choice;
- merged node set;
- merged weight vector;
- coordinate ordering;
- duplicate-merge map;
- factorization branch for covariance square roots;
- any acceptance/veto thresholds that decide whether the branch is valid.

This list should appear once, clearly, and then be referenced consistently.

### 2. Separate fixed structural objects from parameter-dependent numerical objects

Add a subsection that answers:

- what is frozen when the branch is declared;
- what remains a differentiable function of `\theta` within that branch;
- what is recomputed at perturbed parameter values during same-scalar finite differences.

This should prevent the engineer from confusing “branch fixed” with “all intermediate values fixed.”

### 3. Make the factor-derivative path implementable

The current `Square-Root Branch` subsection should be expanded until the engineer can code it.

The report should specify:

- what factorization is assumed (`P = CC^\top` with a named branch convention);
- what equation determines `\dot C` from `\dot P` on that branch;
- whether the factor is Cholesky, symmetric square root, or another fixed choice;
- what triangular or symmetry constraints are imposed to make `\dot C` unique.

If the main body becomes too cluttered, the derivation can be split between the main text and a local proposition, but the implementation formula itself must remain in the body.

### 4. Add the full derivative dependency chain

The note should provide the derivative sequence in explicit implementation order:

1. `\dot x^{(r)}` from `\dot m` and `\dot C`;
2. `\dot a^{(r)}` through the transition map;
3. `\dot z^{(r)}` through the observation map;
4. `\dot{\bar z}_t`;
5. `\dot S_t`;
6. `\dot C_{xz,t}`;
7. `\dot v_t` and `\dot K_t`;
8. `\dot m_t` and `\dot P_t`;
9. `\dot\ell_t`.

Each object should be identified as a weighted sum, Jacobian action, matrix solve, or product rule application.

### 5. Make the innovation-score derivative explicit

The report should not assume the engineer can fill in the scalar derivative from familiarity.

It should explicitly derive the derivative of

- `\log\det S_t`;
- `v_t^\top S_t^{-1} v_t`;
- the combined innovation log-likelihood term.

This is one of the most likely places an implementation engineer would otherwise rely on external notes.

### 6. Make the posterior sensitivity propagation explicit

The report must show how derivative information is carried to the next time step.

That means the note should state clearly:

- what derivative objects are propagated along with the value-path objects;
- how `\dot m_t` and `\dot P_t` become inputs to the next prediction step;
- whether the next-step factor derivative uses only `\dot P_t` or also stored factor data from the current step.

### 7. Rewrite the boxed algorithm to include derivative ordering

The `One Boxed Mathematical Algorithm` and `End-To-End Mathematical Algorithm` should be upgraded so the derivative pass is not merely described but sequenced.

The algorithm should make clear:

- what must already be available from the value pass;
- what can be reused exactly;
- what is recomputed numerically on the fixed branch;
- what order of matrix operations avoids ambiguity.

### 8. Strengthen the finite-difference same-scalar section

The finite-difference section should say exactly what is held fixed during the check:

- cloud structure;
- weights;
- coordinate order;
- factorization branch;
- veto rules.

It should also say exactly what is recomputed at perturbed parameters:

- moments;
- innovation quantities;
- posterior update quantities;
- scalar value.

Finally, it should explain what constitutes branch mismatch and why branch mismatch invalidates the comparison rather than merely creating numerical noise.

## Branch identity and mismatch decision table

The rewritten report must include one explicit branch-identity table or decision block that removes all ambiguity about when two evaluations are considered to be on the same branch.

At minimum, the table must contain the following columns:

- object or decision component;
- part of branch identity? (`yes`/`no`);
- how equality is judged;
- consequence of mismatch.

The rows must include at least:

- sparse-grid level choice;
- index-set convention;
- merged node set;
- merged node ordering;
- merged weight vector;
- duplicate-merge convention and any tolerance rule;
- covariance factorization family;
- factorization branch choices internal to that family;
- branch-validity or veto thresholds.

The report must also state one deterministic mismatch policy. For example, if any branch-identity row marked `yes` changes between the central and perturbed evaluations, the finite-difference comparison is declared invalid rather than interpreted as numerical error.

This table is mandatory because same-branch language is otherwise too easy to interpret loosely.

## Mandatory implementation deliverables from this subplan

The gradient-path rewrite is not complete unless P32 contains all of the following:

1. **A frozen-branch contract** listing every object that defines branch identity.
2. **A fixed-versus-variable object contract** distinguishing structural branch choices from parameter-dependent numerical quantities.
3. **An explicit factor-derivative recipe** with the governing equation and uniqueness convention.
4. **All gradient formulas** for moment sensitivities, innovation-score derivative, posterior sensitivities, and propagated derivative state.
5. **A gradient-path algorithm block** in implementation order.
6. **A same-branch finite-difference contract** specifying what is fixed, what is recomputed, and what invalidates the comparison.
7. **A branch identity and mismatch decision table** that states exactly how branch sameness is judged and what happens when it fails.

If any of these seven items is absent, the engineer criterion is not met for the gradient path.

## Specific hidden gaps this subplan must eliminate

This subplan is successful only if P32 no longer leaves the engineer to infer:

- the exact contents of the frozen branch;
- how the factor derivative is computed;
- how the innovation-score derivative is assembled;
- how posterior sensitivities are propagated to the next time step;
- what same-scalar finite differences actually hold fixed.

## Engineer-facing success test

After this rewrite, an engineer should be able to write a full fixed-branch gradient routine from P32 alone, including:

- derivative-aware cloud placement;
- sensitivity accumulation for moments;
- innovation-score derivative;
- posterior sensitivity update;
- finite-difference branch-consistency check.

## Risks to guard against

- Do not hide derivative assumptions inside prose caveats.
- Do not state only high-level matrix identities when the implementation needs an ordered computation.
- Do not claim derivative validity across branch changes.
- Do not let the finite-difference section become a generic gradient-check paragraph; it must remain same-scalar specific.

## Block review gate

After the gradient-path block is drafted, it must be reviewed by the opposite agent family before the worked-example block is finalized.

The review must check:

- whether the frozen-branch contract is explicit and internally consistent;
- whether the factor-derivative convention is fully pinned down;
- whether the branch identity and mismatch decision table is operational rather than aspirational;
- whether the gradient algorithm block matches the derivation ordering;
- whether the finite-difference semantics truly compare the same scalar on the same branch.

Only after that review passes should the rewrite proceed to Subplan D completion.

## Done criterion

This subplan is complete only if the fixed-branch value-and-gradient recursion is implementable from P32 alone, with explicit branch contracts, formulas, algorithm order, and finite-difference semantics, and with no missing derivative bridges.
