# Claude Read-Only Review Bundle: LEDH Forward Scalar Phase 4 Result And Phase 5 Handoff

Date: 2026-07-07

## Role Contract

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex is supervisor and executor. Claude is a read-only reviewer only.

## Review Scope

Review only these fixed paths:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py`
- `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.md`
- `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json`
- `tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-execution-ledger-2026-07-07.md`

Do not review the whole repository.

## Objective

Check whether Phase 4 correctly admits only the predator-prey forward scalar
and whether the Phase 5 actual-SV subplan safely forces the transformed-target
bridge before any full-row actual-SV run.

Target scalar: `observed_data_log_likelihood_estimator`, reported in artifacts
as `log_likelihood`.

## Phase 4 Summary

Phase 4 added a current-route streaming LEDH-PFPF-OT predator-prey value runner:

```text
docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py
```

The runner emits only the forward scalar. It uses:

- row id `zhao_cui_predator_prey_T20`;
- physical theta `[0.6, 114.0, 25.0, 0.3, 0.5, 0.5]`;
- additive-Gaussian RK4 predator-prey transition density;
- direct noisy-state Gaussian observation density;
- streaming LEDH-PFPF-OT value core;
- correction identity
  `transition_log_density + observation_log_density - pre_flow_log_density + forward_log_det`.

The full-row artifact:

- path:
  `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json`;
- status: `n10000_same_target_value_admitted`;
- `N=10000`, `T=20`;
- batch seeds `[81120,81121,81122,81123,81124]`;
- finite `log_likelihood_by_seed`;
- output tensor device `/job:localhost/replica:0/task:0/device:GPU:0`;
- validates with
  `validate_ledh_forward_scalar_artifact(..., require_admitted=True)`.

## Local Check Evidence

Tiny CPU-hidden smoke:

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

Result: passed, finite output, `tiny_executed_not_full_row`.

Trusted GPU full-row:

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

Result: passed, GPU output tensor, finite output, schema validation passed.

Required check set:

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

Focused checks after writing result/subplan:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py -q
```

Result:

```text
2 passed, 2 warnings in 2.71s
```

```text
python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py
```

Result: passed.

```text
git diff --check -- \
  docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py \
  docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-result-2026-07-07.md \
  docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-subplan-2026-07-07.md \
  docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-execution-ledger-2026-07-07.md \
  docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.md
```

Result: passed.

## Phase 5 Handoff Summary

The Phase 5 subplan treats actual-SV as a target-bridge problem before any
full-row run. The declared target is the transformed actual-SV row:
`transformed_actual_sv_log_y_square`.

The subplan forbids admitting:

- KSC surrogate evidence as actual-SV evidence;
- augmented-noise Gaussian-closure scalar as same-target actual-SV evidence;
- raw-likelihood-corrected LEDH output as transformed-row evidence without a
  reviewed bridge written before full-row execution.

## Review Questions

1. Does Phase 4 avoid borrowing LGSSM/SIR evidence and avoid claiming score
   admission, score correctness, exact nonlinear likelihood correctness,
   Zhao-Cui TT/SIRT source-faithfulness, HMC readiness, posterior correctness,
   scientific superiority, or runtime ranking?
2. Is the predator-prey artifact sufficient for the Phase 1 executable
   forward-scalar schema and `require_admitted=True` gate?
3. Does the replay test read the actual Phase 4 artifact from disk and enforce
   row id, target policy, theta, N=10000, target correction, streaming mode,
   GPU output, and nonclaims?
4. Does the Phase 5 actual-SV subplan correctly force the transformed-target
   bridge decision before any full-row actual-SV execution?
5. Are Phase 5 stop and handoff conditions strong enough before generalized-SV
   Phase 6?

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
