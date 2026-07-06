# P02 CPU Tuning Grid And Focused Repair Loop Subplan

Status: `READY_AFTER_P01`

## Phase Objective

Run an actual filter-loop CPU tuning grid so that low-rank route parameters are
validated in the integration context before medium or GPU scale execution.
Every viable active row must prove that low-rank resampling executed inside the
filter loop.

## Entry Conditions Inherited From Previous Phase

P01 must have passed small CPU harness checks.  The harness is the only
implementation surface for this phase.  The component-lane tuned setting is a
seed, not a promotion result.

Inherited P01 evidence:

- P01 JSON status: `PASS`.
- Low-rank route invocation count: `2`.
- Active resampling mask count: `2`.
- Transport matrix shapes: `[[2, 0, 0], [2, 0, 0]]`.
- No P01 hard vetoes.

## Required Artifacts

- Tuning JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.json`
- Tuning Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p02-tuning-result-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p02-tuning-cpu.log`

## Required Checks, Tests, And Reviews

- CPU-hidden tuning command with `--mode tuning-cpu`.
- Initial tuning grid:
  `particle_counts=[512]`, `batch_size=1`, `time_steps=2`, `state_dim=6`,
  `obs_dim=4`, `tuning_ranks=[16, 32, 64, 128]`,
  `tuning_assignment_epsilons=[0.0625, 0.03125, 0.015625]`.
- JSON artifact inspection for viable rows, hard vetoes, selected setting, and
  non-claim list.
- Focused repair/tuning rerun if the first grid has no viable row and no
  harness-validity veto fires.
- At most two focused tuning reruns after the initial grid.  Each rerun must
  record its grid before execution and may not widen fixed diagnostic thresholds.
- Artifact inspection that viable active rows include
  `low_rank_resampling_invocations > 0` and
  `low_rank_resampling_invocations == active_resampling_mask_count`.
- Read-only Claude review for material tuning-result interpretation or repair.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which low-rank configuration remains viable under actual filter-loop diagnostics at CPU tuning scale? |
| Baseline/comparator | Tuning grid over rank and assignment epsilon, seeded by but not validated by prior component-lane setting. |
| Primary pass criterion | At least one active row proves low-rank route execution and passes finite, factor, induced residual, log-weight, no-dense, and output sanity hard checks under the master fixed-threshold table. |
| Veto diagnostics | No viable row after the initial grid plus at most two focused reruns; missing/zero low-rank invocation evidence for active rows; invocation count mismatch; nonfinite output; invalid factor; dense materialization in scale mode; missing artifact; harness validity failure. |
| Explanatory diagnostics | Runtime, memory, ESS, moment deltas, rank, assignment epsilon, projection iterations, TF32 metadata if present. |
| Not concluded | No speedup, ranking, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |
| Artifact | P02 JSON/Markdown/result/log and selected setting for P03/P04. |

## Forbidden Claims And Actions

- Do not select by observed runtime as a promotion criterion.
- Do not rank viable settings statistically.
- Do not continue to medium/GPU scale if all tuning rows fail after the bounded
  initial grid plus at most two focused reruns.
- Do not change shared contracts to make tuning pass.
- Do not widen the master fixed diagnostic thresholds after seeing tuning
  results.

## Exact Next-Phase Handoff Conditions

P03 may start only if P02 records a selected tuned setting with explicit
`rank`, `assignment_epsilon`, hard-veto-free tuning row, and route-execution
evidence showing low-rank invocation count equal to active mask count.
Runtime/memory remain explanatory only.

## Stop Conditions

- `LOW_RANK_FILTER_INTEGRATION_SCALE_FAILED_TUNING_OR_VALIDITY`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`
- Review nonconvergence after five rounds for the same material blocker.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P02 result/close record.
3. Draft or refresh P03 subplan with the selected setting.
4. Review P03 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
