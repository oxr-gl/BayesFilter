# Phase 1 Result: Batched Callback And Shape Contract

Date: 2026-06-15

## Status

`PASS_READY_FOR_PHASE_2`

## Phase Objective

Define the experimental batch callback/data contract and minimal deterministic
fixtures for LEDH-PFPF-OT without changing production APIs.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the experimental API express the batched LEDH-PFPF-OT contract without changing semantics or production exports? |
| Baseline/comparator | Phase 0 scalar path inventory and existing experimental batched value+score shape conventions. |
| Primary criterion | `PASS`: shape tests and import smoke passed; deterministic fixed-contract fixture is explicit; no public API/default change was made. |
| Veto diagnostics | No ambiguous callback shape, hidden RNG requirement, missing fixed branch mask, public export drift, missing deterministic noise contract, or missing tolerance policy. |
| Explanatory diagnostics | Static dimensions, fixture ranks, tolerance constants, source-level RNG rejection. |
| Not concluded | No scalar value parity, no full value recursion, no score correctness, no performance claim. |

## Implemented Artifacts

New experimental module:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`

New focused tests:

- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`

Implemented Phase 1 contract surface:

- `BatchedLEDHPFPFOTShapeContract`
- `BatchedLEDHPFPFOTFixedInputs`
- `BatchedLEDHFlowTensors`
- `BatchedLEDHPFPFOTCallbacks`
- `uniform_log_weights`
- `validate_batched_value_tensor`
- `validate_batched_score_tensor`
- `validate_flow_tensors_against_contract`
- `assert_callback_has_no_forbidden_rng`

No `bayesfilter` top-level or package export was added.

## Local Checks

| Check | Status | Notes |
| --- | --- | --- |
| Focused pytest | `PASS` | `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_ledh_pfpf_ot_tf.py`: 6 passed. |
| Source RNG check | `PASS` | AST/source test verifies the module does not call random generators; negative test callback is rejected. |
| Public export check | `PASS` | Test verifies `experimental_batched_ledh_pfpf_ot_tf` is not in `bayesfilter.__all__` or `_EXPORT_MODULES`. |
| `git diff --check` | `PASS` | No whitespace errors in Phase 1 files. |

## Fixed Contract Decisions

- Leading batch axis indexes independent model-parameter rows.
- Observations are shared across rows with shape `[T,O]`.
- Initial particles have shape `[B,N,D]`.
- Fixed pre-flow particles or fixed transition innovations are represented as
  `[B,T,N,D]`.
- Fixed resampling masks have shape `[B,T]`.
- Values must have shape `[B]`.
- Scores must have shape `[B,p]`, but score recursion is not implemented in
  Phase 1.
- Random ops are forbidden inside the value/score core contract.
- Starting scalar parity tolerances remain `atol=1e-10, rtol=1e-10`.
- Starting transport parity tolerances remain `atol=1e-8, rtol=1e-8`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_READY_FOR_PHASE_2` | Shape/import/RNG/export checks passed. | No Phase 1 veto fired. | Phase 2 may find graph-safe LEDH/transport implementation constraints. | Implement batched per-time LEDH flow and masked transport core. | No scalar parity, no score correctness, no GPU/JIT benchmark, no production readiness. |

## Post-Run Red Team

Strongest alternative explanation: a shape-only contract can pass while the
actual batched flow/transport math in Phase 2 still drifts from scalar
semantics.

What would overturn this phase decision: a Phase 2 implementation requires
hidden RNG, runtime branch decisions, public API changes, or shape meanings
incompatible with the fixed-contract fixture.

Weakest evidence link: source RNG rejection is conservative text inspection,
not a proof of callback determinism.

## Next Phase

Phase 2 may begin after the refreshed Phase 2 subplan passes local review.
