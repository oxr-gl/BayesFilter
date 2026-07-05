# Phase 2 Subplan: Dense-IAF Frozen Transport Schema

Date: 2026-07-04

Status: `PHASE2_DRAFT_FOR_REVIEW`

## Phase Objective

Define a BayesFilter-owned dense-IAF frozen transport schema that can represent
the legacy dense autoregressive IAF payload shapes discovered in Phase 1 while
requiring a canonical generic target-signature scheme, topology/tensor hashes,
explicit log-Jacobian semantics, and fail-closed rejection rules before loader
implementation. A field named `target_signature` is not sufficient; the schema
artifact must define what exact `SSMTargetContract` payload is hashed, what
legacy evidence can and cannot populate it, and which cases remain reject-only.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result exists with status
  `PHASE1_GATE_PASSED_WITH_TARGET_SIGNATURE_BLOCKER`.
- Phase 1 inventory JSON exists and classifies every discovered in-scope
  candidate.
- No historical artifact has been loaded through BayesFilter.
- The next blocker is schema and target-signature readiness, not HMC tuning or
  posterior validation.
- The Phase 2 schema may define the canonical target-signature requirement, but
  it must not pretend Phase 1 supplied generic target signatures.

## Required Artifacts

- Phase 2 schema artifact:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-2026-07-04.md`
- Phase 2 result:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-result-2026-07-04.md`
- Phase 3 implementation subplan:
  `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, And Reviews

Local checks:

```text
test -f docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-2026-07-04.json
rg -n "schema id|target_signature|SSMTargetContract|topology_hash|tensor_hash|dimension|component|dense_autoregressive_iaf|log_jacobian_available|log_abs_det_jacobian|sha256|process-local|mapping/rejection|reject-only|nonclaims" <Phase 2 schema artifact>
git diff --check -- <Phase 2 schema/result/subplan artifacts>
```

Reviews:

- Codex reviews the schema against the Phase 1 observed payload classes.
- Claude reviews the Phase 3 implementation subplan as an exact-path read-only
  review before implementation begins.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What stable dense-IAF frozen transport schema should BayesFilter implement before loading historical NeuTra artifacts? |
| Baseline/comparator | Observed evidence: Phase 1 taxonomy JSON. Legacy semantic inference: `DenseAutoregressiveIAFTransport` forward/logdet semantics from `/home/chakwong/python/src/dsge_hmc/estimation/_transports.py`. Unresolved design item: canonical generic `SSMTargetContract` signature bridge for legacy targets. |
| Primary pass criterion | Schema artifact covers required fields, observed legacy component types, topology hash rules, tensor hash rules, canonical target-signature rules, class-by-class mapping/rejection table, logdet semantics, and rejection/nonclaim boundaries. |
| Veto diagnostics | Schema omits target signature, permits process-local identity, permits dimension mismatch, omits logdet convention, treats inverse diagnostics as correctness, or allows historical artifacts to be loaded without target bridge. |
| Explanatory diagnostics | Component taxonomy, observed transport kinds, topology fields, tensor payload fields, and legacy helper names. |
| Not concluded | No loader implementation, migrated payload, HMC convergence, posterior correctness, sampler ranking, or default readiness. |
| Result artifact | Phase 2 schema and result Markdown. |

## Forbidden Claims And Actions

- Do not implement the loader in Phase 2.
- Do not load historical artifacts through BayesFilter.
- Do not copy large artifacts into the repo.
- Do not run HMC, training, GPU/CUDA commands, or network fetches.
- Do not claim compatibility with every future normalizing flow family.
- Do not claim posterior correctness or HMC readiness from a schema definition.
- Do not treat legacy target names, class paths, runtime object identities, or
  process-local metadata as valid generic target signatures.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- the Phase 2 schema artifact exists and passes local checks;
- the schema covers at least `composed`, `mixing_linear`, `affine`,
  `affine_dense`, and `dense_autoregressive_iaf` components as observed in
  Phase 1;
- the schema defines canonical `target_signature` as the stable hash of a
  generic `SSMTargetContract` manifest, and explicitly states that legacy
  target names or runtime identities are insufficient;
- the schema requires `dimension`, `log_jacobian_available`, `topology_hash`,
  stable tensor hashes, and nonclaims;
- the schema artifact includes a class-by-class mapping/rejection table for
  every Phase 1 candidate status and observed payload class, including
  reject-only handling when generic target-signature evidence is absent;
- Phase 2 result records what is `correct`, `unsupported`, and `not checked`;
- Phase 3 implementation subplan exists and is reviewed;
- no human-required approval boundary is crossed. Human-required approval
  boundaries are network fetch, GPU/CUDA execution, serious HMC/MCMC, training,
  package or environment mutation, large artifact copy, modifying
  `/home/chakwong/python`, or changing default product/scientific claim policy.

## Stop Conditions

Stop and write a blocker result if:

- Phase 1 taxonomy is missing or invalid;
- the observed legacy payload shape is too ambiguous to define a safe schema;
- no stable generic target-signature scheme can be specified without unsafe
  assumptions;
- the only available signature candidates are process-local/runtime-specific,
  class-path-specific without a reviewed generic manifest, dependent on
  executing legacy code, or unstable across environments;
- schema design would require executing legacy model code;
- schema design would require network, GPU, HMC, training, large copy, package
  installation, or modifying `/home/chakwong/python`;
- Claude review for the Phase 3 subplan cannot be obtained after the
  probe/narrowing protocol. The protocol is: run a tiny Claude health probe,
  then retry with a smaller exact-path prompt; if that still fails, write a
  blocker result instead of advancing;
- Claude and Codex do not converge after five review rounds for the Phase 3
  subplan.

## Skeptical Plan Audit

Phase 2 is a schema-design phase. It does not promote old HMC metrics or
payload existence to migration success. Its output answers the schema question
directly and leaves implementation, target bridge, real-artifact loading, and
mechanics checks to later gates.

`PHASE2_DRAFT_FOR_REVIEW`
