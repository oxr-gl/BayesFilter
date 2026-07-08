# Phase 2 Result: Dense-IAF Frozen Transport Schema

Date: 2026-07-04

Status: `PHASE2_GATE_PASSED_WITH_TARGET_BRIDGE_REMAINING`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What stable dense-IAF frozen transport schema should BayesFilter implement before loading historical NeuTra artifacts? |
| Baseline/comparator | Phase 1 taxonomy JSON for observed evidence; legacy `DenseAutoregressiveIAFTransport` for semantic inference only; target-signature bridge remains unresolved. |
| Primary criterion | Passed: schema artifact covers required fields, observed component types, topology/tensor hashes, canonical target-signature rules, mapping/rejection table, logdet semantics, and nonclaims. |
| Veto diagnostics | No Phase 2 veto fired. The schema preserves reject-only handling for historical artifacts lacking canonical generic target signatures. |
| Explanatory diagnostics | Component taxonomy, observed transport kinds, topology fields, tensor payload fields, and legacy helper semantics. |
| Not concluded | No loader implementation, migrated payload, HMC convergence, posterior correctness, sampler ranking, or default readiness. |
| Result artifact | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md` and this result. |

## Decision

The schema is ready for synthetic loader implementation. It is not a real
artifact migration by itself. The correct next step is to implement and test a
TensorFlow/TFP loader against synthetic dense-IAF payloads that satisfy this
schema, while keeping historical artifacts reject-only until Phase 4 supplies
a canonical target-signature bridge.

## Checks

Commands:

```text
test -f docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json
rg -n "schema id|target_signature|SSMTargetContract|topology_hash|tensor_hash|dimension|component|dense_autoregressive_iaf|log_jacobian_available|log_abs_det_jacobian|sha256|process-local|mapping/rejection|reject-only|nonclaims" docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md
git diff --check -- docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-result-2026-07-04.md docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-subplan-2026-07-04.md
```

Result:

- Passed.

## Plain-Language Classification

| Statement | Classification | Support |
| --- | --- | --- |
| The schema defines canonical target-signature semantics. | `correct` | It requires `stable_ssm_target_signature(SSMTargetContract(..., frozen_transport=None))`. |
| The schema admits legacy target names as signatures. | `wrong relative to the stated target` | The schema explicitly rejects legacy names, class paths, runtime identities, and process-local ids. |
| Historical embedded dense-IAF tensors are representable by schema topology. | `correct` | The schema covers `composed`, `mixing_linear`, `affine`, `affine_dense`, and `dense_autoregressive_iaf`. |
| Historical artifacts are now loadable. | `unsupported` | Loader implementation and target-signature bridge have not run. |

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed. |
| Veto diagnostic status | No unsafe artifact reuse; target bridge remains required. |
| Main uncertainty | Whether Phase 4 can reconstruct canonical generic target contracts for any historical evidence cell. |
| Next justified action | Phase 3 TensorFlow/TFP loader implementation on synthetic schema-valid fixtures only. |
| What is not concluded | No migrated real artifact, no HMC convergence, no posterior correctness, no sampler superiority, no default readiness. |

## Phase 3 Handoff

Phase 3 may implement:

- a TensorFlow/TFP dense-IAF frozen transport class;
- schema-valid synthetic loader tests;
- rejection tests for missing target signature, hash mismatch, process-local
  identity, shape mismatch, nonfinite tensors, and summary-only artifacts.

Phase 3 must not:

- load historical artifacts as reusable;
- run HMC, training, GPU jobs, or network fetches;
- claim posterior validity or HMC readiness.

`PHASE2_GATE_PASSED_WITH_TARGET_BRIDGE_REMAINING`
