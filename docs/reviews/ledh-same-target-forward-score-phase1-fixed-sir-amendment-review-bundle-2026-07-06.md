# Claude Read-Only Review Bundle

Date: 2026-07-06
Review name: `ledh-same-target-forward-score-phase1-fixed-sir-amendment`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run commands, launch agents, approve boundary
crossings, or act as execution authority. Codex remains supervisor and
executor.

## Objective

Review the fixed SIR Phase 1 amendment. Decide whether the amended artifacts
are internally consistent and safe for Phase 2:

- fixed row `zhao_cui_spatial_sir_austria_j9_T20` now uses model parameters as
  free parameters;
- the coordinate is `sir_log_scale_theta`;
- theta is `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`;
- truth theta is `[0,0,0]`;
- this does not admit the full observed-data SIR LEDH score.

## Artifacts To Inspect

- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-contract-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-result-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-fixed-sir-free-theta-amendment-result-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-subplan-2026-07-06.md`
- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`
- `tests/test_ledh_score_memory_n10000.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed SIR row now expose model parameters as free theta without promoting unsupported score evidence? |
| Baseline/comparator | The prior Phase 1 zero-dimensional decision, the existing `ParameterizedZhaoCuiSIRSSM` 3D log-scale surface, and the human amendment on 2026-07-06. |
| Primary criterion | The fixed SIR row uses `sir_log_scale_theta`, theta dimension 3, truth theta `[0,0,0]`, and exact parameter order in docs, dataset generator, dataset tests, and active LEDH admission ledger. |
| Veto diagnostics | Any active artifact still treating fixed SIR as no-free-theta; any claim that the author fixed-parameter example had free inference theta; any promotion of scoped/local-complete-data score evidence as full observed-data SIR score evidence; any score admission before same-target forward scalar admission. |
| Explanatory diagnostics | Existing P8/P81/P91 analytical score hooks for the 3D surface and CPU-hidden focused tests. |
| Not concluded | No SIR LEDH score admission, exact nonlinear likelihood correctness, HMC readiness, or leaderboard promotion. |

## Checks Already Run

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_score_remains_blocked \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful \
  -q
```

Result: passed, `11 passed, 2 warnings`.

```bash
python -m py_compile \
  scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py \
  docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py
```

Result: passed.

```bash
git diff --check -- <amended files>
```

Result: passed.

## Review Questions

1. Are the amended fixed SIR theta contract and dataset metadata consistent?
2. Does the amendment preserve the boundary that no full observed-data SIR
   score is admitted yet?
3. Is Phase 2 safe to continue under this amended fixed SIR contract?
4. Is there any unsupported claim or stale active no-free-theta status that
   should block?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
