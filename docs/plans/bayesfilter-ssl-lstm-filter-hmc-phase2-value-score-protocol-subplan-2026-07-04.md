# Phase 2 Subplan: Shared Value/Score Protocol And Diagnostics

Date: 2026-07-04

Status: `DRAFT_FUTURE_PHASE`

## Phase Objective

Define and implement the shared TensorFlow/TFP value-and-score adapter protocol
that all candidate filters must satisfy before HMC or benchmarking. The protocol
must advertise gradient authority explicitly and reject unsupported target
paths.

## Entry Conditions Inherited From Previous Phase

- Phase 1 closed the SSL-LSTM model, priors, transforms, shapes, and invariant
  metric definitions.
- The target remains HMC over parameters for a declared filter likelihood.
- Analytic or manual VJP gradients are required for target paths.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-result-2026-07-04.md`
- Code changes, if needed, under BayesFilter-owned TensorFlow/TFP adapter
  surfaces.
- Adapter metadata schema tying each filter to `ValueScoreCapability` or a
  stricter project equivalent.
- Gradient authority labels for fixed SGQF, UKF, Zhao-Cui fixed branch, and LEDH
  manual VJP.
- JSON/Markdown artifact schema for value, score, finite-difference check, JIT
  mode, device, seed policy, and nonclaims.
- Refreshed Phase 3 subplan.

## Required Checks, Tests, And Reviews

- Unit tests for adapter contract validation and failure on unsupported gradient
  authority.
- Small CPU debug import/shape checks are allowed but must be labeled as debug.
- XLA/JIT defaults must be checked for production-like paths unless a reviewed
  exception is recorded.
- Finite-difference checks are independent diagnostics only, not target gradient
  implementation.
- Claude read-only review for the protocol and any public-facing authority
  labels.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can all candidate filters expose a common deterministic value/score contract suitable for HMC? |
| Baseline/comparator | Existing `posterior_adapter.py`, HMC runtime contract, fixed SGQF/UKF score APIs, Zhao-Cui score APIs, and LEDH value/score surfaces. |
| Primary pass criterion | Contract tests pass and unsupported target gradient routes fail closed. |
| Veto diagnostics | GradientTape marked as target authority, missing shape signature, non-deterministic seed policy, non-finite value/score on the smoke fixture, or no artifact schema. |
| Explanatory diagnostics | Runtime, compile mode, score norm, and finite-difference residuals. |
| Not concluded | No filter accuracy, no HMC convergence, no SSL-LSTM estimation success. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not promote automatic differentiation through the filter as the requested
  target gradient path.
- Do not change default policies or public API without a reviewed artifact and
  user approval.
- Do not rank filters from protocol checks.
- Do not run long HMC chains.
- Do not use NumPy for BayesFilter-owned differentiable implementation paths.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only when:

- the shared adapter protocol is implemented or confirmed sufficient;
- contract tests pass;
- artifact schema is locked for value/score evidence;
- SGQF and UKF target gradient authorities are identified as analytic paths to
  be implemented or wired in Phase 3;
- Phase 3 subplan is refreshed and reviewed.

## Stop Conditions

- Existing HMC runtime cannot consume the planned value/score contract without a
  larger architecture decision.
- The required authority labels conflict with current BayesFilter policy.
- Deterministic fixed-shape execution cannot be represented in the artifact
  schema.
- A public API or default-policy change is required before user approval.

## End-Of-Phase Protocol

1. Run protocol unit tests and focused import/shape checks.
2. Write the Phase 2 result/close record.
3. Draft or refresh the Phase 3 subplan.
4. Review Phase 3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
