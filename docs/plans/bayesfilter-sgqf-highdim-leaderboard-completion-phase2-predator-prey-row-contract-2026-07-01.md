# Phase 2 SGQF Predator-Prey T20 Row Contract

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Purpose

Freeze the exact SGQF row contract for `zhao_cui_predator_prey_T20` before any
predator-prey SGQF implementation or leaderboard regeneration work proceeds.

## Governing Row Identity

The row is exactly:

```text
zhao_cui_predator_prey_T20
```

This row is the source-scope predator-prey T20 row with:

- horizon `T = 20`
- initial state `[50.0, 5.0]`
- process covariance `4 * I_2`
- observation covariance `4 * I_2`
- paper physical truth
  `(r=0.6, K=114.0, a=25.0, s=0.3, u=0.5, v=0.5)`

It is **not** the lower-rung two-observation predator-prey SGQF diagnostic from
P47 unless a reviewed artifact explicitly redefines the row contract. Lower-rung
diagnostic evidence may inform debugging, but it is not source-row admission
by itself.

## Current Authority Inputs

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md`
- `docs/plans/bayesfilter-source-scope-sgqf-analytical-gradient-ledger-2026-06-24.md`
- `tests/highdim/test_p47_predator_prey_filtering.py`

## Current Reviewed Status

Current leaderboard state:

- SGQF: `blocked`
- UKF: `executed_value_only`
- Zhao-Cui: `blocked_or_status_only`

Current SGQF blocker reason:

- `blocked_target_alignment: no reviewed fixed-SGQF evaluator is wired for the source-scope T20 predator-prey observations; the available P47 two-observation lower-rung value is diagnostic-only and is not reported as this T20 row`

Important context from older SGQF ledgers:

- SGQF predator-prey has family-level analytical score evidence in
  `tests/highdim/test_p47_predator_prey_filtering.py`,
- but that evidence is not yet automatically a source-scope T20 leaderboard row
  admission without a reviewed row contract.

## Required Conditions For SGQF Value Admission

The row may be admitted as `executed_value_only` only if a reviewed SGQF route:

- evaluates the exact T20 source-row observations rather than the lower-rung
  two-observation diagnostic,
- computes a finite value for the exact reviewed row target,
- is not mislabeled from lower-rung or auxiliary evidence,
- and preserves row-specific nonclaims honestly.

## Required Conditions For SGQF Value+Score Admission

The row may be admitted as `executed_value_score` only if, in addition to value
admission:

- the row has a reviewed free-theta contract,
- the analytical/manual score route differentiates the same declared scalar,
- autodiff/`GradientTape`/finite differences are not the admitted score route,
- any supporting FD evidence is same-branch and tied to the T20 source-row
  scalar rather than only to the lower-rung diagnostic.

## Analytical/Manual Provenance Rule

For this row, admitted analytical/manual score provenance must be supported by a
reviewed artifact that does all of the following:

- names the declared scalar being differentiated for the exact T20 row,
- identifies the free-theta contract used by the row,
- identifies the derivative ownership route as one of:
  - hand-derived / manually coded score recurrence or formula,
  - paper-cited closed-form score mapped into repo notation,
  - manually coded derivative route checked against the same declared scalar,
- explicitly states that autodiff/`GradientTape`/finite differences are not the
  admitted score route,
- and records any supporting FD or score-at-true diagnostics only at their
  reviewed explanatory or repair-trigger role.

Negative definition alone is insufficient. A row cannot be admitted merely by
saying what the provenance is not; it must positively identify the admitted
manual/analytical route.

## Explicit Nonclaims

- lower-rung two-observation predator-prey SGQF evidence is not by itself the
  T20 source-row admission,
- no SGQF score row is admitted merely because family-level analytical evidence
  exists elsewhere,
- no HMC readiness, production readiness, or default-policy claim follows from
  this row contract.
