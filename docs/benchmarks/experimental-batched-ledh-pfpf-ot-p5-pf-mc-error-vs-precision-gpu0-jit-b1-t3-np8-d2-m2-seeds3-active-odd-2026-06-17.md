# LEDH-PFPF-OT PF MC Error vs Precision

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-pf-mc-error-vs-precision-gpu0-jit-b1-t3-np8-d2-m2-seeds3-active-odd-2026-06-17.json`
- Overall passed: `True`
- Shape: `{'batch_size': 1, 'time_steps': 3, 'num_particles': 8, 'state_dim': 2, 'obs_dim': 2, 'parameter_dim': 3}`
- Seeds: `[20260617, 20261626, 20262635]`

## FP64 MC Noise

- Value sample SD: `[0.025699403596717567]`
- Score sample SD: `[[0.05630582349604793, 0.015880961407543265, 0.008793608079236197]]`

## Precision Ratios

| precision | value RMS / FP64 SD | max score RMS / FP64 SD |
| --- | ---: | ---: |
| fp32_no_tf32 | [2.5213270905237544e-05] | 1.89658e-05 |
| fp32_tf32 | [9.623909211576227e-05] | 0.000948405 |

## Nonclaims

- focused PF MC noise-floor diagnostic only
- small seed count is descriptive, not a precise uncertainty interval
- no HMC readiness claim
- no production default precision change
- seed-to-seed fixture variability is a practical PF MC proxy here
