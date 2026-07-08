# Codex Substitute Review: Low-Rank SPD Quadratic Geometry Phase 0

Date: 2026-07-08
Review name: `bayesfilter-low-rank-spd-quadratic-geometry-phase0`
Reviewer: Codex substitute reviewer
Reason for substitute review: Trusted Claude review gate was rejected because it would transmit private repository plan/context to an external Claude review service. No workaround or indirect external transfer was attempted.

## Scope

Reviewed:

- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-visible-gated-execution-runbook-2026-07-08.md`
- `docs/reviews/bayesfilter-low-rank-spd-quadratic-geometry-phase0-review-bundle-2026-07-08.md`

## Findings

No material blocker found.

The plan correctly classifies the low-rank SPD quadratic utility as `extension_or_invention` and does not use it to close a Zhao-Cui source-faithfulness gap. The evidence contract separates mechanical geometry validity from HMC convergence, posterior correctness, default readiness, and GPU/XLA readiness.

The Phase 1 subplan includes the required gates for:

- finite sample count at least `5 * regression_parameter_count`;
- SPD precision by construction;
- bounded condition number;
- nonfinite value handling;
- holdout-fit rejection;
- center-refinement accept/reject behavior;
- deterministic seed behavior.

The master program preserves the correct baseline: the existing Phase 5 initial-geometry path and the 2026-07-07 geometry/tau-gate result. Regression residuals, score changes, HMC acceptance, runtime, and tau summaries are explanatory only and are not promoted to readiness or posterior-validity claims.

## Residual Risks

This substitute review is weaker than independent Claude review. It does not provide external model diversity.

The default rank and condition cap remain hypotheses. Phase 1 must keep them as configurable diagnostics and must not treat them as scientifically validated defaults.

The planned utility may be useful mechanically while still failing to improve minimal SSL-LSTM HMC tuning. That outcome must be recorded as a tuning/geometry candidate failure, not as evidence against the broader research direction.

## Verdict

VERDICT: AGREE
