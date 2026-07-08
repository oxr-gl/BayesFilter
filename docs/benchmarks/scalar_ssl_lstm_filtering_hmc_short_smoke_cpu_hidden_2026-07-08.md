# Scalar SSL-LSTM Filtering Short HMC Smoke - 2026-07-08

## Decision

- short_smoke_passed: `True`
- vetoes: `[]`
- next_justified_action: draft and review Phase 5 replicated scalar HMC diagnostic subplan

## Fixed Kernel

- leapfrog steps: `4`
- step size: `0.3925`
- trajectory length: `1.57`
- retained samples: `8`
- burn-in steps: `2`

## Smoke Telemetry

- row status: `passed_short_smoke`
- row vetoes: `[]`
- acceptance: `1.0`
- target log prob: `{'finite': True, 'finite_count': 8, 'nonfinite_count': 0, 'min': -43.9264837911716, 'max': -37.82041866289685}`
- log accept ratio: `{'finite_count': 8, 'nonfinite_count': 0, 'min_finite': -0.07800942592144944, 'max_finite': 1.2216570464910503, 'max_abs_finite': 1.2216570464910503}`
- native divergence: `{'available': False, 'status': 'not_exposed_by_kernel', 'nonclaim': 'unavailable native divergence telemetry is not zero divergences'}`
- max abs u: `5.029991817355426`

## Inference Status

| field | value |
| --- | --- |
| hard_veto_screen | passed |
| statistically_supported_ranking | none; single short-smoke kernel |
| descriptive_only_differences | acceptance, target log-prob range, log-accept range, sample range, and runtime |
| default_readiness | not assessed |
| hmc_readiness | not assessed; short smoke only |
| next_evidence_needed | reviewed Phase 5 replicated scalar HMC diagnostic only if Phase 4 passes |

## Nonclaims

- short fixed-kernel HMC smoke only
- not HMC readiness evidence
- not HMC convergence evidence
- not posterior correctness evidence
- not a tuned kernel claim
- not a zero-divergence claim
- not sampler superiority evidence
- not statistical ranking evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not Zhao-Cui source-faithfulness evidence
