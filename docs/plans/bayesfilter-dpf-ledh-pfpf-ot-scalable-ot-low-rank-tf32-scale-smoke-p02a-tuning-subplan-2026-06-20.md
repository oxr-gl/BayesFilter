# LR-TF32-2A Subplan: Low-Rank Solver-Route Tuning CPU No-Dense

Date: 2026-06-20
Owner: peer agent

## Status

`READY_FOR_EXECUTION`

## Phase Objective

Repair the planning/usage error by tuning the implemented low-rank solver-route
before applying renewed medium or GPU acceptance gates.

## Entry Conditions Inherited From Previous Phase

- P00 governance and P01 small invariants passed.
- Prior P02 is amended to `WRONG_PLANNING_AND_USAGE_ERROR_MISSING_TUNING_PHASE`.
- The observed second-moment failure at `rank=64`, `assignment_epsilon=0.5` is
  a tuning signal only.

## Required Artifacts

- Tuning JSON/Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.json`
  and `.md`
- Tuning log:
  `docs/benchmarks/logs/low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.log`
- P02A result/close record.

## Required Checks, Tests, And Reviews

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py tests/test_low_rank_tf32_scale_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_tf32_scale_smoke.py`
- CPU-hidden tuning command with `timeout`.
- JSON parse and embedded-manifest checks.
- Confirm no dense scale matrix materialization.
- Forbidden-claim/boundary scan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a bounded tuning grid find a no-dense low-rank solver-route setting that preserves weighted moments under the frozen fixture? |
| Baseline/comparator | Exact weighted input moments are the downstream reference; naive uniform no-transport remains explanatory only. |
| Tuning grid | `N=4096`, `B=2`, `D=8`, `dtype=float32`, ranks `{64,128,256,512}`, assignment epsilons `{0.5,0.25,0.125,0.0625}`, `max_projection_iterations=240`. |
| Promotion criterion | At least one grid row has empty hard vetoes: finite/sign-valid factors, residuals below thresholds, output log weights normalized, weighted mean error `<=2.5e-2`, weighted second-moment error `<=7.5e-2`, and no dense scale materialization. |
| Veto diagnostics | Invalid JSON, missing manifest, dense scale materialization, nonfinite/invalid factors or particles, residual/moment threshold failure for every row, timeout, unsupported claim, or boundary edit. |
| Explanatory diagnostics | Runtime, memory, projection iterations, factor minima, candidate-vs-naive deltas, and relative order among viable rows. |
| Not concluded | No speedup, ranking, 50k/100k feasibility, GPU feasibility, TF32 help, posterior correctness, HMC readiness, public/default readiness, or dense equivalence. |

## Forbidden Claims And Actions

- Do not infer speedup from tuning runtime.
- Do not rank viable settings by descriptive runtime alone.
- Do not run trusted GPU scale from this phase.
- Do not change thresholds after seeing results.
- Do not edit positive-feature, public/default/API, shared schema, or
  coordinator files.

## Exact Next-Phase Handoff Conditions

If at least one tuned setting passes, refresh the medium validation subplan and
run a renewed medium CPU no-dense gate at `N=4096,8192` using a representative
viable tuned setting.  If no tuned setting passes, write a tuning-failure
closeout and stop without GPU scale.

## Stop Conditions

Stop with `LOW_RANK_TUNING_NO_VIABLE_SETTING` if the bounded grid finds no
passing row.  Stop with `LOW_RANK_TUNING_BLOCKED` if tuning requires a
shared-contract, package/network, public/default/API, positive-feature, or GPU
boundary crossing.
