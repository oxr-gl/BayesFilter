# Phase 4 Result: Fixed SIR Score Target Classification

Date: 2026-07-03

Status: `FIXED_SIR_MAIN_ROW_NO_FREE_THETA_VALUE_ONLY`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Keep the fixed spatial SIR main row value-only for LEDH; do not define or admit a score for that row. |
| Primary criterion status | Passed: the main row has no free theta; the parameterized SIR row is scoped component evidence only. |
| Veto diagnostic status | No scoped local-complete-data score was promoted to the full observed-data filtering row. |
| Main uncertainty | Whether a future human-approved parameterized full observed-data SIR row should be created separately. |
| Next justified action | Continue to nonlinear adapter admission with fixed SIR classified as `no_free_theta_value_only`. |
| What is not concluded | No LEDH SIR score, no HMC readiness, no Zhao-Cui source-faithfulness claim, no full observed-data parameterized SIR score. |

## Evidence

Fixed spatial SIR main row:

- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:214-225`
  builds `zhao_cui_spatial_sir_austria_j9_T20` with
  `truth_theta_coordinate = "no_free_theta"` and `truth_theta = []`.
- `bayesfilter/highdim/models.py:705-706` defines
  `SpatialSIRSSM.parameter_dim()` as `0`.
- The LEDH-inclusive admission ledger records the fixed SIR row as
  `main_observed_data_filtering_row`, with a fixed-parameter observed-data
  value target candidate and score blocked unless a full-row total-derivative
  score target is defined.

Parameterized SIR scoped row:

- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:228-255`
  builds `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` with
  `truth_theta_coordinate = "sir_log_scale_theta"` and three parameters.
- `bayesfilter/highdim/models.py:935-945` defines
  `ParameterizedZhaoCuiSIRSSM.parameter_dim()` as `3`.
- The LEDH-inclusive admission ledger records this row as
  `scoped_component_row_in_current_baseline`, not a full observed-data
  filtering row.
- The July 3 LEDH-inclusive leaderboard records the parameterized SIR LEDH row
  as `scoped_component_status_only`, with no LEDH score vector.

## Plain Scientific Classification

The fixed spatial SIR main row has no score coordinate.  A score with respect
to `log_kappa_scale`, `log_nu_scale`, or `log_obs_noise_scale` would be a score
for a different parameterized target, not the fixed main row.

Therefore, for the current leaderboard:

- fixed SIR main row: `no_free_theta_value_only`;
- parameterized SIR log-scale row: scoped component evidence only;
- no LEDH SIR score row is admitted.

## Checks Run

- Inspected current LEDH-inclusive row ledger and July 3 LEDH-inclusive
  leaderboard JSON for both SIR rows.
- Inspected dataset generator and model definitions for fixed versus
  parameterized SIR parameter dimensions.
- Confirmed the Phase 3 LGSSM blocker remains:
  `blocked_total_transport_vjp_needs_no_tape_repair`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded for this audit-only classification. |
| Commands | `rg`, `python` JSON inspection, `nl`. |
| Environment | Local repository audit; no GPU or TensorFlow execution required. |
| CPU/GPU status | GPU not used. |
| Data version | July 3 LEDH-inclusive leaderboard and P8 dataset generator. |
| Random seeds | N/A. |
| Wall time | N/A. |
| Output artifacts | This result file; refreshed Phase 5 subplan. |
| Plan file | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-subplan-2026-07-03.md` |

## Phase 5 Handoff

Phase 5 should list nonlinear rows that still need same-target LEDH adapters.
It must carry forward:

- LGSSM score blocked by
  `blocked_total_transport_vjp_needs_no_tape_repair`;
- fixed SIR main row classified as `no_free_theta_value_only`;
- parameterized SIR log-scale row classified as scoped component evidence only,
  not full observed-data filtering score evidence.
