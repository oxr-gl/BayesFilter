# R4 Cutover Judgment: Restarted High-Dimensional Staging Block

**Date:** 2026-06-15  
**Runbook gates:** `R4` from `docs/plans/bayesfilter-highdim-monograph-restart-runbook-2026-06-15.md` and cutover criteria from `docs/plans/bayesfilter-highdim-monograph-restart-cutover-audit-plan-2026-06-15.md`

## Scope

Final substantive judgment on the restarted staging surface after:
- source-truth staging rewrites of `ch34`--`ch38`,
- whole-book staging driver correction,
- whole-book reference-cleanliness cleanup.

Reviewed surface:
- `docs/main_highdim_restart_staging.tex`
- `docs/main_highdim_restart_staging.pdf`
- `docs/chapters_restart_staging/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
- `docs/chapters_restart_staging/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
- `docs/chapters_restart_staging/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
- `docs/chapters_restart_staging/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters_restart_staging/ch38_highdim_validation_defect_calculus_and_promotion.tex`

## Technical cutover prerequisites

### Build status
Command run:
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- `docs/main_highdim_restart_staging.pdf` was written successfully.
- Current staged PDF length: 272 pages.
- No fatal LaTeX errors remain.
- No undefined-reference warnings remain.
- No undefined-citation warnings remain.

Technical R4 blockers are therefore cleared.

## Substantive cutover judgment

### 1. Does the staged block actually carry p47 and p50 material rather than merely summarizing it?
Judgment: **yes, materially enough for the assigned chapter roles.**

- `staging ch34` now clearly carries the p47 foundations burden:
  deterministic Gaussian carried object, exact filtering / Gaussian projection,
  deterministic point-rule family language, and export to sparse-grid
  specialization.
- `staging ch35` now clearly carries the p47 sparse-grid / fixed-cloud method
  burden:
  low-dimensional cloud construction, active bands, Smolyak structure, merged
  cloud object, filtering value path, and fixed-cloud scalar export.
- `staging ch36` now clearly carries the p50 retained-object burden:
  recursive bottleneck, coordinate systems, retained-object flow, TT toolkit,
  rank plausibility, KR maps, and squared-density / retained-object recursion.
- `staging ch37` now clearly carries the shared fixed-branch burden drawn from
  p47 and p50:
  branch identity, fixed-vs-differentiable ledgers, finite-difference
  branch-validity logic, value-path vs derivative-path distinction, and
  exact-target vs approximate-target HMC admissibility boundaries.
- `staging ch38` now clearly carries the shared validation / promotion burden:
  validation ledgers, finite-difference parity gate, benchmark roles, defect
  calculus, and promotion logic.

### 2. Are chapter boundaries aligned with the intended architecture?
Judgment: **yes.**

The staging block now reads as:
1. exact foundations (`ch33`),
2. deterministic Gaussian / point-rule foundations,
3. sparse-grid / fixed-cloud method,
4. retained-object TT/KR lane,
5. shared fixed-branch same-scalar contract,
6. validation / defect / promotion closeout.

This matches the restart crosswalk and no longer relies on the compressed
five-chapter legacy structure.

### 3. Does the staged block read as part of the monograph rather than as appended source-note prose?
Judgment: **mostly yes, with manageable residual caution.**

The restarted chapters now read as a sequence rather than as appended note
fragments. The largest residual issue is not chapter-role confusion but normal
migration residue:
- inherited label namespaces,
- compatibility labels,
- and some remaining local source cadence.

These are real polish issues but no longer enough, in my judgment, to block the
whole-block architectural cutover.

### 4. Are references, bibliography, labels, and source-map / reset-memo links clean enough for canonical use?
Judgment: **yes, for the staging high-dimensional block surface.**

The corrected whole-book staging build is now reference-clean.  The remaining
issue is not technical cleanliness but whether the source-fidelity and whole-book
fit are strong enough to justify switch.

### 5. Does the handoff from the restarted block to the later HMC part make sense at the whole-book level?
Judgment: **yes.**

The block now ends with:
- retained-object method chapter,
- shared fixed-branch/same-scalar contract chapter,
- validation/promotion closeout,
then hands off to the generic HMC part.

This is now a better whole-book shape than the earlier compressed architecture.
The restarted block specializes high-dimensional filtering objects and leaves the
generic sampler doctrine to the later HMC part.

## Remaining caution

The only substantive caution I would keep on record is this:
- the p50 lane in `staging ch36` is now materially present and no longer summary-only,
  but some of the richest route-specific operational detail from the source
  manuscript is still compressed relative to the original companion note.

I do **not** think this remaining compression is severe enough to block cutover
under the current chapter-role contract. The current staged set now plausibly
replaces the need to read p47 and p50 for the monograph’s canonical high-
dimensional block, even if the source manuscripts remain richer technical
companions.

## Gate status

- `G4` staging verification: **PASS**
- Token: `PASS_R4_CUTOVER_PREFLIGHT_READY`

## Recommendation

Proceed to **R5 canonical cutover**.

The technical blockers are cleared, the staged block now materially carries the
p47/p50 burden in chapter form, the architecture is coherent, and whole-book
fit is acceptable for canonical switch. Any remaining work should be treated as
post-cutover refinement rather than as a reason to keep the canonical surface in
a failed/non-canonical state.
