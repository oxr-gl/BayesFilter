# Integration Audit: Expanded High-Dimensional Block After Architecture-Normalization Sweep

**Date:** 2026-06-15  
**Scope:** `docs/main.tex`, `ch33`, and the expanded `ch34`--`ch38` block

## Overall assessment

The expanded high-dimensional block is now **architecturally coherent** and the
monograph remains build-green, but it is not yet deeply rewritten enough to feel
fully monograph-native.  The sequence in `docs/main.tex`

1. `ch33` exact foundations,
2. new `ch34` deterministic Gaussian / point-rule foundations,
3. new `ch35` sparse-grid / fixed-cloud method chapter,
4. new `ch36` low-rank retained-object TT/KR chapter,
5. new `ch37` shared fixed-branch same-scalar chapter,
6. new `ch38` validation / defect / promotion closeout,

is conceptually right.  The main remaining issue is that the **architecture has
outrun the full source migration**: several chapters now have the right role, but
still carry inherited seeded material from the old compressed architecture.

## Best-integrated chapters right now

### 1. `ch33` foundations
- [docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex](docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex)
- Still the cleanest and most normalized chapter in the block.
- Its exact-target / normalizer / same-scalar defect export still functions well
  as the shared foundation.

### 2. `ch38` validation / promotion closeout
- [docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex](docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex)
- After the front rewrite, it now clearly reads as the downstream consumer of the
  block’s methods, not merely a leftover synthesis note.
- The validation-ledger framing is now a strong architectural close for the
  expanded block.

## Chapters that still most visibly read like inherited seeded material

### Highest priority: `ch35`
- [docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex](docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex)
- Why:
  - It remains very large and still feels like the largest surviving seeded chunk.
  - It still carries mixed internal label residue and an older combined
    Gaussian/quadrature identity.
  - It promises a fixed-cloud scalar export, but does not yet close with an
    export contract as explicit as `ch33`, `ch36`, or `ch38`.
- High-level diagnosis:
  - This chapter is doing the right job, but still in the voice and pacing of an
    inherited source-heavy packet rather than a contract-first monograph chapter.

### Second priority: `ch36`
- [docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex](docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex)
- Why:
  - The front architecture is improved, but the body is still survey-like and
    too broad for the chapter role.
  - It still reads as if it has not fully decided whether it is:
    - a broad non-Gaussian alternatives chapter, or
    - the true p50 retained-object chapter.
- High-level diagnosis:
  - This is now better framed, but still the largest unresolved p50 fidelity gap.

### Third priority: `ch37`
- [docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex](docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex)
- Why:
  - The new front architecture is correct, but the chapter is still short and its
    body remains partly inherited from the old HMC-consequence chapter.
  - It works as a bridge chapter, but does not yet feel fully inhabited as the
    shared fixed-branch same-scalar chapter.
- High-level diagnosis:
  - This chapter is structurally correct, but still underdeveloped relative to its
    architectural importance.

### Lower priority: `ch34`
- [docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex](docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex)
- Why:
  - The role is now much clearer.
  - But it still carries old “note”-style cadence, old label namespaces, and some
    lingering whole-lane implications that belong in `ch35`.
- High-level diagnosis:
  - It is conceptually sound, but still needs final monograph normalization once
    the next deeper method rewrites are done.

## Where import/export handoffs are weakest

### Weakest handoff: `ch34` → `ch35`
- `ch34` now correctly declares itself as deterministic Gaussian / point-rule
  foundations and points into sparse-grid specialization.
- But the later block still mostly imports the old alias role attached to `ch35`
  when referring to the Gaussian/quadrature lane.
- This means `ch34` is conceptually foundational but under-consumed in the formal
  import graph.

### Second-weakest handoff: `ch35` → `ch37`
- `ch35` promises to export the fixed-cloud scalar into later derivative/promotion
  logic.
- `ch37` consumes that scalar role.
- But `ch35` still lacks the strongest possible explicit export ledger for that
  handoff.

### Better handoff: `ch36` → `ch37`
- `ch36` now has a cleaner front role and still retains a usable downstream export
  boundary.
- The problem there is less missing handoff and more underdeveloped source-level
  explanatory weight.

### Strong handoffs
- `ch33` → later chapters
- `ch37` → `ch38`

These now read more clearly than the interior method-to-method transitions.

## Old compressed-architecture residue still visible

The biggest visible residues are:
- compatibility alias labels on the new files,
- mixed old p-number label namespaces,
- older short titles and role names that still reflect the compressed block,
- inherited table/section organization that still assumes the old chapter was
  doing more than the new role should allow.

This residue does not currently break the build, but it does keep the block from
feeling fully re-authored.

## Biggest remaining source-migration gaps

### p47 fidelity gap
The new `ch35` still has the right content mass, but not yet the right
contract-first sparse-grid chapter structure.  The explanatory ladder survives,
but the chapter does not yet package its exports cleanly enough for the expanded
block.

### p50 fidelity gap
The new `ch36` still under-carries the algorithmic retained-object / coordinate-
system / object-flow burden from p50.  This is now the single biggest fidelity
loss in the expanded architecture.

## Highest-value next rewrite priorities

### Priority 1 — Deep rewrite `new ch36`
- Goal: make it a true p50 retained-object chapter rather than a broad survey.
- Restore more of:
  - coordinate systems,
  - retained-object flow,
  - squared-density object logic,
  - TT/KR operational object continuity.

### Priority 2 — Deep rewrite `new ch35`
- Goal: make it a contract-first sparse-grid method chapter.
- Add a clear closing export ledger and better chapter-local identity.
- Reduce old mixed-role residue.

### Priority 3 — Strengthen `new ch37`
- Goal: give the shared fixed-branch chapter more of the actual branch-record /
  scalar-identity / finite-difference logic that currently still lives only by
  implication or inherited carryover.

### Priority 4 — Final normalization pass on `new ch34`
- Goal: complete the conversion from seeded front matter to monograph-native
  foundational chapter once the downstream chapters are more stable.

## Recommended next move

The next best deep rewrite target is:
- [docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex](docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex)

Reason:
- it is now the chapter with the largest remaining fidelity gap to its source base
  and the clearest tension between architecture and inherited seeded body.
- fixing it will also clarify what `ch37` should import and what `ch38` should
  validate/promote.

After that, the next target should be:
- [docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex](docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex)

## Conclusion

The expansion succeeded architecturally.  The block is now in the right chapter
shape and still compiles.  The work that remains is no longer architecture repair;
it is **deep source migration**.  The first sweep made the block readable as a
sequence.  The next sweep should make its heaviest chapters actually carry the
explanatory burden of `p47` and `p50` in their new roles.