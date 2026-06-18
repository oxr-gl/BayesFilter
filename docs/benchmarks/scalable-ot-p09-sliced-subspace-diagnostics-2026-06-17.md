# Phase 9 Sliced/Subspace Diagnostic

- Status: `PASS`
- Phase 9 status: `PHASE_9_SLICED_SUBSPACE_EXPLORATORY_DIAGNOSTIC_PASSED_SEMANTIC_REPLACEMENT`
- Semantic class: `semantic_replacement`
- Implementation scope: `fixed_projection_monotone_displacement_diagnostic`
- Mini-batch/BoMb status: `blocked_unexecuted_source_partial_user_needed`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| max projected reconstruction error | `5.551115e-17` |
| max dense-reference particle error, explanatory | `6.491195e-01` |
| max dense-reference RMS error, explanatory | `1.697636e-01` |
| max log-weight normalization residual | `0.000000e+00` |

## Fixture Rows

| Fixture | Valid | Projections | Projected reconstruction error | Dense max error, explanatory | Dense RMS error, explanatory |
| --- | --- | ---: | ---: | ---: | ---: |
| tiny_manual | `True` | 3 | `1.387779e-17` | `3.559003e-01` | `1.465349e-01` |
| small_parity | `True` | 4 | `5.551115e-17` | `2.077745e-01` | `8.767786e-02` |
| high_dim_low_rank | `True` | 4 | `5.551115e-17` | `6.491195e-01` | `1.697636e-01` |
| high_dim_locality | `True` | 4 | `2.775558e-17` | `2.660982e-01` | `7.478807e-02` |

## Semantics

- Fixed deterministic projection directions are used.
- One-dimensional monotone weighted-quantile maps are lifted by averaged projection displacements.
- Dense-reference discrepancy is explanatory only.
- Mini-batch/BoMb remains blocked and unexecuted.

## Non-Claims

- Phase 9 sliced/subspace semantic-replacement diagnostic only
- not dense entropic OT equivalence
- not a sparse solver implementation
- Mini-batch/BoMb remains blocked and unexecuted
- no speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no HMC-readiness claim
