# Phase 4 Result: Target-Signature Bridge

Date: 2026-07-04

Status: `PHASE4_BLOCKED_NO_BRIDGEABLE_TARGET_SIGNATURE`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can any historical dense-IAF embedded-payload candidate be assigned a canonical generic `SSMTargetContract` target signature without unsafe assumptions? |
| Baseline/comparator | Phase 1 taxonomy JSON, exact Phase 2 schema artifact, and Phase 3 synthetic-loader nonclaims. |
| Primary criterion | Passed fail-closed classification, but no bridgeable candidate was found. Every embedded-payload candidate was classified with a fixed reject-only status. |
| Veto diagnostics | Continuation veto fired for Phase 5: no stable target-signature bridge can be defined for any historical embedded-payload candidate without inventing missing fields. |
| Explanatory diagnostics | Candidate path, observed legacy problem labels, observed dense-IAF transport kinds, and missing generic contract fields. |
| Not concluded | No payload export success, real-artifact loading, HMC convergence, posterior correctness, sampler ranking, GPU readiness, or default policy change. |
| Result artifact | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json` and this result. |

## Decision

Phase 4 blocks Phase 5 payload export/restoration. The historical embedded
dense-IAF payload candidates contain useful transport tensors, but they do not
carry enough metadata to construct a canonical generic `SSMTargetContract`
signature without inventing fields.

This is not evidence against NeuTra or against the historical HMC runs. It is a
generic BayesFilter reuse blocker: the stated target requires exact
`SSMTargetContract` identity, and the artifacts only expose legacy names or
partial transport metadata.

## Bridge Inventory Summary

| Bridge status | Count | Meaning |
| --- | ---: | --- |
| `missing_static_shape` | 8 | Embedded dense-IAF payload exists, but the artifact lacks complete generic static shape, data signature, prior, and filter-program metadata. |
| `not_embedded_payload_candidate` | 39 | Outside Phase 4 bridge population; summary/provenance/diagnostic/missing-payload artifact. |

Embedded-payload candidates classified: 8.

Bridgeable candidates: 0.

## Representative Missing Fields

All eight embedded-payload candidates were blocked by:

- missing canonical static shape;
- missing canonical data signature;
- missing prior manifest and support/log-density authority;
- missing filter-program manifest and deterministic target policy;
- only legacy problem labels such as `nk` or `rotemberg` available;
- chart evidence limited to payload dimension, not full parameter names and
  transform manifest.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `99263ff22d11128a61c35668c7b530d870f91397` |
| Worktree state | Dirty; Phase 0-4 artifacts and loader implementation are uncommitted. |
| Command | `python docs/plans/bayesfilter_general_neutra_dense_iaf_phase4_bridge.py --output docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json` |
| Environment | Current BayesFilter shell, Python standard library only. |
| CPU/GPU status | CPU-only/read-only bridge classification. No GPU/CUDA device was probed or used. |
| Network status | No network fetch. |
| External mutation | None. `/home/chakwong/python` was not modified. |
| Output | 47 total candidates, 8 embedded-payload candidates, 0 bridgeable signatures. |

## Checks

Commands:

```text
python docs/plans/bayesfilter_general_neutra_dense_iaf_phase4_bridge.py --output docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json
python -m json.tool docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json
git diff --check -- docs/plans/bayesfilter_general_neutra_dense_iaf_phase4_bridge.py docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md
```

Result:

- Passed.

## Plain-Language Classification

| Statement | Classification | Support |
| --- | --- | --- |
| Synthetic dense-IAF loader implementation remains usable for schema-valid synthetic fixtures. | `correct` | Phase 3 focused tests passed. |
| Any historical embedded dense-IAF artifact currently has a canonical generic target signature. | `wrong relative to the stated target` | Phase 4 found 0 bridgeable candidates and 8 missing-static-shape reject-only candidates. |
| Legacy problem labels are enough to bind generic BayesFilter targets. | `wrong relative to the stated target` | Phase 2/4 require a canonical `SSMTargetContract`, not legacy names. |
| HMC/posterior validity follows from this bridge inventory. | `unsupported` | No HMC or posterior validation was run. |

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed fail-closed classification. |
| Veto diagnostic status | Continuation veto fired for Phase 5 payload export: no bridgeable target signature. |
| Main uncertainty | Whether a later human-guided/model-specific target-contract reconstruction can provide reviewed static shape, data signature, chart, prior, and filter-program manifests. |
| Next justified action | Stop this master program before Phase 5, or open a new model-specific target-contract reconstruction program with explicit approval. |
| What is not concluded | No real-artifact loader success, HMC convergence, posterior correctness, sampler superiority, GPU readiness, or default readiness. |

`PHASE4_BLOCKED_NO_BRIDGEABLE_TARGET_SIGNATURE`
