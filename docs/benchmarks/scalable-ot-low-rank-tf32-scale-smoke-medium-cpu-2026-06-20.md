# Low-Rank TF32 Scale Smoke Diagnostics

- Status: `FAIL`
- Phase: `LR-TF32-2`
- Mode: `medium-cpu`
- Algorithm: `P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `['N=4096:weighted_second_moment_abs_error_threshold', 'N=8192:weighted_second_moment_abs_error_threshold']`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `2` | explanatory |
| num_executed_rows | `2` | explanatory |
| num_hard_vetoes | `2` | hard veto |
| max_factor_marginal_residual | `3.725290298461914e-08` | hard veto |
| max_induced_row_residual | `4.172325134277344e-07` | hard veto |
| max_induced_column_residual | `7.152557373046875e-07` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_weighted_mean_abs_error | `1.341104507446289e-07` | hard veto |
| max_weighted_second_moment_abs_error | `0.29352012276649475` | hard veto |
| max_tiny_materialized_apply_parity | `None` | hard veto |
| max_wall_time_seconds_explanatory | `2.9693876260425895` | explanatory |
| total_wall_time_seconds_explanatory | `3.3677104990929365` | explanatory |
| max_memory_maxrss_kb_explanatory | `479232` | explanatory |

## Rows

| N | Status | Hard vetoes | Factor residual | Row residual | Column residual | Mean error | Second error | Dense materialized |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 4096 | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `1.6763806343078613e-08` | `3.5762786865234375e-07` | `7.152557373046875e-07` | `1.1920928955078125e-07` | `0.29352012276649475` | `False` |
| 8192 | `FAIL` | `['weighted_second_moment_abs_error_threshold']` | `3.725290298461914e-08` | `4.172325134277344e-07` | `7.152557373046875e-07` | `1.341104507446289e-07` | `0.2935119569301605` | `False` |

## Run Manifest

- Git commit: `3b11bb1b4848eeeafdd60671f476ba90d54b4caa`
- Command: `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode medium-cpu --particle-counts 4096 8192 --batch-size 2 --state-dim 8 --rank 64 --dtype float32 --fixture-id bounded_smooth_v1 --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.md`
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
