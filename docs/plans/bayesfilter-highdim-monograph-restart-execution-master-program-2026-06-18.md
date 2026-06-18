# High-Dimensional Monograph Restart Execution Master Program

**Date:** 2026-06-18  
**Program ID:** `bayesfilter-highdim-monograph-restart-execution-master-program-2026-06-18.md`

## Status

Active governing program for the current restart-governed execution phase of the
high-dimensional nonlinear filtering block.

This program supersedes the earlier compressed-topology assumptions in:
- `docs/plans/bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`
- `docs/plans/bayesfilter-highdim-monograph-restart-master-program-2026-06-15.md`

It does **not** discard their core purpose.  It preserves the same source-truth
commitment and monograph-level goal, but updates the governing execution surface
to match the current staged part, the source-restoration reset memo, and the
recent skeptical audits.

## Governing Purpose

The purpose of this execution program is to guide the remaining work needed to
turn the restarted high-dimensional block into a source-sufficient monograph
part that:

1. uses the authored p47 manuscript as the primary source for the deterministic
   Gaussian / sparse-grid lane,
2. uses the authored p50 manuscript as the primary source for the TT / KR /
   fixed-branch lane,
3. reads as a coherent monograph part rather than as interleaved research notes,
4. carries enough explanatory, implementation-facing, and validation burden that
   a careful reader no longer needs to reopen p47 or p50 for the operational
   middle of the argument,
5. reaches canonical `docs/main.tex` only after the staged part passes a fresh
   source-fidelity review.

## Governing Policy

This program inherits and makes explicit the restart discipline recorded in:
- `docs/plans/bayesfilter-highdim-monograph-restart-source-restoration-reset-memo-2026-06-15.md`

Binding rules for the current phase:

1. **The staging surface is the trusted active work surface.**
2. **Source restoration outranks architectural neatness.**
3. **The current canonical high-dimensional block is not final.**
4. **No canonical cutover should happen until the staged part survives a fresh
   source-fidelity audit.**
5. **Plans may change.**  Chapter shape, burden split, and subplans may be
   revised when audits show that the current structure is too compressed or does
   not carry the useful source explanation.
6. **However, every topology change must be recorded here or in a directly linked
   subplan before it becomes the new execution baseline.**

## Trusted Surfaces

### Source truth
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

### Trusted active execution surface
- `docs/main_highdim_restart_staging.tex`
- `docs/chapters_restart_staging/`

### Comparison-only / non-final surfaces
- canonical chapter files under `docs/chapters/ch34`--`ch38`
- canonical `docs/main.tex`
- canonical `docs/main.pdf`

## Current Active Staged Topology

The active staged high-dimensional part is currently defined in:
- `docs/main_highdim_restart_staging.tex`

Current include order:
1. `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
2. `docs/chapters_restart_staging/ch34_highdim_gaussian_projection_and_point_rule_foundations.tex`
3. `docs/chapters_restart_staging/ch35_highdim_sparse_grid_quadrature_and_fixed_cloud_scalar.tex`
4. `docs/chapters_restart_staging/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
5. `docs/chapters_restart_staging/ch36_highdim_low_rank_density_filters_and_kr_maps.tex`
6. `docs/chapters_restart_staging/ch36b_highdim_squared_tt_recursion_and_fixed_branch_likelihoods.tex`
7. `docs/chapters_restart_staging/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
8. `docs/chapters_restart_staging/ch38_highdim_validation_defect_calculus_and_promotion.tex`

This is the **current execution baseline**, not a declared permanent final shape.
Future chapter additions, splits, merges, or burden moves are allowed when a
skeptical audit shows they are needed.  If the topology changes again, update
this section and create or revise the relevant subplan before continuing.

## Chapter Roles In The Current Execution Baseline

### `ch33` — High-dimensional nonlinear filtering foundations
Role:
- exact filtering target,
- likelihood and derivative discipline,
- import/export bridge to the rest of the monograph.

### `ch34` — Deterministic Gaussian projection and point-rule foundations
Role:
- deterministic Gaussian carried object,
- Gaussian projection contract,
- point-rule family comparison language,
- boundary between family foundations and SGQF specialization.

### `ch35` — Sparse-grid quadrature and fixed-cloud scalar construction
Role:
- low-dimensional SGQF construction,
- active bands,
- Smolyak coefficients,
- duplicate merging,
- fixed cloud as stored runtime object.

### `ch35b` — Fixed-cloud filtering and SGQF validation
Role:
- SGQF value path,
- one-step numeric oracle,
- same-branch fixed-cloud scalar contract,
- SGQF finite-difference and validation ladder.

### `ch36` — Low-rank density filters, KR maps, and retained objects
Role:
- retained-object semantics,
- coordinate systems,
- conditional maps,
- KR/preconditioning flow,
- what object is carried.

### `ch36b` — Squared-TT recursion and fixed-branch likelihoods
Role:
- squared-TT recursive closure,
- fixed-branch scalar construction,
- stored-field and next-step closure contract,
- fixed least-squares route.

### `ch37` — Fixed-branch likelihoods and same-scalar gradients
Role:
- shared same-scalar derivative discipline,
- copied-core / branch-identity audit logic,
- derivative-path mechanics,
- HMC admissibility boundary.

### `ch38` — Validation, defect calculus, and promotion
Role:
- cross-lane validation architecture,
- benchmark logic,
- veto and promotion rules,
- what the part may and may not conclude.

## Residual Burden Map (Current Best Read)

This section records the remaining meaningful source-fidelity gaps after the
current restoration pass.  It should be updated after each skeptical audit.

### Residual p47 burdens

#### `ch35`
Still under-carried relative to p47:
- raw-to-merged 2D/3D cloud walkthroughs,
- explicit deterministic merge/order/prune policy,
- builder diagnostics that make the stored cloud executable as a contract.

#### `ch35b`
Still under-carried relative to p47:
- general analytical SGQF derivative recursion beyond the toy oracle,
- full mathematical validation model ladder and comparator/report details.

### Residual p50 burdens

#### `ch36`
Still under-carried relative to p50:
- fuller conditional-density / KR construction chain,
- more of the five-density preconditioning bookkeeping,
- more explicit operational coordinate flow.

#### `ch36b`
Still under-carried relative to p50:
- a more fully instantiated concrete branch,
- more explicit forward-step object flow,
- stronger saved-object detail for derivative-aware next-step closure.

#### `ch37`
Still under-carried relative to p50:
- fuller derivative algebra and checklist depth,
- more of the mass-contraction / carried-filter derivative story as a stable
  implementation-facing object.

#### `ch38`
Still under-carried relative to p50:
- explicit veto ledger,
- concrete benchmark backbone,
- benchmark-specific “can / cannot establish” statements,
- fuller derivative reporting contract,
- more explicit resource/report schema.

## Execution Phases For The Current Program

These are the live phases for the current execution baseline.

### Phase E0 — Maintain trusted staging surface
Purpose:
- preserve a green build on `docs/main_highdim_restart_staging.tex`,
- keep the staged part as the authoritative work surface.

### Phase E1 — Restore SGQF source burden
Surface:
- `ch35`
- `ch35b`

Purpose:
- make the deterministic Gaussian / sparse-grid lane source-sufficient enough
  that the reader no longer needs p47 for construction, same-branch, and core
  validation mechanics.

### Phase E2 — Restore TT/KR operational middle
Surface:
- `ch36`
- `ch36b`

Purpose:
- make the retained-object and fixed-branch operational middle source-sufficient
  enough that the reader no longer needs p50 for coordinate flow, stored fields,
  and next-step closure.

### Phase E3 — Restore derivative discipline
Surface:
- `ch37`

Purpose:
- make the same-scalar derivative lane source-sufficient enough that the reader
  no longer needs p50 for copied-core logic, branch identity, and the core fixed
  derivative story.

### Phase E4 — Restore validation and promotion discipline
Surface:
- `ch38`

Purpose:
- make the benchmark, veto, reporting, and promotion logic source-sufficient
  enough that the reader no longer needs p50 for validation interpretation.

### Phase E5 — Fresh whole-part skeptical audit
Purpose:
- re-audit the staged high-dimensional part against p47 and p50,
- decide whether the staged part now carries enough explanatory burden for
  canonical cutover.

### Phase E6 — Canonical cutover only after E5 passes
Purpose:
- mirror the approved staged part into `docs/main.tex` and canonical chapter
  files only after the staged part is judged source-sufficient.

## Current Recommended Edit Order

This order is not a permanent law; it is the current best sequencing after the
latest audits.

1. `ch38` — restore explicit veto ledger, benchmark backbone, and derivative
   reporting contract.
2. `ch35` / `ch35b` — restore raw-to-merged cloud walkthroughs, explicit merge
   policy, and fuller SGQF derivative/validation burden.
3. `ch36b` — restore more fully instantiated branch and forward-step stored-object
   flow.
4. `ch37` — restore fuller derivative algebra / checklist depth.
5. `ch36` — deepen KR / conditional-density chain further if the prior passes
   still leave a source-fidelity gap.

If later audits show a different priority ordering is better, revise this
section and continue under the new order.

## Anti-Drift Rule

Future work in this lane is governed by the following rule:

> **Restore source burden, audit, record, and only then cut over.**

Corollaries:
- do not treat clean builds as proof of source sufficiency;
- do not treat elegant chapter topology as proof that the useful source
  explanation has been carried;
- do not make unrecorded topology changes;
- do not canonically cut over while the staged part still feels materially
  thinner than p47/p50 in explanatory burden.

## Verification And Cutover Gate

A canonical cutover may be considered only when all of the following are true:

1. `docs/main_highdim_restart_staging.tex` builds cleanly.
2. The staged part survives a fresh skeptical audit against p47 and p50.
3. The audit conclusion is that the staged part no longer meaningfully sends a
   careful reader back to the source notes for the operational middle.
4. Remaining gaps, if any, are judged editorial or nice-to-have rather than
   structurally explanatory.
5. A cutover note records why the staged part is now trusted as canonical.

## Relationship To Prior Programs

This program supersedes prior compressed-topology execution assumptions but keeps
three durable commitments from the older plans:

1. `ch33` remains the foundations/import/export chapter.
2. p47 remains the primary source for the deterministic Gaussian / sparse-grid
   lane.
3. p50 remains the primary source for the TT / KR / fixed-branch lane.

The present program is therefore not a rejection of the older work.  It is the
current tracking document for the restart-governed execution phase after the
older compressed architecture proved too thin.
