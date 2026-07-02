# Phase P5 Subplan: Low-Dimensional Execution

metadata_date: 2026-06-24
status: DRAFT_PENDING_P4_CLOSEOUT
master_program: docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md
phase: P5
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Execute the low-dimensional lane under the frozen protocol and produce the first
accuracy/time comparison tables for rows that are already declared same-target
and rankable.

## Entry Conditions Inherited From Previous Phase

- P4 result must freeze the execution protocol.
- P1 result must freeze low-dimensional rankability.

## Required Artifacts

- Phase P5 result:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p5-lowdim-execution-result-2026-06-24.md`
- Refreshed Phase P6 subplan:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p6-highdim-execution-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

- Run only the low-dimensional rankable lane.
- Keep `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3` diagnostic-only.
- Keep actual transformed SV out of low-dimensional rankable leaderboard tables.
- Record run manifests and timing manifests exactly.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On the frozen low-dimensional same-target rows, what are the accuracy and computation-time outcomes by algorithm? |
| Baseline/comparator | Frozen low-dimensional lane contract and execution protocol. |
| Primary pass criterion | Every executed low-dimensional rankable cell has explicit accuracy and time records, and every non-rankable cell remains labeled as diagnostic-only or blocked. |
| Veto diagnostics | Actual-vs-surrogate SV mix-up, diagnostic-only row promoted to rankable, missing timing manifest, or SGQF score claim exceeding admitted analytical scope. |
| Explanatory diagnostics | Warmup timing, repeat spread, uncertainty summaries if applicable. |
| Not concluded | No high-dimensional claim yet. |
| Artifact preserving result | P5 result and refreshed P6 subplan. |

## Stop Conditions

Stop with a blocked P5 result if any low-dimensional executed table violates the
P0/P1 contract or if timing data cannot be collected fairly.
