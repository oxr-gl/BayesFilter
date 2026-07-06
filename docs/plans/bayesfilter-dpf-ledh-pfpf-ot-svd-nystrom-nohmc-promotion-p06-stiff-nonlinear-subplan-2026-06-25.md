# P06 Subplan: Stiff Nonlinear Dynamics Gate

Date: 2026-06-25

Status: `DRAFT_AFTER_P05`

## Phase Objective

Assess fixed SVD-Nystrom under stiff nonlinear dynamics or sharp Jacobian stress
where transport/factor robustness can degrade.

## Entry Conditions Inherited From Previous Phase

- P05 non-Gaussian/heavy-tail gate passed or produced a reviewed non-blocking
  scope decision.
- Candidate policy remains locked.
- A stiff nonlinear fixture or blocker path is identified.

## Required Artifacts

- Per-run JSON/Markdown/log artifacts with prefix
  `svd-nystrom-nohmc-promotion-p06-stiff-nonlinear`.
- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p06-stiff-nonlinear-summary-2026-06-25.json`
- P06 result and refreshed P07 subplan.

## Required Checks, Tests, And Reviews

- Identify stiff nonlinear fixture and comparator before execution.
- Trusted GPU preflight.
- Predeclare deterministic and statistical quality screens.
- Verify finite outputs, route/policy metadata, residuals, no dense
  materialization, and factor/core stability diagnostics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does SVD-Nystrom remain viable under stiff nonlinear dynamics stress? |
| Baseline/comparator | Streaming TF32 route or declared reference. |
| Primary criterion | Deterministic validity and predeclared quality/stability screen pass. |
| Veto diagnostics | Nonfinite outputs, route/policy mismatch, comparator failure, stability/quality failure, malformed artifacts, or post-hoc threshold changes. |
| Explanatory diagnostics | Runtime, memory, residuals, ESS/tails, stiffness/Jacobian diagnostics, factor/core diagnostics. |
| Not concluded | No broad stiff-system validity, no HMC readiness, no statistical superiority. |
| Artifact | P06 aggregate summary and result. |

## Forbidden Claims And Actions

- Do not treat a single stiff fixture as broad robustness proof.
- Do not tune candidate policy.
- Do not claim HMC/autodiff readiness.
- Do not use descriptive stiffness diagnostics as pass criteria unless
  predeclared.

## Exact Next-Phase Handoff Conditions

- `P06_PASS_TO_P07_RESOURCE_DEFAULT_INTEGRATION`: gate passes and P07 subplan
  reviewed.
- `P06_FAIL_OPTIONAL_OR_REPAIR`: deterministic validity passes but quality gate
  fails.
- `P06_BLOCKED`: no fair executable stiff nonlinear harness exists.

## Stop Conditions

- Missing comparator/reference.
- Deterministic invalidity.
- Trusted GPU unavailable.
- Required artifact missing or malformed.

## Local Self-Review Of Next Subplan

P07 separates operational resource/default-integration evidence from scientific
model-suite quality and still does not change code defaults.
