# LGSSM Paper-Table Gated Comparator Plan

## Question

Does the BayesFilter experimental TF/TFP implementation reproduce the executable
FilterFlow LGSSM paper-table behavior under a matched table contract?

This is a comparator test. It does not assert that either implementation is
mathematically correct, nor does it promote the printed paper table as the
primary baseline.

## Evidence Contract

- Primary comparator: current local patched `.localsource/filterflow`
  executable, run in float64.
- Primary metric: per-time log-likelihood error against the matched exact
  Kalman reference, summarized over fixed replications.
- Promotion criterion: BayesFilter table-cell means are within one FilterFlow
  sample standard deviation for all executed cells, with finite values. Residual
  diagnostics are recorded and can explain instability, but are not a
  BayesFilter-specific veto after the same-state localization test showed that
  executable FilterFlow shares the first smoke residual breach.
- Veto diagnostics: non-finite values, missing FilterFlow execution, Kalman
  mismatch, or a one-cell smoke failure against the FilterFlow table-cell
  comparator.
- Explanatory diagnostics: printed paper-table agreement, finite-difference
  gradients, speed, Monte Carlo standard errors, and transport residuals above
  `1e-4`.
- Not concluded: posterior correctness, gradient correctness, production
  readiness, or correctness of the printed table.

## Contract

Use the existing FilterFlow Section-5.1-style LGSSM contract:

- state dimension `2`;
- `T=150`, `N=25`, `100` replications for the full table;
- theta grid `(0.25, 0.5, 0.75)`;
- epsilon grid `(0.25, 0.5, 0.75)`;
- fixed observation path from FilterFlow seed `111`;
- fixed initial particle cloud shared from FilterFlow seed `111`;
- fixed filter seed `555`;
- `NeffCriterion(0.5, True)`;
- `RegularisedTransform(epsilon, scaling=0.9)`.

Solver policy after the T4 residual ladder:

- smoke and full table use `convergence_threshold=1e-8`, `max_iter=500` for
  the FilterFlow-style transport table lane.
- printed paper-table comparison remains explanatory because the paper may have
  used the historical default `max_iter=100`, `convergence_threshold=1e-3`, and
  rounded reporting.

## Gating

1. Run a hard-cell smoke: `theta=0.75`, `epsilon=0.25`, full `T=150`, `N=25`,
   but fewer replications if needed for turnaround.
2. If the smoke cell has finite values and within-one-SD agreement, run the
   full theta-by-epsilon table. Record residual diagnostics, including whether
   they exceed `1e-4`, but do not block solely on the residual tolerance when
   the same residual behavior is shared by executable FilterFlow.
3. If the smoke cell fails, stop and localize before spending the full table
   budget.

## Skeptical Audit

This plan avoids the old wrong baseline: the printed paper table is not the
promotion target. It also avoids treating a single deterministic scalar fixture
as table evidence: the table criterion is Monte Carlo agreement under a fixed
observation path and shared initial cloud. The one-cell smoke prevents a long
run from producing an artifact that already fails the comparator contract.

## Residual Gate Revision

The initial smoke run was vetoed because BayesFilter observed a transport row
residual above `1e-4`. The follow-up localization artifact
`docs/plans/bayesfilter-dpf-lgssm-paper-table-smoke-residual-localization-result-2026-06-06.md`
replayed the first failing state through executable FilterFlow and found the
same maximum residual, the same transported particles, and transport matrices
matching to roundoff. Therefore, for this table-comparator question, that
residual is a shared solver diagnostic rather than a BayesFilter-vs-FilterFlow
mismatch. A stricter transport-solver investigation remains a separate
research-engineering question.
