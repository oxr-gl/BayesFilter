# P2 Mathematical Foundations Chapter Plan

## Question

What self-contained notation and derivations are needed before comparing
high-dimensional nonlinear filters and HMC targets?

## Evidence Contract

Baseline:

- Existing BayesFilter state-space and HMC target chapters.
- V1 target-contract evidence.

Primary criterion:

- The foundations chapter states nonlinear SSM notation, filtering recursion,
  likelihood recursion, posterior target, degeneracy mechanisms, and ledger
  separation in BayesFilter notation, with labeled derivation blocks for core
  identities.
- For scholarly readiness, each major identity must include assumptions,
  a proof or derivation sketch, a MathDevMCP audit attempt where feasible, and
  a clear statement of what the identity does not imply for approximate filters
  or HMC targets.

Veto diagnostics:

- Filtering likelihood and posterior target are conflated.
- Approximate likelihoods are described as exact without a special structure.
- HMC target validity is inferred from value-only evidence.
- A major identity is left as informal exposition without being marked as a
  blocker for final scholarly acceptance.

Explanatory diagnostics:

- MathDevMCP derivation audit availability.

Non-implications:

- Passing P2 does not certify any numerical algorithm.

Artifact:

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`

## MathDevMCP Use

Audit, or explicitly downgrade, at least:

- filtering prediction/update recursion;
- likelihood factorization;
- posterior target decomposition;
- approximate-target boundary for sigma-point and particle filters.

An unaudited mathematical identity may remain only as informal exposition and
must be listed in the unresolved-claim register.
For final scholarly acceptance, an unaudited major identity must either receive
a successful/manual audit recorded in the ledger or be demoted so it is no
longer a load-bearing chapter claim.

## Stop Rules

Stop P2 with a blocker if the filtering recursion or likelihood factorization
cannot be stated in labeled form, audited by MathDevMCP, or downgraded without
damaging the chapter's purpose.

Stop P2 scholarly refinement with a blocker if any major equation lacks
assumptions, a derivation/proof sketch, audit evidence or audit limitation, and
a non-implication boundary.

## Exit Label

`P2_FOUNDATIONS_ACCEPTED` if the chapter is self-contained and derivation
claims are auditable or explicitly informal.

`P2_SCHOLARLY_DERIVATIONS_ACCEPTED` only if no load-bearing identity remains
merely informal.
