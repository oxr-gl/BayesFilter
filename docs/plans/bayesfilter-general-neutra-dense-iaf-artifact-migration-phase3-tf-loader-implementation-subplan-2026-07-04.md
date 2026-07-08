# Phase 3 Subplan: TensorFlow/TFP Dense-IAF Loader Implementation

Date: 2026-07-04

Status: `PHASE3_DRAFT_FOR_REVIEW`

## Phase Objective

Implement the BayesFilter-owned TensorFlow/TFP dense-IAF frozen transport loader
for synthetic schema-valid fixtures, with fail-closed validation for target
signature, topology hash, tensor hash, transport hash, shapes, finite tensors,
component semantics, and process-local identity.

Phase 3 target-signature checks are synthetic only: they verify exact equality
against a canonical synthetic `SSMTargetContract` signature constructed with
`frozen_transport=None`. They do not bridge or validate any historical target
identity.

## Entry Conditions Inherited From Previous Phase

- Phase 2 result exists with status
  `PHASE2_GATE_PASSED_WITH_TARGET_BRIDGE_REMAINING`.
- Phase 2 schema artifact exists and defines
  `bayesfilter.neutra.dense_iaf_frozen_transport.v1`.
- Historical artifacts remain reject-only until Phase 4 target bridge.
- Implementation defaults to TensorFlow/TFP for differentiable code.

## Required Artifacts

- Implementation updates in `bayesfilter/inference/neutra_artifacts.py` or a
  focused sibling module imported from `bayesfilter.inference`.
- Export updates in `bayesfilter/inference/__init__.py` if public symbols are
  added.
- Focused tests:
  `tests/test_dense_iaf_neutra_artifact_loader.py`.
- Phase 3 result:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-result-2026-07-04.md`.
- Phase 4 target-signature bridge subplan:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md`.

## Required Checks, Tests, And Reviews

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_dense_iaf_neutra_artifact_loader.py tests/test_neutra_artifact_loader.py -q -p no:cacheprovider
git diff --check -- bayesfilter/inference/neutra_artifacts.py bayesfilter/inference/__init__.py tests/test_dense_iaf_neutra_artifact_loader.py docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-result-2026-07-04.md docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md
```

Required focused tests:

- accepts a schema-valid synthetic composed dense-IAF payload and exposes stable
  manifest fields;
- computes batch forward values and `log_abs_det_jacobian` for a tiny
  deterministic dense-IAF fixture;
- checks synthetic `target_signature` equality against an expected canonical
  signature and rejects mismatch;
- rejects missing or individually tampered `topology_hash`, `tensor_hash`, and
  `transport_hash`;
- rejects nonfinite tensor payloads;
- rejects shape mismatches in dense-IAF weights/biases, mixing matrices, and
  affine components;
- rejects process-local identity in ids, hashes, or manifest text;
- rejects unsupported component kind and summary/latest/historical artifacts
  that lack schema-valid transport payloads;
- rejects a historical-style payload that is otherwise schema-shaped/hash-shaped
  but uses a legacy target name, class path, or noncanonical target identity
  instead of the expected synthetic canonical `SSMTargetContract` signature;
- verifies existing affine-diagonal loader behavior still passes.

Reviews:

- Codex reviews implementation against Phase 2 schema before result close.
- Claude reviews Phase 4 target-signature bridge subplan before Phase 4 begins.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter load and evaluate schema-valid synthetic dense-IAF frozen transports fail-closed? |
| Baseline/comparator | Phase 2 schema and existing affine-diagonal loader behavior in `bayesfilter/inference/neutra_artifacts.py`. |
| Primary pass criterion | Focused synthetic tests pass for forward, batch forward, logdet, stable manifest hashes, synthetic canonical target-signature match, individual topology/tensor/transport hash rejection, nonfinite tensor rejection, process-local identity rejection, shape rejection, unsupported component rejection, historical summary reject-only behavior, historical-style noncanonical target identity rejection, and existing affine-loader regression coverage. |
| Veto diagnostics | Any historical artifact loaded as reusable, NumPy used in differentiable implementation path, missing hash check, missing target-signature check, process-local identity accepted, shape mismatch accepted, nonfinite tensor accepted, or existing affine loader regression. |
| Explanatory diagnostics | Synthetic topology, tensor shapes, logdet values, hash values, and rejection messages. |
| Not concluded | Real-artifact migration, target bridge success, HMC convergence, posterior correctness, sampler ranking, GPU readiness, or default policy change. |
| Result artifact | Phase 3 result Markdown and focused test output. |

## Forbidden Claims And Actions

- Do not load historical artifacts as reusable.
- Do not copy large artifacts from `/home/chakwong/python`.
- Do not run training, HMC, GPU/CUDA commands, or network fetches.
- Do not use NumPy in BayesFilter-owned differentiable implementation paths.
- Do not change default HMC or production policy.
- Do not claim target-bridge success.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- synthetic dense-IAF loader tests pass;
- existing affine-diagonal loader tests still pass;
- implementation exposes stable manifest signatures and rejection errors;
- Phase 3 result states CPU-only test choice with `CUDA_VISIBLE_DEVICES=-1`;
- Phase 4 target-signature bridge subplan exists and is reviewed;
- no historical artifact was loaded as reusable.
- Phase 3 result includes a run manifest, decision table, CPU-only
  `CUDA_VISIBLE_DEVICES=-1` statement, command output summary, dirty-worktree
  note, and what is `correct`, `unsupported`, and `not checked`.

## Stop Conditions

Stop and write a blocker result if:

- tests cannot run locally;
- implementation requires NumPy, JAX, or PyTorch in differentiable paths;
- schema hash checks cannot be implemented without ambiguity;
- loader parity requires executing legacy model code;
- any historical artifact is accidentally loaded as reusable;
- required test coverage cannot be expressed without weakening the Phase 2
  schema;
- Codex review finds an implementation/schema mismatch that cannot be repaired
  locally;
- continuing would require network, GPU, HMC, training, large copy, package
  installation, or modifying `/home/chakwong/python`;
- Claude review for the Phase 4 subplan cannot be obtained after the
  probe/narrowing protocol. The protocol is: run a tiny Claude health probe,
  then retry with a smaller exact-path prompt; if that still fails, write a
  blocker result instead of advancing;
- Claude and Codex do not converge after five review rounds for the Phase 4
  subplan.

## Skeptical Plan Audit

Phase 3 is an implementation and synthetic-fixture gate. Passing it proves only
that schema-valid synthetic dense-IAF payloads can be loaded and evaluated. It
does not prove any historical artifact has a valid target signature, and it
does not establish HMC or posterior validity.

`PHASE3_DRAFT_FOR_REVIEW`
