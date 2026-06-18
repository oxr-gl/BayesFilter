# Phase 8 Sparse/Localized Locality Diagnostics

- Status: `PASS`
- Phase 8 status: `PHASE_8_SPARSE_LOCALITY_DIAGNOSTIC_COMPLETED_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW`
- Decision: `SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW`
- Semantic class: `reference_only_diagnostic`
- Implementation scope: `dense_plan_locality_and_truncation_diagnostic`
- Hard vetoes: `[]`
- Promotion vetoes: `['tiny_manual:truncated_row_residual_too_large', 'small_parity:median_99_support_too_large', 'small_parity:truncated_row_residual_too_large', 'high_dim_low_rank:median_99_support_too_large', 'high_dim_low_rank:p90_99_support_too_large', 'high_dim_low_rank:truncated_column_residual_too_large', 'high_dim_locality:median_99_support_too_large', 'high_dim_locality:p90_99_support_too_large', 'high_dim_locality:truncated_column_residual_too_large']`

## Summary

| Metric | Value |
| --- | ---: |
| max dense row residual | `1.875914e-02` |
| max dense column residual | `2.220446e-15` |
| max truncated row residual | `1.875914e-02` |
| max truncated column residual | `2.113375e-01` |
| max truncated particle error | `8.125627e-03` |
| max 99% support p90 fraction of N | `1.000000e+00` |

## Fixture Rows

| Fixture | Decision | N | Median k99 | P90 k99 | Trunc row residual | Trunc column residual | Trunc max particle error | Nonzero fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tiny_manual | `SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW` | 6 | `5.500` | `6.000` | `1.257253e-02` | `1.649076e-02` | `6.269549e-03` | `9.166667e-01` |
| small_parity | `SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW` | 16 | `16.000` | `16.000` | `1.875914e-02` | `1.735277e-02` | `4.697058e-03` | `9.062500e-01` |
| high_dim_low_rank | `SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW` | 64 | `61.000` | `63.000` | `3.468684e-04` | `2.113375e-01` | `8.125627e-03` | `9.543457e-01` |
| high_dim_locality | `SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW` | 64 | `62.000` | `63.000` | `1.283582e-03` | `1.794334e-01` | `3.441947e-03` | `9.694824e-01` |

## Threshold Definitions

- `N = transport_matrix.shape[2]`, the source-particle count.
- `k_i(t)` uses a deterministic stable descending sort of row mass.
- Ties are not expanded beyond the first stable prefix reaching the threshold.
- The truncated transport is diagnostic-only and is not a sparse solver.

## Non-Claims

- Phase 8 dense-plan locality diagnostic only
- not a sparse solver implementation
- no sparse speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no general scalability claim
- source availability is not locality evidence
