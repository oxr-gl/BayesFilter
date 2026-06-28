# Low-Rank LEDH/PFPF-OT Filter Integration Smoke

- Status: `PASS`
- Phase: `LR-LEDH-PFPF-INT-2`
- Mode: `tuning-cpu`
- Algorithm: `LEDH/PFPF-OT filter loop with P = Q diag(1/g) R^T lazy low-rank solver-route resampling`
- Hard vetoes: `[]`

## Summary

| Metric | Value | Role |
| --- | ---: | --- |
| num_rows | `12` | explanatory |
| num_executed_rows | `12` | explanatory |
| num_hard_vetoes | `0` | hard veto |
| num_viable_rows | `12` | explanatory |
| max_low_rank_resampling_invocations | `2` | hard veto |
| max_active_resampling_mask_count | `2` | hard veto |
| max_factor_marginal_residual | `2.468354068696499e-06` | hard veto |
| max_induced_row_residual | `0.0012637972831726074` | hard veto |
| max_induced_column_residual | `0.0012629032135009766` | hard veto |
| max_output_log_weight_normalization_residual | `0.0` | hard veto |
| max_wall_time_seconds_explanatory | `1.591207329183817` | explanatory |
| total_wall_time_seconds_explanatory | `8.403738541062921` | explanatory |
| max_memory_maxrss_kb_explanatory | `485376` | explanatory |

## Rows

| N | Rank | Epsilon | Status | Hard vetoes | Invocations | Active count | Factor residual | Row residual | Column residual | Sentinel shapes |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 512 | `16` | `0.0625` | `PASS` | `[]` | `2` | `2` | `2.9802322387695312e-08` | `1.5497207641601562e-06` | `1.5497207641601562e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `16` | `0.03125` | `PASS` | `[]` | `2` | `2` | `2.9802322387695312e-08` | `1.3709068298339844e-06` | `1.1920928955078125e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `16` | `0.015625` | `PASS` | `[]` | `2` | `2` | `1.4901161193847656e-08` | `1.430511474609375e-06` | `1.5497207641601562e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `32` | `0.0625` | `PASS` | `[]` | `2` | `2` | `2.2351741790771484e-08` | `4.5299530029296875e-06` | `3.814697265625e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `32` | `0.03125` | `PASS` | `[]` | `2` | `2` | `5.25033101439476e-08` | `2.6881694793701172e-05` | `2.586841583251953e-05` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `32` | `0.015625` | `PASS` | `[]` | `2` | `2` | `1.7916318029165268e-07` | `9.161233901977539e-05` | `9.1552734375e-05` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `64` | `0.0625` | `PASS` | `[]` | `2` | `2` | `7.450580596923828e-09` | `2.2649765014648438e-06` | `2.1457672119140625e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `64` | `0.03125` | `PASS` | `[]` | `2` | `2` | `9.313225746154785e-09` | `2.5033950805664062e-06` | `2.7418136596679688e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `64` | `0.015625` | `PASS` | `[]` | `2` | `2` | `7.450580596923828e-09` | `2.0265579223632812e-06` | `2.1457672119140625e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `128` | `0.0625` | `PASS` | `[]` | `2` | `2` | `4.6566128730773926e-09` | `2.5033950805664062e-06` | `2.1457672119140625e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `128` | `0.03125` | `PASS` | `[]` | `2` | `2` | `8.032657206058502e-09` | `4.231929779052734e-06` | `3.933906555175781e-06` | `[[1, 0, 0], [1, 0, 0]]` |
| 512 | `128` | `0.015625` | `PASS` | `[]` | `2` | `2` | `2.468354068696499e-06` | `0.0012637972831726074` | `0.0012629032135009766` | `[[1, 0, 0], [1, 0, 0]]` |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Command: `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py --mode tuning-cpu --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-tuning-cpu-2026-06-20.md`
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
