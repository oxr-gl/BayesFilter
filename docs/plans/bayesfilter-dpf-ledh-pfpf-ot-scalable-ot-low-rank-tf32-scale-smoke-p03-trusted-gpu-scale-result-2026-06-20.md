# LR-TF32-3 Result: Tuned Trusted GPU FP32/TF32 Scale Smoke

Date: 2026-06-20
Owner: peer agent

## Status

`PASSED_TUNED_GPU_SCALE_DIAGNOSTIC_ONLY`

## Result

Trusted GPU scale passed with the tuned setting:

- `rank=64`
- `assignment_epsilon=0.015625`
- `B=2`, `D=8`, `dtype=float32`
- `N=50000`, then conditional `N=100000`
- `CUDA_VISIBLE_DEVICES=1`, visible as `/GPU:0`
- `tf32-mode enabled`

## Diagnostic Summary

| Diagnostic | N=50000 | N=100000 | Threshold | Role |
| --- | ---: | ---: | ---: | --- |
| dense transport materialized | `False` | `False` | forbidden | hard veto |
| weighted mean absolute error | `3.26499342918396e-04` | `3.426671028137207e-04` | `2.5e-02` | hard veto |
| weighted second-moment absolute error | `6.98322206735611e-02` | `6.983824074268341e-02` | `7.5e-02` | hard veto |
| max factor marginal residual | `7.430207915604115e-08` | `8.195638656616211e-08` | `5.0e-03` | hard veto |
| max induced row residual | `3.7151575088500977e-03` | `3.7178397178649902e-03` | `5.0e-03` | hard veto |
| max induced column residual | `3.1145811080932617e-03` | `3.116786479949951e-03` | `5.0e-03` | hard veto |
| output log-weight normalization residual | `0.0` | `0.0` | `1.0e-06` | hard veto |

Runtime, memory, TF32 metadata, and row ordering are explanatory only.

## Artifacts

- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.json`
- `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.md`
- `docs/benchmarks/logs/low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.log`

## Interpretation

This component scale smoke shows that the tuned low-rank solver-route can run
at the requested particle counts under this deterministic fixture and hard
diagnostic contract without dense scale materialization.  It does not establish
speedup, ranking, posterior correctness, HMC readiness, public API readiness,
production/default readiness, dense Sinkhorn equivalence, full solver fidelity,
broad scalable-OT selection, or that TF32 helped.

## Non-Claims

No speedup, ranking, TF32-help, posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense equivalence, full solver
fidelity, broad scalable-OT selection, or production claim is made.
