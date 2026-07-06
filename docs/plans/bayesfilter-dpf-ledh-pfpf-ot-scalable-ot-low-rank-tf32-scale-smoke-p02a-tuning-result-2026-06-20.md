# LR-TF32-2A Result: Coarse Low-Rank Solver-Route Tuning

Date: 2026-06-20
Owner: peer agent

## Status

`COMPLETED_NO_VIABLE_ROW_BUT_REPAIR_SIGNAL`

## Result

The coarse tuning grid ran cleanly with no dense scale matrix materialization
and no harness error.  It found no row below the weighted second-moment
threshold, but it showed a strong repair signal as `assignment_epsilon`
decreased.

Best coarse row by weighted second moment:

- `rank=64`, `assignment_epsilon=0.0625`
- weighted second-moment error: `1.1541613936424255e-01`
- threshold: `7.5e-02`

This justified the predeclared focused low-epsilon tuning phase.

## Artifacts

- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-tuning-cpu-2026-06-20.log`

## Non-Claims

No speedup, ranking, GPU feasibility, TF32 help, posterior correctness, HMC
readiness, public/default readiness, dense equivalence, or production claim is
made.
