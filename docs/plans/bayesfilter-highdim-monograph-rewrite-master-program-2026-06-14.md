# High-Dimensional Monograph Rewrite Master Program

**Date:** 2026-06-14  
**Program ID:** `bayesfilter-highdim-monograph-rewrite-master-program-2026-06-14.md`

## Status

Active governing program for the rewrite of the high-dimensional nonlinear
filtering block of the BayesFilter monograph.

This program supersedes the earlier assumption that the current `ch34`--`ch37`
chapters provide a stable skeleton.  They do not.  The rewrite should instead use
`p47` and `p50` as the strongest authored source manuscripts and rebuild the
block so it reads coherently inside the monograph.

## Governing Purpose

The purpose of this program is to replace the current disconnected
high-dimensional filtering block in `docs/main.tex` with a chapter sequence that:

1. is coherent with the rest of the monograph,
2. makes the exact target, approximation families, and HMC/derivative discipline
   visible in one cumulative arc,
3. uses `p47` as the primary source manuscript for the deterministic
   Gaussian / sparse-grid lane,
4. uses `p50` as the primary source manuscript for the TT / KR / fixed-branch
   lane,
5. preserves the strongest technical and pedagogical material from the standalone
   notes while discarding the weaker, disconnected scaffolding from the current
   `docs/chapters/ch34`--`ch37` block,
6. compiles inside `docs/main.tex` as the new canonical readable exposition.

## Program Diagnosis

The current monograph high-dimensional block is not just locally weak.  It has
systemic coherence problems:

- the chapters are not sufficiently connected to the earlier monograph chapters;
- they do not clearly state what they import from earlier chapters or export to
  later ones;
- they repeatedly restart or reframe their core claims;
- they behave like interleaved research notes rather than authored monograph
  chapters;
- their implementation-facing material is not consistently staged around what is
  mathematically interesting or easy to get wrong.

The standalone notes `p47` and `p50` were created precisely because the current
chapters were not good enough.  The correct strategy is therefore to treat the
standalone notes as the authored source base and the current high-dimensional
chapters as salvage material only.

## Lane Boundary

### In scope
- `docs/main.tex`
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/plans` plans, rewrite artifacts, and result notes for this monograph
  rewrite stream
- standalone authored source manuscripts:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
  - `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

### Out of scope
- production `bayesfilter/` algorithmic code
- unrelated DPF / student baseline / controlled experiments lanes
- unrelated pre-existing chapters outside the high-dimensional block except where
  cross-references must be updated

## Canonical Source Manuscripts

### Deterministic Gaussian / sparse-grid lane
Primary source manuscript:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`

This note owns the strongest current exposition of:
- standard-normal GHQ family,
- tensor labels,
- sparse-grid level,
- Smolyak combination,
- low-dimensional cloud construction,
- UKF relation,
- fixed-cloud scalar / derivative discipline.

### TT / KR / fixed-branch lane
Primary source manuscript:
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`

This note owns the strongest current exposition of:
- TT approximation toolkit,
- coordinate systems and retained coordinates,
- KR transport logic,
- fixed-branch likelihood construction,
- derivative warmups and branch identity,
- validation ladder and benchmark interpretation.

## Target high-dimensional block architecture

The rewritten monograph block should behave as one integrated sequence answering
one overarching question:

> Given the exact filtering target and the monograph’s target/gradient discipline,
> which approximation families remain scientifically and computationally viable in
> the high-dimensional nonlinear regime?

### Chapter roles

#### `ch33` — High-dimensional nonlinear filtering foundations
Role:
- exact filtering target,
- why high dimension changes the admissible object classes,
- import of earlier target/derivative/HMC discipline.

#### `ch34` — Deterministic Gaussian and sparse-grid filtering
Role:
- rewritten from `p47` as the canonical deterministic Gaussian / sparse-grid lane.

#### `ch35` — Tensor-train / KR / transport filtering
Role:
- rewritten from `p50` as the canonical non-Gaussian TT / KR lane.

#### `ch36` — HMC and transformed-target consequences
Role:
- use the objects from `ch34` and `ch35` to study target discipline,
  transformed-target consequences, and HMC admissibility.

#### `ch37` — Candidate synthesis and promotion rules
Role:
- compare the lanes from `ch34` and `ch35`,
- state vetoes, limits, and promotion rules,
- close the high-dimensional block as synthesis rather than fresh exposition.

## Rewrite phases

## Phase 0 — Block architecture and import/export contract
Purpose:
- define the new high-dimensional monograph block as a coherent sequence,
- specify what each chapter imports and exports,
- stop assuming the existing `ch34`--`ch37` block is a stable skeleton.

Deliverables:
- one block-level architecture note,
- chapter responsibilities,
- import/export map to earlier and later monograph chapters.

## Phase 1 — Rewrite `ch34` from `p47`
Purpose:
- rebuild the deterministic Gaussian / sparse-grid lane using `p47` as the
  primary authored source.

Key content to carry:
- GHQ family clarification,
- what `F` means,
- tensor labels,
- sparse-grid level,
- Smolyak construction,
- merged 2D/3D clouds,
- UKF relation,
- low-level weight-matching discussion,
- fixed-cloud scalar/gradient contract.

Rule:
- keep `ch33` as the general foundation chapter,
- do not force `ch34` to re-explain what `ch33` already does well,
- but make `ch34` self-contained enough that the lane itself reads clearly.

## Phase 2 — Rewrite `ch35` from `p50`
Purpose:
- rebuild the TT / KR / fixed-branch lane using `p50` as the primary authored
  source.

Key content to carry:
- running example discipline,
- TT approximation toolkit,
- rank plausibility,
- coordinate systems,
- KR conditional maps,
- squared-TT filtering object,
- fixed-branch likelihood construction,
- derivative motivation and warmups,
- validation framing.

Rule:
- the rewritten chapter should read as a chapter, not as a reorganized technical
  note,
- and implementation-facing details should be staged around what matters and what
  is subtle.

## Phase 3 — Rewrite `ch36` as the high-dimensional target/HMC consequence chapter
Purpose:
- rebuild the HMC research-program chapter so it clearly imports objects from the
  rewritten `ch34` and `ch35` rather than behaving as a detached research note.

Key content:
- transformed-target discipline,
- same-scalar/HMC admissibility,
- TT/KR-to-HMC bridge,
- sparse-grid versus TT/KR implications for target design,
- limits of adaptive or branch-changing algorithms under HMC.

Rule:
- generic HMC target doctrine remains anchored in earlier HMC chapters;
  this chapter should be the high-dimensional specialization.

## Phase 4 — Rewrite `ch37` as synthesis
Purpose:
- turn `ch37` into a true synthesis chapter that uses the rewritten `ch34` and
  `ch35` as inputs.

Key content:
- selection criteria,
- vetoes,
- lane-specific strengths and limits,
- promotion rules,
- relation of deterministic Gaussian versus TT/KR lanes.

Rule:
- no long derivations,
- no repeated pedagogy,
- only synthesis and decision logic.

## Phase 5 — `main.tex` integration and cleanup
Purpose:
- rebuild the whole monograph with the rewritten block,
- repair labels, citations, references, and cross-chapter continuity,
- verify that the rewritten block now reads coherently inside the whole book.

Deliverables:
- clean or materially cleaner `main.tex` build,
- cross-reference repair,
- bibliography resolution,
- final integration assessment.

## Subplan structure

This master program should be supported by one subplan per phase:

1. `...phase0-block-architecture-subplan-...md`
2. `...phase1-ch34-sgqf-rewrite-subplan-...md`
3. `...phase2-ch35-zhaocui-ttkr-rewrite-subplan-...md`
4. `...phase3-ch36-hmc-consequence-rewrite-subplan-...md`
5. `...phase4-ch37-synthesis-rewrite-subplan-...md`
6. `...phase5-maintex-integration-subplan-...md`

## Governing editorial rules

1. The standalone notes `p47` and `p50` are the **authored source base**.
2. Existing `ch34`--`ch37` are **salvage material**, not presumed good skeletons.
3. Every rewritten chapter must state or imply clearly:
   - what it imports from earlier chapters,
   - what it contributes,
   - what later chapters will use.
4. Implementation material is not secondary; it must be staged around:
   - what the runtime object is,
   - what choices change the scalar,
   - what is mathematically subtle.
5. Repetition is allowed only when it deepens the concept.
6. Validation and HMC chapters should test or specialize previously defined
   objects, not restart the derivation from scratch.

## Verification criteria for the program

The program succeeds when:

1. the rewritten high-dimensional block is readable as one connected monograph
   sequence, not as a set of detached digressions;
2. `ch34` can replace the need to read `p47` for the canonical SGQF lane;
3. `ch35` can replace the need to read `p50` for the canonical Zhao--Cui lane;
4. `ch36` clearly connects those lanes to target/HMC consequences without
   re-deriving them;
5. `ch37` reads as synthesis rather than as another parallel note;
6. `docs/main.tex` compiles with the new block and its citations/references are
   materially cleaner;
7. a future reader or future agent can understand why the high-dimensional block
   exists without needing hidden long-context memory from earlier drafting
   history.
