# Phase 3 Common Interface Schema Smoke

- Status: `PASS`
- Schema version: `scalable_ot_candidate_result_v1`
- Example count: `9`

## Examples

| Candidate | Object kind | Source status | Semantic class | Warnings |
| --- | --- | --- | --- | --- |
| dense_baseline_schema_example | `dense_matrix` | `source_locked` | `exact_semantics` | `[]` |
| streaming_baseline_schema_example | `streaming_nonmaterialized` | `source_locked` | `exact_semantics` | `[]` |
| nystrom_schema_example | `kernel_factors` | `source_locked` | `approximate_kernel` | `[]` |
| exact_online_lazy_operator_schema_example | `lazy_operator` | `source_reference_only` | `exact_semantics` | `[]` |
| low_rank_coupling_schema_example | `low_rank_coupling_factors` | `source_locked` | `semantic_replacement` | `[]` |
| sparse_schema_example | `sparse_plan` | `source_reference_only` | `reference_only` | `[]` |
| sliced_schema_example | `projection_plan` | `source_locked` | `semantic_replacement` | `[]` |
| projected_output_schema_example | `projected_output` | `source_locked` | `semantic_replacement` | `[]` |
| minibatch_blocked_schema_example | `blocked` | `source_partial_user_needed` | `blocked` | `[]` |

## Non-Claims

- schema/harness validation only
- no candidate algorithm implemented
- no candidate correctness claim
- no speedup claim
- no ranking claim
- no production default change
