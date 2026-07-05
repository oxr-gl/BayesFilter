# P85 Phase 2 Subplan: Config Interface And XLA Contract

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE1`

## Phase Objective

Design the BayesFilter setup configuration surface for basis family, basis
parameters, domain mapping, dimension replication, manifest identity, and
XLA/static compilation boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 1 has classified author operations and local gaps with source anchors.
- Phase 1 has not authorized code implementation.
- P84 Phase 2 fitting remains blocked.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase2-config-interface-xla-contract-result-2026-06-23.md`
- Proposed setup schemas for `BasisSpec`, `DomainMapSpec`, and
  `ProductBasisSpec` or equivalent names.
- Proposed manifest payload fields and classification labels.
- Refreshed Phase 3 subplan.

## Required Checks / Tests / Reviews

- Scan existing basis, product-basis, and manifest payload APIs before naming
  new structures:

```bash
rg -n "ProductBasis|LegendreBasis1D|manifest_payload|basis_dim_tuple|FixedTTFitConfig|BranchManifest" bayesfilter/highdim tests/highdim -S
```

- Run P85 documentation hygiene checks.
- Claude read-only review of the Phase 2 result if it is used to authorize
  implementation.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What setup API can express the author basis/domain route while remaining XLA-safe and locally maintainable? |
| Baseline/comparator | Phase 1 inventory and existing `ProductBasis`/manifest APIs. |
| Primary criterion | A reviewed design states setup fields, allowed families, manifest identity, classification labels, and static compilation rules. |
| Veto diagnostics | Runtime tensor-controlled basis dispatch; hidden Python branching inside `tf.function` hot paths; missing manifest identity; unsupported source-faithful labels. |
| Explanatory diagnostics | Expected retrace/recompile triggers, basis cardinality, domain-map formulas, import/export surface. |
| Not concluded | No implementation, no performance claim, no fit quality, no production readiness. |
| Artifact | Phase 2 result and refreshed Phase 3 subplan. |

## Forbidden Claims / Actions

- Do not implement code in Phase 2.
- Do not promise one XLA executable across different basis families or
  cardinalities.
- Do not make `Lagrangep` the default unless explicitly approved.
- Do not run TensorFlow tests or fitting commands.
- Do not claim Phase 1 repair is complete.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if Phase 2 defines:

- exact setup fields and defaults;
- which fields are compile-static and may trigger retrace/recompile;
- manifest identity fields and nonclaim fields;
- unsupported or deferred operations;
- required implementation files and tests to be frozen in Phase 3.

## Stop Conditions

Stop if:

- no clean setup API can preserve both the legacy diagnostic route and author
  route;
- XLA/static-shape boundaries remain ambiguous;
- implementation would require third-party code copying or license review
  before design can proceed.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 2 result / close record;
3. draft or refresh the Phase 3 subplan;
4. review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
