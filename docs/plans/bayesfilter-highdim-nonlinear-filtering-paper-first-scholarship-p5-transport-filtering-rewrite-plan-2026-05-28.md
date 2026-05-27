# P5 Transport-Map Filtering And Smoothing Rewrite Plan

## Objective

Rewrite transport-map filtering and smoothing as a central high-dimensional
non-Gaussian pillar, not a short proposal-density note.

## Inputs

- P1 source ledger entries for Spantini-Baptista-Marzouk nonlinear ensemble
  filtering, ensemble transport smoothing Part I, decomposable transports, and
  transport-map foundations.
- Existing `ch35` and `ch37`.

## Execution Precondition

Execution is forbidden unless every transport filtering/smoothing paper used by
P5 is `LOCAL_FULL_TEXT_CHECKED` in the P1 ledger with local artifact path,
inspected technical sections, inspected equation/theorem/algorithm identifiers
where available, and chapter consumers recorded.  Summaries and abstracts are
not sufficient for map, coupling, or smoothing derivations.

## Required Content

1. Coupling formulation for filtering updates.
2. Triangular/Knothe-Rosenblatt map structure and conditional factorization.
3. Ensemble nonlinear filtering map construction and finite-ensemble
   approximation.
4. Smoothing factorization and decomposable transport structure.
5. Derivation of change-of-variables, map-induced proposal/correction, and
   exact versus approximate map target.
6. Algorithmic local/decomposable transport filtering and smoothing steps.
7. Complexity in ensemble size, map dimension, polynomial/basis size,
   localization blocks, and transport solve.
8. Failure modes: map expressivity, sample collapse, localization bias,
   Jacobian singularity, density-evaluation instability, and smoothing
   inconsistency.
9. Paper-by-paper mapping from source equation/theorem/algorithm to chapter
   subsection and derivation/proof sketch.

## Outputs

- Rewritten transport sections in `ch35` and synthesis links in `ch37`.
- P5 result note.
- Paper-by-paper exposition checklist and source-to-chapter mapping table.

## Stop Conditions

- Stop if primary transport filtering/smoothing sources are not locally
  inspected.
- Stop if triangular/decomposable map claims cannot be tied to source support.

## Verification

- `rg -n "transport|coupling|triangular|Knothe|Rosenblatt|smoothing|decomposable" docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex` only for
  synthesis cross-references introduced by P5.
- `docs/references.bib` only for checked sources consumed by P5.
- `docs/source_map.yml` only for P5 provenance entries.

## What Must Not Be Concluded

P5 does not validate a BayesFilter transport backend or claim transport maps
solve high-dimensional nonlinear filtering without source and downstream
evidence.
