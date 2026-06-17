# LEDH-PFPF-OT PF MC Error vs Precision

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-pf-mc-error-vs-precision-gpu0-b1-t5-np32-d4-m4-seeds6-2026-06-15.json`
- Overall passed: `False`
- Shape: `{'batch_size': 1, 'time_steps': 5, 'num_particles': 32, 'state_dim': 4, 'obs_dim': 4, 'parameter_dim': 3}`
- Seeds: `None`

## FP64 MC Noise

- Value sample SD: `None`
- Score sample SD: `None`

## Precision Ratios

| precision | value RMS / FP64 SD | max score RMS / FP64 SD |
| --- | ---: | ---: |

## Nonclaims

- focused PF MC noise-floor diagnostic only
- small seed count is descriptive, not a precise uncertainty interval
- no HMC readiness claim
- no production default precision change
- seed-to-seed fixture variability is a practical PF MC proxy here
