# P2 Foundations Rewrite Plan

## Objective

Rewrite `ch33` as a self-contained mathematical foundation for high-dimensional
nonlinear filtering, including exact filtering recursions, continuous-discrete
PDE formulations, posterior targets, and approximation boundaries.

## Inputs

- P1 source ledger.
- Existing `ch33`.
- Primary sources for nonlinear filtering equations after P1 permits them.
- MathDevMCP label lookup and proof-obligation diagnostics.

## Execution Precondition

Execution is forbidden unless every source used for continuous-discrete
filtering, Zakai, Kushner-Stratonovich, Fokker-Planck, or DMZ formulations is
`LOCAL_FULL_TEXT_CHECKED` in the P1 ledger with local artifact path, inspected
technical sections, inspected equation/theorem identifiers where available, and
chapter consumers recorded.  `LOCAL_SUMMARY_ONLY`, `METADATA_ONLY`, and
abstract-level knowledge are blockers for chapter mathematics.

## Required Content

1. Discrete-time nonlinear SSM recursion and likelihood factorization.
2. Continuous-discrete filtering notation.
3. Zakai, Kushner-Stratonovich, Fokker-Planck, and DMZ-style formulations where
   supported by inspected sources.
4. Exact posterior and approximate posterior distinction.
5. High-dimensional failure mechanisms in mathematical terms: concentration,
   exponential quadrature, particle collapse, rank growth, map degeneracy, and
   sampler geometry.
6. A compact implementation-boundary note moved away from the main exposition.

## Review Criteria

- No BayesFilter evidence box in the main mathematical flow.
- Each PDE identity has assumptions and derivation or source equation support.
- MathDevMCP audit attempted for local derivable identities.

## Outputs

- Rewritten `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`.
- P2 result note.
- Paper-by-paper mapping table: source section/equation/theorem to chapter
  subsection and derivation/proof sketch.

## Stop Conditions

- Stop if P1 did not approve source support for PDE/filtering identities.
- Stop if major identities cannot be stated with assumptions.

## Verification

- `latexmk` after integration phase, not necessarily during P2.
- `rg -n "\\\\begin{proposition}|\\\\begin{proof}|DMZ|Zakai|Kushner|Fokker" docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/references.bib` only for checked sources consumed by P2.
- `docs/source_map.yml` only for P2 provenance entries.

## What Must Not Be Concluded

P2 does not validate any numerical filter, tensor method, HMC scheme, or NAWM
readiness.
