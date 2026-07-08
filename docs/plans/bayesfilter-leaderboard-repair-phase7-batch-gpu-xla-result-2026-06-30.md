# Phase 7 result: batched CPU/GPU/XLA status integration

Date: 2026-06-30

Status: `PASSED_WITH_STATUS_FIELDS_AND_SIDECAR_ISOLATION`

## Phase Objective

Add batched evaluator status and trusted CPU/GPU/XLA timing/status fields to
the high-dimensional leaderboard without allowing timing to override value or
score correctness gates.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Which current leaderboard cells have reviewed batched and GPU/XLA evidence, and which cells remain blocked/not-applicable because the value/score row is not admitted? |
| Baseline/comparator | Correctness-passing value/score rows from Phases 1-6 plus scoped P91 local complete-data sidecar evidence. |
| Primary criterion | Met. Every row has `phase7_batch_gpu_xla_status`; blocked or value-only rows are marked `not_applicable_until_value_score_row_exists`; P91 timing is structurally isolated under `p91_scoped_evidence.phase7_sidecar_performance`. |
| Veto diagnostics | Not fired. No new GPU claim was generated in Phase 7; no blocked main row was ranked by timing; P91 local complete-data timings were not promoted to the full SIR observed-data/filtering row. |
| Explanatory diagnostics | Reused P91 sidecar first-call and steady-call CPU/GPU/XLA timings from trusted prior P91 manifests. Existing P8D source runtimes remain explanatory only. |
| Not concluded | No universal GPU superiority; no HMC convergence; no production deployment claim beyond reported gates; no full SIR observed-data/filtering readiness from P91 sidecar timing. |
| Artifact | Regenerated JSON/Markdown leaderboard, Phase 7 tests, and this result note. |

## Actions Taken

- Added `phase7_batch_gpu_xla_status` to every main leaderboard row.
- Marked non-`executed_value_score` rows as not timing-rankable:
  `not_applicable_until_value_score_row_exists`.
- Marked admitted value/score rows as not ranked by Phase 7 timing unless a
  row-specific reviewed batched/GPU/XLA manifest exists.
- Added structurally isolated P91 local complete-data timing under:
  `p91_scoped_evidence.phase7_sidecar_performance`.
- Regenerated the high-dimensional leaderboard JSON and Markdown artifacts.

## Reused Trusted Evidence

No new GPU benchmark was run in Phase 7. The only GPU/XLA timing values carried
forward are scoped P91 local complete-data sidecar values from reviewed prior
artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json`

The P91 sidecar reports:

| Target | Status | Looped steady s | Batched steady s | Batched per-item steady s |
| --- | --- | ---: | ---: | ---: |
| CPU | `PASS_P91_PHASE6_CPU_BENCHMARK` | 0.0034192421939224006 | 0.003697521169669926 | 0.0009243802924174815 |
| GPU/XLA | `PASS_P91_PHASE6_GPU_XLA_BENCHMARK` | 0.0009009486064314842 | 0.0017791393911466002 | 0.00044478484778665006 |

These timings are not full observed-data/filtering SIR timings and are not part
of main leaderboard sorting, ranking, or admission.

## Artifacts

- Code:
  `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- Tests:
  `tests/test_two_lane_highdim_leaderboard_phase7.py`
- Regenerated leaderboard:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  and
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- Subplan:
  `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`
- Refreshed next subplan:
  `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`

## Local Checks

CPU-only TensorFlow checks intentionally used `CUDA_VISIBLE_DEVICES=-1` before
framework import. The CPU-only regeneration emitted CUDA factory/cuInit warning
noise; per repo policy this is not evidence of a broken GPU stack.

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase7.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase7.py -q`: passed, 4 tests, 2 warnings, 380.15 seconds.
- `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase7.py docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`: passed.
- Regenerated JSON assertion for `phase7_batch_gpu_xla_status` and P91 sidecar isolation: passed.

A parallel JSON assertion was accidentally launched before regeneration
completed and read the previous artifact, producing `KeyError:
'phase7_batch_gpu_xla_status_policy'`. The assertion was rerun after
regeneration and passed; the earlier failure is a stale-read race, not a final
artifact failure.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 8 after Claude result review | Passed: every row has Phase 7 batch/GPU/XLA status; blocked rows are not rankable; P91 timing is sidecar-isolated | No veto fired | Main row-specific batched/GPU/XLA benchmarks remain future work for admitted rows | Final regeneration, release/reset note, full focused test set, and final Claude review | No production GPU timing packet; no universal GPU advantage; no full SIR observed-data/filtering timing from P91 |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Working tree dirty; generated artifact from current workspace state. |
| Commands | Listed in Local Checks. |
| Environment | `tf-gpu` Python environment; CPU-only checks hid GPU with `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | Phase 7 generated no new GPU run; reused trusted P91 GPU/XLA evidence only as sidecar. |
| Data version | Existing P8D numeric artifact and P91 manifests listed above. |
| Random seeds | N/A for Phase 7 schema/status integration. |
| Wall time | Focused pytest: 380.15 seconds; regeneration completed successfully. |
| Output artifacts | Listed in Artifacts. |
| Plan file | `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md`. |
| Result file | `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-result-2026-06-30.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: the Phase 7 status fields could be mistaken
for a completed performance benchmark if a downstream consumer ignores
`timing_rank_status` and the P91 sidecar namespace.

Mitigation: tests require blocked/value-only rows to be
`not_rankable_correctness_gate_open`, admitted rows to be
`not_ranked_by_phase7_timing` without row-specific manifests, and P91 timing to
remain under `p91_scoped_evidence.phase7_sidecar_performance` with
`excluded_from_main_leaderboard_ranking = true`.

## Handoff To Phase 8

Phase 8 may start after Claude result review agrees. Phase 8 must preserve the
Phase 7 schema fields, nonclaims, P91 sidecar isolation, and final artifact
paths while running the final regeneration and closeout checks.
