# P16 Zhao-Cui Fixed-Branch Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.
- P15 fixed-branch implementability specification.

what_is_not_concluded:
- No claim that Zhao--Cui's adaptive implementation is globally differentiable.
- No posterior accuracy claim.

## Fixed Objects

The P16 note requires freezing domain maps, basis families, fitting points,
weights, ranks, core-construction sequence, regularization, defensive reference,
defensive mass, scaling shifts, preconditioner branch, and rootfinding branches.

## Proposition

P16 Proposition 1 proves normalization for the declared approximate recursion.
It does not prove equality to the exact posterior.

Decision: `FIXED_BRANCH_SCOPE_EXPLICIT`
