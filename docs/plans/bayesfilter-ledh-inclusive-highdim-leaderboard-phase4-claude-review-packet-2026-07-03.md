# Phase 4 Claude Review Packet: LEDH Leaderboard Value-Only Repair

Date: 2026-07-03

Role: Claude is read-only reviewer. Codex is supervisor and executor.

## Review Question

Does the Phase 4 repair correctly prevent wrong-target LGSSM score evidence
from being promoted into the leaderboard, while preserving value-only LEDH
evidence for the admitted rows?

## Exact Paths For Review

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-subplan-2026-07-03.md`
- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- `tests/test_two_lane_highdim_ledh_leaderboard.py`

## Critical Repair

The previous Phase 3 LGSSM score diagnostic was Contract E:

- `D=2`;
- `T=10`;
- three parameters;
- value around `-13.8`;
- valid only as route evidence for that fixture.

The actual leaderboard row is `benchmark_lgssm_exact_oracle_m3_T50`:

- `D=3`;
- `T=50`;
- five parameters;
- dataset seed `81100`;
- theta `[0.72, 0.55, 0.35, 0.35, 0.45]`;
- exact total Kalman log likelihood `-136.0759748579247`;
- exact per-time average log likelihood `-2.721519497158494`.

Therefore Contract E cannot be used as same-target leaderboard value or score
evidence. Using it as leaderboard score evidence would be wrong.

## Phase 4 Executed Evidence

Same-target LGSSM value-only runner:

- path: `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`;
- imports `_lgssm_dataset` and `_lgssm_benchmark_model`;
- does not import `benchmark_two_lane_highdim_leaderboard.py`, which hides CUDA
  on import;
- emits total and per-time average log likelihood;
- emits `score_status =
  blocked_score_same_target_total_derivative_not_implemented`.

LGSSM `N=10000` artifact:

- path:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.json`;
- status: `executed_value_only_score_blocked`;
- average log likelihood mean: `-2.719201477051`;
- MCSE: `0.0001186681274`;
- exact average: `-2.721519497158`;
- relative error: `0.0852%`;
- adjacent-rung rule versus `N=1000`: passed;
- MCSE decreased versus `N=1000`.

Fixed spatial SIR `N=10000` artifact:

- path:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json`;
- status: value-only;
- mean log likelihood: `-902.830151367187`;
- MCSE: `0.208222111736`;
- adjacent-rung rule versus `N=1000`: passed;
- MCSE decreased versus `N=1000`;
- score remains blocked.

## Local Checks

- `python -m py_compile docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`: passed.
- `python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q`: `6 passed`.
- JSON content assertions for same-target LGSSM and fixed SIR `N=10000`
  artifacts: passed.
- `git diff --check`: passed.

## Claims Allowed After Phase 4

- Same-target LGSSM LEDH value-only row passed at `N=10000`.
- Fixed spatial SIR LEDH value-only row passed at `N=10000`.
- Both rows are score-blocked.
- Runtime ranking against frozen non-LEDH rows remains forbidden.

## Claims Forbidden After Phase 4

- Do not claim any LEDH leaderboard score is working.
- Do not merge Contract E score evidence as the `m3_T50` leaderboard score.
- Do not claim HMC readiness.
- Do not claim exact nonlinear likelihood correctness for fixed SIR.
- Do not claim Zhao-Cui TT/SIRT source-faithfulness.

## Verdict Request

Findings first. End with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
