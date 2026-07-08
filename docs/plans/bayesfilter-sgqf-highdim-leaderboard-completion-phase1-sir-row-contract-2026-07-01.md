# Phase 1 SGQF Spatial SIR Row Contract

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Purpose

Freeze the exact SGQF row contract for `zhao_cui_spatial_sir_austria_j9_T20`
before any SGQF implementation or runtime work begins.

## Governing Row Identity

The row is exactly:

```text
zhao_cui_spatial_sir_austria_j9_T20
```

This row is a source-scope spatial SIR observed-data leaderboard row. It is not
the lower-rung spatial SIR reference-equality fixture, not the P91 local
complete-data sidecar, and not a free-theta score row unless a reviewed artifact
first declares the required free-theta / derivative ownership for that row.

## Current Authority Inputs

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`

## Current Reviewed Status

Current leaderboard state:

- SGQF: `blocked`
- UKF: `executed_value_only`
- Zhao-Cui: `blocked_or_status_only`

Current SGQF blocker reason:

- `no reviewed SGQF source-scope spatial SIR route is wired`

Current row caveat:

- the row currently has no admitted SGQF analytical-score route,
- and no full observed-data SGQF evaluator contract has been reviewed.

## Required Conditions For SGQF Value Admission

The row may be admitted as `executed_value_only` only if a reviewed SGQF route:

- evaluates the full observed-data row rather than a local complete-data sidecar,
- computes a finite value for the exact reviewed row target,
- is not mislabeled from lower-rung or auxiliary evidence,
- and preserves row-specific nonclaims honestly.

## Required Conditions For SGQF Value+Score Admission

The row may be admitted as `executed_value_score` only if, in addition to value
admission:

- the row has a reviewed free-theta contract,
- the analytical/manual score route differentiates the same declared scalar,
- autodiff/`GradientTape`/finite-difference provenance is not used as the
  admitted score route,
- any score-at-true or FD diagnostics are recorded with the correct scoped
  interpretation.

## Explicit Nonclaims

- P91 local complete-data evidence is not full observed-data/filtering row
  admission evidence.
- No SGQF score row is admitted merely because UKF or sidecar evidence exists.
- No HMC readiness, production readiness, or default-policy claim follows from
  this row contract.
