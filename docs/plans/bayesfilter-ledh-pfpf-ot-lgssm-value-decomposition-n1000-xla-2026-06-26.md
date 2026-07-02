# LEDH-PFPF-OT LGSSM Value-Decomposition Diagnostic Result

Date: 2026-06-26T07:49:25.253919+00:00

## Manifest

| Field | Value |
|---|---|
| num_particles | `1000` |
| seed_count | `10` |
| time_steps | `10` |
| xla | `True` |
| device_scope | `visible` |
| cuda_visible_devices | `0` |
| tf32_execution_enabled | `True` |
| runtime_seconds | `18.536563058034517` |

## Decision Table

| Field | Status |
|---|---|
| Decision | Value gap appears only after OT/reset; prioritize transport/resampling semantics. |
| Primary criterion | Failure requires abs(delta)/MCSE > 2 and abs(delta)/seed_sd > 2 at the same prefix. |
| Main uncertainty | Whether finite Sinkhorn epsilon or reset-to-uniform is the dominant OT effect. |
| Next action | Inspect whether OT reset preserves the marginal likelihood estimator. |
| Not concluded | No gradient correctness, SIR correctness, posterior correctness, HMC readiness, or production validity. |

## Arm Totals

| State dim | Arm | Mean | Kalman | Delta | SD | MCSE | abs z | abs seed-SD units | First failing prefix |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | sis_no_transport | -6.925509 | -6.914505 | -0.011004 | 0.065124 | 0.020594 | 0.534 | 0.169 | None |
| 1 | ledh_no_ot | -6.912147 | -6.914505 | 0.002358 | 0.004565 | 0.001444 | 1.634 | 0.517 | None |
| 1 | ledh_ot | -6.507701 | -6.914505 | 0.406804 | 0.008215 | 0.002598 | 156.597 | 49.520 | 1 |
| 2 | sis_no_transport | -13.858361 | -13.784139 | -0.074222 | 0.228468 | 0.072248 | 1.027 | 0.325 | None |
| 2 | ledh_no_ot | -13.793434 | -13.784139 | -0.009296 | 0.021238 | 0.006716 | 1.384 | 0.438 | None |
| 2 | ledh_ot | -12.874837 | -13.784139 | 0.909302 | 0.019806 | 0.006263 | 145.181 | 45.910 | 1 |

## Convention Probes

State dim 1:

- transition-first total: `-6.914505`
- observe-initial-first total: `-6.981905`
- transition-first drop-first total: `-6.250688`
- transition-first drop-last total: `-6.242581`

State dim 2:

- transition-first total: `-13.784139`
- observe-initial-first total: `-13.918564`
- transition-first drop-first total: `-12.452392`
- transition-first drop-last total: `-12.447368`

## Interpretation

- state_dim=1: first failures SIS=None, LEDH-no-OT=None, LEDH+OT=1.
- state_dim=2: first failures SIS=None, LEDH-no-OT=None, LEDH+OT=1.
