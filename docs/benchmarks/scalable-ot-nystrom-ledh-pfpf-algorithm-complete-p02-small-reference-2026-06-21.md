# Nystrom LEDH/PFPF-OT Algorithm-Complete Diagnostics

- Status: `PASS`
- Mode: `small-reference`
- Algorithm family: `fixed_rank_nystrom_kernel_sinkhorn_ledh_pfpf_ot_diagnostic`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| `num_rows` | `15` |
| `num_passed_rows` | `14` |
| `num_hard_vetoes` | `0` |
| `max_row_residual` | `9.902792837324093e-05` |
| `max_column_residual` | `2.220446049250313e-16` |
| `max_output_log_weight_normalization_residual` | `None` |
| `min_ess_fraction` | `None` |
| `max_dense_reference_particle_error` | `0.08564275772586204` |
| `max_dense_reference_rms_error` | `0.026235230425731913` |
| `total_wall_time_seconds_explanatory` | `2.106267180060968` |
| `max_memory_maxrss_kb_explanatory` | `519968` |

## Rows

| Row | Rank | Status | Hard vetoes | Row residual | Column residual | ESS fraction | Dense max error | Sentinel shapes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| `tiny_manual` | `2` | `PASS` | `[]` | `3.423223794640773e-05` | `0.0` | `None` | `0.046072075360535814` | `[1, 0, 0]` |
| `tiny_manual` | `3` | `PASS` | `[]` | `9.902792837324093e-05` | `0.0` | `None` | `0.026505075334772796` | `[1, 0, 0]` |
| `tiny_manual` | `4` | `PASS` | `[]` | `3.891248824050564e-05` | `2.220446049250313e-16` | `None` | `0.0012440674291325227` | `[1, 0, 0]` |
| `small_parity` | `2` | `PASS` | `[]` | `9.436508849869352e-05` | `0.0` | `None` | `0.03443605007438879` | `[2, 0, 0]` |
| `small_parity` | `4` | `PASS` | `[]` | `6.463268846501613e-05` | `1.1102230246251565e-16` | `None` | `0.013549860012208842` | `[2, 0, 0]` |
| `small_parity` | `8` | `PASS` | `[]` | `5.491017766423578e-05` | `0.0` | `None` | `0.00597720123656359` | `[2, 0, 0]` |
| `high_dim_low_rank` | `2` | `FAIL` | `['dense_reference_max_error_threshold']` | `2.9893476441111844e-05` | `1.1102230246251565e-16` | `None` | `0.08564275772586204` | `[1, 0, 0]` |
| `high_dim_low_rank` | `4` | `PASS` | `[]` | `4.383282823938739e-05` | `2.220446049250313e-16` | `None` | `0.005010762618737341` | `[1, 0, 0]` |
| `high_dim_low_rank` | `8` | `PASS` | `[]` | `4.9666325111941134e-05` | `0.0` | `None` | `8.37116401308513e-05` | `[1, 0, 0]` |
| `high_dim_low_rank` | `16` | `PASS` | `[]` | `4.9690458262974246e-05` | `0.0` | `None` | `7.080026602812595e-05` | `[1, 0, 0]` |
| `high_dim_low_rank` | `32` | `PASS` | `[]` | `4.9603402864750734e-05` | `1.1102230246251565e-16` | `None` | `7.080342960219532e-05` | `[1, 0, 0]` |
| `ledh_specific_smoke` | `4` | `PASS` | `[]` | `6.0194807598890065e-05` | `1.1102230246251565e-16` | `None` | `0.05964056912650698` | `[1, 0, 0]` |
| `ledh_specific_smoke` | `8` | `PASS` | `[]` | `8.65669471270536e-05` | `2.220446049250313e-16` | `None` | `0.016749752181481226` | `[1, 0, 0]` |
| `ledh_specific_smoke` | `16` | `PASS` | `[]` | `8.937221444971222e-05` | `2.220446049250313e-16` | `None` | `0.013161355498723215` | `[1, 0, 0]` |
| `ledh_specific_smoke` | `32` | `PASS` | `[]` | `8.938865505481175e-05` | `2.220446049250313e-16` | `None` | `0.01316147673587198` | `[1, 0, 0]` |

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
