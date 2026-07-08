# BayesFilter leaderboard repair reset memo

Date: 2026-06-30

Status: `PROGRAM_CLOSED_REVIEWED`

## Summary

The governed leaderboard repair program closed the non-LEDH high-dimensional
leaderboard rebuild for SGQF, UKF, and Zhao-Cui rows. The final artifacts are:

- JSON:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- Immutable Phase 7 preservation baseline:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json`

LEDH/PFPF-OT/DPF rows remain omitted from this leaderboard program by scope.

## Final Row Status

| Row | Executed algorithms | Remaining blocked/missing algorithms |
| --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | fixed-SGQF, UKF, Zhao-Cui | none |
| `zhao_cui_sv_actual_nongaussian_T1000` | fixed-SGQF, UKF, Zhao-Cui | none |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | fixed-SGQF, UKF, Zhao-Cui | none |
| `zhao_cui_spatial_sir_austria_j9_T20` | UKF value-only | fixed-SGQF source-scope route; Zhao-Cui full observed-data/filtering evaluator |
| `zhao_cui_predator_prey_T20` | UKF | fixed-SGQF T20 evaluator; Zhao-Cui model-specific evaluator adapter |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | UKF | exact source-row fixed-SGQF evaluator; exact source-row Zhao-Cui evaluator adapter |

## Key Repairs

- Actual transformed-SV fixed-SGQF no longer carries the stale
  `blocked_not_same_target` blocker.
- Fixed-SGQF actual-SV, KSC surrogate-SV, and LGSSM rows emit analytical score
  provenance from reviewed manual/analytical routes, not `GradientTape` fallback.
- Zhao-Cui LGSSM m3 uses a user-amended exact-oracle adapter and does not claim
  paper-scale/source-faithful TT training.
- Predator-prey fixed-SGQF T20 is blocked precisely instead of reusing the P47
  two-observation diagnostic as a T20 source-scope value.
- SIR d18 P91 evidence is preserved only as scoped local complete-data sidecar
  evidence; the full observed-data/filtering leaderboard row remains blocked.
- Generalized-SV fixed-SGQF and Zhao-Cui rows now state exact source-row
  evaluator blockers and explicitly forbid precursor, native-oracle, auxiliary,
  actual-SV, and KSC evidence as admission evidence.
- Phase 7 batch/GPU/XLA status fields are present for every row. Blocked and
  value-only rows are not timing-rankable.
- P91 CPU/GPU/XLA timings are structurally isolated under
  `p91_scoped_evidence.phase7_sidecar_performance`.

## Final Evidence Gates

- Phase 7 preservation baseline SHA-256:
  `cb71a48830d6daf62062a3dec55ad93f238c1d41aad6a75e5f1bfc6b803c6f2f`.
- Final focused tests:
  `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py -q`
  passed, 9 tests, 2 warnings, 382.52 seconds.
- Final schema/preservation validation passed against the immutable Phase 7
  baseline.
- Claude agreed on the final Phase 8 result in the review ledger.

## Nonclaims

- This is not a scientific superiority claim for any algorithm.
- This is not exact nonlinear likelihood certification.
- This is not posterior convergence or HMC production readiness.
- Main leaderboard rows are not a production-GPU timing packet.
- P91 Zhao-Cui SIR d18 CPU/GPU/XLA timings are scoped local complete-data
  sidecar evidence and are not full observed-data/filtering leaderboard timing.
- Rows with blocked or missing algorithms are not full three-way leaderboard
  rows.
- CUT4, LEDH/PFPF-OT, and DPF transport rows remain outside this leaderboard
  repair program.

## Recommended Next Program

Open a separate governed implementation program for remaining blockers:

- fixed-SGQF spatial SIR source-scope route;
- Zhao-Cui full SIR observed-data/filtering evaluator;
- fixed-SGQF and Zhao-Cui predator-prey T20 evaluator/adapters;
- fixed-SGQF and Zhao-Cui generalized-SV exact source-row evaluators;
- row-specific batched/GPU/XLA benchmarks for admitted main rows.
