# Actual-SIR Low-Rank N1024 Seed-Replication Review Ledger

Date: 2026-06-23

Status: `SUBPLAN_REVIEW_CONVERGED`

## Round 1

Reviewer: Claude Opus/max, read-only.

Scope:

- Compact packet for
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-seed-replication-subplan-2026-06-23.md`
- Previous result summary from
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-paired-validation-result-2026-06-23.md`

Verdict: `VERDICT: REVISE`

Material findings:

- The phase close artifact contract needed to explicitly require the run
  manifest and the inference-status and decision tables.
- The warm-screen pass/fail boundary needed an exact source field and
  threshold because it is a promotion/veto boundary.

Patch:

- Added an explicit close-record requirement for a decision table,
  inference-status table, post-run red-team note, and run manifest with git
  commit, command, environment, GPU/CPU status, seeds, wall time, output
  artifact paths, plan path, and result path.
- Added the exact warm-screen condition:
  `paired_comparability.warm_median_streaming_over_low_rank >= paired_comparability.thresholds.warm_median_streaming_over_low_rank`,
  using the aggregate runner `_speed_screen_pass` condition and the harness
  default threshold `1.25`.

Focused checks after patch:

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed`.
- Local patch consistency check.
  - Result: pass, `n1024-seed-subplan-r1-patch-consistency-pass`.

## Round 2

Reviewer: Claude Opus/max, read-only focused review.

Scope:

- The two Round 1 blockers only.

Verdict: `VERDICT: AGREE`

Reviewer summary:

- The close-record artifact contract now explicitly requires the decision
  table, inference-status table, post-run red-team note, and run manifest with
  the specified fields.
- The warm-screen boundary now names the exact source condition and fields plus
  threshold.

## Final Review State

The N1024 seed-replication subplan is reviewed and ready for execution subject
to trusted GPU availability and the pre-run checks in the subplan.
