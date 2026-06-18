# Phase 6 Low-Rank Coupling Prototype Diagnostics

- Status: `PASS`
- Phase 6 status: `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED`
- Semantic class: `semantic_replacement`
- Implementation scope: `transport_object_fixture_route`
- Validity pass: `True`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| max factor marginal residual | `8.981518e-06` |
| max induced row residual | `3.709804e-04` |
| max induced column residual | `5.748172e-04` |
| max dense-reference particle error, explanatory | `9.884159e-02` |
| max dense-reference RMS error, explanatory | `4.010295e-02` |

## Fixture Rows

| Fixture | Rank | Valid | Factor residual | Row residual | Column residual | Max dense error, explanatory | RMS dense error, explanatory |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| tiny_manual | 4 | `True` | `6.969942e-06` | `2.657128e-05` | `4.181965e-05` | `9.884159e-02` | `4.010295e-02` |
| small_parity | 4 | `True` | `8.056853e-06` | `1.199952e-04` | `1.289097e-04` | `8.689544e-02` | `3.555603e-02` |
| high_dim_low_rank | 4 | `True` | `5.796569e-06` | `3.709804e-04` | `1.312180e-04` | `7.290280e-02` | `2.352029e-02` |
| high_dim_locality | 4 | `True` | `8.981518e-06` | `3.008620e-04` | `5.748172e-04` | `6.560401e-02` | `2.594369e-02` |

## Non-Claims

- Phase 6 low-rank coupling transport-object fixture diagnostics only
- semantic replacement, not dense Sinkhorn equivalence
- not low-rank Sinkhorn solver fidelity
- no speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no general scalability claim
