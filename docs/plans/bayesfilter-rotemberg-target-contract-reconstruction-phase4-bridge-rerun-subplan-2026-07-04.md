# Phase 4 Subplan: Bridge Rerun And Payload Boundary Decision

Date: 2026-07-04

Status: `PHASE4_DRAFT_FOR_REVIEW`

## Phase Objective

Rerun the Rotemberg bridge classification against the validated metadata-only
contract and determine whether any embedded dense-IAF candidate is signature
ready for the generic BayesFilter loader. This phase remains fail-closed and
must not export or load payloads unless a later approved gate exists.

## Entry Conditions Inherited From Previous Phase

- Phase 3 validation passed and produced a stable manifest signature.
- The manifest contains no invented fields.
- The reviewed Phase 4 bridge procedure is unchanged from the earlier blocked
  evidence boundary except for the recovered Rotemberg metadata.
- No historical artifact has been loaded as reusable.

## Required Artifacts

- Phase 4 bridge rerun JSON:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json`
- Phase 4 result:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-result-2026-07-04.md`
- Phase 5 subplan draft or refresh:
  `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase5-closeout-subplan-2026-07-04.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, And Reviews

Local checks:

```text
python docs/plans/bayesfilter_rotemberg_target_contract_phase4_bridge.py --output docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json
python -m json.tool docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json
git diff --check -- docs/plans/bayesfilter_rotemberg_target_contract_phase4_bridge.py docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-2026-07-04.json docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-result-2026-07-04.md
```

Reviews:

- Codex reviews the bridge classifications for invented fields or legacy-name
  shortcuts.
- Claude reviews the Phase 5 closeout subplan as a read-only exact-path review
  before Phase 5 begins.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the validated Rotemberg metadata support any bridgeable generic `SSMTargetContract` target signature without inventing fields? |
| Baseline/comparator | Phase 3 validation result and the earlier dense-IAF Phase 4 bridge blocker. |
| Primary pass criterion | Every embedded-payload candidate is classified bridgeable or reject-only with exact missing fields or exact blocker reasons. |
| Veto diagnostics | Legacy-name-only bridge, process-local identity, invented field, unsupported payload assumption, or any claim that bridge classification proves payload reuse. |
| Explanatory diagnostics | Candidate path, supported fields, missing fields, and review notes. |
| Not concluded | No payload export, no real-artifact load, no HMC convergence, no posterior correctness, and no sampler ranking. |
| Result artifact | Phase 4 bridge rerun JSON and Phase 4 result Markdown. |

## Forbidden Claims And Actions

- Do not load historical artifacts through BayesFilter.
- Do not export payloads unless a later reviewed gate explicitly authorizes it.
- Do not run HMC, training, GPU/CUDA commands, or network fetches.
- Do not treat legacy target names, class paths, or run labels as canonical
  signatures.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- the bridge rerun JSON exists and validates with `python -m json.tool`;
- each embedded payload candidate is classified with an exact bridge or reject
  status;
- Phase 4 result states what is `correct`, `wrong relative to the stated
  target`, `unsupported`, and `not checked`;
- Phase 5 subplan exists and is reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- no Phase 4 stop condition fired.

## Stop Conditions

Stop and write a blocker result if:

- no stable bridgeable signature exists for the target cell;
- bridge classification would require invented fields or legacy code execution;
- local checks fail for a non-fixable reason;
- `/home/chakwong/python` access becomes necessary beyond the reviewed sources;
- Claude and Codex do not converge after five review rounds for the same
  blocker.

`PHASE4_DRAFT_FOR_REVIEW`
