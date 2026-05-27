# P8 Synthesis Chapter With Propositions And Proof Sketches Plan

## Objective

Rewrite `ch37` as a long synthesis chapter that explains how the paper pillars
could be combined, with propositions and proof sketches for what is exact, what
is approximate, and what diagnostics must control each approximation.

## Inputs

- Accepted P2-P7 rewritten chapters.
- P1 source ledger.
- Existing `ch37`.

## Execution Precondition

Execution is forbidden unless P2-P7 are accepted and every source needed for
each synthesis proposition is `LOCAL_FULL_TEXT_CHECKED` in the P1 ledger with
technical sections/equations/theorems/algorithms recorded.  No synthesis
proposition may rely on inherited chapter prose, summaries, metadata, or
abstract-level knowledge.

## Required Architecture

The synthesis must combine:

1. Block-local Gaussian filtering as a stabilizing scaffold.
2. Sparse-grid/high-degree cubature as local high-order diagnostics.
3. TT/TN compression for density/operator/covariance structure.
4. Decomposable/triangular transport maps for filtering and smoothing.
5. Transport-preconditioned HMC/NeuTra as posterior inference substrate.
6. Explicit error and diagnostic gates for composing these approximations.

## Required Proposition/Proof Topics

- Factorized or block-local filtering approximation and cross-block residual.
- Projection error decomposition: quadrature error plus projection/closure error.
- TT truncation propagation as residual-controlled approximation, not
  validation.
- Transport-map correction identity and approximation residual.
- Transport-preconditioned HMC target identity under exact invertible map.
- Composite promotion theorem: a method may be promoted only if each ledger
  passes its own veto diagnostics and the downstream posterior/filtering target
  is checked.

Each proposition must include a source-dependency row mapping it to the P1
ledger and to the earlier chapter derivation it composes.

## Outputs

- Rewritten `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`.
- P8 result note.
- Proposition-to-source dependency table.
- Composite error/diagnostic ledger distinguishing mathematical identity,
  numerical approximation, sampler validity, and scientific interpretation.

## Stop Conditions

- Stop if P2-P7 are not accepted.
- Stop if propositions cannot be stated without overclaiming.

## Verification

- `rg -n "\\\\begin{proposition}|\\\\begin{proof}|synthesis|composite|residual|promotion" docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/references.bib` only for checked sources consumed by P8.
- `docs/source_map.yml` only for P8 provenance entries.

## What Must Not Be Concluded

P8 proposes a research architecture and promotion logic; it does not establish
NAWM readiness, posterior accuracy, HMC convergence, or production defaults.
