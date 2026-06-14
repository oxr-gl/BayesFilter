# BayesFilter Common Filtering/HMC Refactor Result

Date: 2026-06-06

## Scope

This result note records bounded infrastructure work only. It does not run or
interpret DSGE, MacroFinance, NeuTra, score-matching, empirical HMC, or GPU
experiments.

## Skeptical Execution Audit

Status: passed before implementation.

- Wrong baseline: no baseline experiment was launched.
- Proxy metrics: compile and focused tests are engineering checks only.
- Stop conditions: no BayesFilter filtering equations, target definitions,
  sampler transition math, priors, or evidence criteria were changed.
- Environment mismatch: no GPU probe was required; CPU-only helpers enforce
  pre-import `CUDA_VISIBLE_DEVICES=-1` semantics.
- Artifact fit: this note preserves the engineering change and nonclaims.

## Command Log

Commands run from `/home/ubuntu/python/BayesFilter` unless stated otherwise:

- `git status --short`
- `python -m py_compile bayesfilter/inference/posterior_adapter.py bayesfilter/inference/hmc.py bayesfilter/inference/mass_matrix.py bayesfilter/inference/hmc_diagnostics.py bayesfilter/runtime/device_policy.py bayesfilter/runtime/runner.py bayesfilter/runtime/selection.py`
- `pytest -q tests/test_common_inference_runtime_contracts.py tests/test_macrofinance_adapter.py tests/test_macrofinance_linear_compat_tf.py tests/test_hmc_linear_qr_readiness_tf.py tests/test_backend_readiness.py tests/test_dsge_adapter_gate.py tests/test_v1_public_api.py`
- `python -m py_compile bayesfilter/inference/posterior_adapter.py bayesfilter/inference/hmc.py bayesfilter/inference/mass_matrix.py bayesfilter/inference/hmc_diagnostics.py bayesfilter/runtime/device_policy.py bayesfilter/runtime/runner.py bayesfilter/runtime/selection.py > docs/plans/artifacts/bayesfilter-common-filtering-hmc-refactor-pycompile-2026-06-06.txt 2>&1`
- `pytest -q tests/test_common_inference_runtime_contracts.py tests/test_macrofinance_adapter.py tests/test_macrofinance_linear_compat_tf.py tests/test_hmc_linear_qr_readiness_tf.py tests/test_backend_readiness.py tests/test_dsge_adapter_gate.py tests/test_v1_public_api.py > docs/plans/artifacts/bayesfilter-common-filtering-hmc-refactor-focused-pytest-2026-06-06.txt 2>&1`

## Run Manifest

- Git commit before implementation: `3dac444c22e8a366063f0fa0a73788cc9db96201`.
- Dirty status after implementation: modified `bayesfilter/__init__.py`,
  `tests/test_macrofinance_adapter.py`, and
  `tests/test_macrofinance_linear_compat_tf.py`; added `bayesfilter/inference/`,
  `bayesfilter/runtime/`,
  `tests/test_common_inference_runtime_contracts.py`, and this result note.
- CPU/GPU status: no GPU probe or GPU run was performed. CPU-only policy was
  tested as environment metadata/guard behavior only.
- External repositories: DSGE and MacroFinance were reference-only; no edits.

## Verification Results

- `py_compile`: passed for the new inference/runtime modules.
- `py_compile` output artifact:
  `docs/plans/artifacts/bayesfilter-common-filtering-hmc-refactor-pycompile-2026-06-06.txt`.
- Focused pytest output artifact:
  `docs/plans/artifacts/bayesfilter-common-filtering-hmc-refactor-focused-pytest-2026-06-06.txt`.
- Focused pytest after Claude review round-4 fixes:
  `49 passed, 17 skipped, 2 warnings`.
- Skips: optional MacroFinance checkout tests skipped unless
  `BAYESFILTER_MACROFINANCE_ROOT` is set.
- Warnings: TensorFlow Probability deprecation warnings from the installed
  environment, not from the new BayesFilter contracts.

## Implementation Summary

- Added model-agnostic posterior value/score authority contracts under
  `bayesfilter/inference/`.
- Added fail-closed HMC target helper, precomputed MAP validation, stable adapter
  signatures, and dense whitening orientation helpers.
- Added mass-matrix provenance utilities and operational HMC diagnostics that do
  not claim convergence.
- Added runtime device-policy, robust-runner metadata/hash/JSON helpers, and
  candidate selection utilities that preserve index order and tie behavior.
- Removed the stale user-specific MacroFinance checkout path from tests; optional
  MacroFinance tests now require `BAYESFILTER_MACROFINANCE_ROOT`.

## Nonclaims

- No scientific posterior validity or HMC convergence claim is made.
- No default inference policy is promoted.
- No cross-repo integration has been migrated yet; this is the shared contract
  layer for future repo-local integration work.
- Existing MacroFinance adapter fields named `convergence_claim` remain legacy
  compatibility shims only and are not used by the new core contracts.

## Claude Review

- Round 1: `NEEDS_REVISION`.
  - Fixed remaining hard-coded optional MacroFinance root in
    `tests/test_macrofinance_linear_compat_tf.py`.
  - Added `tests/test_v1_public_api.py` to the focused verification set because
    top-level exports changed.
- Round 2: `NEEDS_REVISION`.
  - Fixed explicit `adapter_signature` validation so process-local object IDs or
    object-repr strings fail closed before becoming persisted reuse guards.
- Round 3: `NEEDS_REVISION`.
  - Added target-scope binding for reviewed GradientTape XLA exceptions so a
    reviewed exception cannot silently authorize an unrelated target.
  - Preserved focused pytest output as a checkable artifact on rerun.
- Round 4: `NEEDS_REVISION`.
  - Fixed stale review bookkeeping in this result note.
  - Rewrote the compile artifact with command text and an explicit pass marker.
  - Added top-level public API verification for the new inference/runtime
    exports.
  - Added an independent covariance-shape mismatch test for precomputed MAP
    validation.
- Round 5: `CONVERGED_NO_MATERIAL_FINDINGS`.
  - Claude reported no material findings in the reviewed source diff, artifacts,
    result note, or scope discipline.
  - Non-material generated `__pycache__/` files from verification were removed
    after the review.

## Residual Risks

- The new HMC helpers are contract utilities, not a full production sampler.
- External DSGE/MacroFinance adoption still needs repo-local migration plans and
  tests.
- Optional MacroFinance reference tests skip unless the checkout path is provided
  explicitly through `BAYESFILTER_MACROFINANCE_ROOT`.

## Post-Run Red-Team Note

The strongest alternative explanation for a passing test suite is that the new
contracts are too small to reveal integration mistakes. The next evidence needed
is repo-local adoption in one bounded runner without changing model math.
