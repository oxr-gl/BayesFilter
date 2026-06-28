# LR-TF32-2B Result: Focused Low-Epsilon Tuning

Date: 2026-06-20
Owner: peer agent

## Status

`PASSED_FOUND_VIABLE_TUNED_SETTING`

## Result

Focused low-epsilon tuning found two viable no-dense CPU rows at `N=4096`.
The viable rows were `rank=64`, `assignment_epsilon=0.015625` and `rank=128`,
`assignment_epsilon=0.015625`.  The representative tuned setting selected by
the predeclared rule is:

- `rank=64`
- `assignment_epsilon=0.015625`
- weighted second-moment error: `6.98426365852356e-02`
- weighted mean error: `3.1322240829467773e-04`
- max factor marginal residual: `9.051291272044182e-07`
- max induced row residual: `3.7071704864501953e-03`
- max induced column residual: `3.115415573120117e-03`

All hard checks passed for the selected row.  Runtime and memory remain
explanatory only.

## Artifacts

- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-focused-tuning-cpu-2026-06-20.log`

## Handoff

Use `rank=64`, `assignment_epsilon=0.015625` for renewed medium CPU no-dense
validation at `N=4096,8192`.

## Non-Claims

No speedup, ranking, GPU feasibility, TF32 help, posterior correctness, HMC
readiness, public/default readiness, dense equivalence, or production claim is
made.
