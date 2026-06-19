# Execution Plan: Expanded High-Dimensional Monograph Migration

**Date:** 2026-06-15  
**Program reference:** `docs/plans/bayesfilter-highdim-monograph-expansion-master-program-2026-06-15.md`  
**Architecture reference:** `docs/plans/bayesfilter-highdim-monograph-expansion-integration-plan-2026-06-15.md`

## Question

How do we migrate the expanded high-dimensional monograph block from the current
seeded architecture into a true p47/p50-synthesized chapter sequence without
losing build stability or chapter-role coherence?

## Execution baseline

- The expanded block is already active in `docs/main.tex`.
- The new target files exist and compile:
  - `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
- These files are currently seeded from the old compressed chapters and are not
  yet true architecture-native rewrites.
- The old compressed files remain salvage material only:
  - `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
  - `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
  - `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
  - `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

## Evidence contract

### Scientific / editorial question
Can we migrate the expanded block into a monograph-native architecture that
faithfully carries the explanatory weight of `p47` and `p50` rather than reading
as a compressed digest?

### Exact baseline / comparator
- Source bases:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
  - `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
- Current seeded expanded files listed above.
- Existing foundation chapter:
  - `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`

### Primary pass criteria
1. Each expanded chapter acquires a clear, architecture-native role rather than a
   copied predecessor role.
2. The deterministic Gaussian / sparse-grid material from `p47` is distributed
   across new `ch34` and `ch35` in a way that no longer truncates the source
   exposition unnaturally.
3. The low-rank / TT / KR / retained-object material from `p50` is concentrated
   in new `ch36` rather than diluted across survey-like structure.
4. The shared fixed-branch scalar/gradient abstraction is moved into new `ch37`
   as a cross-method chapter.
5. Validation / defect / promotion logic is moved into new `ch38` as a shared
   closeout chapter.
6. `docs/main.tex` remains build-green throughout.

### Veto diagnostics
- A chapter still reads mainly like a copied predecessor instead of its new role.
- A migration step creates new undefined references/citations or breaks the
  monograph build.
- Shared material is left duplicated across method chapters rather than moved into
  the shared derivative/validation chapters.
- A source-heavy chapter no longer carries enough explanation to replace the need
  to read the source manuscript for that conceptual unit.

### Explanatory-only diagnostics
- Underfull/overfull box warnings that do not break the chapter contract.
- Transitional compatibility labels still present while the architecture is being
  normalized.

### What will not be concluded even if the pass succeeds
- Success does not imply the high-dimensional block is fully polished stylistically.
- Success does not prove every source-risk has been eliminated; it proves the new
  architecture is carrying the right material in the right places.

### Artifact to preserve the result
- one result/reset note under `docs/plans` describing commands run, migrated
  content, build state, and remaining risks.

## Source allocation by destination chapter

### `ch33_highdim_nonlinear_filtering_foundations.tex` (retained)
**Keep as foundation.**
Imports from earlier chapters only. No large source migration from p47/p50.

**Allowed touch scope later:**
- only light cross-reference and orientation cleanup if required by the new block.

### `ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
**Purpose:** deterministic Gaussian carried object + rule-family foundations.

**Primary source allocation from p47:**
- Introduction / scope material that explains the deterministic Gaussian lane
  before sparse-grid specialization.
- Exact filtering and Gaussian projection sections.
- The GHQ family clarification and one-dimensional rule-family explanation.
- The meaning of the integrand `F` and tensor-rule notation before sparse-grid
  specialization.
- Neighboring Gaussian method comparison language that belongs at the rule-family
  level rather than the sparse-grid method level.

**Salvage from old compressed chapters:**
- front/shared deterministic-Gaussian material now seeded in this file,
- any concise comparison tables that fit the chapter’s foundational role.

**Must be rewritten, not transplanted verbatim:**
- imported-note voice (“this note/report”),
- source-specific scaffolding that presumes the sparse-grid chapter has not yet
  split off,
- any derivative/validation tails that belong in `ch37`/`ch38`.

### `ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
**Purpose:** p47-heavy sparse-grid method chapter.

**Primary source allocation from p47:**
- low-dimensional 1D/2D/3D cloud construction,
- active bands and Smolyak coefficients,
- merged cloud explanation,
- UKF relation at the rule-family level,
- filtering value path,
- worked one-step oracle,
- fixed-cloud scalar object,
- local method-selection material that belongs to the sparse-grid lane itself.

**Salvage from old compressed chapters:**
- the p47-heavy body already seeded into this file,
- repaired same-scalar contract fragments that still naturally belong to the
  method chapter rather than the shared derivative chapter.

**Must be rewritten, not transplanted verbatim:**
- material that really belongs to the shared fixed-branch abstraction chapter,
- appendix-style inventories and global validation templates,
- old references that treat this chapter as the whole deterministic lane.

### `ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
**Purpose:** p50-heavy non-Gaussian retained-object lane.

**Primary source allocation from p50:**
- orientation/scope reframed for the monograph,
- running example and notation discipline relevant to the TT/KR lane,
- exact-target bottleneck framing only where needed locally,
- TT approximation toolkit,
- rank plausibility logic,
- coordinate systems and retained coordinates,
- conditional KR maps,
- squared-density / retained-object filtering recursion,
- local transport/preconditioning context,
- lane-local source-boundary and non-claim sections.

**Salvage from old compressed chapters:**
- the old survey chapter only where it provides useful comparator context,
- old `ch35` defect/export sections where they remain compatible with the new lane.

**Must be rewritten, not transplanted verbatim:**
- the broad survey framing that spreads focus across particles, generic transport,
  TT/QTT PDE filters, and TN covariance compression equally;
- material whose real destination is the shared derivative chapter or the final
  validation/promotion chapter.

### `ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
**Purpose:** shared fixed-branch same-scalar chapter.

**Primary source allocation synthesized from p47 and p50:**
- p47 same-scalar branch contract and analytical gradient discipline,
- p50 fixed-branch likelihood construction,
- p50 derivative warmups and branch-identity framing,
- exact-target vs approximate-target HMC admissibility consequences,
- finite-difference branch-validity logic.

**Salvage from old compressed chapters:**
- current `ch36` HMC consequence framing where it stays strictly downstream of
  filtering-target discipline,
- repaired exact-correction / pseudo-marginal caution language,
- local branch-boundary sections from the old `ch34` that truly belong to the
  shared scalar contract.

**Must be rewritten, not transplanted verbatim:**
- generic HMC tutorial material that belongs in later HMC chapters,
- method-specific forward-recursion exposition that should remain in `ch35` or
  `ch36`.

### `ch38_highdim_validation_defect_calculus_and_promotion.tex`
**Purpose:** shared validation / promotion / industrial synthesis chapter.

**Primary source allocation synthesized from p47 and p50:**
- p47 verification/validation architecture,
- p50 validation ladder and benchmark interpretation,
- source-risk / non-claim discipline from the current synthesis lane,
- defect calculus and promotion rules.

**Salvage from old compressed chapters:**
- old `ch37` defect calculus, synthesis contracts, and source-boundary language,
- validated diagnostic tables where they still fit the new chapter role.

**Must be rewritten, not transplanted verbatim:**
- any method-construction derivations,
- any prose that assumes the deterministic and TT/KR lanes have not already been
  given their own full chapters.

## Migration order

### Step 1 — Normalize new `ch34` into a true foundational Gaussian chapter
Files:
- `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
- source support: p47 + earlier sigma-point chapters + old compressed `ch34`

Goal:
- remove sparse-grid-heavy content that belongs in `ch35`,
- keep deterministic Gaussian projection and point-rule family foundations,
- make the chapter readable as the shared deterministic entry point.

Gate:
- the chapter should no longer pretend to be the whole p47 note,
- and should clearly export to `ch35`.

### Step 2 — Build new `ch35` as the true p47 sparse-grid method chapter
Files:
- `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
- p47 source

Goal:
- migrate the sparse-grid specialization, merged-cloud pedagogy, value path,
  fixed-cloud scalar, and sparse-grid lane comparison into one coherent chapter.

Gate:
- `ch35` alone should substantially replace the need to read p47 for the
  sparse-grid lane.

### Step 3 — Build new `ch36` as the true p50 retained-object chapter
Files:
- `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
- p50 source

Goal:
- convert the seeded survey-like file into the p50-heavy TT/KR retained-object
  chapter.

Gate:
- `ch36` alone should substantially replace the need to read p50 for the TT/KR
  lane proper.

### Step 4 — Build new `ch37` as the shared fixed-branch chapter
Files:
- `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
- p47 same-scalar sections + p50 fixed-branch sections + selected old `ch36`

Goal:
- synthesize the cross-method fixed-branch scalar/gradient abstraction.

Gate:
- the chapter should no longer read like a second general HMC chapter;
- it should read like the shared derivative/target-discipline chapter of the
  high-dimensional block.

### Step 5 — Build new `ch38` as the shared validation/promotion closeout
Files:
- `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
- p47 validation + p50 validation + old `ch37`

Goal:
- give the block a true closeout chapter that consumes the prior chapters rather
  than reopens them.

Gate:
- the chapter should feel like a shared industrial/validation close, not a
  summary of the old synthesis chapter alone.

### Step 6 — Integration cleanup after all five new chapters are role-correct
Files:
- `docs/main.tex`
- all new expanded files
- references/bibliography as needed

Goal:
- preserve the green build,
- remove transitional compatibility assumptions where safe,
- check the handoff from the expanded block to the later HMC part.

## Verification checkpoints

After each chapter step:
1. Rebuild `docs/main.tex` with
   `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `docs/`.
2. Check for:
   - fatal LaTeX errors,
   - undefined references/citations,
   - obvious chapter-role regressions.
3. Record the next blocker immediately if the build fails.

After the final integration step:
4. Read the expanded block in sequence:
   - `ch33`
   - new `ch34`
   - new `ch35`
   - new `ch36`
   - new `ch37`
   - new `ch38`
5. Confirm the later HMC part still reads as a generic continuation rather than a
   duplicate of the high-dimensional derivative chapter.

## Carryover vs rewrite rules

### Allowed carryover
- equations,
- worked examples,
- validated tables,
- source-boundary prose,
- export/defect sections,
- references already made precise in prior cleanup passes.

### Must be rewritten into monograph voice
- source-note introductions,
- “this note/report” language,
- source-specific scaffolding that assumes a two-chapter compression,
- tails that currently exist only because shared material had nowhere else to go.

### Salvage-only rule
The old compressed files may be mined, but should not dictate the expanded
architecture.  If old wording conflicts with the new chapter role, rewrite it.

## Practical stop conditions

- Stop and re-evaluate if the new `ch34` and `ch35` split still leaves the
  sparse-grid lane feeling unnaturally divided.
- Stop and re-evaluate if the new `ch36` still reads mainly as a survey rather
  than a retained-object chapter after the first real migration pass.
- Stop if `ch37` starts duplicating the later HMC part instead of specializing
  the fixed-branch abstraction.
- Stop if `ch38` becomes so large that the optional sixth chapter is clearly
  needed; in that case, pause and replan the final split before continuing.

## Artifact plan

After meaningful migration progress, write a result/reset note under `docs/plans`
recording:
- chapters advanced,
- source sections absorbed,
- build state,
- remaining blockers,
- next justified step.
