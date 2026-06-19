# Wave 4 Launch Review Packet

Date: 2026-06-20
Reviewer: Claude Opus max effort, read-only
Supervisor/executor: Codex in the current conversation

## Scope For Review

Review the Wave 4 launch design by path and summary.  Do not edit files, run
commands, launch agents, or authorize boundary crossings.

Primary paths:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p00-launch-review-subplan-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-subplan-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p02-current-positive-feature-validation-subplan-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p03-final-merge-subplan-2026-06-20.md`
- `docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py`
- `tests/test_wave4_positive_feature_validation.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-visible-gated-execution-runbook-2026-06-20.md`

## Compact Evidence Contract

Wave 4 is a replicated downstream resampling hard screen.  It compares
post-transport uniform estimates against exact weighted input estimates for the
same fixture.  Naive uniform-no-transport estimates, runtime, and per-seed
differences are explanatory only.

The current agent owns only the positive-feature lane.  The peer agent owns the
low-rank lane.  The peer handoff is the first post-launch phase so the peer can
start independently while the current lane runs.  Final merge is blocked until
both lane close records and JSON artifacts exist.

## Hard Boundaries

- Exactly two active algorithm agents: current agent and peer agent.
- Communication through Markdown/JSON artifacts under `docs/plans` and
  `docs/benchmarks`.
- No ranking without a predeclared paired uncertainty analysis verified in the
  final merge.
- No speedup, production/default, public API, HMC, posterior correctness, dense
  equivalence, broad scalable-OT selection, or scientific superiority claim.
- Claude is read-only reviewer only.

## Requested Review Questions

1. Does the plan avoid the earlier dependency-style parallelism mistake by
   keeping the two algorithm lanes independent?
2. Are the baseline/comparator, primary hard screen, explanatory diagnostics,
   nonclaims, and stop conditions correctly separated?
3. Does the final merge correctly block until peer low-rank lane artifacts
   exist?
4. Are any proxy metrics or descriptive summaries accidentally promoted into
   ranking/default evidence?
5. Are there any material artifact coverage or boundary-safety gaps?

End with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.
