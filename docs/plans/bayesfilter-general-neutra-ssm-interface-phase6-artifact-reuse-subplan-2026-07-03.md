# Phase 6 Subplan: Existing NeuTra Artifact Reuse Bridge

Date: 2026-07-03

Status: `REVIEWED_READY_FOR_PHASE6_EXECUTION`

## Phase Objective

Restore or locate existing NeuTra artifact bundles from `~/python`/external
storage, verify hashes and target signatures, load frozen transports through
the generic BayesFilter loader, and run only bounded reuse canaries.

Phase 6 uses live Phase 4/5 boundaries:

- `load_frozen_neutra_artifact`;
- `stable_frozen_neutra_artifact_signature`;
- `bind_fixed_transport_hmc_mechanics`;
- `FixedTransportHMCManifest`;
- `stable_fixed_transport_hmc_manifest_signature`.

Phase 5 result anchor:
`docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-result-2026-07-03.md`.

## Entry Conditions Inherited From Previous Phase

- Phase 5 result states `PHASE5_GATE_PASSED`.
- Fixed-transport HMC binding exists and passes focused tests.
- Phase 6 subplan has been refreshed and reviewed.

Concrete inherited Phase 5 decisions Phase 6 must preserve:

- Phase 5 HMC binding evidence is CPU-only mechanics smoke, not convergence or
  sampler-readiness evidence.
- Artifact inventory/signature status must be recorded before any canary.
- `bind_fixed_transport_hmc_mechanics` may be used only for mechanics canaries
  unless a new reviewed plan authorizes serious HMC.
- Missing/mismatched artifacts must not be loaded as reusable.

## Required Artifacts

- Artifact inventory JSON:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-inventory-2026-07-03.json`
- Reuse result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase6-artifact-reuse-result-2026-07-03.md`
- Optional copied external artifact bundle paths recorded in the result, not
  committed to git.
- Refreshed Phase 7 subplan.

## Required Checks, Tests, And Reviews

Local checks:

- Verify candidate artifact paths exist or record `missing_payload`.
- Verify SHA256 for present training states.
- Load transport without training.
- Compare target signature if present.
- Run tiny load/value smoke only after signature status is recorded.
- Any mechanics canary must record CPU-only status, mechanics-only nonclaims,
  target signature, transport hash, and HMC policy label/hash.

Review:

- Claude read-only review of the artifact inventory result before crossing to
  Phase 7.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which existing NeuTra artifacts are safely reusable as frozen transports for the generic BayesFilter target interface? |
| Baseline/comparator | Existing `~/python` closeout notes and artifact-summary hashes. |
| Primary pass criterion | Each artifact is classified as `reusable`, `missing_payload`, `signature_mismatch`, `signature_not_available_nonreusable`, `loader_blocked`, or `not_checked`; no missing, unsigned, or mismatched artifact is used as reusable. |
| Veto diagnostics | Missing training-state payload used anyway, hash mismatch, target signature mismatch, signature-absent artifact used as reusable, loader warning treated as pass, CPU-only loader/mechanics check described as training or convergence evidence, or serious HMC launched. |
| Explanatory diagnostics | File sizes, hashes, target labels, transport dimensions, and loader roundtrip checks. |
| Not concluded | No new training success, no real-model posterior correctness, no HMC convergence, no method ranking. |
| Artifacts | Artifact inventory JSON, Phase 6 result, loader logs. |

## Forbidden Claims And Actions

- Do not retrain NeuTra in Phase 6.
- Do not launch serious HMC.
- Do not commit large generated artifact payloads.
- Do not use missing `/home/ubuntu` paths without restoration and hash check.
- Do not claim artifact reuse if signature is absent unless result class is
  explicitly `signature_not_available_nonreusable`.
- Do not run `bind_fixed_transport_hmc_mechanics` before the artifact
  classification is recorded.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if:

- artifact inventory exists;
- every artifact has an explicit classification;
- any canary used only `reusable` artifacts or clearly marked synthetic
  fixtures;
- Phase 6 result states `PHASE6_GATE_PASSED` or writes a bounded blocker;
- Phase 7 subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- artifact payload restoration requires network or credentials not already
  approved;
- target signatures cannot be matched and a human decision is needed;
- user approval is needed to copy large generated artifacts into the repo tree;
- a proposed canary becomes a serious HMC run.
- artifact inventory would require reading or copying files outside approved
  paths without explicit approval.

## Skeptical Plan Audit

Status: `PASSED_FOR_PHASE6_EXECUTION_AFTER_REVIEW`

Checked risks:

- Wrong baseline: Phase 6 compares artifacts to recorded hashes/signatures and
  loader requirements, not to sampler performance.
- Proxy metrics: loader/value canaries are explanatory only and cannot promote
  an artifact without signature/hash compatibility.
- Missing stop conditions: network/credential needs, large artifact copies,
  absent target signatures, and serious-HMC drift are explicit stops.
- Hidden assumptions: Phase 5 mechanics smoke remains non-convergence evidence.
- Artifact mismatch: Phase 6 must write inventory JSON, result, and refreshed
  Phase 7 subplan before handoff.

## Phase Execution Steps

1. Inventory named artifacts from previous NeuTra notes.
2. Verify existence and hashes for present payloads.
3. Load only eligible frozen transports.
4. Run bounded load/value canaries.
5. Write Phase 6 result.
6. Refresh and review Phase 7 subplan.

## End-Of-Subplan Closeout Requirements

The result must include a table separating trained-transport availability,
loader success, target-signature compatibility, and HMC canary status.
