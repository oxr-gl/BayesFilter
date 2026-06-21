# P05 Dense Breakpoint Context Subplan

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Phase Objective

Run a small-`N` dense/non-streaming context diagnostic only to document the
dense route's different storage surface and small-`N` timing context. This
phase is not a promotion criterion for the streaming default and cannot by
itself prove a dense large-`N` breakpoint.

## Entry Conditions Inherited From Previous Phase

- P03 and P04 recorded streaming reach and same-route runtime evidence, or
  documented a blocker that still permits small-`N` context.
- Dense comparison remains explicitly contextual.

## Required Artifacts

- P05 JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-gpu-2026-06-21.json`
- P05 Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-gpu-2026-06-21.md`
- P05 child artifact directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-gpu-children-2026-06-21/`
- P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-result-2026-06-21.md`

## Required Checks, Tests, And Reviews

- Run a bounded small-`N` dense context diagnostic if feasible:
  - particle count `512`;
  - time steps `40`;
  - state dimension `10`;
  - observation dimension `10`;
  - dense route via the older LGSSM scale harness;
  - streaming route via the current streaming LGSSM harness;
  - GPU selected by P02.
- Record that the dense harness reports `transport_plan_mode` and timing/device
  metadata, but does not emit streaming-style explicit
  `dense_transport_matrix_materialized` or full-storage flags.
- Record that dense uses a different storage surface and is not a large-`N`
  comparator or a dense-storage proof beyond the harness route description.
- If dense context is skipped, write a result explaining that P03/P04 already
  answer the primary question and dense context would not change promotion.
- Claude review is required only if P05 result is used in P06 interpretation
  beyond context.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What small-`N` context documents the dense route's different storage surface without using dense as a large-`N` promotion comparator? |
| Baseline/comparator | Dense/non-streaming small-`N` context versus current streaming route. |
| Primary criterion | Context artifact records dense route status, its limited artifact surface, and explicitly labels it non-promotional. |
| Veto diagnostics | Dense result interpreted as large-`N` ranking, dense artifact treated as explicit storage proof beyond its fields, missing contextual label, or failure to preserve artifact paths. |
| Explanatory diagnostics | Dense runtime, memory metadata, and any dense failure at small `N`. |
| Not concluded | No dense large-`N` limit unless tested, no streaming superiority ranking, no posterior correctness. |
| Artifact | P05 JSON/Markdown and P05 result. |

## Forbidden Claims Or Actions

- Do not run large dense jobs that risk OOM just to demonstrate dense failure.
- Do not treat dense small-`N` timing or artifact fields as a large-`N` speed
  ranking or explicit dense-storage proof beyond the harness route description.
- Do not let P05 override P03/P04 hard-gate interpretation.

## Exact Next-Phase Handoff Conditions

Advance to P06 if:

- P05 result exists as either an executed context diagnostic or a justified
  skip record;
- P05 result states that dense context is not a streaming-default promotion
  criterion.

## Stop Conditions

- Dense context would require unsafe large-memory execution.
- The only possible interpretation would overclaim beyond the evidence.

## End-Of-Phase Actions

1. Run required context checks or write a justified skip.
2. Write the P05 result/close record.
3. Draft or refresh the P06 subplan.
4. Review the P06 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
