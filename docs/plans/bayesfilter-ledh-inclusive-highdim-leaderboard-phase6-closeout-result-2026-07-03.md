# Phase 6 Closeout: LEDH-Inclusive Highdim Leaderboard

Date: 2026-07-03

Status: `COMPLETE_VALUE_ONLY_LEDGER_SCORE_BLOCKED`

## Final Result

The LEDH-inclusive leaderboard artifact now exists:

- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`

It compares four algorithm labels on every highdim row:

- `fixed_sgqf`;
- `ukf`;
- `zhao_cui_scalar_or_multistate`;
- `ledh_pfpf_ot`.

Comparator mode is `frozen_non_ledh_baseline_plus_fresh_ledh`. Runtime
cross-ranking is forbidden.

## LEDH Row Statuses

| Row | LEDH status | Plain meaning |
| --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `executed_value_only_score_blocked` | Same-target LEDH value ran at `N=10000`; score is not implemented/admitted. |
| `zhao_cui_spatial_sir_austria_j9_T20` | `executed_value_only_score_blocked` | Fixed spatial SIR LEDH value ran at `N=10000`; score is not implemented/admitted. |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | `scoped_component_status_only` | Scoped component status only; not a full observed-data leaderboard LEDH score row. |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked` | No reviewed same-target LEDH adapter. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked` | No reviewed KSC LEDH adapter. |
| `zhao_cui_predator_prey_T20` | `blocked` | No reviewed same-target GPU/XLA LEDH adapter. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked` | No reviewed same-target LEDH adapter. |

No LEDH leaderboard score row is admitted.

## Key Numerical Results

LGSSM same-target LEDH value, `N=10000`:

- average log likelihood mean: `-2.719201477051`;
- MCSE: `0.0001186681274`;
- exact average Kalman value: `-2.721519497158`;
- relative error: `0.0852%`;
- score status: `blocked_score_same_target_total_derivative_not_implemented`.

Fixed spatial SIR LEDH value, `N=10000`:

- average log likelihood mean: `-45.141507568359`;
- MCSE: `0.010411105587`;
- score status: `blocked_score_for_full_leaderboard_row`.

## Important Repair

The earlier Contract E LGSSM diagnostic is not the leaderboard LGSSM row. It is
route evidence only. It is not merged as `benchmark_lgssm_exact_oracle_m3_T50`
score evidence.

Plainly: using Contract E as the leaderboard LGSSM score would be wrong-target
evidence.

## Checks

- `py_compile`: passed.
- Focused tests: `8 passed`.
- JSON content checks: passed.
- `git diff --check`: passed.
- Claude Phase 4 packet review: `VERDICT: AGREE`.
- Claude Phase 5 packet review: `VERDICT: REVISE`; wording patched to
  distinguish blocked main-row scores from scoped parameterized SIR evidence.

## Nonclaims

- This does not certify LEDH total-derivative score correctness.
- This does not certify HMC readiness.
- This does not certify posterior correctness or scientific superiority.
- This does not rank fresh LEDH runtime against frozen non-LEDH rows.
