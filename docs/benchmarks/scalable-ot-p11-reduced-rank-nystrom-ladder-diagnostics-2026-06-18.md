# Phase 11 Reduced-Rank Nystrom Ladder Diagnostics

- Status: `PASS`
- Phase 11 status: `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_PASSED_DIAGNOSTIC_ONLY`
- Validity pass: `True`
- Viability pass: `True`
- Hard vetoes: `[]`
- Candidate records: `23`

## Summary

| Metric | Value |
| --- | ---: |
| max row residual | `9.717282e-05` |
| max column residual | `4.440892e-16` |
| max dense-reference particle error | `4.352423e-01` |
| max dense-reference RMS error | `1.412411e-01` |
| wall time seconds | `2.257123e+00` |

## Viable Reduced Ranks

| Fixture | Viable reduced ranks |
| --- | --- |
| `tiny_manual` | `['3']` |
| `small_parity` | `['2', '4', '8']` |
| `high_dim_low_rank` | `['2', '4', '8', '16']` |
| `high_dim_locality` | `[]` |
| `ledh_specific_smoke` | `['4', '8', '16']` |

## Dense-Reference Threshold Hits

These ranks meet the numeric dense-reference screen; `high_dim_locality` remains explanatory.

| Fixture | Reduced ranks meeting dense-reference screen |
| --- | --- |
| `tiny_manual` | `['3']` |
| `small_parity` | `['2', '4', '8']` |
| `high_dim_low_rank` | `['2', '4', '8', '16']` |
| `high_dim_locality` | `['4', '8', '16']` |
| `ledh_specific_smoke` | `['4', '8', '16']` |

## LEDH-Specific Smoke Fixture

| Field | Value |
| --- | --- |
| `construction` | `deterministic latent curve embedded in 12 dimensions with flow-like shear, harmonic perturbation, two deterministic clusters, and fixed uneven weights` |
| `batch_size` | `1` |
| `num_particles` | `32` |
| `state_dim` | `12` |
| `latent_dim` | `3` |
| `runtime_random_draws` | `0` |
| `weight_entropy` | `3.3928247909176057` |
| `particle_norm` | `6.083716172257296` |

## Fixture Rows

| Fixture | Rank | Valid | Reduced-rank viable | Row residual | Column residual | Max dense error | RMS dense error | Memory entry ratio |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| tiny_manual | 1 | `True` | `False` | `4.440892e-16` | `2.220446e-16` | `2.259886e-01` | `9.318264e-02` | `5.277778e-01` |
| tiny_manual | 2 | `True` | `False` | `2.513632e-05` | `0.000000e+00` | `7.677046e-02` | `4.143979e-02` | `7.777778e-01` |
| tiny_manual | 3 | `True` | `True` | `2.894417e-05` | `0.000000e+00` | `6.536308e-02` | `2.955292e-02` | `1.083333e+00` |
| tiny_manual | full | `True` | `False` | `3.959144e-05` | `1.110223e-16` | `2.431739e-03` | `8.734439e-04` | `2.333333e+00` |
| small_parity | 2 | `True` | `True` | `9.717282e-05` | `2.220446e-16` | `3.228854e-02` | `1.219841e-02` | `2.656250e-01` |
| small_parity | 4 | `True` | `True` | `5.541179e-05` | `1.110223e-16` | `1.773784e-02` | `6.414321e-03` | `4.375000e-01` |
| small_parity | 8 | `True` | `True` | `6.000384e-05` | `2.220446e-16` | `6.386896e-03` | `1.997637e-03` | `8.750000e-01` |
| small_parity | full | `True` | `False` | `6.102528e-05` | `2.220446e-16` | `3.532978e-03` | `1.575147e-03` | `2.125000e+00` |
| high_dim_low_rank | 2 | `True` | `True` | `3.324953e-05` | `4.440892e-16` | `6.912475e-02` | `2.052889e-02` | `6.347656e-02` |
| high_dim_low_rank | 4 | `True` | `True` | `3.594986e-05` | `2.220446e-16` | `4.374132e-03` | `1.288894e-03` | `9.765625e-02` |
| high_dim_low_rank | 8 | `True` | `True` | `4.004757e-05` | `2.220446e-16` | `9.681785e-05` | `2.572466e-05` | `1.718750e-01` |
| high_dim_low_rank | 16 | `True` | `True` | `4.009460e-05` | `1.110223e-16` | `6.720853e-05` | `2.236365e-05` | `3.437500e-01` |
| high_dim_low_rank | full | `True` | `False` | `3.999895e-05` | `2.220446e-16` | `6.719007e-05` | `2.236185e-05` | `2.031250e+00` |
| high_dim_locality | 2 | `True` | `False` | `8.197628e-05` | `2.220446e-16` | `1.153202e-01` | `3.894455e-02` | `6.347656e-02` |
| high_dim_locality | 4 | `True` | `False` | `2.148749e-05` | `1.110223e-16` | `5.361009e-03` | `1.051191e-03` | `9.765625e-02` |
| high_dim_locality | 8 | `True` | `False` | `2.623051e-05` | `0.000000e+00` | `2.414333e-04` | `6.301902e-05` | `1.718750e-01` |
| high_dim_locality | 16 | `True` | `False` | `2.623989e-05` | `1.110223e-16` | `2.381813e-04` | `6.121344e-05` | `3.437500e-01` |
| high_dim_locality | full | `True` | `False` | `2.608273e-05` | `1.110223e-16` | `2.381838e-04` | `6.121014e-05` | `2.031250e+00` |
| ledh_specific_smoke | 2 | `True` | `False` | `6.330482e-05` | `2.220446e-16` | `4.352423e-01` | `1.412411e-01` | `1.289062e-01` |
| ledh_specific_smoke | 4 | `True` | `True` | `6.019481e-05` | `1.110223e-16` | `5.964057e-02` | `1.856104e-02` | `2.031250e-01` |
| ledh_specific_smoke | 8 | `True` | `True` | `8.656695e-05` | `2.220446e-16` | `1.674975e-02` | `3.699904e-03` | `3.750000e-01` |
| ledh_specific_smoke | 16 | `True` | `True` | `8.937221e-05` | `2.220446e-16` | `1.316136e-02` | `2.562982e-03` | `8.125000e-01` |
| ledh_specific_smoke | full | `True` | `False` | `8.938866e-05` | `2.220446e-16` | `1.316148e-02` | `2.562761e-03` | `2.062500e+00` |

## Non-Claims

- Phase 11 reduced-rank Nystrom diagnostics only
- no speedup claim
- no ranking claim
- no production default change
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production readiness claim
- no statistically supported ranking
