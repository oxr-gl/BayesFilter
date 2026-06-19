# Integration Audit: Expanded High-Dimensional Block After First Migration Sweep

**Date:** 2026-06-15  
**Scope:** `docs/main.tex`, `ch33`, and the expanded `ch34`--`ch38` sequence

## Overall assessment

The expanded high-dimensional block is now in the **right chapter shape** and the
monograph remains build-green, but the first migration sweep is still closer to
an architecture activation than to a full source-faithful rewrite.  The sequence
in `docs/main.tex`

1. `ch33` exact foundations,
2. new `ch34` deterministic Gaussian / point-rule foundations,
3. new `ch35` sparse-grid / fixed-cloud method chapter,
4. new `ch36` low-rank retained-object TT/KR chapter,
5. new `ch37` shared fixed-branch same-scalar chapter,
6. new `ch38` validation / defect / promotion closeout,

is conceptually coherent and now reads as a true high-dimensional block rather
than the earlier compressed `ch33`--`ch37` structure.  But it still does not yet
carry the full explanatory weight of `p47` and `p50` in a monograph-native way.
The largest remaining gap is **deep source migration**, especially into `new
ch36`, then `new ch35`.

## Best-integrated chapters right now

### 1. `ch33` — shared exact-target foundation
- [docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex](docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex)
- Still the strongest chapter in terms of monograph voice, exact-target framing,
  and exported defect package.

### 2. `ch38` — closeout architecture
- [docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex](docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex)
- After the front rewrite, it now functions clearly as the downstream consumer of
  the block’s methods and diagnostics.
- It is a strong closeout chapter structurally, even if some inherited synthesis
  body remains.

## Chapters still most visibly inherited / seeded

### Highest priority: `new ch36`
- [docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex](docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex)
- This is now the chapter with the largest remaining mismatch between its role and
  its inherited body.
- The front architecture is good, but the body still behaves too much like the old
  broad survey chapter:
  - particles,
  - generic transport,
  - TT/QTT PDE filters,
  - TT/KR,
  - TN covariance compression,
  all still share too much weight.
- This is the clearest unresolved p50 fidelity problem.

### Second priority: `new ch35`
- [docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex](docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex)
- The role is now much clearer, but the chapter still carries the largest seeded
  body from the old compressed `ch34`.
- It remains too long and still lacks the strongest possible explicit closing
  export ledger for the fixed-cloud scalar / sparse-grid method chapter.

### Third priority: `new ch37`
- [docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex](docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex)
- Its front architecture is now correct, but the body remains too thin for such a
  central shared abstraction chapter.
- It still relies on inherited HMC-consequence material and transitional
  compatibility labels rather than a fully developed cross-method branch-record /
  scalar-identity narrative.

### Fourth priority: `new ch34`
- [docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex](docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex)
- It is structurally improved and conceptually aligned, but still retains a large
  amount of inherited `p47` front-matter cadence and old label namespace.
- It is the least urgent of the four because its role is now at least clear.

## Where import/export handoffs are strongest vs weakest

### Strong handoffs
- `ch33` -> later chapters: exact target and defect package remain explicit.
- `ch37` -> `ch38`: the fixed-branch / same-scalar consequences now feed a clear
  downstream validation/promotion architecture.
- `ch38` -> later HMC part: now behaves more clearly as a high-dimensional
  closeout rather than a duplicated HMC tutorial.

### Weakest handoff: `ch34` -> `ch35`
- `new ch34` now states the bridge to sparse-grid specialization clearly, but it
  is still under-consumed in the formal import graph because later chapters
  primarily recognize the sparse-grid lane through the old compatibility label
  attached to `new ch35`.
- The conceptual foundation is right; the chapter-to-chapter contract could still
  be more explicit and more monograph-native.

### Second-weakest handoff: `ch35` -> `ch37`
- `new ch35` promises a fixed-cloud scalar that later chapters consume.
- `new ch37` does consume that role.
- But `new ch35` still needs a more explicit closing export package comparable to
  `ch33` and `ch36` so the handoff feels architectural, not implied.

### Medium-strength handoff: `ch36` -> `ch37`
- Better than before because `new ch36` now has a more explicit front role and a
  cleaner exported boundary.
- Still somewhat underpowered because the retained-object scalar and branch-local
  implications are not yet carried with enough p50-specific procedural weight.

## Old compressed-architecture residue still visible

The most visible remaining residues are:
- compatibility alias labels in the new files,
- inherited p-number label namespaces,
- old short titles / role names retained to preserve compilation continuity,
- seeded section organization that still reflects old combined chapters more than
  the new architecture.

This no longer blocks the build, but it still prevents the block from feeling
fully re-authored.

## Biggest remaining source-migration gaps

### p47 gap
- `new ch35` still contains the right material mass, but not yet the strongest
  contract-first sparse-grid method packaging.
- The pedagogical ladder survives, but the exported scalar/branch/method identity
  is not yet as explicit and clean as it should be for a chapter that must replace
  the need to read p47 directly.

### p50 gap
- `new ch36` still under-carries the algorithmic retained-object / coordinate /
  KR / squared-density object-flow burden from p50.
- This remains the single largest fidelity loss in the expanded architecture.

## Highest-value next rewrite priorities

### Priority 1 — Deep rewrite `new ch36`
- [docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex](docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex)
- Restore more of:
  - coordinate systems,
  - retained-object flow,
  - squared-density object logic,
  - conditional KR map role,
  - algorithmic carried-object continuity.

### Priority 2 — Deep rewrite `new ch35`
- [docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex](docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex)
- Add a clearer export contract and tighten the sparse-grid method identity so the
  chapter reads less like a long inherited packet and more like a purpose-built
  method chapter.

### Priority 3 — Deepen `new ch37`
- [docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex](docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex)
- Build out a fuller branch-record / scalar-identity / finite-difference logic so
  the chapter becomes a true cross-method derivative chapter rather than a thin
  bridge with compatibility labels.

### Priority 4 — Final normalization of `new ch34`
- [docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex](docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex)
- Finish the monograph-voice and label normalization once the downstream method
  chapters are more stable.

## Recommended next move

Proceed with the **deep rewrite of `new ch36`** as the next active migration step.
That is now the chapter with the highest combination of:
- architectural importance,
- remaining inherited-seed residue,
- and fidelity loss versus the p50 source manuscript.

After that, the next best target should be `new ch35`.

## Conclusion

The architecture expansion succeeded.  The first migration sweep succeeded.  The
expanded block is now readable as a sequence and still compiles cleanly.  The
remaining work is no longer architecture rescue or build repair; it is **deep
source migration**, with `new ch36` now the most important unresolved chapter.