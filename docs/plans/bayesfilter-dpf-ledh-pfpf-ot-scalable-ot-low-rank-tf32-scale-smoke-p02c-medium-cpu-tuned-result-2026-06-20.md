# LR-TF32-2C Result: Tuned Medium CPU No-Dense Validation

Date: 2026-06-20
Owner: peer agent

## Status

`PASSED_TUNED_MEDIUM_CPU_NO_DENSE`

## Result

The renewed medium CPU no-dense gate passed with the tuned setting:

- `rank=64`
- `assignment_epsilon=0.015625`
- `B=2`, `D=8`, `dtype=float32`
- `N=4096` and `N=8192`

## Diagnostic Summary

| Diagnostic | N=4096 | N=8192 | Threshold | Role |
| --- | ---: | ---: | ---: | --- |
| dense transport materialized | `False` | `False` | forbidden | hard veto |
| weighted mean absolute error | `3.1322240829467773e-04` | `3.1253695487976074e-04` | `2.5e-02` | hard veto |
| weighted second-moment absolute error | `6.98426365852356e-02` | `6.98208212852478e-02` | `7.5e-02` | hard veto |
| max factor marginal residual | `9.051291272044182e-07` | `4.5191700337454677e-07` | `5.0e-03` | hard veto |
| max induced row residual | `3.7071704864501953e-03` | `3.702104091644287e-03` | `5.0e-03` | hard veto |
| max induced column residual | `3.115415573120117e-03` | `3.1040310859680176e-03` | `5.0e-03` | hard veto |
| output log-weight normalization residual | `0.0` | `0.0` | `1.0e-06` | hard veto |

## Artifacts

- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.log`

## Handoff

P03 trusted GPU scale may be entered with the tuned setting if trusted GPU
execution is still approved and available.  GPU runtime/memory/TF32 metadata
remain explanatory only.

## Non-Claims

No speedup, ranking, GPU feasibility beyond this CPU result, TF32 help,
posterior correctness, HMC readiness, public/default readiness, dense
equivalence, or production claim is made.
