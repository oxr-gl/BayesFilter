# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `bayesfilter-ledh-leaderboard-score-repair-phase2-blocker-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.  Do not edit files, run commands, launch agents, or
change state.

## Objective

Review the Phase 2 retraction and refreshed Phase 3 manual-VJP subplan.

## Self-Contained Summary

Phase 2 added and then retracted:

- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_score.py`
- `tests/test_ledh_same_target_lgssm_score_runner.py`

The runner targets the full LGSSM leaderboard row:

- `benchmark_lgssm_exact_oracle_m3_T50`;
- `D=3,T=50`, dataset seed `81100`;
- theta `[0.72, 0.55, 0.35, 0.35, 0.45]`;
- exact Kalman score
  `[5.655446876369503, -3.83505645148858, 0.3023616684162056,
  -1.9171806685717399, 4.354265155260018]`.

The attempted runner used TensorFlow `GradientTape` for LEDH score
computation.  That route is invalid for this score-repair program.  LEDH score
repair must use manual VJP.  Contract E is not used.

Checks:

- `python -m py_compile ...`: passed before retraction.
- `pytest -q tests/test_ledh_same_target_lgssm_score_runner.py`: `5 passed`
  before retraction.
- eager CPU-hidden prefix diagnostic: finite `[2,5]` score, now classified as
  invalid LEDH score evidence because it used tape-gradient score computation.
- graph CPU-hidden prefix diagnostic: failed at `tape.gradient` inside
  `tf.function`.

Phase 2 result status is `RETRACTED_TAPE_SCORE_ROUTE_INVALID`.  No LEDH score
row is admitted.  The invalid runner and tests have been removed.

Phase 3 was refreshed from graph-safe tape repair to manual-VJP score repair.
It forbids `GradientTape` score computation and requires manual VJP versus
same-scalar finite differences before any trusted GPU/XLA score smoke.

## Exact Paths

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-subplan-2026-07-03.md`

## Review Questions

1. Is it scientifically correct to retract the tape-gradient runner as invalid
   for LEDH score repair?
2. Does the Phase 2 result avoid promoting CPU/eager/prefix evidence to
   leaderboard score evidence?
3. Does Phase 3 correctly require manual VJP before GPU/XLA runs?
4. Is there any material wrong-target, partial-derivative, or authority
   boundary issue?

## Required Output

Findings first, concise.  End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
