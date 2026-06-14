# P47-M5b Subplan: Predator-Prey Production Row Repair

metadata_date: 2026-06-09
phase: P47-M5b
status: `EXECUTED_ACCURACY_TUNING_BLOCKED_REVIEW_PENDING`

## Purpose

Try to repair `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` with a
near-paper horizon row on the same additive-Gaussian RK4 predator-prey target
used by M5a.

## Prerequisites

- `PASS_P47_M2_PAPER_SCALE_READINESS`
- `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`
- M1 route label: `documented-deviation fixed-design substitute`
- S&P 500 reproduction remains out of scope.

## Evidence Contract

Question: does the fixed-design Zhao--Cui predator-prey route remain accurate
on a longer same-target synthetic path under the M2 near-paper horizon cap?

Primary pass criterion: the horizon-25 row preserves target identity,
parameterization, route label, and branch determinism; compares against a
dense/refined same-target reference; reports log-likelihood, per-step
normalizer, state-mean, covariance, and truth-path RMSE metrics; and satisfies
the reviewed tolerances.

Production tolerances for the first repair attempt:

- absolute log-likelihood gap against dense/refined reference: `< 5.0`;
- maximum per-step log-normalizer gap: `< 1.0`;
- maximum state-mean component error against dense/refined reference: `< 5.0`;
- maximum covariance-entry error against dense/refined reference: `< 8.0`;
- truth-path prey RMSE: `< 8.0`;
- truth-path predator RMSE: `< 2.0`;
- deterministic replay: exact branch hash and log-likelihood replay.

These tolerances are production-repair tolerances for the fixed-design
substitute route, not claims of native non-Gaussian predator-prey correctness.

## Ladder

Run one horizon axis at a time:

| Candidate | Horizon | State Dim | TT Fit Order | Dense Reference Order | Rank |
| --- | ---: | ---: | ---: | ---: | ---: |
| M5b-0 | 4 | 2 | 7 | 9 | 8 |
| M5b-1 | 8 | 2 | 7 | 9 | 8 |
| M5b-2 | 16 | 2 | 7 | 9 | 8 |
| M5b-3 | 25 | 2 | 7 | 9 | 8 |

Coordinate-map amendment from M5a:

- M5a window: prey `[20, 110]`, predator approximately `[0, 12]`.
- M5b horizon-25 deterministic path reaches prey about `114`, so the
  production row uses prey window approximately `[10, 130]` while retaining the
  same target family and observation law.

## Veto Diagnostics

- target or parameterization changes from M5a without amendment;
- dense/refined reference is absent;
- deterministic replay fails;
- nonfinite values, normalizers, covariance, or branch hashes appear;
- proposal/preconditioning diagnostics are used as filtering correctness;
- S&P 500 data or claims appear.

## Expected Token

```text
PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING
```

If any production criterion fails, record a reviewed blocker instead of
loosening tolerances after the fact.

## Initial Execution Result

The horizon-25 same-target production candidate ran deterministically and
remained finite, but failed the reviewed production tolerances:

- log-likelihood gap against dense/refined reference: about `145.776`;
- maximum per-step log-normalizer gap: about `11.415`;
- maximum state-mean component error: about `19.455`;
- maximum covariance-entry error: about `44.620`;
- truth-path RMSE: about `[2.992, 0.967]`.

A diagnostic horizon ladder with the widened production window showed that the
gap is already visible at horizon 4.  A quick tuning probe with higher order,
higher rank, and several window choices hit `CONDITION_NUMBER_VETO` rather
than repairing the row.

Decision: record `BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING`; do not emit
`PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING`.
