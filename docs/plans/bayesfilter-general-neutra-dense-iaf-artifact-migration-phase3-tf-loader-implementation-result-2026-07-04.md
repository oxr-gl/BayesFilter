# Phase 3 Result: TensorFlow/TFP Dense-IAF Loader Implementation

Date: 2026-07-04

Status: `PHASE3_GATE_PASSED_SYNTHETIC_ONLY`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can BayesFilter load and evaluate schema-valid synthetic dense-IAF frozen transports fail-closed? |
| Baseline/comparator | Phase 2 schema and existing affine-diagonal loader behavior in `bayesfilter/inference/neutra_artifacts.py`. |
| Primary criterion | Passed: focused synthetic tests pass for forward/logdet, stable manifest hashes, synthetic canonical target-signature equality, individual hash rejection, nonfinite rejection, process-local identity rejection, shape rejection, unsupported component rejection, historical-style noncanonical target rejection, summary-only rejection, and affine-loader regression. |
| Veto diagnostics | No Phase 3 veto fired. No historical artifact was loaded as reusable. |
| Explanatory diagnostics | Synthetic 2D dense-IAF topology, deterministic tensor fixture, expected forward/logdet values, and tamper/rejection cases. |
| Not concluded | No real-artifact migration, target bridge success, HMC convergence, posterior correctness, sampler ranking, GPU readiness, or default policy change. |
| Result artifact | This file plus focused test output. |

## Implementation Summary

Implemented:

- `FrozenDenseIAFTransport`;
- `finalize_dense_iaf_neutra_artifact_payload`;
- loader support for `bayesfilter.neutra.dense_iaf_frozen_transport.v1`;
- topology, tensor, and transport hash validation;
- synthetic canonical target-signature equality validation;
- finite tensor, shape, component-kind, masks-policy, process-local identity,
  and summary-only rejection;
- public exports in `bayesfilter/inference/__init__.py`.

The implementation uses TensorFlow tensors for differentiable transport
operations. NumPy is used only in tests for independent expected values.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `99263ff22d11128a61c35668c7b530d870f91397` |
| Worktree state | Dirty; Phase 0-3 artifacts and loader implementation are uncommitted. Unrelated dirty files were preserved. |
| Command | `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_dense_iaf_neutra_artifact_loader.py tests/test_neutra_artifact_loader.py -q -p no:cacheprovider` |
| Environment | Current BayesFilter shell, TensorFlow import path already available. |
| CPU/GPU status | Deliberate CPU-only check. `CUDA_VISIBLE_DEVICES=-1` was set before TensorFlow import in tests. No GPU readiness claim. |
| Network status | No network fetch. |
| External mutation | None. `/home/chakwong/python` was not modified. |
| Output | `13 passed in 5.65s` |

## Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_dense_iaf_neutra_artifact_loader.py tests/test_neutra_artifact_loader.py -q -p no:cacheprovider
git diff --check -- bayesfilter/inference/neutra_artifacts.py bayesfilter/inference/__init__.py tests/test_dense_iaf_neutra_artifact_loader.py docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
from bayesfilter.inference import FrozenDenseIAFTransport, finalize_dense_iaf_neutra_artifact_payload
print(FrozenDenseIAFTransport.__name__)
print(finalize_dense_iaf_neutra_artifact_payload.__name__)
PY
```

Result:

- Passed.

The import sanity check emitted TensorFlow import diagnostics while devices were
intentionally hidden by `CUDA_VISIBLE_DEVICES=-1`; this is not GPU-readiness
evidence.

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed for synthetic schema-valid payloads. |
| Veto diagnostic status | No veto fired. |
| Main uncertainty | Whether Phase 4 can construct canonical generic target signatures for any historical evidence cell without unsafe legacy assumptions. |
| Next justified action | Phase 4 target-signature bridge design and inventory. |
| What is not concluded | No real-artifact loader success, HMC convergence, posterior correctness, sampler superiority, GPU readiness, or default readiness. |

## Plain-Language Classification

| Statement | Classification | Support |
| --- | --- | --- |
| Schema-valid synthetic dense-IAF payloads can be loaded and evaluated. | `correct` | Focused tests passed under CPU-only execution. |
| Historical dense-IAF artifacts are now reusable. | `wrong relative to the stated target` | Phase 4 target-signature bridge has not run; historical artifacts remain reject-only. |
| The loader proves HMC convergence or posterior correctness. | `unsupported` | No HMC or posterior validation was run. |
| GPU readiness follows from this phase. | `unsupported` | Tests intentionally hid GPUs with `CUDA_VISIBLE_DEVICES=-1`. |

## Phase 4 Handoff

Phase 4 should attempt a read-only target-signature bridge:

- map historical target identities to the exact generic `SSMTargetContract`
  manifest fields needed for canonical signatures;
- classify each candidate as bridgeable or reject-only;
- avoid loading real artifacts until bridge success is established;
- avoid HMC, training, GPU commands, network fetches, and large copies.

`PHASE3_GATE_PASSED_SYNTHETIC_ONLY`
