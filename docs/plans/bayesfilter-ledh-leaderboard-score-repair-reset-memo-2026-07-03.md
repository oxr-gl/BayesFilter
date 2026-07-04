# Reset Memo: LEDH Leaderboard Score Repair

Date: 2026-07-03

## State

The LEDH leaderboard score-repair runbook is closed.

Final status:

- admitted LEDH score rows: `0`;
- active leaderboard artifact:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`;
- no leaderboard merge was performed.

## What Was Established

- `score` means the total derivative of the exact same leaderboard likelihood
  scalar whose value is reported.
- A stopped partial derivative is not a score for MLE/HMC unless the stopped
  scalar is explicitly declared as the target.
- LEDH value and score must share the same scalar route:
  `value_route_id == score_route_id` and
  `value_score_route_status == same_route_value_score`.
- `GradientTape` and `ForwardAccumulator` are banned for production LEDH score
  computation in this program.

## Final Row Statuses

| Row | LEDH score status |
| --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `blocked_total_transport_vjp_needs_no_tape_repair` |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked_adapter_missing` |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked_target_mismatch` |
| `zhao_cui_spatial_sir_austria_j9_T20` | `no_free_theta_value_only` |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | `scoped_component_evidence_only_not_full_observed_data_filtering_score` |
| `zhao_cui_predator_prey_T20` | `blocked_adapter_missing` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_adapter_missing` |

## Main Blocker To Repair Next

The LGSSM route is blocked because:

- the no-tape manual route differentiates a stopped-scale/key target;
- the total-transport helper targets the right finite transport map but still
  uses `tf.GradientTape`;
- therefore no current route is both a total derivative of the unstopped LEDH
  scalar and no-tape/manual.

The next focused plan should implement the no-tape total VJP for finite
streaming Sinkhorn transport and validate it first on
`benchmark_lgssm_exact_oracle_m3_T50`.

## Do Not Do

- Do not resume Phase 6 as if nonlinear rows were admitted.
- Do not promote Contract E LGSSM score evidence to the leaderboard LGSSM row.
- Do not use scoped parameterized SIR diagnostics as the fixed SIR
  observed-data leaderboard score.
- Do not describe a stopped partial derivative as the score of the unstopped
  likelihood.
- Do not use tape/autodiff score routes for LEDH leaderboard score admission.

## Useful Artifacts

- Closeout:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase8-closeout-reset-result-2026-07-03.md`
- Phase 3 blocker:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-result-2026-07-03.md`
- Phase 7 no-op merge:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase7-leaderboard-merge-result-2026-07-03.md`
- Visible ledger:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-execution-ledger-2026-07-03.md`
