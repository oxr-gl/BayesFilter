# P47-M5 Claude Review Ledger

metadata_date: 2026-06-08
phase: P47-M5
status: `DRAFT_REVIEW_PENDING`

## Review Protocol

Claude is read-only reviewer.  Codex is supervisor and execution agent.
Claude must not edit files, run experiments, launch agents, or change state.

Expected terminal token for the first M5 gate:

```text
PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING
```

or

```text
BLOCK_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING
```

The production token `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` is not
requested by the M5a review.

## Iteration 1

Claude returned:

```text
BLOCK_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING
```

Blocking finding:

- The executable M5a gate compared value and state means but did not gate
  covariance or second-moment/state-uncertainty agreement, even though the
  result note claimed value/state moments and both the dense reference and
  Zhao--Cui result expose covariance paths.

Resolution before Iteration 2:

- Added `zhao_cui_vs_dense_covariance_abs` to the target manifest.
- Added a focused covariance-path comparison in
  `tests/highdim/test_p47_predator_prey_filtering.py`.
- Updated the result note to claim value, state means, and state covariance
  explicitly rather than using loose "state moments" wording.

## Iteration 2

Claude returned:

```text
PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING
```

Findings summary:

- No blocking findings remained.
- The Iteration 1 covariance/state-uncertainty blocker was resolved by the
  manifest tolerance and executable covariance-path comparison.
- M5a preserves lower-rung versus production-token split; the production token
  is not emitted.
- The promoted target is the near-RK4 replayable additive-Gaussian RK4
  predator-prey closure, while the P44 tense pair remains a diagnostic
  non-promotion.
- Zhao--Cui fixed-design retained-grid filtering is compared to a dense
  reference on the same target for value, state means, and covariance.
- CUT4 and preconditioning metrics remain diagnostic or proxy-only.
