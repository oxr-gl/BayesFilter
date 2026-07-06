# Nystrom LEDH/PFPF-OT Algorithm-Complete Diagnostics

- Status: `PASS`
- Mode: `downstream-smoke`
- Algorithm family: `fixed_rank_nystrom_kernel_sinkhorn_ledh_pfpf_ot_diagnostic`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| `num_rows` | `2` |
| `num_passed_rows` | `2` |
| `num_hard_vetoes` | `0` |
| `max_row_residual` | `2.8744214464193618e-05` |
| `max_column_residual` | `1.1102230246251565e-16` |
| `max_output_log_weight_normalization_residual` | `0.0` |
| `min_ess_fraction` | `0.9999939940500705` |
| `max_dense_reference_particle_error` | `None` |
| `max_dense_reference_rms_error` | `None` |
| `total_wall_time_seconds_explanatory` | `0.32868878194130957` |
| `max_memory_maxrss_kb_explanatory` | `473088` |

## Rows

| Row | Rank | Status | Hard vetoes | Row residual | Column residual | ESS fraction | Dense max error | Sentinel shapes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| `nystrom_ledh_smoke_n64_rank8` | `8` | `PASS` | `[]` | `2.8744214464193618e-05` | `1.1102230246251565e-16` | `0.9999941345181469` | `None` | `[[1, 0, 0], [1, 0, 0]]` |
| `nystrom_ledh_smoke_n128_rank16` | `16` | `PASS` | `[]` | `2.7929399874171423e-05` | `1.1102230246251565e-16` | `0.9999939940500705` | `None` | `[[1, 0, 0], [1, 0, 0]]` |

## Non-Claims

- Nystrom LEDH/PFPF-OT diagnostic only
- no speedup claim
- no ranking claim
- no superiority claim
- no production/default readiness claim
- no production/default route change
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no dense Sinkhorn equivalence claim beyond checked small fixtures
- no broad scalable-OT leaderboard claim
