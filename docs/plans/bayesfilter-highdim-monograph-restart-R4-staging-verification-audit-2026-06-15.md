# R4 Staging Verification Audit: Whole-Block Review Of Restarted P47+P50 Candidate

**Date:** 2026-06-15  
**Runbook gate:** `R4` from `docs/plans/bayesfilter-highdim-monograph-restart-runbook-2026-06-15.md`

## Scope

Whole-block review of the restarted staging surface:
- `docs/main_highdim_restart_staging.tex`
- `docs/chapters_restart_staging/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
- `docs/chapters_restart_staging/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
- `docs/chapters_restart_staging/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
- `docs/chapters_restart_staging/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- `docs/chapters_restart_staging/ch38_highdim_validation_defect_calculus_and_promotion.tex`

## Build result

Command run:
```bash
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main_highdim_restart_staging.tex
```

Observed:
- `docs/main_highdim_restart_staging.pdf` was written successfully.
- Current staged PDF length: 259 pages.
- No fatal LaTeX errors occurred.

## Source-fidelity judgment by chapter role

### Staging `ch34` — deterministic Gaussian / point-rule foundations
Status: **pass** for assigned role.
- The chapter now clearly owns deterministic Gaussian carried object,
  exact filtering / Gaussian projection, deterministic point-rule family language,
  and the bridge into sparse-grid specialization.
- This is plausibly sufficient to replace the need to read the p47 foundations
  material for this chapter role.

### Staging `ch35` — sparse-grid / fixed-cloud method chapter
Status: **pass** for assigned role.
- The chapter now clearly owns low-dimensional cloud construction, active bands,
  Smolyak structure, the fixed merged cloud, filtering value path, worked
  fixed-cloud scalar example, and explicit export of the forward sparse-grid
  scalar.
- This is plausibly sufficient to replace the need to read the p47 sparse-grid
  method burden for this chapter role.

### Staging `ch36` — retained-object TT/KR chapter
Status: **pass with caution**.
- The chapter now clearly carries the exact recursive bottleneck,
  coordinate systems, retained-object flow, TT toolkit, rank plausibility,
  conditional KR maps, and squared-density / retained-object recursion.
- Compared with the failed/non-canonical state, this is a major fidelity
  recovery.
- Remaining caution: some of the richer p50 operational walkthroughs and
  algorithm-level concretization are still compressed.  The reader can now follow
  the lane, but some of p50’s “executable in the reader’s head” density is still
  lighter than in the source manuscript.

### Staging `ch37` — shared fixed-branch / same-scalar chapter
Status: **pass** for assigned role.
- The chapter now clearly owns branch identity, fixed structural vs recomputed
  numerical ledgers, finite-difference branch-validity logic, value-path vs
  derivative-path distinction, and exact-target vs approximate-target HMC
  admissibility boundaries.
- This is plausibly sufficient for the shared fixed-branch contract role.

### Staging `ch38` — validation / defect / promotion closeout
Status: **pass with caution**.
- The chapter now clearly owns validation architecture, benchmark roles,
  finite-difference parity as a first shared gate, downstream defect calculus,
  and promotion logic.
- Remaining caution: the benchmark architecture is strong, but some of the richer
  p50 route-specific validation depth is still compressed into summary-level
  logic.

## Whole-block integration judgment

The staged block now does substantially more than merely demonstrate structural
plausibility.  It carries real p47/p50 material chapter-by-chapter, and the
expanded architecture is readable as a coherent sequence:

1. exact foundations,
2. deterministic Gaussian / point-rule foundations,
3. sparse-grid / fixed-cloud method,
4. retained-object TT/KR lane,
5. shared fixed-branch same-scalar contract,
6. validation / defect / promotion closeout.

The main remaining blockers are therefore not chapter-role confusion, but
cutover-safety issues.

## Cutover blockers

### Blocker 1 — inherited whole-book undefined references remain present in staging
The staging build still reports inherited broad-book unresolved references such as:
- `ch:bf-prediction-error-decomposition`
- `eq:bf-ped-loglik`
- `ch:bf-kalman-hessian`
- `ch:bf-structural-derivatives`
- `ch:bf-factor-derivatives`
- `ch:bf-custom-gradient-wrappers`
- `ch:bf-derivative-validation`
- `eq:bf-solve-hessian-w-dot`
- `eq:bf-solve-hessian-quadratic`
- `ch:bf-kalman-score`
- `ch:bf-state-space-contracts`
- `ch:bf-api-design`
- `def:bf-filtering-target`

These are inherited whole-book consistency issues outside the local restarted
block, but under the current runbook they still block cutover because the staged
surface is not yet reference-clean.

### Blocker 2 — p50 depth is improved but still slightly thinner than source truth
The strongest remaining fidelity caution is on the p50 side:
- `staging ch36` and `staging ch37` now carry the right architecture and key
  mechanics,
- but p50’s densest operational middle and route-specific validation burden are
  still somewhat compressed.
This is no longer a chapter-role failure, but it is still a cutover caution.

## Gate status

- `G4` staging verification: **BLOCKED**
- Token: `BLOCK_R4_CUTOVER_PREFLIGHT_READY`

## What passed

- The restarted staging block is now materially source-truth-driven in all five
  destination chapters.
- p47 coverage is strong enough for chapter-role replacement.
- p50 coverage is substantially improved and now plausible at the chapter-role
  level, though still slightly compressed in operational depth.
- The whole-block architecture is coherent and readable as one monograph
  sequence.

## What remains before cutover

1. Resolve or explicitly gate the inherited whole-book undefined references in the
   staging surface.
2. Make a final whole-book boundary judgment at the interfaces with:
   - `ch20_filter_choice.tex`
   - the later generic HMC part
3. Decide whether the residual p50 depth caution is acceptable for canonical
   cutover or whether one final p50-deepening pass is required.

## Recommendation

Do **not** cut over yet.

The staged block is now strong enough that the next step should not be another
blind chapter migration pass.  The next step should be a targeted R4 cleanup and
cutover-preflight pass focused on:
- inherited whole-book reference cleanup or explicit gating,
- final boundary review with surrounding monograph chapters,
- explicit decision on whether the remaining p50 depth compression is acceptable
  for cutover.
