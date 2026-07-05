# Phase 4 Subplan: Target-Signature Bridge

Date: 2026-07-04

Status: `PHASE4_DRAFT_FOR_REVIEW`

## Phase Objective

Determine whether any historical dense-IAF embedded-payload candidate from the
Phase 1 taxonomy can be mapped, without executing legacy model code, to a
canonical generic BayesFilter `SSMTargetContract` signature. Broader historical
dense-IAF evidence cells remain provenance unless they contain or point to an
embedded payload admitted by Phase 1. This is a read-only bridge and
classification phase, not a loader or HMC phase.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result exists with status `PHASE3_GATE_PASSED_SYNTHETIC_ONLY`.
- Dense-IAF loader support exists for synthetic schema-valid payloads.
- Historical artifacts remain reject-only until this bridge supplies a canonical
  target signature and proves a match.
- No historical artifact was loaded as reusable in Phase 3.
- Governing schema artifact:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md`.

## Required Artifacts

- Phase 4 bridge inventory JSON:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json`
- Phase 4 result:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-result-2026-07-04.md`
- Phase 5 payload export/restoration subplan:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase5-payload-export-subplan-2026-07-04.md`
- Updated execution and Claude review ledgers.
- Governing Phase 2 schema artifact:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md`

## Required Checks, Tests, And Reviews

Local checks:

```text
test -f docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json
test -f docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-result-2026-07-04.md
test -f docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md
rg -n "SSMTargetContract|target_signature|problem_id|static_shape|data_signature|chart|prior|filter_program|bridgeable_signature_defined|missing_problem_manifest|missing_data_signature|missing_chart|missing_prior|missing_filter_program|phase2_rule_mismatch|invented_field_required|reject" docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-result-2026-07-04.md docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json
git diff --check -- docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-result-2026-07-04.md docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase5-payload-export-subplan-2026-07-04.md
```

Reviews:

- Codex reviews every bridgeable classification against the exact generic
  target-contract fields.
- Claude reviews the Phase 5 payload export/restoration subplan before Phase 5
  begins. Phase 5 cannot begin unless that review returns `VERDICT: AGREE`, or
  all fixable `VERDICT: REVISE` findings are patched and rereviewed. If review
  cannot be obtained after the probe/narrowing protocol, write a blocker result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can any historical dense-IAF candidate be assigned a canonical generic `SSMTargetContract` target signature without unsafe assumptions? |
| Baseline/comparator | Phase 1 taxonomy JSON, exact Phase 2 schema artifact `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md`, and Phase 3 synthetic-loader nonclaims. |
| Primary pass criterion | Every candidate with embedded dense-IAF payload is classified as `bridgeable_signature_defined` or one fixed fail-closed reject-only status with exact missing fields. |
| Veto diagnostics | Signature derived from legacy target name only, class path only, runtime identity, memory address, unexecuted model object, missing data signature, missing chart/prior/filter fields, or any need to execute legacy model code. |
| Explanatory diagnostics | Candidate path, target metadata fields found, missing `SSMTargetContract` fields, and proposed generic contract fields if bridgeable. |
| Not concluded | Payload export success, real-artifact loading, HMC convergence, posterior correctness, sampler ranking, GPU readiness, or default policy change. |
| Result artifact | Phase 4 bridge JSON and result Markdown. |

Fixed bridge statuses:

- `bridgeable_signature_defined`;
- `missing_problem_manifest`;
- `missing_static_shape`;
- `missing_data_signature`;
- `missing_chart`;
- `missing_prior`;
- `missing_filter_program`;
- `phase2_rule_mismatch`;
- `invented_field_required`;
- `legacy_identity_only`;
- `requires_legacy_code_execution`;
- `not_embedded_payload_candidate`.

## Forbidden Claims And Actions

- Do not load historical artifacts through the dense-IAF loader.
- Do not copy large artifacts into the repo.
- Do not execute legacy model code to infer target fields.
- Do not run HMC, training, GPU/CUDA commands, or network fetches.
- Do not treat target names, class paths, runtime ids, or result-note labels as
  canonical signatures.
- Do not claim real-artifact migration success.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 inventory classifies every embedded-payload candidate from Phase 1;
- each bridgeable candidate records a metadata-only generic `SSMTargetContract`
  manifest payload using fields observed in artifacts or reviewed static
  metadata, plus the canonical signature. It must not include training-state
  tensors or restored payload content;
- each reject-only candidate records exact missing fields or veto reason;
- Phase 4 result states what is `correct`, `unsupported`, and `not checked`;
- Phase 5 subplan exists and has Claude `VERDICT: AGREE`, or all fixable
  `VERDICT: REVISE` findings were patched and rereviewed;
- no historical artifact was loaded as reusable.

## Stop Conditions

Stop and write a blocker result if:

- no stable target-signature bridge can be defined for any historical embedded
  payload candidate;
- bridge classification requires executing legacy model code;
- bridge classification requires network, GPU, HMC, training, large copy,
  package installation, or modifying `/home/chakwong/python`;
- any candidate is classified bridgeable from a legacy name/class path only;
- the Phase 2 canonical signature rule cannot be instantiated for a candidate
  without inventing fields not present in artifacts or reviewed static metadata;
- bridge classification would require inventing model/data/chart/prior/filter
  fields not present in artifacts or reviewed static metadata;
- Claude review for Phase 5 subplan cannot be obtained after probe/narrowing.
  The protocol is: run a tiny Claude health probe, then retry with a smaller
  exact-path prompt; if that still fails, write a blocker result instead of
  advancing;
- Claude and Codex do not converge after five review rounds for Phase 5.

## Skeptical Plan Audit

Phase 4 can only classify signature bridge readiness. It does not load real
payloads or validate posterior/HMC behavior. A negative result means the
historical artifacts remain valuable evidence but reject-only for generic
BayesFilter loader reuse.

`PHASE4_DRAFT_FOR_REVIEW`
