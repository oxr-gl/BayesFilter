# LEDH-PFPF-OT PF MC Error vs Precision

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-pf-mc-error-vs-precision-cpu-jit-b1-t3-np8-d2-m2-seeds3-active-odd-2026-06-17.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 8, 'state_dim': 2, 'obs_dim': 2, 'parameter_dim': 3}`
- Seeds: `[20260617, 20261626, 20262635]`

## FP64 MC Noise

- Value sample SD: `[0.02569940359671746]`
- Score sample SD: `[[0.05630582349604792, 0.015880961407543578, 0.008793608079235946]]`

## Precision Ratios

| precision | value RMS / FP64 SD | max score RMS / FP64 SD |
| --- | ---: | ---: |
| fp32_no_tf32 | [3.6984086866970433e-06] | 8.44437e-06 |
| fp32_tf32 | [3.6984086866970433e-06] | 8.44437e-06 |

## Nonclaims

- focused PF MC noise-floor diagnostic only
- small seed count is descriptive, not a precise uncertainty interval
- no HMC readiness claim
- no production default precision change
- seed-to-seed fixture variability is a practical PF MC proxy here
