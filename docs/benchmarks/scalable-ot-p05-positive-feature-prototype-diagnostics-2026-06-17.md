# Phase 5 Positive-Feature Prototype Diagnostics

- Status: `PASS`
- Phase 5 status: `PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PASSED_SEMANTIC_REPLACEMENT`
- Semantic class: `semantic_replacement`
- Validity pass: `True`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| max row residual | `3.221883e-05` |
| max column residual | `2.220446e-16` |
| max dense-reference particle error, explanatory | `1.487610e-01` |
| max dense-reference RMS error, explanatory | `8.104504e-02` |

## Fixture Rows

| Fixture | Features | Valid | Row residual | Column residual | Max dense error, explanatory | RMS dense error, explanatory |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| tiny_manual | 128 | `True` | `1.162425e-05` | `0.000000e+00` | `1.443328e-01` | `6.052808e-02` |
| small_parity | 128 | `True` | `3.221883e-05` | `1.110223e-16` | `1.487610e-01` | `8.104504e-02` |
| high_dim_low_rank | 128 | `True` | `8.476849e-07` | `2.220446e-16` | `8.839557e-02` | `2.946738e-02` |
| high_dim_locality | 128 | `True` | `6.278544e-06` | `2.220446e-16` | `1.088364e-01` | `4.344433e-02` |

## Non-Claims

- Phase 5 positive-feature semantic-replacement diagnostics only
- no dense Gibbs equivalence claim
- no speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no general scalability claim
