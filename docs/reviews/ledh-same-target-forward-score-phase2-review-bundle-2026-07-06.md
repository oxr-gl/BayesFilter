# Claude Read-Only Review Bundle: LEDH Same-Target Phase 2

metadata_date: 2026-07-06
review_scope: bounded_phase2_common_forward_api
codex_role: supervisor_and_executor
claude_role: read_only_reviewer

## Objective

Review the Phase 2 common forward likelihood API for LEDH high-dimensional
leaderboard rows.

The review question is narrow:

Does the Phase 2 API and handoff prevent proposal/flow quantities from being
mistaken for the leaderboard target scalar, while preserving the amended fixed
SIR 3D `sir_log_scale_theta` contract and keeping scoped parameterized SIR
diagnostic evidence out of the fixed full-row gate?

## Files To Inspect

- `bayesfilter/highdim/ledh_forward_contract.py`
- `tests/highdim/test_ledh_forward_contract_phase2.py`
- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
  - inspect import of `make_lgssm_m3_t50_forward_contract`
  - inspect `_build_lgssm_tensors` target identity construction
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - inspect import of `make_parameterized_sir_diagnostic_forward_contract`
  - inspect `main()` result metadata around `forward_contract`
- `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
  - inspect helper contract synthesis and `_lgssm_ledh_row`, `_sir_ledh_row`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-result-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-subplan-2026-07-06.md`

Do not inspect unrelated files unless required to answer the bounded question.

## Contract Intended By Codex

- `target_scalar = observed_data_log_likelihood_estimator`
- output tensor field is `log_likelihood`
- target density fields include:
  - `transition_log_density`
  - `observation_log_density`
- proposal/flow correction fields include:
  - `pre_flow_log_density`
  - `forward_log_det`
  - `proposal_observation_surface`
- correction formula:
  `transition_log_density + observation_log_density - pre_flow_log_density + forward_log_det`
- fixed SIR must be:
  - `row_id = zhao_cui_spatial_sir_austria_j9_T20`
  - `row_scope = main_observed_data_filtering_row`
  - `theta_coordinate_system = sir_log_scale_theta`
  - `theta_dimension = 3`
  - parameter order `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`
  - truth theta `[0,0,0]`
- scoped parameterized SIR must remain:
  - `row_id = zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`
  - `row_scope = legacy_scoped_parameterized_sir_diagnostic`
  - `full_leaderboard_row = false`

## Local Checks Already Run

CPU-only checks intentionally hid GPU devices with `CUDA_VISIBLE_DEVICES=-1`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  bayesfilter/highdim/ledh_forward_contract.py \
  bayesfilter/highdim/__init__.py \
  docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_score_remains_blocked \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful -q
```

Result: `18 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_lgssm_manual_score_phase4.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

Result: `13 passed, 2 warnings`.

```text
git diff --check -- <Phase 2 files>
```

Result: passed.

## Pass Criteria

Return `VERDICT: AGREE` only if:

- the contract rejects proposal scalar use as target scalar;
- required target density fields cannot be omitted;
- target density fields and proposal flow fields cannot overlap;
- fixed SIR cannot regress to `no_free_theta`;
- fixed SIR uses the amended 3D `sir_log_scale_theta` contract;
- scoped parameterized SIR cannot be promoted to a full leaderboard row;
- Phase 2 result and Phase 3 subplan do not claim row or score admission from
  metadata alone.

Return `VERDICT: REVISE` if any material blocker remains.

## Forbidden Reviewer Actions

Claude must not edit files, run commands, launch agents, authorize gates, or
make scientific/product claims. Claude is read-only reviewer only.

## Required Output Format

Use concise bullets. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
