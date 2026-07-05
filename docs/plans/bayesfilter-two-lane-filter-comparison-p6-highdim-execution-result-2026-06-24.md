# Phase Result: Two-Lane Comparison P6 High-Dimensional Execution

metadata_date: 2026-06-24
plan_reference: `docs/plans/bayesfilter-two-lane-filter-comparison-p6-highdim-execution-subplan-2026-06-24.md`
master_program: `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
status: PASS_P6_HIGHDIM_REFERENCE_LEADERBOARD_REPAIRED_SGQF_ROWS_REEMITTED

## Phase Objective

Repair the high-dimensional / source-scope leaderboard so SGQF is executed where
existing reviewed code/test routes already support it, while preserving only true
same-target blocks.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for the current reviewed route set: SGQF is now executed on supported highdim rows and kept blocked only where a same-target or reviewed source-scope evaluator is genuinely missing |
| Primary criterion status | satisfied |
| Veto diagnostic status | no blanket SGQF block remains; actual transformed SV and KSC surrogate SV remain separated; CUT4 remains excluded |
| Main uncertainty | some rows still lack full three-way execution because Zhao-Cui or SGQF source-scope evaluators remain missing |
| Next justified action | refresh the final closeout packet to reflect the repaired highdim table |
| What is not concluded | no fully populated three-way highdim winner table and no production-GPU timing claim |

## What Was Repaired

The previous highdim packet incorrectly blanket-blocked SGQF. The repaired
harness now uses row-by-row SGQF support:
- source-scope LGSSM: direct affine SGQF value route executed
- predator-prey: direct SGQF adapter route executed
- actual transformed SV: remains blocked as not same-target under the current additive-state SGQF lane
- KSC surrogate T1000: remains blocked because current SGQF KSC admission is tiny-fixture only, not a reviewed source-scope T1000 route
- spatial SIR: remains blocked because no reviewed SGQF source-scope SIR route is wired
- generalized SV source row: remains blocked because no reviewed SGQF source-scope evaluator is wired

## Emitted Artifact

- JSON: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.json`
- Markdown: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.md`
- Harness: `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

## Audit Of Result Just Produced

P6 now matches the actual codebase support landscape much better:
- SGQF is no longer falsely blocked on every highdim row,
- only real route gaps remain blocked,
- and the packet remains explicit about where execution is value-only versus value+score.

## Verification

```bash
python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.md
python -m compileall -q docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p47_predator_prey_filtering.py -k fixed_sgqf_vs_ukf_same_target_value_row
```

Observed:
- highdim harness re-emitted successfully
- compileall passed
- focused SGQF predator-prey check passed
