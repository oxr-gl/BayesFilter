# Main Monograph Integration Plan For P47 And P50

**Date:** 2026-06-14  
**Target monograph:** `docs/main.tex` and the high-dimensional filtering block in `docs/chapters/`

## Context

The repository’s current high-dimensional nonlinear filtering monograph block is
organized in `docs/main.tex` as:

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

The standalone companion notes now contain much stronger material than the current
monograph chapters in two critical lanes:

- **p47:** the fixed SGQF / sparse-grid quadrature lane with a clearer pedagogical
  treatment of GHQ levels, tensor labels, sparse-grid level, Smolyak
  construction, UKF comparison, low-dimensional cloud geometry, and the
  same-scalar value/gradient contract.
- **p50:** the Zhao--Cui / TT / KR / fixed-branch lane with stronger internal
  chapterization of TT toolkit, coordinate systems, fixed-branch likelihood
  object, derivative warmups, and validation flow.

The goal is to reintegrate these stronger manuscripts back into the main monograph
so that the `docs/main.tex` high-dimensional block becomes the canonical readable
version rather than a weaker original plus digression notes in `docs/plans`.

This is not a one-file merge.  The monograph already distributes conceptual roles
across several chapters.  The integration plan should therefore preserve the
chapter logic of the book while using p47 and p50 as source manuscripts.

## Current monograph chapter roles

### `ch33_highdim_nonlinear_filtering_foundations.tex`
Current role:
- exact filtering target,
- high-dimensional failure modes,
- object-level foundation,
- same-scalar groundwork.

This chapter should remain the canonical home for:
- the exact Bayesian object,
- the filtering bottleneck,
- the statement of what later approximation families replace.

### `ch34_highdim_gaussian_and_sparse_quadrature.tex`
Current role:
- deterministic Gaussian approximation family,
- sigma-point / GHQ / sparse-grid family,
- moment-closure and approximate-score logic.

This is the natural home for the p47 material.

### `ch35_highdim_particle_transport_tensor_filters.tex`
Current role:
- non-Gaussian representation families,
- particle / transport / tensor-density lanes,
- TT/KR filtering object.

This is the natural home for the TT-side of p50.

### `ch36_nonlinear_ssm_hmc_research_program.tex`
Current role:
- HMC target discipline,
- transformed targets,
- same-scalar / transport-preconditioned HMC research program.

This is the natural home for the HMC-facing side of p50.

### `ch37_highdim_filtering_candidate_synthesis.tex`
Current role:
- synthesis,
- vetoes,
- promotion rules,
- selection architecture.

This is where the decision consequences of p47 and p50 should ultimately be
summarized, not where their derivations should live.

## Integration strategy by manuscript

# I. Integrating p47 back into the monograph

## Primary absorption target: `ch34_highdim_gaussian_and_sparse_quadrature.tex`

P47 should not become a new standalone monograph chapter.  Its core material
belongs inside `ch34`, which already owns the deterministic Gaussian and
sparse-quadrature lane.

### Material from p47 to absorb into `ch34`

#### A. GHQ family clarification
Absorb the p47 treatment of:
- standard-normal GHQ,
- the concrete ladder `I_1`, `I_2`, `I_3`,
- and the plain statement that the level label is a rule-family label rather than
  a polynomial degree.

Best placement:
- early in the one-dimensional-rule discussion of `ch34`, before the reader is
  asked to track sparse-grid levels.

#### B. The meaning of `F`
Absorb the explicit explanation that:
- `F` is just the multivariate integrand being averaged,
- it plays the same role that `ψ` plays in one dimension,
- and the low-dimensional examples should keep that role visible.

Best placement:
- immediately before tensor-product notation is introduced.

#### C. Tensor labels and tensor products
Absorb the p47 explanation of:
- `(1,1)`, `(1,2)`, `(2,1)`, `(2,2)`,
- and what `I_{\mathbf i}` means.

Best placement:
- in the early pedagogical part of the SGQF section, before the formal active-band
  and Smolyak rule.

#### D. Sparse-grid level and Smolyak explanation
Absorb the p47 clarification that:
- sparse-grid level `L=2` is not the tensor rule `(2,2)` or `(2,2,2)`,
- Smolyak is a signed combination of tensor rules, not merely point deletion,
- duplicate merging is a central part of the computational object.

Best placement:
- around the current SGQF construction block in `ch34`.

#### E. Low-dimensional 2D/3D cloud buildup
Absorb the p47 low-dimensional construction material:
- 2D active tensor rules,
- Smolyak coefficients,
- duplicate merging,
- merged 2D five-point cloud,
- 3D level-2 merged cloud and what low level misses.

Best placement:
- as the pedagogical heart of the SGQF chapter.

#### F. UKF bridge and low-level cloud-weight comparison
Absorb the p47 UKF relation material:
- why the low-level SGQF cloud can look like a UKF cloud,
- what the source theorem actually supports,
- why low-level weights can coincide in special symmetric-axis cases,
- and why constructional identity still differs.

Best placement:
- immediately after the merged-cloud discussion, not scattered later.

#### G. Same-scalar SGQF value/gradient contract
Absorb enough of the p47 value/gradient material so that `ch34` can state the
SGQF-specific same-scalar contract and fixed-cloud derivative discipline without
forcing the reader into the entire standalone note.

Best placement:
- later in `ch34`, but keep generic HMC policy in `ch36`.

## Secondary p47 absorption target: `ch37_highdim_filtering_candidate_synthesis.tex`

Only the **selection consequences** of p47 should move here, such as:
- when sparse-grid deterministic Gaussian closure is favored,
- what vetoes it must pass,
- where its UKF relation matters in the candidate landscape,
- and how it differs from dense GHQ, adaptive sparse grids, and richer non-Gaussian
  lanes.

Do **not** move derivations or low-dimensional pedagogy here.

## Keep out of `ch33`
Do not move most of p47’s formal SGQF material into `ch33`.

`ch33` should remain the exact-target / general-foundation chapter.  It may keep
only small cross-references or short framing statements that set up why a
Gaussian sparse-grid lane matters later.

## Keep out of `ch35`
Do not move p47’s SGQF derivation into `ch35`.

That chapter owns the non-Gaussian carried-object families, not the deterministic
Gaussian sparse-grid lane.

# II. Integrating p50 back into the monograph

P50 spans three conceptual territories in the current book:
- TT / KR filtering object,
- transport-preconditioned HMC bridge,
- and candidate-synthesis consequences.

So p50 should be split across existing chapters, not pasted into one place.

## Primary absorption target: `ch35_highdim_particle_transport_tensor_filters.tex`

This is the main home for the TT-side of p50.

### Material from p50 to absorb into `ch35`

#### A. Stronger chapter opening and object framing
Use p50’s better opening voice and chapter emphasis to improve the TT/KR lane
presentation in `ch35`.

#### B. Running example and notation discipline
Use the p50 running-example improvements where they help the TT / KR lane become
more readable.

#### C. TT toolkit and rank-plausibility material
Absorb:
- the TT explanation,
- split-rank meaning,
- the worked exponential example,
- the rank-plausibility logic,
- and the more chapter-like sequencing of those pieces.

#### D. Coordinate systems / retained coordinates / conditional-map logic
Absorb the improved coordinate-system and transport narrative into `ch35`, because
this is the chapter where the non-Gaussian tensor / transport object is being
built.

#### E. Squared-TT filtering object and operational recursion
Absorb the stronger operational chapter structure from p50 so that `ch35` becomes
the canonical home for:
- nonnegative squared-TT repair,
- normalizer,
- marginalization,
- retained filter,
- conditional KR map machinery,
- and operational filtering recursion.

#### F. Fixed-branch likelihood construction (TT-side only)
Absorb the p50 fixed-branch object identity material where it clarifies:
- what the runtime object is,
- what must be saved,
- what choices silently redefine the scalar,
- and what the branch means for the TT lane itself.

Best placement:
- still in `ch35`, because the TT carried object is being defined here.

## Secondary absorption target: `ch36_nonlinear_ssm_hmc_research_program.tex`

This chapter should absorb only the **HMC-facing bridge** from p50.

### Material from p50 to absorb into `ch36`

#### A. Fixed-branch scalar and derivative motivation, but at the HMC target level
Use p50’s stronger explanation of:
- why branch identity matters,
- why the fixed-branch scalar differs from the adaptive algorithm,
- and why same-scalar differentiation is the relevant HMC requirement.

#### B. Transport / transformed-target / KR-map consequences for HMC
Absorb the part of p50 that says how the TT/KR lane can serve as a transport or
preconditioning bridge for HMC, but keep generic HMC policy separate from TT/KR
object construction.

#### C. Validation consequences relevant to HMC research claims
Only the parts of the validation chapter that bear directly on transformed-target
correctness, scalar identity, or HMC admissibility should migrate here.

## Tertiary absorption target: `ch37_highdim_filtering_candidate_synthesis.tex`

Only the **decision consequences** of p50 should go into `ch37`:
- when TT/KR is favored,
- what rank / conditioning / coordinate / branch failures veto it,
- how it compares with Gaussian sparse-grid, dense GHQ, particle, and adaptive
  transport alternatives.

Do not paste TT derivations or warmups into `ch37`.

## Keep out of `ch33`
Do not move p50’s detailed TT or derivative material into `ch33`.

`ch33` should remain the general exact-target / high-dimensional failure / same-
scalar foundation chapter.

## Keep out of `ch21` and `ch26` as primary homes
There is overlap with:
- `ch21_hmc_for_state_space.tex`
- `ch26_transport_surrogates.tex`

But those chapters should remain generic.  The high-dimensional TT/KR and fixed-
branch transport logic should stay in the specialized high-dimensional block,
principally `ch35` and `ch36`, with those generic chapters trimmed or cross-
referenced as needed instead of absorbing the new material.

# III. Rewrite plan by chapter file

## `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
Keep as the exact-target foundation chapter.

### Integrate only:
- tiny cross-references to the richer SGQF and TT/KR chapters,
- brief setup statements that motivate why the later lanes exist.

### Do not absorb:
- p47 low-dimensional cloud pedagogy,
- p50 TT/KR derivations,
- fixed-branch implementation detail.

## `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
Major rewrite target using p47 as the source manuscript.

### Replace or heavily rewrite:
- the SGQF explanatory spine,
- the one-dimensional GHQ and sparse-grid pedagogy,
- the low-dimensional 2D/3D merged-cloud exposition,
- the UKF bridge,
- the low-level weight-matching discussion,
- the same-scalar SGQF object framing.

### Keep from old chapter if still useful:
- existing tables where they remain compatible,
- cross-links into `ch33` and `ch37`,
- any concise method-family comparisons that still fit the rewritten chapter.

## `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
Major rewrite target using p50 as the source manuscript.

### Replace or heavily rewrite:
- TT/KR lane exposition,
- TT toolkit voice,
- coordinate and retained-object flow,
- squared-TT object and operational recursion,
- the TT-side fixed-branch object identity.

### Keep from old chapter if still useful:
- broad lane-positioning context,
- short summaries that already fit the monograph flow,
- cross-links to `ch36` and `ch37`.

## `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
Selective rewrite target using p50’s HMC-facing material.

### Absorb:
- TT/KR-to-HMC bridge consequences,
- transformed-target / fixed-branch scalar relevance,
- same-scalar derivative discipline at the HMC target level.

### Keep out:
- heavy TT derivations,
- long coordinate-system expositions already housed in `ch35`.

## `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
Selective synthesis update using decision consequences from p47 and p50.

### Absorb:
- SGQF candidate-selection consequences,
- TT/KR candidate-selection consequences,
- richer veto / promotion guidance informed by the new stronger companion notes.

### Keep out:
- pedagogical derivations,
- object construction details,
- long implementation contracts.

# IV. Recommended integration order of work

1. Record the Phase 1 closure context from
   `docs/plans/bayesfilter-highdim-monograph-rewrite-blocker-clearance-reset-memo-2026-06-15.md`.
   - This fixes the current state: the immediate `ch34` blocker is cleared and
     `docs/main.tex` already builds.
2. Run the Phase 2 editorial/source-discipline pass on `ch35`.
   - This tightens the canonical TT / KR lane against p50 and the Zhao--Cui
     source-anchor discipline.
3. Run the Phase 3 consequence-discipline pass on `ch36`.
   - This keeps the chapter importing `ch34`/`ch35` objects rather than
     re-deriving them.
4. Run the Phase 4 synthesis-pruning pass on `ch37`.
   - This keeps synthesis downstream of the finalized chapter exports.
5. Maintain the green `docs/main.tex` build throughout these chapter passes and
   use Phase 5 for bibliography, cross-reference, provenance, and chapter-boundary
   closeout.
6. Only after those passes revisit `ch33` for any small foundational
   cross-reference cleanup that the integrated reading still requires.

# V. Verification plan

## Structural verification
1. Confirm `docs/main.tex` chapter order still makes sense after integration:
   - `ch33` foundation
   - `ch34` deterministic Gaussian / sparse-grid lane
   - `ch35` TT / KR / transport lane
   - `ch36` HMC research-program consequences
   - `ch37` synthesis

## Content verification
2. Read `ch34` alone and check that it can replace the current need for p47.
3. Read `ch35` alone and check that it can replace the current need for p50’s TT
   exposition.
4. Read `ch36` and confirm it now references TT/KR transport only at the HMC
   target level, not by re-deriving the whole lane.
5. Read `ch37` and confirm it synthesizes rather than re-explains.

## Build verification
6. Keep `docs/main.tex` green while the editorial/source-discipline passes run.
7. Run BibTeX and rebuild as needed.
8. Fix all chapter-level labels, cross-references, bibliography issues, and
   provenance drift exposed by the editorial passes.
9. Confirm the new main PDF remains stable enough for reading and chapter
   navigation after each phase pass, not only at the end.

# Deliverable

A staged monograph rewrite in which:
- p47 is absorbed chiefly into `ch34`,
- p50 is absorbed chiefly into `ch35` and partly into `ch36`,
- and the resulting `main.tex` monograph supersedes the need to read the p47/p50
  standalone notes for the canonical high-dimensional filtering exposition.
