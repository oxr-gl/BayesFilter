# Phase 3 Result: Runner Wiring And Guards

Date: 2026-07-03

Status: `PASS_PHASE3_RUNNER_WIRING_FOCUSED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 3 passes focused wiring checks. The runner can emit the scoped parameterized SIR fixed-variant local complete-data value/manual-score row without selecting the demoted retained-grid route. |
| Primary criterion status | Passed: focused tests and probes exercise row id, score provenance, target scope, row admission, retained-grid exclusion, and Phase 7 scoped timing metadata. |
| Veto diagnostic status | Passed for focused gate: no autodiff/FD score is admitted, the fixed/no-free-theta row remains separate, and the scoped row requires metadata beyond row id. |
| Main uncertainty | Full artifact regeneration is deferred to Phase 4 because the full runner builds expensive unrelated rows. |
| Next justified action | Run Phase 4 regeneration and artifact validation. |
| What is not being concluded | No full observed-data/filtering SIR score identity, no exact likelihood correctness, no posterior correctness, no universal GPU timing claim, and no final leaderboard artifact yet. |

## Implementation Summary

Changed runner:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

Changed focused tests:

- `tests/test_two_lane_highdim_leaderboard_phase5.py`
- `tests/test_two_lane_highdim_leaderboard_phase7.py`

Key behavior:

- Adds `PARAMETERIZED_SIR_ROW =
  zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`.
- Emits a `zhao_cui_scalar_or_multistate` scoped component row with:
  - `comparison_status = executed_value_score`;
  - `row_admission_status = scoped_component_row_admitted`;
  - `target_scope = local_complete_data_zhao_cui_sir_d18_component`;
  - `route_role = fixed_variant_zhao_cui_source_route`;
  - `retained_grid_leaderboard_admission =
    not_admitted_for_production_leaderboard_use_fixed_variant_zhao_cui`;
  - `score_derivative_provenance =
    zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods`.
- Computes value by summing `ParameterizedZhaoCuiSIRSSM` initial,
  transition, and observation log densities along the generated T20 latent
  path and observations.
- Computes score by summing explicit manual parameter-score methods:
  `initial_log_density_parameter_score`,
  `transition_log_density_parameter_score`, and
  `observation_log_density_parameter_score`.
- Emits blocked/not-applicable fixed-SGQF and UKF companion cells for the
  scoped component row.
- Keeps the original `zhao_cui_spatial_sir_austria_j9_T20` fixed/no-free-theta
  row separate.
- Adds a metadata admission guard: row id alone is insufficient for score
  admission.

## Numeric Probe

Scoped row direct probe:

```text
comparison_status = executed_value_score
row_admission_status = scoped_component_row_admitted
target_scope = local_complete_data_zhao_cui_sir_d18_component
average_log_likelihood = -60.44641064507831
score = [1163.1499331099205, -508.7932467308049, 21.10862132639743]
```

The score is analytical/manual under the Phase 3 route. No autodiff or finite
difference score is admitted.

## Local Checks

Commands:

```bash
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py
git diff --check -- docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-*.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py::test_phase7_parameterized_sir_scoped_component_is_not_full_row_timing tests/test_highdim_zhao_cui_leaderboard_phase1.py::test_phase1_enforcement_admits_only_repaired_manual_zhao_cui_rows
```

Outcome:

- `py_compile`: passed.
- `git diff --check`: passed.
- Focused pytest: `5 passed, 2 warnings in 7.08s`.
- Warnings were TensorFlow Probability `distutils` deprecation warnings.

Additional probe:

- A miniature `build_artifact()` probe with unrelated expensive rows stubbed
  confirmed:
  - the parameterized row emits three algorithm cells;
  - fixed-SGQF and UKF are blocked/not-applicable;
  - Zhao-Cui emits `executed_value_score`;
  - row summary has `row_scope = scoped_component_row`;
  - `scoped_component_ready = True`;
  - `full_three_way_ready = False`.

Interrupted check:

- A broader combined pytest command was manually interrupted after it ran
  longer than useful for the focused Phase 3 gate. It had emitted three
  progress dots but no final result. Phase 4 will exercise full artifact
  regeneration directly.

## Worktree Note

The leaderboard runner and focused test files are currently untracked in this
dirty research worktree, so `git diff` does not display their file content.
This result therefore records `rg`, `py_compile`, `git diff --check`, focused
pytest, and miniature builder-probe evidence rather than relying on a normal
tracked-file diff.

## Phase 4 Handoff

Phase 4 may start because:

- focused runner behavior passed;
- scoped-row metadata guards are in place;
- the retained-grid route is not selected for production admission;
- the original fixed row remains distinct;
- final artifact regeneration is the next required evidence.
