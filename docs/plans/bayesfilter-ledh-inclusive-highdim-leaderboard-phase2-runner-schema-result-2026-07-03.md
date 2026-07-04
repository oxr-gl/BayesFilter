# Phase 2 Result: Runner And Artifact Schema

Date: 2026-07-03

Status: `PASSED_PHASE2_SCHEMA_BOUNDARY`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | A separate LEDH-inclusive highdim leaderboard dry-run runner is implemented and emits all requested rows without executing LEDH values or scores. |
| Primary criterion | Passed locally: dry-run JSON/MD exists, has seven row summaries and 28 row cells, and preserves frozen-vs-fresh provenance. |
| Veto diagnostics | Passed locally: no baseline overwrite; no GPU/CPU runtime claim; no runtime cross-ranking; no LEDH score admission; parameterized SIR remains scoped; every non-executed LEDH row/score arm has an explicit reason. |
| Main uncertainty | Phase 3 still must prove real GPU/XLA execution and tiny LGSSM value/score behavior before any LEDH execution evidence is admitted. |
| Next justified action | Run Phase 3 trusted GPU/XLA/tiny value-score gates for the explicitly enumerated arms. |
| Not concluded | No LEDH value correctness, score correctness, runtime superiority, HMC readiness, posterior correctness, or scientific superiority. |

## Artifacts

- Runner:
  `docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py`
- Tests:
  `tests/test_two_lane_highdim_ledh_leaderboard.py`
- Dry-run JSON:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-dry-run-2026-07-03.json`
- Dry-run Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-dry-run-2026-07-03.md`

## What The Runner Does

The runner:

- copies non-LEDH rows from the frozen July 3 baseline with provenance labels;
- adds one `ledh_pfpf_ot` row per requested highdim row from the Phase 1 ledger;
- emits all requested rows and all four comparison algorithms;
- records `runtime_cross_ranking_allowed=false`;
- records LEDH value status and score status separately;
- keeps all LEDH score arms blocked;
- keeps actual SV, KSC SV, predator-prey, and generalized SV blocked until a
  reviewed same-target adapter exists;
- keeps parameterized SIR scoped and not a full observed-data filtering row.

## Checks Run

- `python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py tests/test_two_lane_highdim_ledh_leaderboard.py`: passed.
- `python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q`: passed, `5 passed`.
- Dry-run artifact generation: passed.
- Dry-run JSON content check:
  - `benchmark=bayesfilter_two_lane_highdim_ledh_inclusive_leaderboard_dry_run`;
  - `runtime_cross_ranking_allowed=false`;
  - seven row summaries;
  - 28 row cells;
  - exactly one LEDH row per requested row;
  - every LEDH row has reason, score status reason, and `runtime_rankable=false`.
- `git diff --check` on runner, tests, and dry-run artifacts: passed.

## Phase 3 Handoff

Phase 3 may begin only after Claude review agrees or fixable issues are patched.

Phase 3 must not broaden execution scope. Initial executable arms remain:

- `benchmark_lgssm_exact_oracle_m3_T50:ledh_value_dry_run_or_tiny_value_gate_only`;
- `zhao_cui_spatial_sir_austria_j9_T20:fixed_spatial_sir_value_arm_only`.

All LEDH score arms remain blocked except the LGSSM score gate, which may be
tested against Kalman or trusted same-target finite difference. Passing the
LGSSM score gate does not admit nonlinear LEDH scores.

Phase 3 must use trusted/escalated execution for:

- `nvidia-smi`;
- TensorFlow GPU device probe;
- any TensorFlow GPU/XLA LEDH command.

## Claude Review

Claude read-only review initially hung on a broad prompt. A smaller closure
review returned `VERDICT: AGREE`.

Review conclusion:

- Phase 2 is closed as a schema/admission boundary.
- No LEDH value or score execution is claimed.
- Runtime ranking remains blocked.
- Phase 3 may proceed only for trusted tiny gates: LGSSM value/score and fixed
  SIR value.
