# Phase Result: Two-Lane Comparison P5 Low-Dimensional Execution

metadata_date: 2026-06-24
plan_reference: `docs/plans/bayesfilter-two-lane-filter-comparison-p5-lowdim-execution-subplan-2026-06-24.md`
master_program: `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
status: PASS_P5_LOWDIM_REFERENCE_LEADERBOARD_EMITTED_WITH_EXPLICIT_SGQF_BOUNDARY

## Phase Objective

Execute the low-dimensional lane under the frozen protocol and emit the first
accuracy/time comparison packet.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | partially answered with durable executed outputs: a CPU-only lowdim reference leaderboard packet now exists, with explicit rankable rows and explicit SGQF blocked/status-only boundaries |
| Primary criterion status | satisfied for the implemented CPU-only reference packet |
| Veto diagnostic status | no actual-vs-surrogate SV mixing, no diagnostic-only row promoted to rankable, and no SGQF overclaim beyond the KSC tiny surrogate fixture |
| Main uncertainty | SGQF remains blocked on the frozen lowdim LGSSM rows and the current packet is CPU-only reference timing rather than a production-GPU timing conclusion |
| Next justified action | attempt high-dimensional execution only if a real executable highdim harness exists under the frozen contract |
| What is not concluded | no repo-wide winner, no production-GPU timing claim, no broad SGQF family admission |

## Executed Artifact

- JSON: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-24.json`
- Markdown: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-24.md`
- Harness: `docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py`

## What Was Executed

Rankable lowdim rows emitted with accuracy and timing fields:
- LGSSM dims 1-3 for Kalman / UKF / CUT4 / Zhao-Cui, with SGQF explicitly blocked
- KSC surrogate dims 1-3 for Kalman / UKF / CUT4 / SGQF / Zhao-Cui

Visible status-only rows emitted:
- dedicated SGQF-exact-eligible local Model C fixture for SGQF/UKF/CUT4 timing visibility
- P44 diagnostic-only rows remain visible and non-rankable

## Audit Of Result Just Produced

P5 passes the skeptical audit for a first durable reference packet because:
- rankable rows and status-only rows are separated,
- KSC surrogate stays separate from actual transformed SV,
- SGQF remains blocked where the current additive-state lane is not admitted,
- and the artifact states clearly that CPU-only reference timing is not a production-GPU conclusion.

## Next-Phase Review

P6 cannot proceed unchanged. The current high-dimensional lane still lacks a
reviewed executable harness that directly matches the frozen two-lane accuracy/time
contract across SGQF / UKF / Zhao-Cui rows with durable timing outputs.

## Verification Run

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py --requested-device cpu --repeats 1 --output docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-24.json --markdown-output docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-24.md
python -m compileall -q docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py tests/highdim
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py
```

Observed:
- lowdim harness emitted JSON + markdown successfully
- compileall passed
- focused pytest: `65 passed, 2 warnings`
