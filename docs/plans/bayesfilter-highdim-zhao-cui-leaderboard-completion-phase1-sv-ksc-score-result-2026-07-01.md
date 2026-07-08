# Phase 1 Result: Actual-SV And KSC Zhao-Cui Analytical Score Repair

Date: 2026-07-01

Status: `PASS_PHASE1_SV_KSC_SCORE_REPAIR`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Admit the Zhao-Cui actual-SV T1000 and KSC T1000 cells as `executed_value_score` rows using the repaired scalar fixed-branch TT manual parameter-score adaptor. |
| Primary criterion status | Passed: both rows emit finite values, finite score vectors, theta coordinate order, and `manual_parameter_score_methods_only` provenance. |
| Veto diagnostic status | Passed: no admitted Zhao-Cui SV/KSC row uses `GradientTape`, autodiff, or FD provenance; actual transformed SV and KSC remain separate targets. |
| Main uncertainty | This is the fixed-design scalar TT route, not adaptive MATLAB TT-cross/SIRT source-faithful reproduction, and the run is CPU-only timing evidence. |
| Next justified action | Proceed to Phase 2 predator-prey T20 target/evaluator adapter inventory. |
| Not concluded | No exact native SV likelihood proof, posterior correctness, HMC readiness, production GPU/XLA performance, or source-faithful adaptive Zhao-Cui claim. |

## What Was Repaired

The problem was a wiring/adaptor gap. The previous leaderboard rows had value
execution, but their score provenance was TensorFlow autodiff, so the strict
analytical-score gate correctly demoted them to value-only rows.

The repair added explicit local parameter-score methods for
`StochasticVolatilitySSM` in `bayesfilter/highdim/models.py`, and the exact
transformed-SV and KSC transformed-SV model wrappers now expose manual
initial/transition/observation parameter-score methods in
`bayesfilter/highdim/sv_mixture_cut4.py`.

The scalar fixed-design TT score path in `bayesfilter/highdim/filtering.py`
now requires explicit model parameter-score methods before score execution and
records `target_derivative_backend = model_parameter_score_methods_only`. The
leaderboard Zhao-Cui SV/KSC cells use `finite_difference_h=()` and admit only
`manual_parameter_score_methods_only` provenance.

## Admitted Row Results

| Row | Status | Avg loglik | Loglik | Score | Score L2 | Runtime seconds | Provenance |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| `zhao_cui_sv_actual_nongaussian_T1000` | `executed_value_score` | -2.286226025206944 | -2286.226025206944 | `[5.664976797079538, -2.565685746163207]` | 6.21889905526007 | 779.0544941129629 | `zhao_cui_scalar_fixed_branch_tt_exact_transformed_sv_manual_parameter_score_methods_only` |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `executed_value_score` | -2.2844313590049508 | -2284.4313590049505 | `[4.880417582574909, -2.515938368614356]` | 5.4907578397678565 | 811.6524984900607 | `zhao_cui_scalar_fixed_branch_tt_ksc_mixture_manual_parameter_score_methods_only` |

Artifacts refreshed:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`

## Route Table

| Target | Value route | Score route | Theta order | FD use in leaderboard | Target distinction |
| --- | --- | --- | --- | --- | --- |
| Actual transformed SV | `exact_transformed_sv_independent_panel_zhaocui_tt_score` via scalar fixed-design TT on `z=log(y^2)` | `scalar_nonlinear_fixed_design_tt_score_path` using manual model parameter-score methods | `theta=[probit_gamma,log_beta]` | Disabled by `finite_difference_h=()` | Exact transformed target, not raw native SV likelihood and not KSC. |
| KSC transformed SV | `independent_panel_sv_mixture_zhaocui_tt_score` via scalar fixed-design TT on KSC finite mixture transform | `scalar_nonlinear_fixed_design_tt_score_path` using manual model parameter-score methods | `theta=[probit_gamma,log_beta]` | Disabled by `finite_difference_h=()` | Declared KSC Gaussian-mixture surrogate, not exact native SV and not actual transformed row. |

Function anchors inspected:

- `bayesfilter/highdim/models.py`: `StochasticVolatilitySSM.initial_log_density_parameter_score`, `transition_log_density_parameter_score`, `observation_log_density_parameter_score`.
- `bayesfilter/highdim/sv_mixture_cut4.py`: `ExactTransformedSVSSM.*_parameter_score`, `KSCMixtureTransformedSVSSM.*_parameter_score`, `exact_transformed_sv_independent_panel_zhaocui_tt_score`, `independent_panel_sv_mixture_zhaocui_tt_score`.
- `bayesfilter/highdim/filtering.py`: `_require_explicit_parameter_score_methods`, `scalar_nonlinear_fixed_design_tt_score_path`.
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`: `_zhao_cui_derivative_config_no_fd`, `_zhao_cui_actual_sv_tt_cell`, `_zhao_cui_ksc_tt_cell`, `_enforce_analytical_score_admission`.

Route scan interpretation:

- The admitted Zhao-Cui SV/KSC route contains manual score provenance and no admitted autodiff/FD provenance.
- `finite_difference_h` remains part of the generic scalar score diagnostic API, but the leaderboard config sets it to `()`.
- `GradientTape` occurrences remain in unrelated diagnostics or unit-test comparators; they are not in the admitted Zhao-Cui SV/KSC leaderboard score provenance.

## Checks Run

CPU-only commands used `CUDA_VISIBLE_DEVICES=-1`, `PYTHONDONTWRITEBYTECODE=1`,
and `MPLCONFIGDIR=/tmp` where TensorFlow or matplotlib could initialize.

| Check | Result |
| --- | --- |
| `python -m py_compile bayesfilter/highdim/models.py bayesfilter/highdim/sv_mixture_cut4.py bayesfilter/highdim/filtering.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_highdim_zhao_cui_leaderboard_phase1.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p44_nonlinear_transition.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py` | Passed |
| `pytest -q tests/test_highdim_zhao_cui_leaderboard_phase1.py` | Passed: 3 tests |
| `pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "scalar_fixed_design_tt_score_path or stochastic_volatility_local_parameter_scores or transformed_sv_local_observation_scores"` | Passed: 4 tests, 22 deselected |
| `pytest -q tests/highdim/test_p44_nonlinear_transition.py::test_p44_m4_zhaocui_horizon_4_scalar_helper_runs_full_observation_path` | Passed |
| `pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py::test_zhao_cui_sv_cells_use_manual_tt_score_rows_without_full_payload_rebuild` | Passed |
| `git diff --check` on touched Phase 1 code/tests/artifacts | Passed |
| Full leaderboard regeneration command | Passed; refreshed JSON and Markdown artifacts |

TensorFlow printed CUDA registration/cuInit startup messages despite
`CUDA_VISIBLE_DEVICES=-1`; this run was intentionally CPU-only and did not
claim GPU/CUDA evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Repository | `/home/chakwong/BayesFilter` |
| Git state | Dirty worktree with many unrelated existing changes; Phase 1 touched only Zhao-Cui SV/KSC repair files, leaderboard artifacts, and tests. |
| Command | `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md` |
| Backend/device | TensorFlow CPU-only by explicit device hiding; no GPU/XLA claim. |
| Seeds | Leaderboard helper seeds: `leaderboard-zhaocui-actual-sv-manual-score`, `leaderboard-zhaocui-ksc-manual-score`; dataset helper seed remains the script's `_sv_dataset(81101)` binding. |
| Wall time | Actual-SV Zhao-Cui row: 779.0544941129629 seconds; KSC Zhao-Cui row: 811.6524984900607 seconds. |
| Output artifacts | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-subplan-2026-07-01.md` |
| Result | This file. |

## Handoff

Phase 1 is complete. Phase 2 should start from the refreshed leaderboard where
the actual-SV and KSC Zhao-Cui rows are no longer blocked by autodiff-score
admission. The remaining Zhao-Cui work is predator-prey T20, generalized SV,
and SIR full observed-data/filtering rows; SGQF remains out of scope for this
Zhao-Cui-only program.
