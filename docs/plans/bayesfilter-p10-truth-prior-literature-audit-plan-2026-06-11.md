# P10 Truth-Prior Literature Audit Plan

metadata_date: 2026-06-11
status: PLAN_EXECUTED_FIRST_PASS_P44_DIAGNOSTICS_REMOVED
owner: Codex
skill: scholarly-literature-audit

## Objective

Create a source-grounded prior and tested-parameter ledger for the
synthetic-truth benchmark.  For each in-scope paper or author-code model row in
the P8 benchmark roster, find paper priors for parameters when available; if a
paper prior is not available, record tested values from the paper or reviewed
author code and label the source status explicitly.  P44 cubic, quadratic, and
tanh diagnostic rows are excluded from this literature-prior plan because they
are BayesFilter project fixtures rather than author-paper model rows.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What truth-prior distributions or tested parameter values can seed the P10 synthetic-truth benchmark for each in-scope P8 paper or author-code model row? |
| Baseline/comparator | P8 synthetic-truth contract, P1 target registry, local bibliography, local source cache, and reviewed Zhao--Cui model-suite artifacts. |
| Primary criterion | A Markdown ledger under `docs/plans` maps each model row to prior candidates, tested values, support status, inspected source anchors, source gaps, and recommended P10 action. |
| Veto diagnostics | Inventing priors; treating project fixtures as literature priors; reintroducing P44 diagnostic rows into this literature-prior plan; using abstracts/metadata only; merging paper priors and benchmark-stress priors without labels; failing to mark source gaps. |
| Not concluded | This audit does not freeze final P10 priors, does not run simulations, and does not certify that paper priors are optimal for the benchmark. |
| Artifact | `docs/plans/bayesfilter-p10-truth-prior-literature-audit-result-2026-06-11.md` |

## Source Hierarchy

1. Primary local full text with inspected technical section.
2. Reviewed author code or source-ledger evidence when primary full text is
   incomplete.
3. Source gap requiring network/library lookup or human-supplied paper.

## Model Rows In Scope

Use the P8 frozen roster after removing BayesFilter-only P44 diagnostic rows:

- LGSSM exact Kalman.
- Transformed stochastic volatility actual non-Gaussian.
- KSC Gaussian-mixture stochastic-volatility surrogate.
- Native generalized SV dense lower-rung.
- Spatial SIR lower-rung.
- Spatial SIR d=18 blocked production route.
- Predator-prey lower-rung.
- Predator-prey production tuned horizon 25.

Explicitly excluded from this plan:

- P44 cubic additive Gaussian.
- P44 quadratic observation.
- P44 nonlinear transition horizon 2.
- P44 nonlinear transition horizon 4 diagnostic extension.

## Execution Steps

1. Inspect `docs/references.bib`, local source cache, P1 target registry, and
   P8 contract.
2. Extract model-specific prior/tested-value anchors from locally available
   primary sources, especially Zhao--Cui 2024 Section 6.
3. Compare those anchors to the current P1 target registry values.
4. Write a row-by-row recommendation with support labels:
   `PAPER_PRIOR_FOUND`, `PAPER_TESTED_VALUE_FOUND`,
   `PAPER_FIXED_PARAMETER_FOUND`, `AUTHOR_CODE_VALUE_FOUND`,
   `SOURCE_GAP`.
5. Record omitted-paper risks and next required actions.

## Validation

- Confirm artifact paths exist.
- Confirm every in-scope model row appears exactly once.
- Confirm excluded P44 diagnostic rows do not appear in the row-by-row result
  ledger.
- Run `git diff --check` on the plan/result artifacts.
