# High-Dimensional Monograph Restart Master Program

**Date:** 2026-06-15  
**Program ID:** `bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

## Status

Active governing restart program for the p47+p50 monograph integration reset.

This program supersedes the earlier compressed rewrite workflow and the later
architecture-expansion workflow **as execution drivers**.  Those earlier plans,
chapter files, and compiled outputs are retained as salvage and historical
context, but they are no longer trusted as the canonical integration target.

## Governing purpose

The purpose of this restart is to safely rebuild the p47+p50 monograph
integration from source truth while preventing premature canonical cutover.

The restart therefore imposes one hard rule:

> The active canonical compiled book must not switch to the new p47+p50
> integration until the new block is complete, compiles cleanly in a staging
> surface, and passes a staged whole-block review.

## Program diagnosis

The failure mode of the prior operation was not a lack of chapters or plans.  It
was a sequencing error:

- the active compiled book was switched to replacement chapter files
- before the p47/p50 source migration was actually complete,
- which created architectural churn, stale audits, and a compiled surface that
  looked accepted before it deserved to be accepted.

This restart treats that condition as non-canonical rather than trying to prove
it acceptable by incremental patching.

## Surface classification

### Canonical compiled baseline (frozen conceptually)
- `docs/main.tex`
- the currently compiled active book and its current chapter include graph

### Foundation retained as stable input
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`

### Source truth
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

### Salvage only
- current compressed chapter set:
  - `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
  - `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
  - `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
  - `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- current expanded chapter set:
  - `docs/chapters/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
  - `docs/chapters/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
  - `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
  - `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
  - `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
- earlier rewrite/expansion plans and reset memos

## Active target architecture

The target architecture remains the expanded high-dimensional block:
- retained `ch33` foundations,
- plus the multi-chapter p47+p50 synthesis that will be rebuilt from source truth.

This restart does **not** reopen the chapter-count question.  It reopens the
integration sequencing and governance question.

## Required execution surfaces

### Surface A — canonical compiled baseline
- the currently accepted `docs/main.tex` path
- frozen during restart
- may be read and referenced
- must not become the migration surface for the new integration

### Surface B — staging integration surface
- a separate staging driver file under `docs/`
- used to host the restarted p47+p50 integration while it is incomplete
- may be compiled, reviewed, and revised freely during the restart
- must not be presented as canonical until cutover gates pass

## Restart phases

### Phase R0 — Baseline lock and demotion
Purpose:
- declare the current active expanded state non-canonical,
- freeze the canonical compiled baseline conceptually,
- record that neither the current compressed nor current expanded chapter sets are
  trusted as the final answer.

### Phase R1 — Reset planning spine
Purpose:
- write the restart master program,
- write the reset-safe runbook,
- write the chapter crosswalk,
- write the cutover audit plan,
- establish the staging-vs-canonical distinction explicitly.

### Phase R2 — Staging surface creation
Purpose:
- create the separate staging driver file,
- define which chapter files the staging build will use,
- ensure that staging builds do not alter the canonical compiled surface.

### Phase R3 — From-scratch p47+p50 reintegration in staging
Purpose:
- rebuild the target high-dimensional block from source truth,
- use salvage files only as mined inputs,
- keep all chapter migration and review in the staging surface.

### Phase R4 — Staging-only verification
Purpose:
- compile and review the staged block,
- repair labels, references, bibliography, and source-map consistency,
- perform whole-block integration review against the staged PDF.

### Phase R5 — Canonical cutover
Purpose:
- switch the canonical compiled book only after all gates pass,
- then retire the non-canonical state to historical/salvage status.

## Governing rules

1. Chapter presence in `docs/main.tex` is not evidence of acceptance.
2. p47 and p50 are the authored source truth for the restart.
3. Salvage chapter files may be mined, but must not dictate the final restarted
   integration.
4. The canonical compiled surface must remain distinct from the staging surface
   until cutover.
5. Whole-block review of the staged PDF is required before canonical switch.
6. No future incremental rewrite may collapse the distinction between source
   truth, salvage text, and accepted monograph text.

## Verification criteria

The restart planning spine succeeds when:

1. a fresh reset master program explicitly supersedes the old execution logic;
2. canonical compiled baseline, source truth, and salvage layers are clearly
   classified;
3. a separate staging integration surface is defined;
4. the cutover gate explicitly forbids early canonical switching;
5. future execution can proceed without ambiguity about which surface is trusted.
