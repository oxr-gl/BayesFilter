# P07 Subplan: Resource And Default-Integration Gate

Date: 2026-06-25

Status: `DRAFT_AFTER_P06`

## Phase Objective

Verify operational readiness for a bounded default-candidate recommendation:
resource envelope, metadata, fallback/comparator availability, TensorFlow/TFP
implementation path, and default-integration tests. This phase does not change
code defaults.

## Entry Conditions Inherited From Previous Phase

- P02-P06 model/quality gates passed or were explicitly scoped with reviewed
  non-blocking rationale.
- Candidate policy remains locked.
- No HMC readiness claim is in scope.

## Required Artifacts

- Resource benchmark JSON/Markdown/log artifacts with prefix
  `svd-nystrom-nohmc-promotion-p07-resource`.
- Default-integration check summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p07-default-integration-summary-2026-06-25.json`
- P07 result and refreshed P08 subplan.

## Required Checks, Tests, And Reviews

- Trusted GPU preflight.
- Large-N/long-T resource rows under predeclared time/memory envelope.
- Local tests for metadata/default-selection surfaces, including
  `tests/test_actual_sir_nystrom_compiled_redo.py`,
  `tests/test_actual_sir_nystrom_default_promotion.py`, and
  targeted Nystrom transport tests.
- Verify no dense materialization, no active-path NumPy, fallback/comparator
  remains available, and artifact metadata records SVD policy.
- Claude review required if this phase supports a final promotion-ready state.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is SVD-Nystrom operationally ready as a bounded default-candidate recommendation? |
| Baseline/comparator | Streaming TF32 route for resource rows; local tests for integration metadata. |
| Primary criterion | Resource envelope passes; metadata/default-integration tests pass; no dense/NumPy/fallback vetoes. |
| Veto diagnostics | GPU/TF32 mismatch, memory/time envelope failure, dense materialization, active-path NumPy, missing fallback, missing SVD metadata, failed tests, or malformed artifacts. |
| Explanatory diagnostics | Runtime, memory, warm timing ratios, factor/core diagnostics. |
| Not concluded | No code default switch, public API readiness, package release, HMC readiness, or statistical superiority. |
| Artifact | P07 resource/default-integration summary and result. |

## Forbidden Claims And Actions

- Do not change default policy in code.
- Do not claim public/package readiness.
- Do not use speed alone as promotion evidence.
- Do not remove streaming fallback/comparator.

## Exact Next-Phase Handoff Conditions

- `P07_PASS_TO_P08_FINAL_DECISION`: resource and integration gates pass and P08
  subplan reviewed.
- `P07_FAIL_OPTIONAL_OR_REPAIR`: model gates passed but operational readiness
  fails.
- `P07_BLOCKED`: required GPU/runtime/test boundary unavailable.

## Stop Conditions

- Trusted GPU unavailable for resource claims.
- Required local tests fail.
- Dense materialization or active-path NumPy appears in default candidate path.
- Changing code defaults would be required to continue.

## Local Self-Review Of Next Subplan

P08 is final decision only; it must not perform new experiments or switch code
defaults.
