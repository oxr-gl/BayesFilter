# Phase 4 Nystrom Prototype Diagnostics

- Status: `PASS`
- Phase 4 status: `PHASE_4_NYSTROM_PROTOTYPE_PASSED`
- Validity pass: `True`
- Viability pass: `True`
- Rank scope: `full_rank_factor_correctness_probe`
- Hard vetoes: `[]`

## Summary

| Metric | Value |
| --- | ---: |
| max row residual | `6.102528e-05` |
| max column residual | `2.220446e-16` |
| max dense-reference particle error | `3.532978e-03` |
| max dense-reference RMS error | `1.575147e-03` |

## Fixture Rows

| Fixture | Rank | Valid | Row residual | Column residual | Max dense error | RMS dense error |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| tiny_manual | 6 | `True` | `3.959144e-05` | `1.110223e-16` | `2.431739e-03` | `8.734439e-04` |
| small_parity | 16 | `True` | `6.102528e-05` | `2.220446e-16` | `3.532978e-03` | `1.575147e-03` |
| high_dim_low_rank | 64 | `True` | `3.999895e-05` | `2.220446e-16` | `6.719007e-05` | `2.236185e-05` |
| high_dim_locality | 64 | `True` | `2.608273e-05` | `1.110223e-16` | `2.381838e-04` | `6.121014e-05` |

## Non-Claims

- Phase 4 Nystrom prototype diagnostics only
- no speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no general scalability claim
- no subquadratic runtime or memory claim from full-rank probes
