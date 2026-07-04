# Phase 2 Subplan: Canonical Contract Manifest Draft

Date: 2026-07-04

Status: `PHASE2_DRAFT_FOR_REVIEW`

## Phase Objective

Draft a canonical BayesFilter `SSMTargetContract` manifest for one Rotemberg
cell using only fields that are actually supported by Phase 1 evidence. This
phase may synthesize a manifest-shaped JSON artifact for local validation, but
it must not load historical payloads, export payload tensors, or claim reuse.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result exists and classifies every required field support status.
- The inventory has separated canary payload presence from serious payload
  presence.
- The inventory has named any unresolved state-dimension or semantic decisions.
- Phase 1 remains read-only and no external file mutation has occurred.
- Baseline artifacts:
  - `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-2026-07-04.json`
  - `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-result-2026-07-04.md`
  - `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-target-signature-bridge-result-2026-07-04.md`

## Required Artifacts

- Phase 2 contract manifest JSON:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json`
- Phase 2 result:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-result-2026-07-04.md`
- Phase 3 subplan draft or refresh:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-subplan-2026-07-04.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, And Reviews

Local checks:

```text
python docs/plans/bayesfilter_rotemberg_target_contract_phase2_manifest.py --output docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json
python -m json.tool docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json
git diff --check -- docs/plans/bayesfilter_rotemberg_target_contract_phase2_manifest.py docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-result-2026-07-04.md
```

Reviews:

- Codex reviews the manifest for invented fields, legacy-name-only identity,
  or process-local identity.
- Claude reviews the Phase 3 subplan as a read-only exact-path review before
  Phase 3 begins.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a canonical Rotemberg manifest be drafted from reviewed evidence without inventing any `SSMTargetContract` field? |
| Baseline/comparator | Phase 1 inventory plus exact local Rotemberg source and result evidence. |
| Primary pass criterion | A manifest is written with every field either supported or explicitly marked as blocked/decision-required, and no unsupported field is presented as canonical. |
| Veto diagnostics | Any invented field, any target signature minted from legacy names alone, any process-local identity, any payload export, or any claim that a missing field is “approximately” supported. |
| Explanatory diagnostics | Source anchors, field-by-field support table, and unresolved decision items. |
| Not concluded | No canonical signature, no payload reuse, no HMC convergence, no posterior correctness, no sampler ranking, and no GPU readiness. |
| Result artifact | Phase 2 manifest JSON and Phase 2 result Markdown. |

## Forbidden Claims And Actions

- Do not mint `stable_ssm_target_signature` unless Phase 1 evidence explicitly
  supports every field.
- Do not load historical artifacts through BayesFilter.
- Do not copy payloads into the repo.
- Do not modify `/home/chakwong/python`.
- Do not train, retune, or run HMC.
- Do not run GPU/CUDA commands.
- Do not infer support from legacy names, class paths, or process-local ids.
- Do not classify missing payloads as present.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Phase 2 manifest JSON exists and validates with `python -m json.tool`;
- every manifest field is classified as supported, blocked, or decision-required
  with evidence;
- no invented field appears in the manifest;
- Phase 2 result states what is `correct`, `wrong relative to the stated
  target`, `unsupported`, and `not checked`;
- Phase 3 subplan exists and is reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- no Phase 2 stop condition fired.

## Stop Conditions

Stop and write a blocker result if:

- the manifest would require inventing any field;
- local evidence cannot support a canonical signature without unresolved
  decisions that should be externalized to a human;
- `/home/chakwong/python` is inaccessible;
- the inventory cannot support a field-by-field manifest draft;
- any classification would require executing legacy model code, network fetch,
  GPU execution, HMC, training, or modifying external files;
- Claude review for the Phase 3 subplan cannot be obtained after the
  probe/narrowing protocol;
- Claude and Codex do not converge after five review rounds for the Phase 3
  subplan.

`PHASE2_DRAFT_FOR_REVIEW`
