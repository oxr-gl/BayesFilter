# Phase 3 SGQF Generalized-SV Source-Row Contract

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Purpose

Freeze the exact SGQF row contract for
`zhao_cui_generalized_sv_synthetic_from_estimated_values` before any
source-row SGQF implementation or leaderboard regeneration work proceeds.

## Governing Row Identity

The row is exactly:

```text
zhao_cui_generalized_sv_synthetic_from_estimated_values
```

This row is a **source-scope generalized-SV synthetic prior-mean row**. It is
not:

- the native generalized-SV dense oracle by itself,
- a precursor engineering route relabeled as source-row execution,
- actual SV evidence,
- KSC surrogate SV evidence,
- or a direct SP500 benchmark-data row.

## Current Authority Inputs

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`
- `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`
- `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-result-2026-06-29.md`
- `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-result-2026-06-29.md`
- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase8-final-decision-result-2026-07-01.md`

## Current Reviewed Status

Current leaderboard state:

- SGQF: `blocked`
- UKF: `executed_value_only`
- Zhao-Cui: `blocked_or_status_only`

Current SGQF blocker reason:

- `blocked_source_row_evaluator_missing: no reviewed fixed-SGQF exact-row evaluator is wired for zhao_cui_generalized_sv_synthetic_from_estimated_values; native-oracle, precursor, auxiliary, actual-SV, and KSC evidence are not source-row admission evidence`

Current reviewed generalized-SV governance state:

- the governed generalized-SV program closed the current SGQF source-row class
  as `BLOCKED_PENDING_SOURCE_SCOPE_EVALUATOR`;
- the native generalized-SV dense raw-y route is oracle-only evidence;
- precursor/auxiliary/native-oracle evidence is not source-row admission.

## Required Conditions For SGQF Value Admission

The row may be admitted as `executed_value_only` only if a reviewed SGQF route:

- evaluates the exact reviewed source-row target,
- uses the synthetic prior-mean generalized-SV row contract,
- computes a finite value for the same declared scalar,
- does not rely on native-oracle or precursor evidence as admission by itself,
- and explicitly states whether the admitted route is exact-target or
  approximate-but-explained.

## Required Conditions For SGQF Value+Score Admission

The row may be admitted as `executed_value_score` only if, in addition to value
admission:

- the row has a reviewed free-theta contract,
- the analytical/manual score route differentiates the same declared scalar,
- autodiff/`GradientTape`/finite differences are not the admitted score route,
- any supporting FD or score-at-true diagnostics are interpreted only in their
  reviewed explanatory or repair-trigger role,
- and any approximation gap is measured and honestly explained at the reviewed
  claim level.

## Analytical/Manual Provenance Rule

For this row, admitted analytical/manual score provenance must be supported by a
reviewed artifact that does all of the following:

- names the declared scalar being differentiated for this exact source row,
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

- native generalized-SV dense oracle evidence is not source-row SGQF admission
  evidence by itself;
- precursor or auxiliary generalized-SV evidence is not source-row SGQF
  admission evidence by itself;
- no HMC readiness, production readiness, or default-policy claim follows from
  this row contract.
