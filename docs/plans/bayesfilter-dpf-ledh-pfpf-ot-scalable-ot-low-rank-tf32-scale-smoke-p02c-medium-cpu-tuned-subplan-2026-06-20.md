# LR-TF32-2C Subplan: Tuned Medium CPU No-Dense Validation

Date: 2026-06-20
Owner: peer agent

## Status

`COMPLETED_TUNED_MEDIUM_CPU_NO_DENSE`

## Amendment Note

This subplan records the user-approved amendment path after the initial P02
untuned screen was reclassified as a planning/usage error.  The P02B result
provided the operational handoff into this tuned medium validation.  This file
is refreshed during closeout to make the phase contract explicit for audit and
future reruns; it does not add evidence beyond the P02C result artifact.

## Phase Objective

Validate the focused-tuning selected low-rank solver-route setting on the
medium CPU-hidden no-dense screen at `N=4096` and `N=8192` before entering
trusted GPU scale.

## Entry Conditions Inherited From Previous Phase

- P00 governance and P01 small invariant gates passed.
- Initial P02 untuned moment failure is amended as
  `WRONG_PLANNING_AND_USAGE_ERROR_MISSING_TUNING_PHASE`.
- P02A coarse tuning ran without dense scale materialization and showed that
  smaller `assignment_epsilon` improved weighted second-moment preservation.
- P02B focused tuning found a viable no-dense row with `rank=64` and
  `assignment_epsilon=0.015625`.
- Runtime and memory remain explanatory only.

## Required Artifacts

- Tuned medium CPU JSON/Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.json`
  and `.md`
- Tuned medium CPU log:
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.log`
- P02C result/close record:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-result-2026-06-20.md`

## Required Checks, Tests, And Reviews

- CPU-hidden tuned medium command with `timeout`.
- JSON parse and embedded-manifest checks.
- Confirm no dense scale matrix materialization.
- Confirm finite/sign-valid factors and transported particles.
- Confirm output log weights are normalized.
- Confirm residual and weighted-moment thresholds pass for both medium rows.
- Forbidden-claim/boundary scan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the selected tuned no-dense low-rank solver-route setting pass the frozen medium CPU screen at both medium particle counts? |
| Baseline/comparator | Exact weighted input moments are the downstream reference; naive uniform no-transport remains explanatory only. |
| Tuned setting | `rank=64`, `assignment_epsilon=0.015625`, `N in {4096,8192}`, `B=2`, `D=8`, `dtype=float32`, CPU hidden, fixture `bounded_smooth_v1`. |
| Promotion criterion | Both rows have empty hard vetoes: no dense scale materialization, finite/sign-valid factors, residuals below thresholds, output log weights normalized, weighted mean error `<=2.5e-2`, and weighted second-moment error `<=7.5e-2`. |
| Veto diagnostics | Timeout, invalid JSON, missing manifest, dense scale materialization, nonfinite/invalid factors or particles, residual/moment threshold failure, unsupported claim, or boundary edit. |
| Explanatory diagnostics | Runtime, memory, projection iterations, factor minima, and candidate-vs-naive deltas. |
| Not concluded | No speedup, ranking, 50k/100k feasibility, GPU feasibility, TF32 help, posterior correctness, HMC readiness, public/default readiness, dense equivalence, or production claim. |

## Forbidden Claims And Actions

- Do not infer speedup from tuned medium runtime.
- Do not compare against or read positive-feature lane intermediates as
  evidence.
- Do not run trusted GPU scale from this phase unless P02C passes.
- Do not change thresholds after seeing results.
- Do not edit positive-feature, public/default/API, shared schema, or
  coordinator files.

## Exact Next-Phase Handoff Conditions

Advance to LR-TF32-3 only if both tuned medium rows pass with empty hard vetoes
and the artifact set includes JSON, Markdown, log, and P02C result records.
The handoff setting is `rank=64`, `assignment_epsilon=0.015625`.

## Stop Conditions

Stop with `LOW_RANK_TUNED_MEDIUM_CPU_FAILED` if either medium row fails a hard
veto.  Stop with `LOW_RANK_TUNED_MEDIUM_CPU_BLOCKED` if validation requires a
shared-contract, package/network, public/default/API, positive-feature, or GPU
boundary crossing.
