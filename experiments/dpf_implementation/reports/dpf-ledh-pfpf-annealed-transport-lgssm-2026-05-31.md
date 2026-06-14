# LEDH-PF-PF Annealed Transport LGSSM

## Decision

`ledh_pfpf_annealed_transport_lgssm_finite_diagnostics`

## Summary

| Key | Value |
| --- | --- |
| `row_count` | `27` |
| `executed_row_count` | `27` |
| `finite_row_count` | `27` |
| `nonfinite_row_count` | `0` |
| `max_abs_error_per_time` | `0.015512713400855773` |
| `max_sinkhorn_residual` | `3.552713678800501e-15` |
| `max_abs_corrected_log_weight` | `14.856345448972045` |
| `min_jacobian_singular_value` | `0.30151134457776363` |
| `interpretation` | `finite bounded diagnostics on the matched filterflow LGSSM protocol; not a requirement that LEDH equal filterflow RegularisedTransform` |
| `annealed_transport_row_count` | `27` |
| `transport_method` | `filterflow_style_annealed_transport_tf` |
| `pfpf_correction_status` | `recorded_in_rows` |
| `fixed_target_sinkhorn_status` | `not_default_local_comparator_only` |

## Non-Implications

- No production readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No claim that LEDH must equal filterflow RegularisedTransform is concluded.
