# BayesFilter-MacroFinance Phase 4 Result: Finite Invalid-Region Target Policy

Date: 2026-06-09

## Status

`PASSED`

## Role And Runtime Classification

Codex is supervisor and executor. Claude is read-only reviewer only.

Runtime classification:

- BayesFilter library primitive: deterministic target-wrapper fixture/test
  helper for known invalid target regions.
- MacroFinance compatibility: no-HMC stress-direction classification around the
  current matched-DGP Phase 4 artifact surface.
- No HMC chain execution, tuning change, posterior convergence, sampler
  superiority, empirical validity, GPU/XLA readiness, default target policy, or
  production readiness is authorized by this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter provide deterministic finite invalid-region target handling for known target-support failures while preserving fail-loud behavior for programmer errors, shape errors, and ambiguous backend numerical breakdowns? |
| Baseline/comparator | Accepted Phase 4 of `docs/plans/bayesfilter_macrofinance_hmc_filtering_consolidation_plan_2026_06_09.md`, visible runbook Stage 6, current BayesFilter value/score and HMC target wrappers, Stage 3 HMC diagnostics, Stage 5 parity gates, and current MacroFinance matched-DGP stress/failure artifacts. |
| Primary criterion | A BayesFilter-owned policy wrapper handles only explicitly declared target-region failures or nonfinite value/score returns with deterministic low log density, finite fallback gradient, bounded branch labels, and diagnostics; shape/programmer exceptions still raise; valid Gaussian and LGSSM fixture evaluations do not take fallback; MacroFinance stress rows are classified as target boundary, backend numerical breakdown, sampler energy error, or unknown/ambiguous without changing the target silently. |
| Veto diagnostics | Fallback masks shape errors or programmer errors; fallback value depends on nondeterministic state; failure labels are missing or unbounded; fallback cannot distinguish declared target support exclusion from backend numerical breakdown; valid targets take fallback; or the phase changes HMC tuning/default runtime behavior. |
| Repair triggers | Missing policy helper/export/test, overbroad exception catching, nonfinite fallback gradient, unbounded branch labels, fallback activation on valid fixtures, MacroFinance stress classifier ambiguity not labeled, or Claude `NEEDS_REVISION` with fixable findings. |
| Explanatory diagnostics | Exact exception classes caught, fallback value/gradient, branch labels, target scope, stress direction labels, and whether a failure is support, stationarity, covariance positive definiteness, factorization, solve residual, nonfinite value/gradient, sampler energy, backend numerical breakdown, or ambiguous. |
| Non-claims | Passing this phase does not prove posterior convergence, sampler robustness, global target validity, numerical backend superiority, GPU/XLA readiness, or default-policy readiness. |

## Skeptical Audit

- Wrong baseline: The baseline is accepted Phase 4 and current matched-DGP
  stress/failure surfaces, not a fresh HMC tuning ladder or old mismatched
  Phase 4 data.
- Proxy metric promotion: Finite fallback behavior is an engineering validity
  gate only. It is not evidence that a chain samples correctly or that a target
  is globally well behaved.
- Stop conditions: Overbroad catching, masked shape/programmer errors,
  nondeterministic fallback, unbounded labels, or ambiguous backend breakdown
  reported as valid support exclusion stop the stage until repaired.
- Fair comparison: Valid fixture targets must be compared with and without the
  policy to prove fallback did not activate.
- Hidden assumptions: Only declared target-region exceptions or nonfinite
  target outputs are eligible for fallback. Generic `Exception`, `ValueError`,
  `RuntimeError`, TensorFlow shape errors, and programmer bugs are not
  catch-all fallback authorities.
- Stale context: BayesFilter and MacroFinance both have dirty worktrees;
  unrelated changes must not be reverted.
- Environment/import mismatch: BayesFilter tests run from
  `/home/ubuntu/python/BayesFilter`; MacroFinance compatibility should use
  `PYTHONPATH=/home/ubuntu/python/BayesFilter` and CPU-only no-HMC settings.
- Artifact relevance: Required artifacts are this result note, focused
  BayesFilter target-policy tests, a MacroFinance stress classifier
  compatibility test, and Claude read-only pre/post reviews.
- Role-contract check: Claude pre-review must be read-only; Codex performs all
  edits and tests.
- BayesFilter/MacroFinance ownership: Reusable target failure policy belongs in
  BayesFilter; MacroFinance remains a client fixture and should not force
  MacroFinance-specific fields into BayesFilter.

## Current Code Audit

BayesFilter currently builds target wrappers through
`bayesfilter.inference.hmc._make_hmc_target_log_prob_fn` and
`_make_tfp_target_log_prob_fn`. These wrappers validate value/score authority
but do not provide a reusable finite invalid-region policy.

BayesFilter diagnostics can already classify nonfinite arrays and log-accept
hard vetoes, and Stage 5 parity gates can label branch/failure policies, but
there is no policy primitive that says which target failures may receive a
deterministic finite fallback and which exceptions must remain loud.

MacroFinance matched-DGP Phase 4 artifacts currently classify hard HMC screens
and nonfinite traces after the fact. Stage 6 should add a no-HMC compatibility
classifier for stress-direction target evaluations; it should not change the
current MacroFinance likelihood, priors, data payload, HMC config, or default
sampler behavior.

## Planned Minimal Implementation

1. Add a BayesFilter module such as
   `bayesfilter/inference/target_failure_policy.py`.
2. Define explicit exception classes for declared target-region failures, for
   example `TargetRegionError` with subclasses or labels for prior support,
   stationarity, covariance positive definiteness, factorization failure, solve
   residual, and nonfinite value/gradient.
3. Define `TargetFailurePolicy` with deterministic low log density, finite
   fallback gradient strategy, bounded allowed branch labels, target scope, and
   nonclaims.
4. Provide a value/score wrapper that catches only declared
   `TargetRegionError` subclasses and nonfinite value/score returns from an
   otherwise successful target call. It must not catch shape errors,
   programmer errors, generic `ValueError`, generic `RuntimeError`, or TensorFlow
   shape/type exceptions.
5. Return a structured result with value, score, branch label, failure label,
   fallback-used flag, and diagnostics. If a caller needs a pure callable for
   HMC, that callable should be opt-in and should preserve the same branch
   diagnostics when possible.
6. Add focused tests:
   known invalid support returns deterministic low finite value and finite
   gradient;
   programmer and shape errors still raise;
   branch labels are stable and bounded;
   nonfinite value/gradient is classified;
   valid Gaussian fixture does not use fallback;
   valid LGSSM fixture does not use fallback.
7. Add MacroFinance compatibility test that evaluates selected current
   matched-DGP stress directions through a BayesFilter classifier and labels the
   outcome as target boundary, backend numerical breakdown, sampler energy
   error, or ambiguous without changing the target.
8. Export the helper through `bayesfilter.inference` and top-level
   `bayesfilter` if public API tests require it.

## Planned Checks

- `python -m pytest tests/test_common_inference_runtime_contracts.py -q`
- `python -m pytest tests/test_v1_public_api.py -q` if export surface changes.
- Focused BayesFilter linear/LGSSM test if the valid LGSSM no-fallback check is
  added outside the common contract module.
- MacroFinance focused compatibility test with
  `PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1
  PYTHONDONTWRITEBYTECODE=1`, targeting the matched-DGP SVD pilot test module.

If MacroFinance stress classification is ambiguous, the compatibility test must
label it as ambiguous or backend numerical breakdown. It must not convert an
ambiguous nonfinite value into a valid target-boundary fallback claim.

## Pre-Review Request

Claude should verify that this Stage 6 precheck is consistent with accepted
Phase 4, avoids overbroad exception catching, preserves fail-loud
shape/programmer errors, keeps finite fallback deterministic and labeled,
avoids HMC tuning/default changes, and keeps MacroFinance as a client
compatibility fixture.

## Pre-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_6_finite_invalid_region_pre_review_round_01.md`
  returned `VERDICT: NEEDS_REVISION` because the live ledger header still said
  `ACTIVE_STAGE_5_PRECHECK`.
- Codex patched the live ledger header to `ACTIVE_STAGE_6_PRECHECK` without
  changing the Stage 6 scientific contract.
- `docs/plans/bayesfilter_macrofinance_stage_6_finite_invalid_region_pre_review_round_02.md`
  returned `VERDICT: PROCEED`.
- Implementation must prove the three-way distinction between declared
  support exclusions, ambiguous backend numerical breakdowns, and
  programmer/shape bugs.

## Implementation Summary

Implemented an opt-in BayesFilter target failure policy in
`bayesfilter/inference/target_failure_policy.py`.

The implementation adds:

- `TargetRegionError` base class;
- `PriorSupportError`;
- `StationarityError`;
- `CovariancePositiveDefiniteError`;
- `FactorizationFailure`;
- `SolveResidualError`;
- `TargetFailurePolicy`;
- `TargetPolicyEvaluation`;
- `TargetFailureClassification`;
- `evaluate_target_with_failure_policy(...)`;
- `classify_target_failure_mode(...)`.

The evaluator catches only declared `TargetRegionError` subclasses and
nonfinite value/score returns from an otherwise successful target call. It does
not catch generic `Exception`, `ValueError`, `RuntimeError`, TensorFlow shape or
type exceptions, or programmer bugs. Shape mismatches between the supplied
position and returned score also fail loudly.

The policy records deterministic finite fallback value, deterministic finite
fallback gradient, bounded allowed failure labels, bounded allowed branch
labels, target scope, diagnostics, and nonclaims. The classifier separates:

- declared target boundary (`prior_support`, `stationarity`,
  `covariance_positive_definite`);
- backend numerical breakdown (`factorization_failure`, `solve_residual`);
- ambiguous nonfinite target/backend evidence (`nonfinite_value_gradient`);
- sampler energy error when a valid target evaluation is paired with sampler
  hard-veto diagnostics;
- valid target region when no fallback is used.

The helper is not wired into default HMC execution and does not change HMC
tuning or sampler policy.

Exports were updated through `bayesfilter.inference` and top-level lazy
`bayesfilter`.

## MacroFinance Compatibility Pin

Exact MacroFinance compatibility test:

- `/home/ubuntu/python/MacroFinance/tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_target_failure_policy_classifies_matched_dgp_stress_rows`

Exact current matched-DGP artifact used by that test:

- `/home/ubuntu/python/MacroFinance/results/hmc/mixed_frequency_tfp_phase4_matched_dgp_hessian_scaled_initialization_gate.json`

The compatibility test evaluates current matched-DGP SVD-derived stress rows
with the BayesFilter policy and confirms they remain valid without fallback.
It also uses synthetic declared BayesFilter exceptions to verify separate
classification of target boundary and backend numerical breakdown, and pairs a
valid target evaluation with hard-veto sampler diagnostics to classify sampler
energy error. No MacroFinance likelihood, priors, data payload,
parameterization, HMC config, or default sampler behavior were changed.

## Files Touched For Stage 6

BayesFilter:

- `bayesfilter/inference/target_failure_policy.py`
- `bayesfilter/inference/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_common_inference_runtime_contracts.py`
- `tests/test_linear_kalman_svd_tf.py`
- `tests/test_v1_public_api.py`
- `docs/plans/bayesfilter_macrofinance_phase_4_finite_invalid_region_target_policy_result_2026_06_09.md`
- `docs/plans/bayesfilter_macrofinance_stage_6_finite_invalid_region_pre_review_round_01.md`
- `docs/plans/bayesfilter_macrofinance_stage_6_finite_invalid_region_pre_review_round_02.md`

MacroFinance:

- `tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`
- `docs/plans/bayesfilter_macrofinance_visible_execution_ledger_2026_06_09.md`

## Checks Run

| Command | Result | Role |
| --- | --- | --- |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | `46 passed in 0.23s` | BayesFilter target policy contract gate |
| `python -m pytest tests/test_v1_public_api.py -q` from `/home/ubuntu/python/BayesFilter` | `4 passed, 2 warnings in 2.61s` | Public export/lazy import gate |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_linear_kalman_svd_tf.py::test_target_failure_policy_does_not_activate_on_valid_lgssm_value -q` from `/home/ubuntu/python/BayesFilter` | `1 passed, 1007 warnings in 3.39s` | LGSSM valid no-fallback gate |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_linear_kalman_svd_tf.py -q` from `/home/ubuntu/python/BayesFilter` | `10 passed, 5077 warnings in 6.62s` | BayesFilter SVD module compatibility |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_target_failure_policy_classifies_matched_dgp_stress_rows -q` from `/home/ubuntu/python/MacroFinance` | `1 passed, 2 warnings in 9.36s` | MacroFinance target policy compatibility gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py -q` from `/home/ubuntu/python/MacroFinance` | `14 passed, 20867 warnings in 159.36s` | Full matched-DGP compatibility module |

Warnings were TensorFlow Probability `distutils` deprecations, `gast`
deprecations, and BayesFilter `.pytest_cache` write warnings from a read-only
cache path. They are explanatory only for this no-HMC target-policy gate.

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stage 6 implementation ready for Claude read-only post-review |
| Primary criterion status | Passed focused BayesFilter and MacroFinance no-HMC target-policy gates |
| Veto diagnostic status | No overbroad catch, masked shape/programmer error, nondeterministic fallback, unbounded label, valid-fixture fallback, or HMC tuning/default change observed |
| Main uncertainty | Classifier is local diagnostic evidence; stronger target-boundary semantics require future target-specific contracts |
| Next justified action | Claude read-only post-review |
| What is not concluded | No posterior convergence, sampler robustness, global target validity, backend superiority, GPU/XLA readiness, default-policy readiness, or production readiness |

## Post-Run Red Team

Strongest alternative explanation: the policy is correct for declared
BayesFilter exceptions but future client targets may mislabel backend numerical
breakdowns as support exclusions.

What would overturn the Stage 6 gate: a reproduced path where generic
programmer/shape errors are swallowed, fallback labels are unbounded, fallback
values or gradients are nonfinite/nondeterministic, valid Gaussian/LGSSM or
matched-DGP rows activate fallback, or ambiguous backend breakdown is reported
as target support exclusion.

Weakest evidence: MacroFinance compatibility uses current matched-DGP stress
rows and synthetic declared exceptions for taxonomy coverage; it is not a
global search over all target boundary cases.

## Post-Review Request

Claude should verify that the implementation satisfies accepted Phase 4,
preserves fail-loud shape/programmer errors, avoids overbroad exception
catching, keeps fallback deterministic and bounded, distinguishes declared
target boundary/backend breakdown/ambiguous nonfinite/sampler energy classes,
does not change HMC defaults or tuning, and preserves BayesFilter/MacroFinance
ownership boundaries.

## Post-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_6_finite_invalid_region_post_review_round_01.md`
  returned `VERDICT: PROCEED`.
- Claude confirmed no wrong-baseline drift, no proxy promotion, no missing stop
  conditions, narrow exception boundaries, fail-loud shape/programmer errors,
  deterministic finite fallback, bounded labels, no ambiguous evidence promoted
  to support exclusion, valid Gaussian/LGSSM/MacroFinance rows avoiding
  fallback, no HMC default/tuning change, no ownership drift, and no artifact
  mismatch.
- Residual risks: MacroFinance target-boundary/backend-breakdown taxonomy
  coverage is synthetic; custom allowed-label subsets can intentionally make
  nonfinite fallback fail loudly; sampler-energy classification is broad for
  local diagnostics.
