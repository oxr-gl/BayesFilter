# Phase 1 Result: Predator-Prey T20 Zhao-Cui Evaluator And Analytical Score

Date: 2026-07-02

Status: `PASS_PHASE1_PREDATOR_PREY_T20_ZHAOCUI_VALUE_SCORE_ROW_LOCAL`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Admit a row-local Zhao-Cui predator-prey T20 value/manual-score adapter for the additive-Gaussian RK4 source-scope closure. |
| Primary criterion status | Passed row-local gate: finite value, finite six-coordinate manual score, theta coordinates `(r, K, a, s, u, v)`, and no admitted autodiff/FD provenance. |
| Veto diagnostic status | Passed: no P47/two-observation evidence was reported as T20; FD is disabled for the admitted row; diagnostic tape is used only in a local formula test, not in row provenance; no GPU/XLA/HMC claim is made. |
| Main uncertainty | Full all-row leaderboard regeneration was intentionally deferred to Phase 6 because the full runner recomputes unrelated SV/KSC rows and exceeded the Phase 1 focused evidence budget. |
| Next justified action | Advance to Phase 2 generalized-SV exact source-row evaluator/score repair. |
| Not concluded | No native/non-Gaussian predator-prey likelihood claim, no source-faithful adaptive Zhao-Cui MATLAB TT-cross/SIRT reproduction, no production GPU/XLA readiness, no HMC readiness, no posterior correctness, and no ranking/timing claim. |

## Row-Local Result

Artifact:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json`

Key row values:

| Field | Value |
| --- | --- |
| `row_id` | `zhao_cui_predator_prey_T20` |
| `algorithm_id` | `zhao_cui_scalar_or_multistate` |
| `comparison_status` | `executed_value_score` |
| `numeric_execution_status` | `executed_zhao_cui_predator_prey_t20_multistate_tt_value_score` |
| `average_log_likelihood` | `-8.996196972444926` |
| `log_likelihood` | `-179.92393944889852` |
| `score_coordinate_system` | `theta=(r,K,a,s,u,v)` |
| `score` | `[141.17730810693365, 6.651004553129841, 0.16459087453501595, -61.27719592118952, -5.441160015818105, 6.293474048370024]` |
| `score_l2_norm` | `154.27055472098652` |
| `score_status` | `analytical_score_emitted` |
| `score_derivative_provenance` | `zhao_cui_predator_prey_t20_multistate_fixed_design_tt_manual_parameter_score_methods_only` |
| `runtime_seconds` | `107.88529662997462` |

The row's `phase7_batch_gpu_xla_status` remains
`not_claimed_no_trusted_row_specific_gpu_xla_manifest`; the runtime above is
CPU-only explanatory evidence and is not a Phase 7 timing/ranking artifact.

## Implementation Summary

Changed files:

- `bayesfilter/highdim/models.py`
  - Added manual predator-prey RK4 transition sensitivity propagation.
  - Added explicit manual density-score methods:
    `initial_log_density_parameter_score`,
    `transition_log_density_parameter_score`, and
    `observation_log_density_parameter_score`.
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
  - Added source-row T20 predator-prey observations/theta helpers.
  - Added a conservative 2D fixed-design multistate TT configuration.
  - Added `_zhao_cui_predator_prey_tt_cell()` and local admission through the
    analytical-score guard.
- `tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py`
  - Added T20 row identity, finite value/manual-score, FD-disabled, local
    analytical-score contract, and manual formula diagnostic tests.

Implementation classification:

- `extension_or_invention` / documented-deviation fixed-design substitute.
- This does not claim Zhao-Cui source-faithful adaptive TT-cross/SIRT behavior.

## Checks Run

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_predator_prey_comparison_blocker.py` | `8 passed, 2 warnings` |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py` | `4 passed, 2 warnings` |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/models.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_predator_prey_comparison_blocker.py` | passed |
| `git diff --check -- bayesfilter/highdim/models.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-subplan-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-claude-review-ledger-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md` | passed |
| Row-local JSON generation and `_validate_analytical_score_contract([row])` | passed |

The route scan still finds generic fallback/FD/tape code in shared modules and
a `GradientTape` diagnostic oracle in the new local formula test. These are not
admitted row provenance. The admitted row uses the model's explicit manual
parameter-score methods and has `finite_difference_h=()`.

## Interrupted Broad Checks

Two broad checks were interrupted with exit code `130` after exceeding the
Phase 1 focused evidence budget:

- combined pytest including `tests/test_two_lane_highdim_leaderboard_analytical_scores.py`;
- full `/tmp` leaderboard regeneration with
  `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.

Reason: both rebuild unrelated highdim rows. Phase 1 only needed row-local
admission evidence. Full all-row regeneration remains a Phase 6 responsibility
after the other blocker families are handled.

## Environment Notes

All TensorFlow checks were launched with `CUDA_VISIBLE_DEVICES=-1` and
`MPLCONFIGDIR=/tmp`. TensorFlow still printed CUDA plugin/cuInit messages from
the installed GPU build; these are environment-noise only and are not GPU
readiness evidence.

## Handoff

Phase 1 is closed as row-local admitted for the Zhao-Cui predator-prey T20
cell. Phase 2 may begin after its refreshed subplan review. Phase 2 must
preserve the rule that actual-SV, KSC, native-oracle, precursor, and auxiliary
evidence are context only and cannot admit the generalized-SV exact source row.
