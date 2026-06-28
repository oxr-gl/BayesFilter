# Low-Rank TF32 Scale Smoke Diagnostics

- Status: `PASS`
- Phase: `LR-TF32-2C`
- Mode: `medium-cpu`
- Algorithm: `P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `2` | explanatory |
| num_executed_rows | `2` | explanatory |
| num_hard_vetoes | `0` | hard veto |
| num_viable_rows | `2` | explanatory |
| max_factor_marginal_residual | `9.051291272044182e-07` | hard veto |
| max_induced_row_residual | `0.0037071704864501953` | hard veto |
| max_induced_column_residual | `0.003115415573120117` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_weighted_mean_abs_error | `0.00031322240829467773` | hard veto |
| max_weighted_second_moment_abs_error | `0.0698426365852356` | hard veto |
| max_tiny_materialized_apply_parity | `None` | hard veto |
| max_wall_time_seconds_explanatory | `3.036758274072781` | explanatory |
| total_wall_time_seconds_explanatory | `4.78382641589269` | explanatory |
| max_memory_maxrss_kb_explanatory | `486788` | explanatory |

## Rows

| N | Rank | Epsilon | Status | Hard vetoes | Factor residual | Row residual | Column residual | Mean error | Second error | Dense materialized |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 4096 | `64` | `0.015625` | `PASS` | `[]` | `9.051291272044182e-07` | `0.0037071704864501953` | `0.003115415573120117` | `0.00031322240829467773` | `0.0698426365852356` | `False` |
| 8192 | `64` | `0.015625` | `PASS` | `[]` | `4.5191700337454677e-07` | `0.003702104091644287` | `0.0031040310859680176` | `0.00031253695487976074` | `0.0698208212852478` | `False` |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Command: `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode medium-cpu --phase-id LR-TF32-2C --phase-result-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-result-2026-06-20.md --particle-counts 4096 8192 --batch-size 2 --state-dim 8 --rank 64 --assignment-epsilon 0.015625 --dtype float32 --fixture-id bounded_smooth_v1 --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-tuned-2026-06-20.md`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
- TF32 requested: `default`
- TF32 execution recorded: `True`
- Fixture: `bounded_smooth_v1`

## Non-Claims

- low-rank TF32 scale-smoke diagnostic only
- no speedup claim
- no ranking claim
- no superiority claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default readiness claim
- no dense Sinkhorn equivalence claim
- no full low-rank Sinkhorn solver-fidelity claim
- no broad scalable-OT selection claim
- no TF32-help claim
