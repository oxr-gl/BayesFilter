# P4 Subplan: Deterministic Filter Wiring

metadata_date: 2026-06-10
phase: FILTER_BENCH_P4
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Wire deterministic filters into the common adapter: Kalman, UKF, SVD
sigma-point, CUT4, and Zhao-Cui scalar/multistate routes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can deterministic filters run through the same benchmark adapter across the declared model rows? |
| Baseline/comparator | Existing sigma-point and CUT4 TF APIs, highdim Zhao-Cui scalar and multistate routes, SV mixture routes, LGSSM Kalman routes. |
| Primary criterion | Each deterministic algorithm has adapter smoke coverage and emits value/gradient/status/diagnostics through P2 protocol. |
| Veto diagnostics | Zhao-Cui routed through stale scalar-only blocker on multistate rows; superseded scalar-only assumption reintroduced through registry metadata or Markdown tables; derivative-only status hidden; SVD/CUT4 gradients promoted when branch diagnostics veto; approximations treated as exact. |
| Explanatory diagnostics | Per-filter smoke values, finite-gradient checks, branch diagnostics, rank/floor counts. |
| Not concluded | Smoke coverage does not rank filters. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-result-2026-06-10.md` |

## Tasks

- Add Kalman adapter for LGSSM and declared Gaussian-mixture enumeration rows,
  with mixture-surrogate status preserved when the row is not the actual
  non-Gaussian target.
- Add UKF/SVD/CUT4 adapters for structural/additive benchmark rows.
- Add SV mixture CUT4/Kalman adapters for transformed/log-additive SV rows.
- Add Zhao-Cui adapter that chooses scalar or multistate route by registry row,
  never by stale P45 blocker text.
- Preserve diagnostic boundaries for factorized scalar Zhao-Cui substitute rows.
- Name the superseded scalar-only Zhao-Cui assumption in the result artifact and
  show where the benchmark uses the current multistate route or an explicit
  row-level reason code instead.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS` only if every deterministic
algorithm has a structured result for every target row: value, value error, or a
machine-readable reason code.  Block if any row can only be recovered from old
Markdown tables.

## Validation

- Focused CPU-only adapter tests.
- Branch and finite-gradient diagnostics for SVD/CUT4.
- Claude read-only review, max five iterations.
