# Phase 1 Subplan: Metadata-Source Inventory

Date: 2026-07-04

Status: `PHASE1_DRAFT_FOR_REVIEW`

## Phase Objective

Build a read-only, field-by-field inventory of exact evidence for reconstructing
the Rotemberg linear/Kalman generic `SSMTargetContract`. Each required field
must be classified as `supported`, `supported_with_semantic_decision_required`,
`unsupported`, `blocked_by_absent_artifact`, or
`not_applicable_untransported_signature`.

This phase may draft a noncanonical manifest-shaped summary for review, but it
must not mint a canonical `target_signature` or export/load historical dense-IAF
payloads.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists and records `PHASE0_GATE_PASSED`.
- The master program and visible runbook exist.
- Claude read-only review of this subplan returned `VERDICT: AGREE`, or all
  fixable review findings were patched and rereviewed.
- Phase 1 remains read-only with respect to `/home/chakwong/python`.
- No network fetch, GPU command, large copy, NeuTra training, or serious HMC is
  authorized by Phase 1.
- Baseline artifacts:
  - `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json`
  - `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-result-2026-07-04.md`
  - `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-stop-handoff-2026-07-04.md`

## Required Artifacts

- Inventory helper:
  `docs/plans/bayesfilter_rotemberg_target_contract_phase1_inventory.py`
- Phase 1 inventory JSON:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-2026-07-04.json`
- Phase 1 result:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-result-2026-07-04.md`
- Phase 1 blocker result, if a stop condition fires:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-blocker-2026-07-04.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-execution-ledger-2026-07-04.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-claude-review-ledger-2026-07-04.md`
- Phase 2 subplan draft or refresh, success-path only:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-subplan-2026-07-04.md`

## Required Checks, Tests, And Reviews

Read-only local checks:

```text
python docs/plans/bayesfilter_rotemberg_target_contract_phase1_inventory.py --output docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-2026-07-04.json
python -m json.tool docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-2026-07-04.json
python -m py_compile docs/plans/bayesfilter_rotemberg_target_contract_phase1_inventory.py
git diff --check -- docs/plans/bayesfilter_rotemberg_target_contract_phase1_inventory.py docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-2026-07-04.json docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-result-2026-07-04.md
```

Discovery and classification rule:

- The inventory must record the exact discovery commands or scripts and their
  include/exclude rules.
- Every discovered candidate in the declared scope must receive a status. It is
  not sufficient to classify only a selected subset.
- If a discovered artifact is too large for bounded JSON inspection, the
  inventory must still record path, size, hash if feasible, status, and the
  reason payload-level inspection was deferred.
- Uninspected discovered candidates are forbidden unless they are assigned a
  fail-closed status with an explicit reason.

Reviews:

- Codex reviews the inventory for fail-closed classifications before any next
  phase is drafted.
- Claude reviews the Phase 2 schema subplan as a read-only exact-path review.
- If Claude review cannot be obtained after the probe/narrowing protocol, write
  a blocker result instead of advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which historical dense-IAF artifacts and source surfaces are candidates for a BayesFilter dense-IAF migration bridge, and what blocks each candidate? |
| Baseline/comparator | Exact prior inventory `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json`, exact prior stop handoff `docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`, and legacy dense-IAF source surfaces such as `/home/chakwong/python/src/dsge_hmc/estimation/_transports.py` and replay helpers in legacy scripts. |
| Primary pass criterion | Every discovered candidate in the declared Phase 1 scope is classified fail-closed with path, size, SHA-256 when feasible, payload status, target-signature status, schema status, and next required action. |
| Veto diagnostics | Missing payload, missing generic target signature, unsupported or unknown transport kind, process-local identity, nonfinite JSON payload, unreadable source, or classification ambiguity that would make a future loader unsafe. |
| Explanatory diagnostics | Candidate ID, arm, seed, topology, tensor counts, source result status, step size, leapfrog count, R-hat when available, and whether a training or replay state exists. |
| Not concluded | Loader compatibility, migrated payload success, HMC convergence, posterior correctness, sampler ranking, and default readiness. |
| Result artifact | Phase 1 inventory JSON and Phase 1 result Markdown. |

## Forbidden Claims And Actions

- Do not load historical artifacts through BayesFilter yet.
- Do not copy large payloads into the repo.
- Do not modify `/home/chakwong/python`.
- Do not train, retune, or run HMC.
- Do not run GPU/CUDA commands.
- Do not infer generic target-signature compatibility from legacy target names
  alone.
- Do not classify an artifact as reusable unless schema, payload, logdet
  semantics, and target-signature requirements are explicit and satisfied.
- Do not leave a discovered in-scope candidate without a fail-closed status.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 inventory JSON exists and validates with `python -m json.tool`;
- every discovered candidate in the declared scope has one of these statuses:
  `schema_candidate`, `missing_payload`, `missing_target_signature`,
  `unsupported_transport_kind`, `unsafe_identity`, `ambiguous_needs_manual_review`,
  `too_large_for_bounded_payload_inspection`, `not_readable`, or
  `not_migration_candidate`;
- Phase 1 result states what is `correct`, `unsupported`, and `not checked`;
- Phase 1 result records actual commands run, environment, CPU/GPU status, and
  reasons when SHA-256 or JSON parsing was not feasible;
- Phase 2 schema subplan exists and is reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- no Phase 1 stop condition fired.

## Stop Conditions

Stop and write a blocker result if:

- `/home/chakwong/python` is inaccessible;
- legacy dense-IAF source surfaces cannot be located;
- all candidate JSON payloads needed for taxonomy are unreadable;
- any discovered in-scope artifact remains ambiguous without either
  `ambiguous_needs_manual_review` status or a blocker result;
- the inventory cannot account for every discovered in-scope candidate;
- inventory classification would require loading model code, running training,
  running HMC, network fetch, GPU execution, or modifying external files;
- Claude review for the Phase 2 subplan cannot be obtained after the
  probe/narrowing protocol;
- Claude and Codex do not converge after five review rounds for the Phase 2
  subplan.

`PHASE1_DRAFT_FOR_REVIEW`
