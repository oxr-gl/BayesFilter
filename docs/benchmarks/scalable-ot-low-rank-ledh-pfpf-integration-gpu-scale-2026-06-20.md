# Low-Rank LEDH/PFPF-OT Filter Integration Smoke

- Status: `PASS`
- Phase: `LR-LEDH-PFPF-INT-4`
- Mode: `gpu-scale`
- Algorithm: `LEDH/PFPF-OT filter loop with P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `2` | explanatory |
| num_executed_rows | `2` | explanatory |
| num_hard_vetoes | `0` | hard veto |
| num_viable_rows | `2` | explanatory |
| max_low_rank_resampling_invocations | `1` | hard veto |
| max_active_resampling_mask_count | `1` | hard veto |
| max_factor_marginal_residual | `2.9802322387695312e-08` | hard veto |
| max_induced_row_residual | `1.1920928955078125e-06` | hard veto |
| max_induced_column_residual | `1.5497207641601562e-06` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_wall_time_seconds_explanatory | `18.85347507498227` | explanatory |
| total_wall_time_seconds_explanatory | `33.96942170592956` | explanatory |
| max_memory_maxrss_kb_explanatory | `2083248` | explanatory |

## Rows

| N | Rank | Epsilon | Status | Hard vetoes | Invocations | Active count | Factor residual | Row residual | Column residual | Sentinel shapes |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 50000 | `16` | `0.015625` | `PASS` | `[]` | `1` | `1` | `1.4901161193847656e-08` | `1.1920928955078125e-06` | `1.5497207641601562e-06` | `[[1, 0, 0]]` |
| 100000 | `16` | `0.015625` | `PASS` | `[]` | `1` | `1` | `2.9802322387695312e-08` | `1.1920928955078125e-06` | `1.3709068298339844e-06` | `[[1, 0, 0]]` |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Command: `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py --mode gpu-scale --rank 16 --assignment-epsilon 0.015625 --conditional-100k --tf32-mode enabled --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.md`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `None`
- Fixture: `ledh_lgssm_forced_resampling_v1`

## Non-Claims

- low-rank LEDH/PFPF-OT filter-integration diagnostic only
- no speedup claim
- no ranking claim
- no superiority claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no TF32-help claim
