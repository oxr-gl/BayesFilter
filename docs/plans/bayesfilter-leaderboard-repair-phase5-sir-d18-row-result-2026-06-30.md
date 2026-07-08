# Phase 5 result: spatial SIR d18 parameterized observed-data row

Date: 2026-06-30

Status: `PASSED_WITH_PRECISE_BLOCKER`

Subplan: `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Do not promote P91 Zhao-Cui SIR d18 local complete-data component evidence into a full observed-data/filtering leaderboard value/score row. Preserve the P91 sidecar and keep the full filtering row blocked. |
| Primary criterion status | Passed by precise blocker: no reviewed full observed-data/filtering evaluator with previous-marginal and fixed-TTSIRT proposal/transport derivatives is available in this phase. |
| Veto diagnostic status | Passed: no complete-data component is called a full filtering likelihood; no score row is emitted without a full observed-data target; no GPU/XLA/HMC sidecar is promoted to row admission. |
| Main uncertainty | A future observed-data SIR d18 row may be possible, but it requires derivative/evaluator work beyond the scoped P91 local component. |
| Next justified action | Advance to Phase 6 after Claude result review convergence. |
| Not concluded | No exact likelihood correctness, no full observed-data/filtering score identity, no posterior correctness or convergence, no broad Zhao-Cui production/readiness claim for the full leaderboard row. |

## Row-Admission Audit

The agreed Phase 5 subplan required an observed-data row-admission contract before execution: declared free `theta`, observed-data target, finite value/score, and expected-score calibration across generated observed-data datasets.

Audit result: no full observed-data/filtering evaluator is currently available. The available P91 route is scoped to:

- `ParameterizedZhaoCuiSIRSSM`;
- three-parameter log-scale surface `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`;
- local complete-data component value/score conditioned on a fixed latent state path and observation path.

The following blockers remain preserved for the full observed-data/filtering route:

- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`;
- `full_observed_data_filtering_score_identity = NOT_CLAIMED`.

Because no full observed-data score row was admitted, no expected-score calibration manifest was generated in Phase 5.

## What Changed

- Added `tests/test_two_lane_highdim_leaderboard_phase5.py` to lock the SIR row boundary:
  - P91 remains sidecar evidence;
  - the Zhao-Cui full observed-data/filtering leaderboard row remains blocked;
  - nonclaims preserve no exact likelihood, no full observed-data/filtering score identity, and no posterior correctness/convergence.
- Regenerated:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

## Generated Leaderboard Status

For row `zhao_cui_spatial_sir_austria_j9_T20`, algorithm `zhao_cui_scalar_or_multistate`:

| Field | Value |
| --- | --- |
| comparison status | `blocked_or_status_only` |
| numeric status | `blocked_full_filtering_evaluator_pending_p91_local_component_ready` |
| target contract | `full_filtering_blocked_local_complete_data_component_ready` |
| reason codes | `P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED`, `P91_SCOPED_LOCAL_COMPLETE_DATA_READY`, `FULL_FILTERING_LEADERBOARD_CELL_STILL_BLOCKED` |
| P91 sidecar scope | `local_complete_data_zhao_cui_sir_d18_component` |
| P91 sidecar status | `P91_SCOPED_PRODUCTION_READY_CLOSED` |
| P91 score identity | `PASS_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY` |
| P91 GPU/XLA | `PASS_P91_PHASE5_GPU_XLA_JIT_LOCAL_COMPLETE_DATA` |
| P91 benchmark | `PASS_P91_PHASE6_PERFORMANCE_BENCHMARK` |
| P91 HMC smoke | `PASS_P91_PHASE7_HMC_SMOKE` |

## Local Checks

All TensorFlow checks were CPU-only with `CUDA_VISIBLE_DEVICES=-1`. TensorFlow emitted CUDA factory/cuInit startup warnings during import/regeneration despite CPU masking; these are non-authoritative for this CPU-only artifact.

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase5.py -q` | Passed: 1 passed |
| `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md` | Passed |
| regenerated JSON assertion for SIR P91 sidecar plus full-filtering blocker | Passed |

## Evidence Contract Close

The Phase 5 evidence contract asked whether the SIR d18 row can be turned into a real observed-data likelihood/score row.

Result: not in this phase. The row remains blocked with a precise missing full-filtering evaluator/derivative item, while the P91 local complete-data component evidence is preserved as sidecar context only. This satisfies the phase by avoiding the false claim that a local complete-data component is the full observed-data likelihood.

## Next-Phase Handoff

Phase 6 may start. Phase 6 target:

- `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md`
- objective: freeze the exact generalized-SV target/evaluator status and either wire reviewed SGQF/Zhao-Cui cells or preserve precise target/evaluator blockers.
