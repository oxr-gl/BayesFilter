# Streaming Transport Gradient NaN Localization

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-streaming-gradient-nan-localization-2026-06-17.json`
- Overall passed: `False`
- JIT compile: `True`

## Probes

| probe | status | outputs finite | gradients finite | first non-finite gradient |
| --- | --- | ---: | ---: | --- |
| dense_transport_reference | ok | True | True | `none` |
| streaming_softmin | ok | True | True | `none` |
| streaming_sinkhorn_potentials | ok | True | True | `none` |
| streaming_column_log_normalizer | ok | True | False | `grad_scaled_x` |
| streaming_transport_from_potentials | ok | True | False | `grad_scaled_x` |
| streaming_transport | ok | True | False | `grad_scaled_x` |

## Nonclaims

- NaN-localization diagnostic only
- dense transport is a tiny reference, not a scalable implementation
- no HMC readiness claim
- no posterior validity claim
- no production/default readiness claim
