# Phase 3 result: Zhao-Cui LGSSM m3 evaluator adapter

Date: 2026-06-30

Status: `PASSED`

Subplan: `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-subplan-2026-06-30.md`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Wire `zhao_cui_scalar_or_multistate` on `benchmark_lgssm_exact_oracle_m3_T50` through the user-amended exact-oracle LGSSM adapter. |
| Primary criterion status | Passed locally: finite value and score, target-compatible exact-oracle status, Kalman tie-out, and explicit derivative provenance. |
| Veto diagnostic status | Passed locally: no ALS/training route used; no source-faithful or paper-scale Zhao-Cui claim; score coordinate is `physical_theta`; value gap to Kalman is below `1e-7`. |
| Main uncertainty | This is an exact-oracle affine LGSSM adapter for the user-amended benchmark row, not a Zhao-Cui MATLAB `rng(0)` reproduction or TT-cross/SIRT training result. |
| Next justified action | Advance to Phase 4 after Claude result review convergence. |
| Not concluded | No nonlinear Zhao-Cui production readiness, no paper-scale Zhao-Cui TT source-faithfulness, no HMC/GPU readiness. |

## Rationale

The source-scope contract says `zhao_cui_lgssm_kalman_m3_T50` was superseded by `benchmark_lgssm_exact_oracle_m3_T50`, and that exact Zhao-Cui MATLAB `rng(0); rand(3,3)` reproduction is not required for LGSSM. Phase 3 therefore closes the adapter blocker by using the reviewed exact-oracle LGSSM value/score reference for this amended row, not by reviving historical Zhao-Cui training or ALS.

## What Changed

- Added `_zhao_cui_lgssm_exact_oracle_adapter()` to `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.
- Routed only the `benchmark_lgssm_exact_oracle_m3_T50` / `zhao_cui_scalar_or_multistate` cell through that adapter.
- Added `tests/test_two_lane_highdim_leaderboard_phase3.py`.
- Regenerated:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

## Numerical Result

For row `benchmark_lgssm_exact_oracle_m3_T50`, algorithm `zhao_cui_scalar_or_multistate`:

| Metric | Value |
| --- | ---: |
| status | `executed_value_score` |
| numeric status | `executed_lgssm_exact_oracle_adapter_value_score` |
| log likelihood | -136.07597485308665 |
| average log likelihood | -2.721519497061733 |
| value gap to Kalman | 4.838057066081092e-09 |
| score | `[5.655446876369503, -3.83505645148858, 0.3023616684162056, -1.9171806685717399, 4.354265155260018]` |
| score L2 norm | 8.331768521408039 |
| score coordinate system | `physical_theta` |
| score provenance | `zhao_cui_lgssm_user_amended_exact_oracle_affine_adapter_to_tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta` |

The LGSSM row summary is now full three-way ready with `fixed_sgqf`, `ukf`, and `zhao_cui_scalar_or_multistate` executed.

## Local Checks

All TensorFlow checks were CPU-only with `CUDA_VISIBLE_DEVICES=-1`. TensorFlow emitted CUDA factory/cuInit startup warnings during import/regeneration despite CPU masking; these are non-authoritative for this CPU-only artifact.

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase3.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase3.py -q` | Passed: 1 passed |
| adapter row assertion for status, finite 5-vector score, and Kalman value gap below `1e-7` | Passed |
| adapter boundary guard for no fixed TT training route, no source-faithful claim, and explicit no-historical-ALS nonclaim | Passed |
| regenerated leaderboard JSON assertion for LGSSM row full three-way readiness | Passed |
| `git diff --check` on changed Phase 3 code/test/artifact paths | Passed |

## Evidence Contract Close

The Phase 3 evidence contract asked whether Zhao-Cui can evaluate the affine LGSSM m3 row with value and score rather than an adapter blocker.

Result: yes, because the source-scope row is the user-amended exact-oracle LGSSM benchmark. The emitted adapter is target-compatible for that amended row and explicitly does not claim source-faithful Zhao-Cui TT training.

## Claude Review

Claude read-only bounded review of this result returned `VERDICT: AGREE`.

Review caveat: Claude reviewed exactly this result path and did not independently inspect the cited code, tests, or subplan.

## Next-Phase Handoff

Phase 4 may start. Phase 4 target:

- `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-subplan-2026-06-30.md`
- objective: preserve the predator-prey SGQF value row, admit strict analytical score only if implemented safely, and repair or precisely close the Zhao-Cui predator-prey adapter.
