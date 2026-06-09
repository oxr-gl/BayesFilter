# BayesFilter-MacroFinance Phase 2 Result: Precomputed MAP And Mass Artifact

Date: 2026-06-09

## Status

`PASSED`

## Role And Runtime Classification

Codex is supervisor and executor. Claude is read-only reviewer only.

Runtime classification:

- BayesFilter library primitive: NumPy verification oracle and deterministic
  fixture/test helper for this phase.
- MacroFinance compatibility: small diagnostic client gate that reads the
  current matched-DGP initialization artifact and does not run HMC.
- No long-run HMC, posterior convergence, MAP-quality claim, GPU/XLA readiness,
  default sampler promotion, or empirical claim is authorized by this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter represent and validate precomputed position, covariance, and covariance factor artifacts so downstream HMC transforms know the adapter signature, position role, covariance source, exact matrix square-rooted, factor orientation, eigen summaries, and nonclaims? |
| Baseline/comparator | Existing `PrecomputedMAP`, `validate_precomputed_map`, `MassMatrixResult`, `covariance_from_negative_hessian`, `whitening_from_covariance`, Stage 1 `LatentAffineHMCTransform`, and the current MacroFinance matched-DGP Hessian-scaled initialization artifact. |
| Primary criterion | A BayesFilter-owned artifact persists position, position role, adapter signature, covariance, factor, matrix used for square root, covariance source, factor orientation, eigen summaries, and nonclaims; rejects process-local or stale adapter signatures; validates shape/finiteness/reconstruction; and builds a Stage 1 latent transform without changing the target. |
| Veto diagnostics | Matrix square-rooted is ambiguous, position role conflates MAP with truth/prior center, covariance source missing, factor orientation missing or inconsistent with Stage 1, adapter signature accepts process-local identity, shape/finiteness/reconstruction check fails, or MacroFinance compatibility changes model target/data/priors. |
| Repair triggers | Missing metadata field, missing export, failed Hessian/covariance round trip, stale result note, inability to represent the matched-DGP initialization artifact as a non-MAP diagnostic center, or Claude `NEEDS_REVISION` with fixable findings. |
| Explanatory diagnostics | Eigenvalue summaries, condition numbers, jitter, runtime, exact class name, and whether the artifact is named `PrecomputedMassArtifact` or a compatible extension of `PrecomputedMAP`. |
| Non-claims | No posterior convergence, production MAP quality, sampler superiority, empirical validity, GPU/XLA readiness, or default HMC replacement is concluded. |

## Skeptical Audit

- Wrong baseline: The baseline is the current BayesFilter artifact and mass
  helpers plus the current matched-DGP initialization artifact, not the old
  mismatched Phase 4 failed HMC run.
- Proxy metric promotion: Eigen summaries, condition numbers, and
  reconstruction residuals are artifact validity diagnostics only; they are not
  posterior, convergence, or sampler-quality evidence.
- Stop conditions: Ambiguous factor orientation, missing covariance source,
  adapter signature mismatch, process-local signature acceptance, shape/finiteness
  failure, or MAP/truth conflation stop the phase until repaired.
- Fair comparison: Compatibility must consume the same `Sigma_phi_reg` and `L`
  fields that MacroFinance uses for its matched-DGP Hessian-scaled
  initialization gate.
- Hidden assumptions: The MacroFinance matched-DGP center is explicitly
  `matched_dgp_prior_center_not_map`; BayesFilter must persist a position role
  instead of silently calling every center a MAP.
- Stale context: BayesFilter and MacroFinance both have dirty worktrees;
  unrelated changes must not be reverted. The compatibility gate must preserve
  source-artifact freshness checks already present in MacroFinance.
- Environment/import mismatch: BayesFilter tests run from
  `/home/ubuntu/python/BayesFilter`; MacroFinance compatibility should use
  `PYTHONPATH=/home/ubuntu/python/BayesFilter` or an equivalent explicit local
  import contract.
- Artifact relevance: The required artifacts are this result note, focused
  BayesFilter tests, a MacroFinance compatibility test, and Claude read-only
  pre/post reviews.
- Role-contract check: Claude pre-review must be read-only; Codex performs all
  edits and tests.
- BayesFilter/MacroFinance ownership: Reusable artifact validation belongs in
  `bayesfilter.inference`; MacroFinance remains a client compatibility fixture.

## Current Code Audit

BayesFilter already has:

- `PrecomputedMAP(position, covariance, adapter_signature, source)` and
  `validate_precomputed_map(...)`, which validate shape and stable adapter
  signature but do not persist position role, covariance source, factor
  orientation, matrix square-rooted, eigen summaries, or nonclaims.
- `MassMatrixResult`, `covariance_from_negative_hessian`, and
  `whitening_from_covariance`, which can produce a covariance and Cholesky
  factor but do not bind them into a reusable artifact with adapter/target
  metadata.
- Stage 1 `LatentAffineHMCTransform`, which already owns the row-vector
  orientation `theta = center + z @ factor.T`.

MacroFinance's current matched-DGP initialization artifact contains:

- `center_type = matched_dgp_prior_center_not_map`;
- `covariance.Sigma_phi_reg`;
- `covariance.matrix_used_for_square_root = Sigma_phi_reg`;
- `covariance.L`;
- `covariance.L_L_transpose_allclose_Sigma_phi_reg`;
- `covariance.covariance_source = macro_model_error_v1_truth_hessian_full`;
- `covariance.mass_matrix_sqrt_convention = lower_cholesky_L_maps_rows_as_center_plus_z_at_L_transpose`.

The Stage 2 implementation must therefore allow a precomputed mass artifact
whose position is not a MAP while still preserving the legacy `PrecomputedMAP`
path for true MAP callers.

## Planned Minimal Implementation

1. Add `PrecomputedMassArtifact` in `bayesfilter/inference/hmc.py` with:
   position, covariance, factor, adapter signature, position role,
   covariance source, matrix used for square root, factor orientation, source,
   eigen summaries, log-Jacobian convention, and nonclaims.
2. Validate:
   one-dimensional finite position;
   square finite covariance/factor with matching dimension;
   supported factor orientation `row_right_transpose`;
   nonempty covariance source and matrix-used-for-square-root;
   stable adapter signature without process-local identity;
   covariance reconstruction `factor @ factor.T` within configurable tolerance.
3. Add constructors:
   `from_covariance(...)` using BayesFilter `whitening_from_covariance`;
   `from_negative_hessian(...)` using BayesFilter mass-matrix helpers.
4. Add methods:
   `validate_for_adapter(adapter, expected_dim=None)`;
   `build_latent_transform()`;
   `signature_payload()`.
5. Keep `PrecomputedMAP` and `validate_precomputed_map` as compatibility
   surfaces. Do not rename the existing artifact in a way that breaks clients.
6. Export the new artifact through `bayesfilter.inference` and top-level
   `bayesfilter` if public API tests require it.
7. Add focused BayesFilter tests for stale/process-local signatures, covariance
   and factor shape mismatch, Hessian-to-covariance/factor round trip,
   reconstruction failure, non-MAP position-role preservation, and transform
   construction.
8. Add a focused MacroFinance compatibility test that represents the current
   matched-DGP initialization artifact as `position_role="diagnostic_center_not_map"`
   or equivalent, validates reconstruction, and builds a BayesFilter latent
   transform with the same factor without changing the target.

## Planned Checks

- `python -m pytest tests/test_common_inference_runtime_contracts.py -q`
- `python -m pytest tests/test_v1_public_api.py -q`
- MacroFinance focused compatibility test with
  `PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1
  PYTHONDONTWRITEBYTECODE=1`, targeting the matched-DGP SVD pilot test module.

If the matched-DGP MacroFinance gate cannot be run because of import-path,
environment, stale-artifact, or fixture issues, Stage 2 enters the repair loop.
It must not substitute a synthetic-only compatibility check for the accepted
real client gate.

## Pre-Review Request

Claude should verify that this Stage 2 precheck is consistent with accepted
Phase 2, starts from existing BayesFilter primitives, preserves Stage 1
orientation authority, does not conflate MAP with a diagnostic prior/truth
center, avoids proxy-metric claims, and does not treat a fixable implementation
issue as a human stop.

## Pre-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_2_precomputed_map_mass_artifact_pre_review_round_01.md` returned `VERDICT: PROCEED`; implementation may proceed.

## Implementation Summary

Implemented a BayesFilter-owned `PrecomputedMassArtifact` in
`bayesfilter/inference/hmc.py`.

The artifact records:

- position;
- position role;
- covariance;
- factor;
- adapter signature;
- covariance source;
- matrix used for square root;
- factor orientation;
- source;
- covariance eigen summary;
- log-Jacobian convention;
- nonclaims.

The implemented contract validates:

- finite one-dimensional position;
- finite square covariance and factor with matching dimension;
- symmetric positive-definite covariance;
- stable, non-process-local adapter signature;
- nonempty position role, covariance source, and matrix-used-for-square-root;
- factor orientation `row_right_transpose`;
- reconstruction `factor @ factor.T == covariance` within declared tolerance.

The class provides:

- `from_covariance(...)`;
- `from_negative_hessian(...)`;
- `validate_for_adapter(...)`;
- `build_latent_transform()`;
- `signature_payload()`.

The existing `PrecomputedMAP` and `validate_precomputed_map` surfaces remain as
compatibility APIs. They were not renamed or removed.

Exports were updated through `bayesfilter.inference` and the top-level
`bayesfilter` lazy export table.

MacroFinance compatibility was implemented as a focused test in
`/home/ubuntu/python/MacroFinance/tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`.
It reads the current matched-DGP initialization artifact, represents
`Sigma_phi_reg` and `L` with `position_role="diagnostic_center_not_map"`, checks
the adapter signature and reconstruction, and builds a BayesFilter Stage 1
latent transform without changing the target, data, or priors.

## Files Touched For Stage 2

BayesFilter:

- `bayesfilter/inference/hmc.py`
- `bayesfilter/inference/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_common_inference_runtime_contracts.py`
- `tests/test_v1_public_api.py`
- `docs/plans/bayesfilter_macrofinance_phase_2_precomputed_map_mass_artifact_result_2026_06_09.md`
- `docs/plans/bayesfilter_macrofinance_stage_2_precomputed_map_mass_artifact_pre_review_round_01.md`

MacroFinance:

- `tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`
- `docs/plans/bayesfilter_macrofinance_visible_execution_ledger_2026_06_09.md`

## Checks Run

| Command | Result | Role |
| --- | --- | --- |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | `26 passed in 0.17s` | BayesFilter focused contract gate |
| `python -m pytest tests/test_v1_public_api.py -q` from `/home/ubuntu/python/BayesFilter` | `4 passed, 2 warnings in 2.48s` | BayesFilter public export gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_precomputed_mass_artifact_represents_matched_dgp_initialization -q` from `/home/ubuntu/python/MacroFinance` | `1 passed, 2 warnings in 2.70s` | Direct MacroFinance matched-DGP mass-artifact compatibility gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py -q` from `/home/ubuntu/python/MacroFinance` | `10 passed, 20867 warnings in 117.51s` | Existing real-client matched-DGP suite evidence |

The warnings are TensorFlow Probability `distutils` deprecation warnings and
TensorFlow AutoGraph/gast deprecation warnings; they are explanatory only for
this phase.

## Gate Assessment

| Gate | Status |
| --- | --- |
| Position role persisted | passed |
| Non-MAP matched-DGP center not conflated with MAP | passed |
| Covariance source persisted | passed |
| Matrix used for square root persisted | passed |
| Factor orientation persisted | passed |
| Adapter signature validation | passed |
| Process-local signature rejection | passed |
| Covariance/factor reconstruction validation | passed |
| Hessian-to-covariance/factor round trip | passed |
| Stage 1 latent transform construction | passed |
| MacroFinance matched-DGP client gate | passed |
| Old mismatched Phase 4 data used as evidence | no |
| Posterior convergence, MAP-quality, sampler, or GPU/XLA promotion claimed | no |

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stage 2 implementation passed focused checks and Claude read-only post-review |
| Primary criterion status | passed focused BayesFilter and MacroFinance compatibility checks |
| Veto diagnostic status | no MAP/truth conflation, signature acceptance, covariance-source omission, orientation ambiguity, reconstruction failure, or target/data/prior change observed |
| Main uncertainty | this is an artifact contract only; later phases still own diagnostics, manifests, parity gates, invalid-region policy, tuning, and migration |
| Next justified action | advance to Stage 3, HMC diagnostics and classification |
| What is not concluded | no posterior convergence, production MAP quality, sampler superiority, default HMC replacement, empirical validity, GPU/XLA readiness, or production readiness |

## Post-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_2_precomputed_map_mass_artifact_post_review_round_01.md` returned `VERDICT: PROCEED`.
