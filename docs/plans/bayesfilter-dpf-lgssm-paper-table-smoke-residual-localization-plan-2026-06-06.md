# LGSSM Paper-Table Smoke Residual Localization Plan

## Question

Why does the gated LGSSM paper-table smoke cell veto in BayesFilter with a
transport residual of about `0.069` while executable FilterFlow completes the
same `theta=0.75`, `epsilon=0.25` table cell?

## Evidence Contract

- Comparator: executable FilterFlow `transport()` on the exact BayesFilter
  first-failing particle/log-weight state.
- Primary diagnostic: first failing time, failing batch rows, BayesFilter
  active transport residuals, FilterFlow residuals on the same active state,
  and max transport-matrix delta.
- Veto threshold: `1e-4` for row/column residuals, matching the gated table
  runner.
- Explanatory diagnostics: ESS values, log-weight range, source-weight range,
  iteration count, and cost scale.
- Not concluded: table reproduction, printed-paper agreement, mathematical
  correctness, or production readiness.

## Skeptical Audit

This plan intentionally avoids the full table after the smoke veto. It compares
one exact state before changing solver settings or relaxing thresholds. If
FilterFlow has the same residual on the same state, the table smoke veto is a
shared solver residual issue. If FilterFlow residuals are healthy while
BayesFilter residuals are not, the mismatch is in the local transport
implementation or the exact state contract passed into it.

