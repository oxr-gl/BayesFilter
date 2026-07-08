# Phase 4 Result: Predator-Prey Forward Scalar Admission

metadata_date: 2026-07-07
status: `PASSED_PREDATOR_PREY_FORWARD_SCALAR_LOCAL_PENDING_REVIEW`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 4

## Phase Objective

Build or locate an executable same-target observed-data LEDH forward scalar
artifact for the additive-Gaussian predator-prey row.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions

- Phase 1 schema guard passed after theta-equality repair.
- Phase 2 LGSSM canonical artifact validated locally.
- Phase 3 fixed SIR canonical artifact validated locally under
  `sir_log_scale_theta`.
- Phase 3/4 handoff review passed.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong baseline | Phase 4 did not reuse LGSSM or SIR evidence. It started from predator-prey row callbacks, model code, and the Phase 4 contract. |
| Proxy metric promoted | Runtime, memory, GPU output, and finite output were explanatory until the canonical artifact passed `validate_ledh_forward_scalar_artifact(..., require_admitted=True)`. |
| Missing stop conditions | Missing runner, missing likelihood vector, wrong theta, absent target correction, failed validation, and score creep were stop conditions. |
| Hidden assumptions | The runner freezes row id, theta, dataset seed, horizon, particle count, seed list, target observation policy, and streaming transport policy before execution. |
| Artifact mismatch | Produced a canonical Phase 1 schema artifact and mandatory replay test, not a leaderboard rebuild or score artifact. |

Audit status: passed.

## Implementation

Added a row-specific current-route runner:

```text
docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py
```

The runner uses:

- `bayesfilter.highdim.p30_predator_prey_fixture_model()`;
- dataset seed `81104`;
- theta coordinate `physical`;
- theta `(r,K,a,s,u,v) = (0.6,114.0,25.0,0.3,0.5,0.5)`;
- horizon `T=20`;
- batch seeds `[81120,81121,81122,81123,81124]`;
- particle count `N=10000`;
- streaming LEDH-PFPF-OT value core;
- target transition density from the additive-Gaussian RK4 transition;
- target observation density from the direct noisy-state Gaussian observation;
- correction identity
  `transition_log_density + observation_log_density - pre_flow_log_density + forward_log_det`.

The runner is forward-scalar-only. It does not implement scores.

## Canonical Artifact

Wrote canonical Phase 1 schema artifacts:

- `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json`
- `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.md`

The canonical artifact records:

- `row_id = zhao_cui_predator_prey_T20`;
- `theta_coordinate_system = physical`;
- `theta_values = [0.6, 114.0, 25.0, 0.3, 0.5, 0.5]`;
- `flow_observation_policy = predator_prey_identity_state_gaussian_flow_observation`;
- `target_observation_policy = additive_gaussian_predator_prey`;
- `target_density_used_for_correction = true`;
- `admission_status = n10000_same_target_value_admitted`;
- `log_likelihood_by_seed =
  [-169.6912841796875, -169.636962890625, -169.46498107910156,
  -171.49961853027344, -169.044677734375]`;
- `average_log_likelihood_by_seed =
  [-8.484564208984375, -8.48184814453125, -8.473249053955078,
  -8.574980926513671, -8.45223388671875]`.

Validation:

```text
validate_ledh_forward_scalar_artifact(
    artifact,
    expected_row_id="zhao_cui_predator_prey_T20",
    require_admitted=True,
)
```

passed during artifact generation and during the mandatory replay test.

## Execution Evidence

Tiny CPU-hidden smoke command:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python \
  docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py \
  --device-scope cpu --device /CPU:0 --expect-device-kind cpu \
  --batch-seeds 81120 --time-steps 2 --num-particles 16 \
  --transport-policy active-all --sinkhorn-iterations 2 \
  --sinkhorn-epsilon 1.0 --row-chunk-size 16 --col-chunk-size 16 \
  --particle-chunk-size 16 --history-mode value-only --warmups 0 \
  --repeats 1 --output /tmp/ledh-predator-prey-tiny.json
```

Result:

- passed;
- emitted `admission_status = tiny_executed_not_full_row`;
- finite likelihood;
- CPU output as requested.

Trusted GPU full-row command:

```text
MPLCONFIGDIR=/tmp python \
  docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py \
  --device-scope visible --device /GPU:0 --expect-device-kind gpu \
  --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 \
  --num-particles 10000 --transport-policy active-all \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --history-mode value-only --warmups 0 --repeats 1 \
  --output docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json \
  --markdown-output docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.md
```

Result:

- passed;
- XLA compiled on `/device:GPU:0`;
- output tensor device `/job:localhost/replica:0/task:0/device:GPU:0`;
- compile plus first call: `34.134711731923744` seconds;
- warm call: `19.095908388961107` seconds;
- reported TensorFlow GPU peak memory info: `48685312` bytes;
- finite output.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the predator-prey row produce an executable same-target observed-data log likelihood artifact under the shared schema? |
| Baseline/comparator | Predator-prey row contract, P30 model fixture, dataset seed 81104, legacy callback inventory, and the shared Phase 1 validator. |
| Primary criterion | Passed locally: canonical predator-prey artifact validates with `require_admitted=True`, finite `log_likelihood_by_seed`, row id `zhao_cui_predator_prey_T20`, theta coordinate `physical`, theta values `(0.6,114,25,0.3,0.5,0.5)`, full-row scale, and target-density correction. |
| Veto diagnostics | No LGSSM/SIR evidence was borrowed; no metadata-only or callback-only evidence was admitted; no wrong theta; no missing target correction; no score evidence used for value admission; no runtime-only admission. |
| Explanatory diagnostics | Runtime, memory, compile time, XLA/GPU device, and tiny smoke evidence are explanatory only. |
| Not concluded | No score admission, score correctness, exact nonlinear likelihood correctness, Zhao-Cui TT/SIRT source-faithfulness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |

## Local Checks

Mandatory Phase 4 replay check was included in:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py -q
```

Result:

```text
30 passed, 2 warnings in 2.79s
```

## Phase 5 Handoff

Phase 5 actual-SV may begin only after read-only review agrees with this result
and the Phase 5 actual-SV subplan.

Phase 5 must explicitly resolve or block the actual-SV target-bridge issue:
the declared target is the transformed actual-SV row, while existing LEDH
surfaces historically used a log-square flow proposal with a raw-likelihood
correction. A candidate artifact may not be admitted unless the target scalar,
target observation policy, and correction density match the Phase 1 contract or
a reviewed same-target bridge is written before execution.

## Nonclaims

- No score route is implemented or admitted.
- This is not actual-SV, KSC, generalized-SV, LGSSM, or SIR evidence.
- This is not exact nonlinear likelihood correctness evidence.
- This is not Zhao-Cui TT/SIRT source-faithfulness evidence.
- No leaderboard is rebuilt.
- No HMC readiness, posterior correctness, scientific superiority, or runtime
  ranking is claimed.
