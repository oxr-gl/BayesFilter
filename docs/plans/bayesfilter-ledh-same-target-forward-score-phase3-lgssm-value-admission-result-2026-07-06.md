# Phase 3 Row Result: LGSSM Forward Value Admission

metadata_date: 2026-07-06
status: VALUE_ADMITTED_FROM_EXISTING_GPU_EVIDENCE_PLUS_CURRENT_CONTRACT_SMOKE
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 3
row_id: benchmark_lgssm_exact_oracle_m3_T50

## Question

Does the LGSSM row have an admitted same-target LEDH observed-data likelihood
estimator before score work?

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Target scalar | LGSSM observed-data log likelihood estimator. |
| Comparator | Exact Kalman log likelihood on the same observations/model. |
| Existing production evidence | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.json` |
| Current metadata smoke | `docs/plans/ledh-phase3-lgssm-forward-contract-tiny-2026-07-06.json` |
| Primary status | Admitted for value only. |
| Score status | Not changed by this result. Score evidence belongs to later score phases and existing separate score artifacts. |

## Existing N=10000 GPU/XLA Evidence

The July 3 artifact records:

- `primary_pass_same_target_value_execution = true`
- `runtime_gate_applicable = true`
- `finite_output = true`
- `target_identity.full_leaderboard_row = true`
- `target_identity.exact_value_comparator = tf_kalman_log_likelihood on same observations/model`
- exact average log likelihood `-2.721519497158494`
- LEDH average log likelihood mean `-2.719201477050781`
- average absolute delta `0.0023180201077130924`
- average relative error `0.0008517374614193686`

This artifact predates the Phase 2 `forward_contract` field, so it is treated
as existing value evidence normalized through the Phase 2 contract.

## Current Contract Smoke

The tiny CPU-hidden diagnostic run:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python \
  docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py \
  --device-scope cpu --device /CPU:0 --expect-device-kind cpu \
  --batch-seeds 81120 --num-particles 4 --time-steps 2 \
  --sinkhorn-iterations 2 --sinkhorn-epsilon 0.5 \
  --row-chunk-size 4 --col-chunk-size 4 --particle-chunk-size 4 \
  --history-mode value-only --warmups 0 --repeats 1 \
  --dtype float64 --tf32-mode disabled \
  --output docs/plans/ledh-phase3-lgssm-forward-contract-tiny-2026-07-06.json \
  --markdown-output docs/plans/ledh-phase3-lgssm-forward-contract-tiny-2026-07-06.md
```

Result: passed as a prefix diagnostic and emitted:

- `target_scalar = observed_data_log_likelihood_estimator`
- `output_tensor_field = log_likelihood`
- target density fields `transition_log_density`, `observation_log_density`
- proposal/flow fields `pre_flow_log_density`, `forward_log_det`,
  `proposal_observation_surface`
- correction formula
  `transition_log_density + observation_log_density - pre_flow_log_density + forward_log_det`

This tiny CPU-hidden run is not production GPU evidence and is not a full-row
value admission by itself.

## Local Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

Result: `10 passed, 2 warnings`.

## Decision

LGSSM is admitted for Phase 3 value. It may appear in the Phase 4 admitted-row
list as already value-admitted. This result does not create any new score
admission and does not claim exact Kalman score, HMC readiness, posterior
correctness, scientific superiority, or fair runtime ranking.
