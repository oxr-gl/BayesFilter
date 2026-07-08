# Phase 4 Result: Bridge Rerun and Payload Boundary Decision

Date: 2026-07-04

Status: `PHASE4_BLOCKED_NO_BRIDGEABLE_TARGET_SIGNATURE`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can any historical Rotemberg embedded dense-IAF candidate be assigned a canonical generic `SSMTargetContract` target signature without unsafe assumptions? |
| Baseline/comparator | Phase 1 inventory JSON/result, Phase 2 manifest JSON/result, and Phase 3 local validation result. |
| Primary criterion | Passed fail-closed classification. Exactly two embedded payload candidates were classified, and both were reject-only with the same exact missing fields. |
| Veto diagnostics | Continuation veto fired for Phase 5: no stable target-signature bridge can be defined for any historical embedded payload candidate without inventing missing fields. |
| Explanatory diagnostics | Candidate path, observed legacy problem labels, observed dense-IAF transport kinds, and missing generic contract fields. |
| Not concluded | No payload export success, real-artifact loading, HMC convergence, posterior correctness, sampler ranking, GPU readiness, or default policy change. |
| Result artifact | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json` and this result. |

## Decision

The bridge rerun did not produce any bridgeable Rotemberg candidate. Both
embedded payload candidates remain blocked by the same four missing generic
fields:

- `static_shape`
- `data_signature`
- `prior`
- `filter_program`

That is the end of the evidence inside this repo. There is no safe canonical
`SSMTargetContract` signature to mint from the available metadata without
inventing fields.

This is not evidence against the historical NeuTra runs. It is a generic
BayesFilter reuse blocker.

## Bridge Inventory Summary

| Bridge status | Count | Meaning |
| --- | ---: | --- |
| `missing_static_shape` | 2 | Embedded dense-IAF payload exists, but the artifact lacks complete generic static shape, data signature, prior, and filter-program metadata. |

Embedded-payload candidates classified: 2.

Bridgeable candidates: 0.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `99263ff22d11128a61c35668c7b530d870f91397` |
| Worktree state | Dirty; unrelated user changes preserved. |
| Command | `python docs/plans/bayesfilter_rotemberg_target_contract_phase4_bridge.py --input docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-2026-07-04.json --manifest docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json --output docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json` |
| Validation | `python -m json.tool docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json` |
| CPU/GPU status | CPU-only/read-only bridge classification. No GPU/CUDA device was probed or used. |
| Network status | No network fetch. |
| External mutation | None. `/home/chakwong/python` was not modified. |
| Output | `bridgeable_count=0`, `candidate_status_counts={"missing_static_shape": 2}` |

## Checks

Commands:

```text
python docs/plans/bayesfilter_rotemberg_target_contract_phase4_bridge.py --input docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-2026-07-04.json --manifest docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json --output docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json
python -m json.tool docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json
git diff --check -- docs/plans/bayesfilter_rotemberg_target_contract_phase4_bridge.py docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-result-2026-07-04.md docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-subplan-2026-07-04.md
```

Result:

- Passed.

## Plain-Language Classification

| Statement | Classification | Support |
| --- | --- | --- |
| Both embedded Rotemberg candidates remain reject-only. | `correct` | Bridge rerun output. |
| A canonical generic target signature can be minted from the available evidence. | `wrong relative to the stated target` | Both candidates are missing the same four generic fields. |
| Legacy names are enough to bridge the candidates. | `wrong relative to the stated target` | Bridge classification recorded exact missing fields instead. |
| HMC/posterior validity follows from this bridge result. | `unsupported` | No HMC or posterior validation was run. |

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed fail-closed classification. |
| Veto diagnostic status | Continuation veto fired for Phase 5. |
| Main uncertainty | None inside the current repo evidence set; the missing fields are the blocker. |
| Next justified action | Stop the program and write the closeout handoff. |
| What is not concluded | No real-artifact loader success, no payload export, no HMC/posterior claim. |

`PHASE4_BLOCKED_NO_BRIDGEABLE_TARGET_SIGNATURE`
