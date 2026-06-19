# P12E LEDH Sparse-Locality Screen

- Artifact scope: `official`
- Status: `PASS`
- P12E status: `LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION`
- Diagnostic completed: `True`
- Reopens sparse implementation plan only: `False`
- Semantic class: `reference_only_diagnostic`
- Implementation scope: `ledh_post_flow_dense_plan_locality_and_truncation_diagnostic`
- Hard vetoes: `[]`
- Promotion vetoes: `['ledh_lgssm_tiny_manual:truncated_row_residual_too_large', 'ledh_lgssm_moderate_clustered:median_99_support_too_large', 'ledh_lgssm_moderate_clustered:p90_99_support_too_large', 'ledh_lgssm_moderate_clustered:truncated_column_residual_too_large', 'ledh_lgssm_moderate_diffuse:median_99_support_too_large', 'ledh_lgssm_moderate_diffuse:p90_99_support_too_large', 'ledh_lgssm_moderate_diffuse:truncated_column_residual_too_large']`

## Summary

| Metric | Value |
| --- | ---: |
| max dense row residual | `3.010697e-02` |
| max dense column residual | `1.776357e-15` |
| max truncated row residual | `3.010697e-02` |
| max truncated column residual | `1.244273e-01` |
| max truncated particle error | `3.929614e-03` |
| max 99% support p90 fraction of N | `1.000000e+00` |
| min nearest-neighbor k=1 median mass | `3.222256e-02` |

## Fixture Rows

| Fixture | Decision | N | Median k99 | P90 k99 | Trunc row residual | Trunc column residual | Trunc max particle error | Nonzero fraction | Digest |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| ledh_lgssm_tiny_manual | `fixture_does_not_reopen_sparse_implementation` | 8 | `8.000` | `8.000` | `3.010697e-02` | `2.676974e-03` | `1.870943e-03` | `9.375000e-01` | `0e782f89ee79` |
| ledh_lgssm_moderate_clustered | `fixture_does_not_reopen_sparse_implementation` | 64 | `62.000` | `63.000` | `4.293260e-04` | `1.244273e-01` | `3.929614e-03` | `9.638672e-01` | `4c87456187f8` |
| ledh_lgssm_moderate_diffuse | `fixture_does_not_reopen_sparse_implementation` | 64 | `59.000` | `61.000` | `4.036299e-03` | `5.358002e-02` | `3.361478e-03` | `9.208984e-01` | `4137e761f73c` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION` | Diagnostic artifact criterion recorded by JSON/Markdown output. | Hard vetoes: `[]`; promotion vetoes: `['ledh_lgssm_tiny_manual:truncated_row_residual_too_large', 'ledh_lgssm_moderate_clustered:median_99_support_too_large', 'ledh_lgssm_moderate_clustered:p90_99_support_too_large', 'ledh_lgssm_moderate_clustered:truncated_column_residual_too_large', 'ledh_lgssm_moderate_diffuse:median_99_support_too_large', 'ledh_lgssm_moderate_diffuse:p90_99_support_too_large', 'ledh_lgssm_moderate_diffuse:truncated_column_residual_too_large']`. | Synthetic LEDH-like fixtures may not represent a future frozen real LEDH run. | Use the reviewed P12E-4 closeout subplan to map this artifact to the final lane result. | No sparse solver validity, speedup, ranking, posterior correctness, HMC/API/default/production readiness. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NONE` |
| Descriptive-only differences | Runtime, memory, support curves outside the 99% thresholds, nearest-neighbor mass, and LEDH log-det ranges. |
| Default-readiness | `NOT_ASSESSED_AND_NOT_CLAIMED` |
| Next evidence needed | P12E-4 closeout under the reviewed evidence contract. |
| Scope non-claim | Official diagnostic metrics require P12E-4 closeout before final lane interpretation. |

## Threshold Definitions

- `N = transport_matrix.shape[2]`, the source-particle count.
- `k_i(t)` uses a deterministic stable descending sort of row mass.
- Ties are not expanded beyond the first stable prefix reaching the threshold.
- The truncated transport is diagnostic-only and is not a sparse solver.
- Fixture digests hash deterministic inputs, LEDH outputs, and diagnostic weights.

## Non-Claims

- P12E LEDH sparse-locality screen diagnostic only
- not a sparse solver implementation
- no sparse solver validity claim
- no sparse speedup claim
- no ranking claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production default change
- no general sparse-OT validation or rejection
