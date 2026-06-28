# LR-TF32-2 Result: Medium CPU No-Dense Smoke

Date: 2026-06-20
Owner: peer agent
Supervisor/executor: Codex

## Status

`AMENDED_INVALID_AS_ROUTE_REJECTION_PLANNING_USAGE_ERROR`

## Phase Objective

Run the fixed CPU-hidden medium particle-count smoke to catch accidental dense
materialization, shape/memory mistakes, and downstream moment-screen failures
before trusted GPU 50k/100k execution.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | The low-rank resampling harness ran one untuned fixed medium CPU configuration, `rank=64` and `assignment_epsilon=0.5`, at `N=4096` and `N=8192`. |
| Baseline/comparator | Exact weighted input moments were the downstream reference; naive uniform no-transport estimates were explanatory only. |
| Primary criterion | Invalid as a route-rejection gate because the plan omitted a required solver-route tuning phase before applying the downstream moment hard gate. |
| Veto diagnostics | The observed `N=4096` and `N=8192` weighted second-moment failures are tuning signals only, not evidence that the low-rank solver-route family fails. |
| Explanatory diagnostics | Runtime, memory, rank, projection iterations, factor minima, and candidate-vs-naive moment deltas are descriptive only. |
| Not concluded | No 50k/100k feasibility, GPU feasibility, TF32 help, speedup, ranking, readiness, or dense equivalence. |

## Commands Run

- `timeout 300 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode medium-cpu --particle-counts 4096 8192 --batch-size 2 --state-dim 8 --rank 64 --dtype float32 --fixture-id bounded_smooth_v1 --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.md > docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.log 2>&1`
- `python -m json.tool docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.json`
- Embedded manifest contract check over the medium JSON.
- Forbidden boundary/claim scans over the medium JSON, Markdown, and log.

## Diagnostic Summary

| Diagnostic | N=4096 | N=8192 | Role |
| --- | ---: | ---: | --- |
| row status | `FAIL` | `FAIL` | hard gate |
| dense transport materialized | `False` | `False` | hard veto |
| finite factors/particles | `True` | `True` | hard veto |
| nonnegative factors and positive g | `True` | `True` | hard veto |
| max factor marginal residual | `1.6763806343078613e-08` | `3.725290298461914e-08` | hard veto |
| max induced row residual | `3.5762786865234375e-07` | `4.172325134277344e-07` | hard veto |
| max induced column residual | `7.152557373046875e-07` | `7.152557373046875e-07` | hard veto |
| output log-weight normalization residual | `0.0` | `0.0` | hard veto |
| weighted mean absolute error | `1.1920928955078125e-07` | `1.341104507446289e-07` | hard veto |
| weighted second-moment absolute error | `2.9352012276649475e-01` | `2.935119569301605e-01` | hard veto |
| weighted second-moment threshold | `7.5e-02` | `7.5e-02` | hard veto |

## Interpretation

Amendment: this result is a planning and usage error as a route-rejection gate.
The solver route was not tuned before applying the downstream moment hard gate,
so the run answered only whether one arbitrary untuned configuration passed.
The factor route ran without dense `[B,N,N]` materialization and passed
finite/sign/residual/log-weight checks, but the second-moment failures must be
treated as tuning signals.

This result does not reject the low-rank solver-route family or the current
candidate after tuning.  It does not rank against any other lane and does not
make GPU/TF32, speedup, posterior, HMC, public API, production/default, or
dense equivalence claims.

## Next-Phase Handoff

A new tuning phase must run before any renewed medium acceptance gate or
trusted GPU scale gate.  LR-TF32-3 remains not entered.

## Stop Conditions

The old P02 route-rejection interpretation is stopped by
`WRONG_PLANNING_AND_USAGE_ERROR_MISSING_TUNING_PHASE`.  No shared-contract,
package, network, public/default/API, or positive-feature boundary issue is
active.
