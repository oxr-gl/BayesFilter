# BayesFilter-MacroFinance Phase 6 Result: Evidence Manifest And Artifact Schema

Date: 2026-06-09

## Status

`PASSED`

## Role And Runtime Classification

Codex is supervisor and executor. Claude is read-only reviewer only.

Runtime classification:

- BayesFilter library primitive: artifact/data preparation and deterministic
  fixture/test helper for this phase.
- MacroFinance compatibility: no-HMC manifest fixture that describes an
  existing Phase 4 compatibility artifact without changing that artifact.
- No long-run HMC, posterior convergence, sampler superiority, GPU/XLA
  readiness, default sampler promotion, or empirical claim is authorized by
  this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter extend or wrap existing runtime manifest authority with a JSON-stable evidence manifest schema that records the fields needed by HMC, target-only, and no-HMC parity artifacts without adding MacroFinance-specific requirements? |
| Baseline/comparator | Existing `bayesfilter.runtime.RunManifest`, `WorkerManifest`, `stable_config_hash`, JSON helpers, Stage 1 transform signatures, Stage 2 mass artifacts, Stage 3 screen classifications, and current MacroFinance Phase 4 manifest-style result payloads. |
| Primary criterion | A BayesFilter-owned evidence manifest helper records git state, command, environment, CPU/GPU status, data hash, target scope, backend, transform signature, MAP/covariance source, tuning policy, diagnostic policy, result paths, and nonclaims; is JSON-stable; rejects or normalizes process-local IDs; and can represent HMC, target-only, and no-HMC parity scopes. |
| Veto diagnostics | Schema omits target scope, backend, transform, diagnostic policy, result paths, or nonclaims; process-local object IDs enter JSON-stable payloads; MacroFinance-specific fields become required in BayesFilter; or schema creates a competing manifest authority instead of extending/wrapping existing runtime contracts. |
| Repair triggers | Missing required field, unstable hash, process-local ID acceptance, insufficient run-scope coverage, missing export, stale result note, MacroFinance compatibility manifest mismatch, or Claude `NEEDS_REVISION` with fixable findings. |
| Explanatory diagnostics | Exact class/function names, payload hash values, artifact paths, and whether the helper is a dataclass or factory function. |
| Non-claims | No posterior convergence, sampler superiority, empirical validity, GPU/XLA readiness, default sampler promotion, or production readiness is concluded. |

## Skeptical Audit

- Wrong baseline: The baseline is existing BayesFilter runtime manifest
  contracts, not MacroFinance's ad hoc result JSON or a new detached manifest
  authority.
- Proxy metric promotion: Manifest completeness and hash stability are artifact
  validity checks only; they do not establish sampler validity or scientific
  evidence.
- Stop conditions: Missing target/backend/transform/nonclaims, process-local ID
  leakage, or MacroFinance-specific required fields stop the phase until
  repaired.
- Fair comparison: Compatibility must emit a BayesFilter manifest for current
  MacroFinance Phase 4 metadata without changing existing MacroFinance
  artifacts or pass/fail interpretation.
- Hidden assumptions: CPU/GPU status is recorded as evidence text; this phase
  does not claim trusted GPU or XLA readiness.
- Stale context: BayesFilter and MacroFinance both have dirty worktrees;
  unrelated changes must not be reverted.
- Environment/import mismatch: BayesFilter tests run from
  `/home/ubuntu/python/BayesFilter`; MacroFinance compatibility should use
  `PYTHONPATH=/home/ubuntu/python/BayesFilter` or an equivalent explicit local
  import contract.
- Artifact relevance: The required artifacts are this result note, focused
  BayesFilter tests, a MacroFinance compatibility manifest fixture, and Claude
  read-only pre/post reviews.
- Role-contract check: Claude pre-review must be read-only; Codex performs all
  edits and tests.
- BayesFilter/MacroFinance ownership: Reusable schema helpers belong in
  `bayesfilter.runtime`; MacroFinance remains a client fixture.

## Current Code Audit

BayesFilter already has:

- `RunManifest` and `WorkerManifest`;
- `stable_config_hash`, `configs_match_exact`, and stale artifact payload
  helpers;
- `atomic_write_json`, `append_jsonl`, and manifest writers;
- nonclaims on runtime metadata surfaces.

The current runtime contracts do not yet provide a compact evidence payload
that binds a scientific/engineering run to target scope, backend, transform,
MAP/covariance source, tuning policy, diagnostic policy, result paths, and
nonclaims. Stage 4 should add a wrapper/factory around the existing runtime
helpers, not a competing manifest system.

## Planned Minimal Implementation

1. Add an `EvidenceManifest` dataclass or equivalent factory in
   `bayesfilter/runtime/runner.py`.
2. Include required fields:
   run scope (`hmc`, `target_only`, or `no_hmc_parity`);
   git state;
   command;
   environment;
   CPU/GPU status;
   data hash;
   target scope;
   backend;
   transform signature;
   MAP/covariance source;
   tuning policy;
   diagnostic policy;
   result paths;
   nonclaims.
3. Add JSON-stable `payload`, `signature_payload`, or hash helper using the
   existing `_normalize_for_json` / `stable_config_hash` conventions.
4. Reject process-local object identity patterns in manifest string fields or
   normalize them out before hashing.
5. Add a compact Markdown result-note helper for evidence manifests.
6. Export the helper through `bayesfilter.runtime` and top-level `bayesfilter`
   if the public API tests require it.
7. Add focused BayesFilter tests for JSON stability, process-local ID rejection,
   required fields for `hmc`, `target_only`, and `no_hmc_parity`, and
   compatibility with existing `RunManifest`/`WorkerManifest` hashing.
8. Add a MacroFinance compatibility test that builds a BayesFilter evidence
   manifest for the current Phase 4 matched-DGP no-HMC compatibility artifact
   without modifying existing artifacts.

## Planned Checks

- `python -m pytest tests/test_common_inference_runtime_contracts.py -q`
- `python -m pytest tests/test_v1_public_api.py -q` if export surface changes.
- MacroFinance focused compatibility test with
  `PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1
  PYTHONDONTWRITEBYTECODE=1`, targeting the matched-DGP SVD pilot test module.

If the MacroFinance compatibility gate cannot be run because of import-path,
environment, stale-artifact, or fixture issues, Stage 4 enters the repair loop.
It must not substitute a MacroFinance-specific BayesFilter schema field or
weaken required nonclaims to make the fixture pass.

## Pre-Review Request

Claude should verify that this Stage 4 precheck is consistent with accepted
Phase 6, extends/wraps existing runtime manifest authority, avoids
MacroFinance-specific schema requirements, preserves nonclaims, and does not
promote manifest completeness to scientific validity.

## Pre-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_4_evidence_manifest_artifact_schema_pre_review_round_01.md` returned `VERDICT: PROCEED`; implementation may proceed.

## Implementation Summary

Implemented a BayesFilter-owned `EvidenceManifest` in
`bayesfilter/runtime/runner.py`.

The manifest records:

- run scope (`hmc`, `target_only`, or `no_hmc_parity`);
- git state;
- command;
- environment;
- CPU/GPU status;
- data hash;
- target scope;
- backend;
- transform signature;
- MAP/covariance source;
- tuning policy;
- diagnostic policy;
- result paths;
- nonclaims;
- optional existing `RunManifest`;
- optional existing `WorkerManifest`.

The helper provides:

- `payload()`;
- `manifest_hash`;
- `markdown_note()`;
- `write_evidence_manifest(...)`.

The implementation wraps existing runtime authority and uses the existing
normalization/hash conventions. It rejects process-local identity patterns in
string fields and normalized payloads.

Exports were updated through `bayesfilter.runtime` and the top-level
`bayesfilter` lazy export table.

MacroFinance compatibility was implemented as a focused test in
`/home/ubuntu/python/MacroFinance/tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`.
It builds a BayesFilter `EvidenceManifest` for the current matched-DGP no-HMC
compatibility artifact using the existing initialization artifact path, target
scope, backend, transform signature, covariance source, diagnostic policy, and
nonclaims. It does not modify existing MacroFinance artifacts.

## Repair Notes

- First focused BayesFilter test run failed during collection with an
  `IndentationError` in `bayesfilter/runtime/__init__.py`; the new export names
  had been inserted after the closing `__all__` bracket. Codex repaired the
  export list and reran the same gate successfully.
- First MacroFinance focused compatibility run failed because the test omitted
  `sha256_file`; Codex added the existing helper import and reran.
- Second MacroFinance focused compatibility run failed because the test omitted
  `COVARIANCE_SOURCE`; Codex added the existing constant import and reran.

These were implementation/test wiring repairs, not evidence-schema contract
failures.

## Files Touched For Stage 4

BayesFilter:

- `bayesfilter/runtime/runner.py`
- `bayesfilter/runtime/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_common_inference_runtime_contracts.py`
- `tests/test_v1_public_api.py`
- `docs/plans/bayesfilter_macrofinance_phase_6_evidence_manifest_artifact_schema_result_2026_06_09.md`
- `docs/plans/bayesfilter_macrofinance_stage_4_evidence_manifest_artifact_schema_pre_review_round_01.md`

MacroFinance:

- `tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`
- `docs/plans/bayesfilter_macrofinance_visible_execution_ledger_2026_06_09.md`

## Checks Run

| Command | Result | Role |
| --- | --- | --- |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | first run failed at collection with `IndentationError`; repaired export list | Repair trigger |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | `33 passed in 0.15s` | BayesFilter focused contract gate |
| `python -m pytest tests/test_v1_public_api.py -q` from `/home/ubuntu/python/BayesFilter` | `4 passed, 2 warnings in 2.55s` | BayesFilter public export gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_evidence_manifest_represents_matched_dgp_no_hmc_compatibility -q` from `/home/ubuntu/python/MacroFinance` | first failed with missing `sha256_file`, second failed with missing `COVARIANCE_SOURCE`, third passed: `1 passed, 2 warnings in 2.44s` | Direct MacroFinance no-HMC manifest compatibility gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py -q` from `/home/ubuntu/python/MacroFinance` | `12 passed, 20867 warnings in 119.78s` | Existing real-client matched-DGP suite evidence |

The warnings are TensorFlow Probability `distutils` deprecation warnings and
TensorFlow AutoGraph/gast deprecation warnings; they are explanatory only for
this phase.

## Gate Assessment

| Gate | Status |
| --- | --- |
| Extends/wraps existing runtime manifest authority | passed |
| JSON-stable manifest hash | passed |
| Process-local ID rejection | passed |
| Required fields for `hmc` | passed |
| Required fields for `target_only` | passed |
| Required fields for `no_hmc_parity` | passed |
| Target scope, backend, transform, diagnostic policy, result paths, nonclaims present | passed |
| MacroFinance-specific fields required in BayesFilter | no |
| MacroFinance no-HMC compatibility manifest | passed |
| Manifest completeness promoted to scientific validity | no |

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stage 4 implementation passed focused checks and Claude read-only post-review |
| Primary criterion status | passed focused BayesFilter and MacroFinance compatibility checks |
| Veto diagnostic status | no competing authority, required-field omission, process-local ID leakage, MacroFinance-specific schema requirement, or scientific-validity promotion observed |
| Main uncertainty | this is an evidence-schema contract only; later phases still own backend parity gates, invalid-region policy, tuning, and migration |
| Next justified action | advance to Stage 5, backend parity gates |
| What is not concluded | no posterior convergence, sampler superiority, default sampler promotion, empirical validity, GPU/XLA readiness, or production readiness |

## Post-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_4_evidence_manifest_artifact_schema_post_review_round_01.md` returned `VERDICT: PROCEED`.
