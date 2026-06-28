# Nystrom LEDH/PFPF-OT Algorithm-Complete Diagnostics

- Status: `PASS`
- Mode: `gpu-scale`
- Algorithm family: `fixed_rank_nystrom_kernel_sinkhorn_ledh_pfpf_ot_diagnostic`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| `num_rows` | `4` |
| `num_passed_rows` | `4` |
| `num_hard_vetoes` | `0` |
| `max_row_residual` | `3.540515899658203e-05` |
| `max_column_residual` | `1.1920928955078125e-07` |
| `max_output_log_weight_normalization_residual` | `0.0` |
| `min_ess_fraction` | `0.9999862909317017` |
| `max_dense_reference_particle_error` | `None` |
| `max_dense_reference_rms_error` | `None` |
| `total_wall_time_seconds_explanatory` | `12.462970233988017` |
| `max_memory_maxrss_kb_explanatory` | `2025472` |

## Rows

| Row | Rank | Status | Hard vetoes | Row residual | Column residual | ESS fraction | Dense max error | Sentinel shapes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| `nystrom_gpu_n1024_rank16` | `16` | `PASS` | `[]` | `2.1696090698242188e-05` | `5.960464477539063e-08` | `0.9999866485595703` | `None` | `[[1, 0, 0], [1, 0, 0]]` |
| `nystrom_gpu_n4096_rank32` | `32` | `PASS` | `[]` | `2.5153160095214844e-05` | `5.960464477539063e-08` | `0.9999880790710449` | `None` | `[[1, 0, 0], [1, 0, 0]]` |
| `nystrom_gpu_n8192_rank32` | `32` | `PASS` | `[]` | `2.0384788513183594e-05` | `5.960464477539063e-08` | `0.9999862909317017` | `None` | `[[1, 0, 0], [1, 0, 0]]` |
| `nystrom_gpu_n16384_rank64` | `64` | `PASS` | `[]` | `3.540515899658203e-05` | `1.1920928955078125e-07` | `0.9999880790710449` | `None` | `[[1, 0, 0], [1, 0, 0]]` |

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
