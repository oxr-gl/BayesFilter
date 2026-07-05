# Phase 1 Subplan: Generic SSM Contract Scaffold

Date: 2026-07-03

Status: `DRAFT_AWAITING_PHASE0_GATE`

## Phase Objective

Add the smallest BayesFilter-owned generic SSM contract scaffold needed to
describe Bayesian nonlinear SSM targets, parameter charts, priors, filter
programs, and frozen transports without implementing a full filter or HMC
runtime.

Objective-surface minimum for Phase 1:

- Bayesian nonlinear SSM target identity: problem ID, static shape, data
  signature, target coordinate convention, and manifest hash fields.
- Parameter chart: parameter names, unconstrained dimension, constrained shape,
  transform manifest, and log-Jacobian convention fields.
- Prior: prior manifest, prior support policy, and prior log-density authority
  fields.
- Filter program: filter ID, required model capabilities, deterministic target
  policy, approximation semantics, and manifest hash fields.
- Frozen transport: transport ID, dimension, target-signature binding,
  log-Jacobian availability, and manifest hash fields.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result states `PHASE0_GATE_PASSED`.
- Master program and visible runbook exist.
- Phase 1 subplan has passed local and Claude read-only review.
- No human-required stop condition is active.

Concrete inherited Phase 0 decisions Phase 1 must preserve:

- Codex remains supervisor/executor; Claude remains read-only reviewer.
- No training, HMC, GPU run, package install, network fetch, or detached
  execution is authorized by Phase 1.
- TensorFlow/TFP remains the default implementation backend for differentiable
  paths.
- NeuTra training remains GPU-default and out of scope for Phase 1.
- Existing dirty user work must be preserved.
- Phase 1 may add only the required source/export/test/result artifacts unless
  the Phase 1 result records a blocker requiring human direction.

## Required Artifacts

- Source module:
  `bayesfilter/ssm/contracts.py`
- Package export:
  `bayesfilter/ssm/__init__.py`
- Focused tests:
  `tests/test_general_ssm_contracts.py`
- Phase 1 result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-result-2026-07-03.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-subplan-2026-07-03.md`

## Required Checks, Tests, And Reviews

Local checks:

- `python -m pytest tests/test_general_ssm_contracts.py -q -p no:cacheprovider`
- Import check for `bayesfilter.ssm`.
- Static manifest/signature stability checks in the focused tests.
- Public namespace/export allowlist test for `bayesfilter.ssm.__all__`.
- Existing import boundary smoke:
  `python - <<'PY'` importing `bayesfilter`, `bayesfilter.inference`, and
  `bayesfilter.ssm`.
- Focused tests must include one positive and one fail-closed case for each
  objective surface: SSM target identity, parameter chart, prior, filter
  program, and frozen transport.

Review:

- Claude read-only review of Phase 2 subplan before crossing to Phase 2.
- Claude review of Phase 1 public surface is required if any symbol outside the
  reviewed `bayesfilter.ssm` allowlist is exported or any existing public module
  other than `bayesfilter/ssm/__init__.py` and top-level import wiring is
  changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter represent a generic Bayesian SSM target boundary with stable manifests and fail-closed metadata checks? |
| Baseline/comparator | Existing `NonlinearSSMAdapterContract`, `ValueScoreCapability`, and stable signature discipline. |
| Primary pass criterion | Focused tests pass and the scaffold represents every Phase 1 objective surface with stable manifests while rejecting missing dimensions, duplicate parameters, process-local identities, missing prior/filter/transport bindings, and unknown HMC target policies. |
| Veto diagnostics | Any unstable signature, process-local identity in manifest, missing parameter chart hash, missing prior manifest, missing filter capability declaration, missing frozen-transport target binding, or import/export failure. |
| Explanatory diagnostics | Number of dataclasses/protocols, manifest payload examples, and test count. |
| Not concluded | No likelihood correctness, no filter implementation, no XLA readiness, no HMC readiness, no NeuTra artifact compatibility. |
| Artifacts | Source module, tests, Phase 1 result. |

## Forbidden Claims And Actions

- Do not implement training or HMC.
- Do not add a production default.
- Do not modify existing filter algorithms unless a test reveals an import
  boundary issue.
- Do not use NumPy in BayesFilter-owned differentiable implementation code.
- Do not claim any existing external model now satisfies the generic interface.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- focused tests pass;
- Phase 1 result states `PHASE1_GATE_PASSED`;
- new public symbols are exported intentionally or kept internal intentionally;
- Phase 1 result records exact exported symbol allowlist;
- Phase 1 result records exact internal-only helper symbols, if any;
- Phase 1 result records guaranteed manifest/schema fields for SSM target
  identity, parameter chart, prior, filter program, and frozen transport;
- Phase 1 result records validation behaviors now guaranteed by tests;
- Phase 1 result records unresolved nonclaims/blockers that Phase 2 must
  preserve;
- Phase 2 subplan is refreshed and reviewed;
- no unresolved public API blocker remains.

## Stop Conditions

Stop if:

- the scaffold would require rewriting existing nonlinear/filter modules;
- contract tests cannot distinguish stable manifests from process-local object
  identities;
- public API naming needs human direction;
- Claude and Codex do not converge after five review rounds for a material
  Phase 2 boundary issue.

## Phase Execution Steps

1. Add contract dataclasses/protocols under `bayesfilter/ssm`.
2. Add focused tests for stable signatures and fail-closed validation.
3. Run local tests.
4. Write Phase 1 result.
5. Refresh Phase 2 subplan with actual exported names.
6. Review Phase 2 subplan before crossing.

## End-Of-Subplan Closeout Requirements

The Phase 1 result must include:

- source paths;
- exact exported symbol inventory;
- exact internal-only helper inventory, if any;
- tests run and each test's role in the evidence contract;
- gate status;
- veto diagnostic status;
- guaranteed manifest/schema fields;
- guaranteed validation behaviors;
- unresolved blockers and nonclaims;
- consumer-facing assumptions that Phase 2 may rely on;
- exact Phase 2 handoff status.
