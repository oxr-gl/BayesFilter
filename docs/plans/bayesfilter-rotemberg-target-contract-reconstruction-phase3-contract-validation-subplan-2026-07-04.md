# Phase 3 Subplan: Local `SSMTargetContract` Validation

Date: 2026-07-04

Status: `PHASE3_DRAFT_FOR_REVIEW`

## Phase Objective

Instantiate the Phase 2 manifest into a local BayesFilter `SSMTargetContract`
validation path and verify that the stable signature, field hashes, and required
metadata are internally consistent. This phase is metadata-only and does not
load historical payloads or run HMC.

## Entry Conditions Inherited From Previous Phase

- Phase 2 manifest JSON exists and passed JSON validation.
- The manifest contains no invented fields.
- The manifest records any unresolved decisions explicitly.
- Phase 2 remains metadata-only with no historical payload load.
- Baseline artifacts:
  - `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json`
  - `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-result-2026-07-04.md`

## Required Artifacts

- Phase 3 validation result:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-result-2026-07-04.md`
- Phase 4 subplan draft or refresh:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-subplan-2026-07-04.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, And Reviews

Local checks:

```text
python -m py_compile docs/plans/bayesfilter_rotemberg_target_contract_phase2_manifest.py
python -m pytest tests/test_rotemberg_target_contract_reconstruction_phase3.py -q -p no:cacheprovider
git diff --check -- docs/plans/bayesfilter_rotemberg_target_contract_phase2_manifest.py tests/test_rotemberg_target_contract_reconstruction_phase3.py docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-result-2026-07-04.md
```

Reviews:

- Codex reviews the validation result for invented claims or signature drift.
- Claude reviews the Phase 4 subplan as a read-only exact-path review before
  Phase 4 begins.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Phase 2 manifest instantiate into a stable `SSMTargetContract`-style validation artifact without drift or invention? |
| Baseline/comparator | Phase 2 manifest plus the local BayesFilter contract validators. |
| Primary pass criterion | Validation passes for the manifest, field hashes remain stable, and the result records any unresolved metadata decisions instead of hiding them. |
| Veto diagnostics | Signature instability, invented field, mismatch between manifest and validator, process-local identity, or any claim that validation proves payload reuse. |
| Explanatory diagnostics | Signature hash, field-by-field validation status, and unresolved decisions. |
| Not concluded | No real-artifact reuse, no payload export, no HMC convergence, no posterior correctness, and no sampler ranking. |
| Result artifact | Phase 3 validation result Markdown. |

## Forbidden Claims And Actions

- Do not load historical artifacts through the new manifest validation path.
- Do not run HMC, training, or GPU/CUDA commands.
- Do not copy large artifacts.
- Do not change pass/fail criteria after seeing results.
- Do not claim payload reuse from metadata validation alone.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- the validation result exists and passes local checks;
- the manifest signature is stable and process-local-free;
- unresolved decisions are either resolved or explicitly carried forward;
- Phase 4 subplan exists and is reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- no Phase 3 stop condition fired.

## Stop Conditions

Stop and write a blocker result if:

- validation exposes an invented or unstable field;
- the manifest cannot instantiate into a stable local validation artifact;
- local checks fail for a non-fixable reason;
- `/home/chakwong/python` access is required unexpectedly;
- Claude and Codex do not converge after five review rounds for the same
  blocker.

`PHASE3_DRAFT_FOR_REVIEW`
