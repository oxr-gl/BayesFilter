# Low-Rank TF32 Scale Smoke Diagnostics

- Status: `PASS`
- Phase: `LR-TF32-3`
- Mode: `gpu-scale`
- Algorithm: `P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `2` | explanatory |
| num_executed_rows | `2` | explanatory |
| num_hard_vetoes | `0` | hard veto |
| num_viable_rows | `2` | explanatory |
| max_factor_marginal_residual | `8.195638656616211e-08` | hard veto |
| max_induced_row_residual | `0.0037178397178649902` | hard veto |
| max_induced_column_residual | `0.003116786479949951` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_weighted_mean_abs_error | `0.0003426671028137207` | hard veto |
| max_weighted_second_moment_abs_error | `0.06983824074268341` | hard veto |
| max_tiny_materialized_apply_parity | `None` | hard veto |
| max_wall_time_seconds_explanatory | `3.7617463720962405` | explanatory |
| total_wall_time_seconds_explanatory | `7.4331724820658565` | explanatory |
| max_memory_maxrss_kb_explanatory | `1931264` | explanatory |

## Rows

| N | Rank | Epsilon | Status | Hard vetoes | Factor residual | Row residual | Column residual | Mean error | Second error | Dense materialized |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 50000 | `64` | `0.015625` | `PASS` | `[]` | `7.430207915604115e-08` | `0.0037151575088500977` | `0.0031145811080932617` | `0.000326499342918396` | `0.0698322206735611` | `False` |
| 100000 | `64` | `0.015625` | `PASS` | `[]` | `8.195638656616211e-08` | `0.0037178397178649902` | `0.003116786479949951` | `0.0003426671028137207` | `0.06983824074268341` | `False` |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Command: `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode gpu-scale --phase-id LR-TF32-3 --phase-result-path docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-result-2026-06-20.md --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --particle-counts 50000 100000 --conditional-100k --batch-size 2 --state-dim 8 --rank 64 --assignment-epsilon 0.015625 --dtype float32 --fixture-id bounded_smooth_v1 --tf32-mode enabled --trust-context trusted_gpu_escalated --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-gpu-scale-tuned-2026-06-20.md`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- TF32 requested: `enabled`
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
