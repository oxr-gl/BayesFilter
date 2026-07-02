# Phase Result: Two-Lane Comparison P3 Artifact Schema And Emitter

metadata_date: 2026-06-24
plan_reference: `docs/plans/bayesfilter-two-lane-filter-comparison-p3-artifact-schema-and-emitter-subplan-2026-06-24.md`
master_program: `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
status: PASS_P3_TWO_LANE_ARTIFACT_SCHEMA_FROZEN

## Phase Objective

Freeze the output families and emitter contract for the two-lane leaderboard
program.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered: the required output families are now explicitly separated by lane and by metric family |
| Primary criterion status | satisfied |
| Veto diagnostic status | no merged overall leaderboard is allowed; blocker rows are required as a separate output family |
| Main uncertainty | the execution phases still need a concrete harness that can populate the frozen output families honestly |
| Next justified action | freeze the execution protocol in P4 |
| What is not concluded | no emitted leaderboard results yet |

## Frozen Output Families

Required final output families:
- low-dimensional accuracy table,
- low-dimensional timing table,
- high-dimensional accuracy table,
- high-dimensional timing table,
- blocker/status table,
- nonclaims section,
- optional Pareto/tradeoff summary only if justified later.

## Audit Of Result Just Produced

P3 passes the skeptical audit because it forbids a single merged leaderboard and
preserves separate blocker reporting, which is necessary for the current partial
same-target support landscape.

## Next-Phase Review

P4 required a small tightening during review: the execution protocol must make an
explicit first-pass environment choice rather than leaving CPU/GPU and warmup
policy implicit.

## Nonclaims

- No leaderboard artifact with populated accuracy/time rows exists yet.
