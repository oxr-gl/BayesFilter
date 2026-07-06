# Actual-SIR Low-Rank N512 Seed-Replication Review Ledger

Date: 2026-06-23

Status: `SUBPLAN_REVIEW_CONVERGED`

## Round 1

Reviewer: Claude Opus/max, read-only.

Scope:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-larger-particle-replication-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n512-seed-replication-subplan-2026-06-23.md`

Verdict: `VERDICT: REVISE`

Material finding:

- The subplan's formal stop-condition section was narrower than the evidence
  contract: stale row mismatch and timeout/incomplete-run blocker handling were
  declared elsewhere but were not explicit stop conditions.

Patch:

- Added stale row mismatch with requested seed batch, shape, candidate id,
  dtype, timing source, TF32 mode, or device policy as a stop condition.
- Added row timeout or incomplete aggregate run as a stop condition requiring a
  blocker/result with partial artifacts preserved.

Focused checks after patch:

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed`.
- Local stop-condition patch consistency check.
  - Result: pass, `n512-seed-subplan-stop-condition-patch-pass`.

## Round 2

Reviewer: Claude Opus/max, read-only focused review.

Scope:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n512-seed-replication-subplan-2026-06-23.md`

Verdict: `VERDICT: AGREE`

Reviewer summary:

- Prior issue fixed in the operative stop list.
- Artifact coverage, post-run aggregate verification, and nonclaim boundaries
  remain intact.
- Non-blocking wording nit: skeptical-audit stop-condition summary did not
  explicitly restate stale-row mismatch and timeout/incomplete-run blockers.

Follow-up patch:

- Updated the skeptical-audit stop-condition summary to include stale-row
  mismatch, row timeout, and incomplete aggregate-run blocker handling.

## Final Review State

The N512 seed-replication subplan is reviewed and ready for execution subject
to trusted GPU availability and the pre-run checks in the subplan.
