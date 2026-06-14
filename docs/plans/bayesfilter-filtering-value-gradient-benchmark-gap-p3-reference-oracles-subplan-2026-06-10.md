# P3 Subplan: Reference Oracle Wiring

metadata_date: 2026-06-10
phase: FILTER_BENCH_P3
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Wire references before algorithm rows are compared.  A filter result cannot be
called an error unless the row has an explicit reference value and reference
gradient status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does each model row have a reference route suitable for value and gradient error reporting? |
| Baseline/comparator | LGSSM Kalman; dense nonlinear lower-rung references; exact/transformed SV references; KSC Gaussian-mixture enumeration; native generalized SV dense reference; P53 spatial SIR route tie-outs. |
| Primary criterion | Reference adapters emit value, declared reference-gradient policy, diagnostics, reference type, and row class for every registry row. |
| Veto diagnostics | UKF/CUT4/Zhao-Cui used as truth without label; missing gradient reference policy; transformed SV confused with native raw-y SV; Gaussian-mixture surrogate row treated as actual non-Gaussian truth. |
| Explanatory diagnostics | Dense order refinement, lower-rung tie-outs, finite-gradient checks. |
| Not concluded | References may still be approximate when labeled as such. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-result-2026-06-10.md` |

## Tasks

- Wire LGSSM exact Kalman reference.
- Wire dense references for P44 small nonlinear rows.
- Wire transformed/log-additive SV actual-target reference and Gaussian-mixture
  surrogate reference as separate row classes.  The Gaussian-mixture row must
  record that it is an approximation lane when compared to the actual
  transformed non-Gaussian target.
- Wire native generalized SV dense reference only on lower-rung rows where the
  current implementation supports it.
- Wire spatial SIR and predator-prey references according to current P53/P51
  route status.
- Classify each row as `benchmarkable_value_gradient`,
  `benchmarkable_value_only`, `surrogate_approximation_lane`, or
  `blocked_only`.
- For every row, declare one of: `reference_gradient_available`,
  `reference_gradient_unavailable_but_value_benchmarkable`, or
  `reference_gradient_missing_blocks_gradient_benchmark`.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P3_REFERENCE_ORACLES` only if every P1 target row
has a reference route or an explicit `blocked_only` reason, every
non-`blocked_only` row has a row class and reference-gradient policy, and the
SV actual-target and Gaussian-mixture surrogate rows cannot be confused.  Block
if any intended non-Gaussian benchmark row lacks a benchmarkable reference
identity.

## Validation

- Dense refinement smokes where references are numerical.
- CPU-only TensorFlow tests for reference adapters.
- Claude read-only review, max five iterations.
