# P03 Medium CPU Filter-Scale Validation Subplan

Status: `READY_AFTER_P02`

## Phase Objective

Run the selected P02 low-rank setting through larger CPU-hidden filter-loop
rows before trusted GPU scale, verifying that the actual integration path still
passes hard diagnostics without dense transport materialization and with
low-rank route-execution evidence.

## Entry Conditions Inherited From Previous Phase

P02 must have selected a hard-veto-free tuned setting.  P03 inherits all
non-claims and forbidden edit boundaries.  CPU-only execution must hide GPU
devices before TensorFlow import.

Inherited P02 setting:

- `rank=16`
- `assignment_epsilon=0.015625`
- selected tuning row status: `PASS`
- selected low-rank invocation count: `2`
- selected active mask count: `2`

## Required Artifacts

- Medium CPU JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.json`
- Medium CPU Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p03-medium-cpu-result-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p03-medium-cpu.log`

## Required Checks, Tests, And Reviews

- CPU-hidden medium command with selected P02 setting.
- Required command setting: `--rank 16 --assignment-epsilon 0.015625`.
- JSON inspection for `PASS`, no hard vetoes, no dense materialization, and
  finite outputs.
- JSON inspection that active rows include `low_rank_resampling_invocations > 0`
  and invocation count equal to active mask count.
- Read-only Claude review for material result interpretation or boundary issues.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the selected tuned low-rank route remain viable in the actual filter loop at medium CPU scale? |
| Baseline/comparator | P02 selected setting and the same harness hard diagnostics at larger `N`. |
| Primary pass criterion | Required medium active rows prove low-rank route execution and pass hard finite/factor/log-weight/no-dense checks under the master fixed-threshold table. |
| Veto diagnostics | Crash/OOM, missing/zero low-rank invocation evidence, invocation count mismatch, nonfinite outputs, invalid factors, factor/induced residual above the master fixed thresholds, dense transport matrix materialized, missing artifact, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory, ESS, moment deltas, projection iterations, selected rank, selected assignment epsilon. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |
| Artifact | P03 JSON/Markdown/result/log. |

## Forbidden Claims And Actions

- Do not infer GPU scale viability from CPU success.
- Do not change tuning parameters without writing a repair record.
- Do not treat runtime or memory as promotion evidence beyond crash/OOM veto.

## Exact Next-Phase Handoff Conditions

P04 may start only if P03 reports `PASS`, no hard vetoes, active route-execution
evidence, and the P04 subplan has the exact selected tuning parameters and
trusted-GPU command.

## Stop Conditions

- `LOW_RANK_FILTER_INTEGRATION_SCALE_FAILED_TUNING_OR_VALIDITY`
- Harness output missing or invalid.
- Need for shared contract/default/public API change.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P03 result/close record.
3. Draft or refresh P04 subplan.
4. Review P04 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
