# BayesFilter-MacroFinance Phase 1 Result: Latent Affine HMC Transform

Date: 2026-06-09

## Status

`PASSED`

## Role And Runtime Classification

Codex is supervisor and executor. Claude is read-only reviewer only.

Runtime classification:

- BayesFilter library primitive: NumPy verification oracle and deterministic
  fixture/test helper for this phase.
- No long-run HMC, posterior convergence, GPU/XLA readiness, default sampler
  promotion, or empirical claim is authorized by this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter promote the existing latent-coordinate helper functions into a first-class metadata-bearing affine HMC transform without changing the scalar target or the row-vector score convention MacroFinance currently relies on? |
| Baseline/comparator | Current BayesFilter `latent_to_position` and `latent_value_and_score` helpers in `bayesfilter/inference/hmc.py`; MacroFinance `_parameter_from_latent` and latent-score mapping in `MacroFinance/inference/hmc.py`; accepted consolidation plan Phase 1. |
| Primary criterion | A BayesFilter-owned transform records center, factor, orientation, covariance provenance, and log-Jacobian convention; maps `theta = center + z @ L.T`; maps `grad_z = L.T @ grad_theta`; provides inverse when the factor is nonsingular; focused tests pass. |
| Veto diagnostics | Any orientation ambiguity, any value/gradient mismatch, silent log-Jacobian convention drop, nonfinite factor accepted, shape mismatch accepted, or MacroFinance compatibility changing model target/data/priors. |
| Repair triggers | Missing metadata field, missing export, failed finite-difference parity, failed dense factor reconstruction/inverse, inability to run the matched-DGP MacroFinance compatibility gate with explicit local import path, or stale result note. |
| Explanatory diagnostics | Runtime, formatting, exact class name, and whether the wrapper reuses the old helper functions. |
| Non-claims | No posterior convergence, sampler superiority, empirical validity, GPU/XLA readiness, or default HMC replacement is concluded. |

## Skeptical Audit

- Wrong baseline: The baseline is the current BayesFilter helpers plus the
  current MacroFinance matched-DGP latent wrapper, not old mismatched Phase 4
  data or a fresh transform authority invented outside BayesFilter.
- Proxy metric promotion: No runtime, acceptance, short-chain diagnostic, or
  HMC result is a promotion criterion in this phase.
- Stop conditions: Orientation ambiguity, gradient parity failure, or missing
  log-Jacobian convention stop the phase until repaired.
- Fair comparison: BayesFilter and MacroFinance must use the same center,
  factor, row-vector convention, and target value/score function.
- Hidden assumptions: The current helper name `whitening_factor` is not enough
  semantic authority; the new contract must persist factor orientation.
- Stale context: BayesFilter and MacroFinance both have dirty worktrees;
  unrelated changes must not be reverted.
- Environment/import mismatch: Focused BayesFilter tests should run from
  `/home/ubuntu/python/BayesFilter`; MacroFinance compatibility must use an
  explicit `PYTHONPATH=/home/ubuntu/python/BayesFilter` if importing the local
  library.
- Artifact relevance: The required artifacts are this result note, focused
  BayesFilter tests, and Claude read-only pre/post reviews.
- Role-contract check: Claude pre-review must be read-only; Codex performs all
  edits and tests.
- BayesFilter/MacroFinance ownership: The reusable transform belongs in
  `bayesfilter.inference`; MacroFinance remains a compatibility client.

## Current Code Audit

BayesFilter already has useful primitives:

- `latent_to_position(z, center, whitening_factor)` implements
  `center + z @ factor.T`.
- `latent_value_and_score(...)` evaluates the target at the mapped position and
  returns `factor.T @ grad_theta`.

The gap is that these free functions do not yet carry semantic authority for
factor orientation, covariance provenance, inverse support, shape validation,
or log-Jacobian convention.

MacroFinance currently uses the same row-vector mapping in
`/home/ubuntu/python/MacroFinance/inference/hmc.py::_parameter_from_latent`.
The companion analytic score path should be checked against that source during
the MacroFinance compatibility gate rather than inferred from this precheck.

## MathDevMCP Orientation Gate

For `theta = c + z L.T` in two dimensions, MathDevMCP/SymPy checked:

- `d/dz1 [g . theta(z)] = l11*g1 + l21*g2`;
- `d/dz2 [g . theta(z)] = l12*g1 + l22*g2`.

Both obligations returned `status=equivalent`, certifying the local chain-rule
orientation `grad_z = L.T @ grad_theta`.

## Planned Minimal Implementation

1. Add `LatentAffineHMCTransform` in `bayesfilter/inference/hmc.py` with:
   center, factor, `factor_orientation="row_right_transpose"`,
   covariance_provenance, log-Jacobian convention, and nonclaims.
2. Validate center/factor shape, finite values, square factor, and supported
   orientation.
3. Provide methods:
   `latent_to_position`, `position_to_latent`,
   `theta_score_to_latent_score`, and `value_and_score`.
4. Keep the existing free functions as compatibility wrappers around the same
   convention.
5. Export the new transform from `bayesfilter.inference` and the package public
   API if the existing public-API test requires it.
6. Add focused tests for dense non-diagonal parity, inverse reconstruction,
   batched row-vector parity, batched shape, shape mismatch, nonfinite factor
   rejection, and helper-wrapper compatibility.

## Planned Checks

- `python -m pytest tests/test_common_inference_runtime_contracts.py -q`
- `python -m pytest tests/test_v1_public_api.py -q` if the public export is
  touched.
- MacroFinance matched-DGP compatibility check after implementation using the
  current Phase 4 matched-DGP adapter path at `z=0` and two Hessian-scaled
  stress directions, with `PYTHONPATH=/home/ubuntu/python/BayesFilter` or an
  equivalent explicit local import contract recorded in the result note.

If the matched-DGP MacroFinance gate cannot be run because of import-path,
environment, stale-artifact, or fixture issues, Stage 1 enters the repair loop.
It must not substitute a looser synthetic-only compatibility check for the
accepted real client gate.

## Pre-Review Request

Claude should verify that this Stage 1 precheck is consistent with the accepted
consolidation plan, does not change the scalar target, preserves the
row-vector orientation, avoids proxy-metric claims, and does not treat a
fixable implementation issue as a human stop.

## Pre-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_1_latent_affine_hmc_transform_pre_review_round_01.md` returned `VERDICT: NEEDS_REVISION`; Codex accepted and repaired all material findings.
- `docs/plans/bayesfilter_macrofinance_stage_1_latent_affine_hmc_transform_pre_review_round_02.md` returned `VERDICT: PROCEED`; implementation may proceed.

## Implementation Summary

Implemented a BayesFilter-owned `LatentAffineHMCTransform` in
`bayesfilter/inference/hmc.py`.

The transform records:

- `center`;
- `factor`;
- `factor_orientation="row_right_transpose"`;
- `covariance_provenance`;
- `log_jacobian_convention`, restricted to `constant_omitted` or
  `constant_included`;
- nonclaims.

The implemented mathematical contract is:

\[
  \theta = \theta_c + z L^\top,
  \qquad
  \nabla_z f(\theta(z)) = L^\top \nabla_\theta f(\theta).
\]

The class provides:

- `latent_to_position(z)`;
- `position_to_latent(theta)` for nonsingular factors;
- `theta_score_to_latent_score(grad_theta)`;
- `value_and_score(z, value_and_grad_fn)`;
- `signature_payload()`.

The existing free functions `latent_to_position(...)` and
`latent_value_and_score(...)` remain compatibility wrappers around the same
row-vector convention.

Exports were updated through `bayesfilter.inference` and the top-level
`bayesfilter` lazy export table. Focused tests were added for dense factor
parity, inverse reconstruction, batched row-vector parity, shape rejection,
nonfinite rejection, and public API visibility.

MacroFinance compatibility was implemented as a focused test in
`/home/ubuntu/python/MacroFinance/tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`.
It uses the current Phase 4 matched-DGP initialization artifact, `z=0`, and the
first two reviewed Hessian-scaled latent stress directions. It compares
BayesFilter's transform against MacroFinance's current `_parameter_from_latent`
and `_chain_log_prob_and_latent_grad` wrapper rows under the explicit local
import contract `PYTHONPATH=/home/ubuntu/python/BayesFilter`.

## Files Touched For Stage 1

BayesFilter:

- `bayesfilter/inference/hmc.py`
- `bayesfilter/inference/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_common_inference_runtime_contracts.py`
- `tests/test_v1_public_api.py`
- `docs/plans/bayesfilter_macrofinance_phase_1_latent_affine_hmc_transform_result_2026_06_09.md`
- `docs/plans/bayesfilter_macrofinance_stage_1_latent_affine_hmc_transform_pre_review_round_01.md`
- `docs/plans/bayesfilter_macrofinance_stage_1_latent_affine_hmc_transform_pre_review_round_02.md`

MacroFinance:

- `tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`
- `docs/plans/bayesfilter_macrofinance_visible_execution_ledger_2026_06_09.md`

## Checks Run

| Command | Result | Role |
| --- | --- | --- |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | `22 passed in 0.14s` after final inverse patch | BayesFilter focused contract gate |
| `python -m pytest tests/test_v1_public_api.py -q` from `/home/ubuntu/python/BayesFilter` | `4 passed, 2 warnings in 2.43s` after final inverse patch | BayesFilter public export gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_latent_affine_transform_matches_matched_dgp_wrapper_rows -q` from `/home/ubuntu/python/MacroFinance` | `1 passed, 2 warnings in 12.07s` | Direct MacroFinance matched-DGP client compatibility gate |
| `python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py -q` from `/home/ubuntu/python/MacroFinance` | `8 passed, 20867 warnings in 105.11s` | Existing real-client matched-DGP suite evidence |

The warnings are TensorFlow Probability `distutils` deprecation warnings and
TensorFlow AutoGraph/gast deprecation warnings; they are explanatory only for
this phase.

## Gate Assessment

| Gate | Status |
| --- | --- |
| Orientation authority persisted | passed |
| Row-vector `theta = center + z @ L.T` mapping | passed |
| Latent score `grad_z = L.T @ grad_theta` | passed |
| Dense and batched parity | passed |
| Shape and nonfinite validation | passed |
| Inverse for nonsingular factor | passed |
| Public export | passed |
| MacroFinance matched-DGP client gate | passed |
| Old mismatched Phase 4 data used as evidence | no |
| Posterior convergence or sampler promotion claimed | no |

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stage 1 implementation passed focused checks and Claude read-only post-review |
| Primary criterion status | passed focused BayesFilter and MacroFinance compatibility checks |
| Veto diagnostic status | no orientation ambiguity, gradient mismatch, nonfinite acceptance, shape acceptance, or target/data/prior change observed |
| Main uncertainty | this is a transform contract only; later phases still own artifact/mass, diagnostics, parity gates, invalid-region policy, tuning, and migration |
| Next justified action | advance to Stage 2, precomputed MAP and mass artifact |
| What is not concluded | no posterior convergence, sampler superiority, default HMC replacement, empirical validity, GPU/XLA readiness, or production readiness |

## Post-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_1_latent_affine_hmc_transform_post_review_round_01.md` returned `VERDICT: PROCEED`.
