# Low-Rank LEDH/PFPF-OT Filter Integration Smoke

- Status: `PASS`
- Phase: `LR-LEDH-PFPF-INT-3`
- Mode: `medium-cpu`
- Algorithm: `LEDH/PFPF-OT filter loop with P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `2` | explanatory |
| num_executed_rows | `2` | explanatory |
| num_hard_vetoes | `0` | hard veto |
| num_viable_rows | `2` | explanatory |
| max_low_rank_resampling_invocations | `2` | hard veto |
| max_active_resampling_mask_count | `2` | hard veto |
| max_factor_marginal_residual | `1.6391277313232422e-07` | hard veto |
| max_induced_row_residual | `1.4901161193847656e-06` | hard veto |
| max_induced_column_residual | `1.7881393432617188e-06` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_wall_time_seconds_explanatory | `1.3552922331728041` | explanatory |
| total_wall_time_seconds_explanatory | `2.8230208880268037` | explanatory |
| max_memory_maxrss_kb_explanatory | `479232` | explanatory |

## Rows

| N | Rank | Epsilon | Status | Hard vetoes | Invocations | Active count | Factor residual | Row residual | Column residual | Sentinel shapes |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 4096 | `16` | `0.015625` | `PASS` | `[]` | `2` | `2` | `1.341104507446289e-07` | `1.4901161193847656e-06` | `1.7881393432617188e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 8192 | `16` | `0.015625` | `PASS` | `[]` | `2` | `2` | `1.6391277313232422e-07` | `1.2516975402832031e-06` | `1.6689300537109375e-06` | `[[1, 0, 0], [1, 0, 0]]` |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Command: `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py --mode medium-cpu --rank 16 --assignment-epsilon 0.015625 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-medium-cpu-2026-06-20.md`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
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
