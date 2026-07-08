# Scalar SSL-LSTM Filtering HMC Mechanics Canary - 2026-07-08

## Decision

- mechanics_canary_passed: `True`
- vetoes: `[]`
- passed_candidate_count: `3` / `3`
- next_justified_action: draft and review Phase 4 short HMC smoke subplan

## Coordinate And Mass Convention

- Phase 1 target coordinate: `theta = center + scale * z`.
- TFP HMC coordinate: `u`.
- Phase 2 mass use: `z = u @ chol(M_z).T`.
- Stock TFP HMC dense mass handling: represented through the affine transform, not a direct dense-mass API.

## Candidate Rows

| candidate | L | step size | L*epsilon | status | vetoes | acceptance | max_abs_u |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0.1 | 0.1 | passed_mechanics_canary | none | 1.0 | 0.07699729249971801 |
| 1 | 2 | 0.25 | 0.5 | passed_mechanics_canary | none | 1.0 | 1.1771417860859845 |
| 2 | 4 | 0.3925 | 1.57 | passed_mechanics_canary | none | 1.0 | 2.704452978845203 |

## Inference Status

| field | value |
| --- | --- |
| hard_veto_screen | passed |
| statistically_supported_ranking | none; fixed tiny mechanics grid |
| descriptive_only_differences | acceptance, log accept ratio, target log-prob range, trajectory length, and runtime |
| default_readiness | not assessed |
| hmc_readiness | not assessed; mechanics canary only |
| next_evidence_needed | reviewed Phase 4 short HMC smoke only if Phase 3 passes |

## Nonclaims

- HMC mechanics canary only
- not HMC readiness evidence
- not HMC convergence evidence
- not posterior correctness evidence
- not a tuned step-size claim
- not a zero-divergence claim
- not sampler superiority evidence
- not statistical ranking evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not Zhao-Cui source-faithfulness evidence
