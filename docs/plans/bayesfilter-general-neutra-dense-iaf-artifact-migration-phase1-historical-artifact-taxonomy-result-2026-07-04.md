# Phase 1 Result: Historical Artifact Taxonomy

Date: 2026-07-04

Status: `PHASE1_GATE_PASSED_WITH_TARGET_SIGNATURE_BLOCKER`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Which historical dense-IAF artifacts and source surfaces are candidates for a BayesFilter dense-IAF migration bridge, and what blocks each candidate? |
| Baseline/comparator | Prior inventory `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json`, prior stop handoff, and legacy dense-IAF source/replay surfaces under `/home/chakwong/python`. |
| Primary criterion | Passed: every discovered in-scope candidate was classified fail-closed. |
| Veto diagnostics | No unsafe reuse occurred. The material blocker is missing generic `SSMTargetContract` target signatures for embedded dense-IAF payload candidates. |
| Explanatory diagnostics | Candidate paths, sizes, SHA-256 hashes, transport kinds, arms, referenced payload paths, and legacy source surface markers. |
| Not concluded | No loader compatibility, migrated payload success, HMC convergence, posterior correctness, sampler ranking, or default readiness. |
| Result artifacts | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json` and this result. |

## Decision

The historical dense-IAF artifacts contain real migration material, including
embedded legacy transport payloads with `dense_autoregressive_iaf`,
`mixing_linear`, `affine_dense`, and `composed` transport states. The correct
classification for those payloads is not `reusable`; it is
`missing_target_signature`, because they do not carry a generic BayesFilter
`SSMTargetContract` target signature.

The next phase should define a BayesFilter-owned dense-IAF frozen transport
schema. That schema should support the observed legacy payload shape while
requiring stable target signatures, topology/tensor hashes, log-Jacobian
semantics, and process-local identity rejection before any artifact can be
loaded.

## Inventory Summary

| Classification | Count | Meaning |
| --- | ---: | --- |
| `missing_payload` | 28 | Summary/latest/result records or prior-inventory rows that reference payloads elsewhere or lack an embedded frozen transport payload. |
| `missing_target_signature` | 10 | Embedded dense-IAF transport payload or prior dense-IAF evidence exists, but generic `SSMTargetContract` signature is absent. |
| `not_migration_candidate` | 9 | Diagnostic statistics, candidate freeze files, tuning summaries, or provenance-only records, not frozen transport payloads. |

Total candidates classified: 47.

Legacy source/result surfaces found for provenance and schema design: 335.

## Representative Candidate Classes

| Class | Representative evidence | Status |
| --- | --- | --- |
| Embedded dense-IAF replay/training payload | `paper_dense_iaf_seed42_mechanics_canary_replay_state.json`, `paper_dense_iaf_seed42_training_timing_canary.training_state.json`, `rotemberg_trainable_canary.json.training_state.json` | `missing_target_signature` |
| Prior intended serious cells | NK candidate 45, NK UKF candidate 44, Rotemberg KF candidate 46, Rotemberg UKF candidate 92, Rotemberg second-solver candidate 603 | Historical evidence preserved; not generic-loader reusable. |
| Summary/latest records | `*.training_latest.json`, `paper_dense_iaf_seed20260702.json`, launch summaries with replay references | `missing_payload` or summary-only. |
| Per-parameter statistics | July 1 Rotemberg UKF / second-solver statistics JSONs | `not_migration_candidate`. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `99263ff22d11128a61c35668c7b530d870f91397` |
| Worktree state | Dirty; Phase 0/1 artifacts are untracked, unrelated dirty files are preserved. |
| Command | `python docs/plans/bayesfilter_general_neutra_dense_iaf_phase1_inventory.py --output docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json` |
| Environment | Current BayesFilter shell, Python standard library only. |
| CPU/GPU status | CPU-only/read-only taxonomy. No GPU/CUDA device was probed or used. |
| Network status | No network fetch. |
| External mutation | None. `/home/chakwong/python` was read-only. |
| Output artifact | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json` |

## Checks

Commands:

```text
python docs/plans/bayesfilter_general_neutra_dense_iaf_phase1_inventory.py --output docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json
python -m json.tool docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json
git diff --check -- docs/plans/bayesfilter_general_neutra_dense_iaf_phase1_inventory.py docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json
```

Result:

- Passed.

## Plain-Language Classification

| Claim target | Classification | Support |
| --- | --- | --- |
| Historical dense-IAF payload candidates exist | `correct` | Phase 1 JSON records embedded legacy transport payloads with dense-IAF transport kinds. |
| Those candidates are generic BayesFilter reusable artifacts | `wrong relative to the stated target` | They lack a generic `SSMTargetContract` target signature and BayesFilter dense-IAF schema. |
| Historical successful HMC runs prove posterior correctness in this repo | `unsupported` | Phase 1 did not run HMC or validate posterior correctness. |
| Phase 2 should define a dense-IAF schema before loader implementation | `correct` | The observed payload candidates need a schema with target-signature and logdet semantics before loading. |

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed. |
| Veto diagnostic status | No unsafe reuse; target-signature blocker preserved. |
| Main uncertainty | Whether legacy target identities can be bridged to stable generic `SSMTargetContract` signatures without model-specific reconstruction work. |
| Next justified action | Phase 2 dense-IAF frozen schema design. |
| What is not concluded | No real-artifact loader success, no HMC convergence, no posterior correctness, no sampler superiority, no default readiness. |

## Phase 2 Handoff

Phase 2 should define a schema with:

- explicit schema id and version;
- target signature and parameter dimension;
- ordered transport components for composed, mixing-linear, affine, and dense
  autoregressive IAF layers;
- topology fields: hidden layers, activation, `s_max`, masks/degrees policy,
  layer order, and dtype;
- tensor payload fields for weights/biases/affine/mixing matrices with hashes;
- forward and log-absolute-Jacobian semantics;
- optional inverse diagnostic semantics only, not a correctness claim;
- SHA-256 and process-local identity rejection requirements;
- nonclaims that preserve the migration/HMC/posterior boundary.

`PHASE1_GATE_PASSED_WITH_TARGET_SIGNATURE_BLOCKER`
