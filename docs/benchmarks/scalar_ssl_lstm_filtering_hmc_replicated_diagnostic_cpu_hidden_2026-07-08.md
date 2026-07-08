# Scalar SSL-LSTM Filtering Replicated HMC Diagnostic - 2026-07-08

## Decision

- replicated_diagnostic_passed: `True`
- vetoes: `[]`
- passed_seed_count: `3` / `3`
- next_justified_action: draft and review Phase 6 closeout subplan

## Aggregate Summary

- acceptance rates: `[0.9375, 0.9375, 0.75]`
- max abs u by seed: `[4.324986106081894, 5.454314651674424, 6.235419774840722]`
- target log-prob overall range: `-42.315244462183216` to `-37.84929182395562`
- log-accept max abs by seed: `[1.8844156046382514, 77.7561559421061, 178.0000990804594]`
- native divergence statuses: `['not_exposed_by_kernel', 'not_exposed_by_kernel', 'not_exposed_by_kernel']`
- interpretation: descriptive only; no ranking, convergence, posterior correctness, or default-readiness claim

## Seed Rows

| seed index | seed | status | vetoes | acceptance | finite samples | max abs u |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [20260708, 5501] | passed_short_smoke | none | 0.9375 | 16 | 4.324986106081894 |
| 1 | [20260708, 5502] | passed_short_smoke | none | 0.9375 | 16 | 5.454314651674424 |
| 2 | [20260708, 5503] | passed_short_smoke | none | 0.75 | 16 | 6.235419774840722 |

## Inference Status

| field | value |
| --- | --- |
| hard_veto_screen | passed |
| statistically_supported_ranking | none; no method comparison and no uncertainty interval |
| descriptive_only_differences | per-seed acceptance, target-log-prob range, log-accept range, sample range, and runtime |
| default_readiness | not assessed |
| hmc_readiness | not assessed; replicated finite-telemetry diagnostic only |
| next_evidence_needed | Phase 6 closeout may summarize boundaries; longer validation requires new reviewed plan |

## Nonclaims

- replicated finite-telemetry diagnostic only
- not HMC readiness evidence
- not HMC convergence evidence
- not posterior correctness evidence
- not a tuned kernel claim
- not a zero-divergence claim
- not sampler superiority evidence
- not statistically supported ranking evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not Zhao-Cui source-faithfulness evidence
