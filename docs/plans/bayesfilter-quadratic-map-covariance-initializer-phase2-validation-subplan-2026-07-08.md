# Phase 2 Subplan: Focused Unit Validation

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Validate the reusable quadratic MAP-covariance initializer on controlled
targets and public API checks, without interpreting those tests as HMC readiness
or posterior correctness.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result status: `PASSED_SOURCE_COMPILE_IMPORT_GATE`.
- New initializer source compiles.
- New symbols import through `bayesfilter.inference` and top-level
  `bayesfilter`.
- Accepted covariance path is intended to route through
  `covariance_from_precision`.

## Required Artifacts

- `tests/test_quadratic_map_covariance.py`
- Updated `tests/test_v1_public_api.py` assertions if required by public API
  behavior.
- Focused pytest log or command output recorded in Phase 2 result.
- Phase 2 result record.
- Draft Phase 3 benchmark smoke subplan.

## Required Checks, Tests, Reviews

- Local checks:
  - `pytest tests/test_quadratic_map_covariance.py tests/test_v1_public_api.py -q`
  - `python -m py_compile bayesfilter/inference/quadratic_map_covariance.py`
  - `git diff --check`
- Review:
  - Codex self-review of failures before any repair.
  - Fresh Codex read-only review if a material boundary/sign/authority concern
    remains ambiguous after local inspection.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the initializer behave correctly on controlled unit targets and export surfaces? |
| Baseline/comparator | Closed-form Gaussian/quadratic target with known mode, precision, and covariance; existing public API test behavior. |
| Primary pass criterion | Focused pytest command passes, including mode/covariance recovery, sign convention, fail-closed nonfinite behavior, sample-budget rejection, locator fallback/disabled path, covariance provenance, and public exports. |
| Veto diagnostics | Accepted nonfinite covariance, non-SPD accepted precision, wrong sign convention, BFGS inverse Hessian covariance authority, accepted under-sampled geometry, missing nonclaims, or public API import failure. |
| Explanatory diagnostics | Locator status, geometry status, mass-matrix regularization report, eigen summaries, candidate role, and center-refinement acceptance. |
| Not concluded | No SSL-LSTM covariance quality, global MAP, posterior covariance correctness, HMC readiness, sampler convergence, statistical superiority, default readiness, or Zhao-Cui source faithfulness. |
| Artifact preserving result | Phase 2 result note plus pytest command/log. |

## Forbidden Claims And Actions

- Do not claim HMC readiness, posterior correctness, global MAP, default
  readiness, or Zhao-Cui faithfulness.
- Do not launch HMC, GPU runs, long benchmarks, package installs, commits,
  pushes, or detached supervisors.
- Do not weaken test assertions after seeing failures unless the Phase 2 result
  records why the original assertion was wrong relative to the stated target.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Focused tests pass or a blocker result clearly states why they cannot pass.
- Phase 2 result is written.
- Phase 3 benchmark smoke subplan is drafted with bounded commands and explicit
  nonclaims.

## Stop Conditions

- Focused test failure reveals a sign convention or covariance-authority flaw
  that cannot be repaired within the intended API.
- Public API import behavior conflicts with repository policy.
- Continuing would require HMC/GPU runtime, broad benchmark refactor, package
  install, or external Claude review despite the prior approval rejection.

## Skeptical Plan Audit

| Risk | Phase 2 audit |
| --- | --- |
| Wrong baseline | Baseline is closed-form Gaussian/quadratic behavior, not benchmark/HMC output. |
| Proxy metric promoted | Unit pass only supports API behavior on controlled cases; no scientific claim. |
| Missing stop conditions | Stop conditions are explicit above. |
| Unfair comparison | No method ranking occurs. |
| Hidden assumptions | Tolerances must be justified by deterministic quadratic fixture and existing fit tolerances. |
| Stale context | Tests import current source after Phase 1 edits. |
| Environment mismatch | CPU-safe pytest only; no GPU/HMC evidence. |
| Artifact mismatch | Focused tests directly answer sign/covariance/fail-closed/public API questions. |

Audit status: `PASSED_FOR_PHASE_2_VALIDATION`.
