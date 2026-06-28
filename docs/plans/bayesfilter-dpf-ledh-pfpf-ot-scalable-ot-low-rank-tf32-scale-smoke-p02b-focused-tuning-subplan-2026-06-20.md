# LR-TF32-2B Subplan: Focused Low-Epsilon Tuning CPU No-Dense

Date: 2026-06-20
Owner: peer agent

## Status

`READY_FOR_EXECUTION`

## Phase Objective

Follow up the coarse tuning result with a focused low-epsilon grid because the
coarse grid showed that reducing `assignment_epsilon` materially improved
weighted second-moment preservation while preserving no-dense/factor checks.

## Entry Conditions Inherited From Previous Phase

- P02A coarse tuning ran cleanly with no dense scale matrix materialization.
- No coarse grid row passed the weighted second-moment threshold.
- Best observed row was `rank=64`, `assignment_epsilon=0.0625`, weighted
  second-moment error approximately `1.154e-01`, still above `7.5e-02`.
- Runtime and memory remain explanatory only.

## Required Artifacts

- Focused tuning JSON/Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.json`
  and `.md`
- Focused tuning log:
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.log`
- P02B result/close record.

## Required Checks, Tests, And Reviews

- CPU-hidden focused tuning command with `timeout`.
- JSON parse and embedded-manifest checks.
- Confirm no dense scale matrix materialization.
- Forbidden-claim/boundary scan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does low-epsilon tuning find a no-dense low-rank setting that passes the weighted moment screen? |
| Baseline/comparator | Exact weighted input moments are the downstream reference; coarse P02A tuning result is context only. |
| Tuning grid | `N=4096`, `B=2`, `D=8`, `dtype=float32`, ranks `{64,128}`, assignment epsilons `{0.05,0.04,0.03125,0.025,0.02,0.015625,0.01}`, `max_projection_iterations=240`. |
| Promotion criterion | At least one row has empty hard vetoes: finite/sign-valid factors, residuals below thresholds, output log weights normalized, weighted mean error `<=2.5e-2`, weighted second-moment error `<=7.5e-2`, and no dense scale materialization. |
| Veto diagnostics | Invalid JSON, missing manifest, dense scale materialization, nonfinite/invalid factors or particles, residual/moment threshold failure for every row, timeout, unsupported claim, or boundary edit. |
| Explanatory diagnostics | Runtime, memory, projection iterations, factor minima, and relative order among viable rows. |
| Not concluded | No speedup, ranking, 50k/100k feasibility, GPU feasibility, TF32 help, posterior correctness, HMC readiness, public/default readiness, or dense equivalence. |

## Forbidden Claims And Actions

- Do not infer speedup from tuning runtime.
- Do not rank viable settings by descriptive runtime alone.
- Do not run trusted GPU scale from this phase.
- Do not change thresholds after seeing focused tuning results.
- Do not edit positive-feature, public/default/API, shared schema, or
  coordinator files.

## Exact Next-Phase Handoff Conditions

If at least one focused tuning row passes, run renewed medium CPU no-dense
validation at `N=4096,8192` using a representative viable setting.  If no row
passes, write a focused tuning failure result and stop without GPU scale.

## Stop Conditions

Stop with `LOW_RANK_FOCUSED_TUNING_NO_VIABLE_SETTING` if the focused grid finds
no passing row.  Stop with `LOW_RANK_FOCUSED_TUNING_BLOCKED` if the run
requires shared-contract, package/network, public/default/API,
positive-feature, or GPU boundary crossing.
