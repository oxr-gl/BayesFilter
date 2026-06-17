# Phase 1 Baseline Fixture Diagnostics

- Status: `PASS`
- Git commit: `70ab32644cedeb95d4b56e096448f3bb2c908763`
- TensorFlow: `2.20.0`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`

## Fixture Summary

| Fixture | Dense finite | Streaming finite | Dense row residual | Dense column residual | Max dense-streaming particle error |
| --- | --- | --- | --- | --- | --- |
| tiny_manual | `True` | `True` | `1.257253e-02` | `4.440892e-16` | `1.110223e-16` |
| small_parity | `True` | `True` | `1.875914e-02` | `6.661338e-16` | `1.665335e-16` |
| high_dim_low_rank | `True` | `True` | `3.468684e-04` | `2.220446e-15` | `4.440892e-16` |
| high_dim_locality | `True` | `True` | `1.283582e-03` | `1.554312e-15` | `2.498002e-16` |

## Hard Vetoes

`[]`

## Non-Claims

- Phase 1 baseline transport diagnostics only
- no scalable candidate correctness claim
- no speedup claim
- no posterior validity claim
- no production default change
- no statistical ranking
- no GPU performance claim
