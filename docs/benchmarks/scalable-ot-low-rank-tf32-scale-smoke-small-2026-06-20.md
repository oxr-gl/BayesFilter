# Low-Rank TF32 Scale Smoke Diagnostics

- Status: `PASS`
- Phase: `LR-TF32-1`
- Mode: `small`
- Algorithm: `P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `1` | explanatory |
| num_executed_rows | `1` | explanatory |
| num_hard_vetoes | `0` | hard veto |
| max_factor_marginal_residual | `2.6095782496710074e-08` | hard veto |
| max_induced_row_residual | `8.350650400057447e-07` | hard veto |
| max_induced_column_residual | `8.034103933240999e-07` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_weighted_mean_abs_error | `6.994832352918978e-08` | hard veto |
| max_weighted_second_moment_abs_error | `0.28594539075338404` | hard veto |
| max_tiny_materialized_apply_parity | `1.6653345369377348e-16` | hard veto |
| max_wall_time_seconds_explanatory | `0.061953924130648375` | explanatory |
| total_wall_time_seconds_explanatory | `0.22737234109081328` | explanatory |
| max_memory_maxrss_kb_explanatory | `473088` | explanatory |

## Rows

| N | Status | Hard vetoes | Factor residual | Row residual | Column residual | Mean error | Second error | Dense materialized |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 32 | `PASS` | `[]` | `2.6095782496710074e-08` | `8.350650400057447e-07` | `8.034103933240999e-07` | `6.994832352918978e-08` | `0.28594539075338404` | `True` |

## Run Manifest

- Git commit: `3b11bb1b4848eeeafdd60671f476ba90d54b4caa`
- Command: `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode small --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.md`
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
