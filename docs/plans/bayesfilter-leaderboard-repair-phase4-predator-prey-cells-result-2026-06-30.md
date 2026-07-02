# Phase 4 result: predator-prey SGQF and Zhao-Cui cells

Date: 2026-06-30

Status: `PASSED_WITH_PRECISE_BLOCKERS`

Subplan: `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-subplan-2026-06-30.md`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Do not report the available P47 two-observation SGQF predator-prey diagnostic as the source-scope `zhao_cui_predator_prey_T20` leaderboard row. Fail the fixed-SGQF predator-prey cell closed with a T20 evaluator blocker. |
| Primary criterion status | Passed: the predator-prey fixed-SGQF row is now either T20-aligned or blocked; in this phase it is blocked because no reviewed T20 fixed-SGQF evaluator is wired. |
| Veto diagnostic status | Passed: no P47 lower-rung value is reported as T20; no tape/autodiff derivative is claimed as analytical; no value/score is emitted for the blocked fixed-SGQF T20 cell. |
| Main uncertainty | A target-compatible T20 fixed-SGQF predator-prey evaluator may still be implementable later, but it was not already present under a reviewed source-scope contract. |
| Next justified action | Advance to Phase 5 after Claude result review convergence. |
| Not concluded | No predator-prey SGQF production readiness, no Zhao-Cui predator-prey adapter readiness, no HMC convergence, and no runtime comparison for the blocked fixed-SGQF cell. |

## What Changed

- Removed the stale P47 fixture import path from `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.
- Replaced the fixed-SGQF `zhao_cui_predator_prey_T20` emitted value with a precise target-alignment blocker:
  - `comparison_status`: `blocked`
  - `numeric_execution_status`: `blocked_predator_prey_sgqf_value`
  - `target_contract_status`: `blocked_missing_t20_fixed_sgqf_evaluator`
  - `score_status`: `blocked_target_alignment`
  - `reason_codes`: `PREDATOR_PREY_T20_FIXED_SGQF_EVALUATOR_REQUIRED`
- Added `tests/test_two_lane_highdim_leaderboard_phase4.py` to prevent the P47 lower-rung diagnostic from drifting back into the T20 leaderboard row.
- Regenerated:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

## Generated Leaderboard Status

For row `zhao_cui_predator_prey_T20`, algorithm `fixed_sgqf`:

| Metric | Value |
| --- | --- |
| comparison status | `blocked` |
| numeric status | `blocked_predator_prey_sgqf_value` |
| target contract | `blocked_missing_t20_fixed_sgqf_evaluator` |
| score status | `blocked_target_alignment` |
| log likelihood | `null` |
| average log likelihood | `null` |
| score | `null` |
| score provenance | `null` |
| blocker | no reviewed fixed-SGQF evaluator is wired for the source-scope T20 predator-prey observations |

The regenerated row explicitly records that the P47 two-observation lower-rung SGQF diagnostic is not reported as the T20 source-scope row.

## Local Checks

All TensorFlow checks were CPU-only with `CUDA_VISIBLE_DEVICES=-1`. TensorFlow emitted CUDA factory/cuInit startup warnings during import/regeneration despite CPU masking; these are non-authoritative for this CPU-only artifact.

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase4.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase4.py -q` | Passed: 1 passed |
| `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase4.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md` | Passed |
| regenerated JSON assertion for the fixed-SGQF predator-prey T20 blocker | Passed |

## Evidence Contract Close

The Phase 4 evidence contract asked whether predator-prey cells can be upgraded without target drift or mislabeling taped derivatives as analytical.

Result: the target-drift risk is removed. The fixed-SGQF T20 predator-prey cell remains blocked, but it is now blocked honestly and narrowly instead of reporting the P47 lower-rung diagnostic under the source-scope T20 row. Zhao-Cui predator-prey remains a model-specific evaluator-adapter blocker from the P8D source artifact.

## Next-Phase Handoff

Phase 5 may start. Phase 5 target:

- `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md`
- objective: distinguish the existing P91 local complete-data SIR d18 component evidence from a true parameterized observed-data/filtering leaderboard row, and either implement the observed-data row or preserve a precise blocker.
