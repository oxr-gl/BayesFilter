# P05 Subplan: Stochastic-Volatility And Heavy-Tail Gate

Date: 2026-06-25

Status: `DRAFT_AFTER_P04`

## Phase Objective

Test fixed SVD-Nystrom on a non-Gaussian stochastic-volatility/heavy-tail
filtering fixture to check robustness beyond Gaussian observation/transition
stress.

## Entry Conditions Inherited From Previous Phase

- P04 nonlinear Gaussian gate passed or produced a reviewed non-blocking scope
  decision.
- Candidate policy remains locked.
- Required comparator/harness is identified before execution.

## Required Artifacts

- Per-run JSON/Markdown/log artifacts with prefix
  `svd-nystrom-nohmc-promotion-p05-sv-heavy-tail`.
- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p05-sv-heavy-tail-summary-2026-06-25.json`
- P05 result and refreshed P06 subplan.

## Required Checks, Tests, And Reviews

- Identify existing stochastic-volatility/heavy-tail fixture or write blocker.
- Trusted GPU preflight.
- Run paired candidate/comparator rows with predeclared seeds and quality gate.
- Verify finite outputs, metadata, no dense materialization, no active-path
  NumPy, and statistical interpretation.
- Claude review required for new harness or material gate changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does SVD-Nystrom remain viable under non-Gaussian/heavy-tail filtering stress? |
| Baseline/comparator | Streaming TF32 route or phase-local declared reference. |
| Primary criterion | Deterministic validity plus predeclared quality/statistical screen. |
| Veto diagnostics | Nonfinite outputs, route/policy mismatch, comparator failure, malformed artifacts, statistically meaningful quality failure, or missing uncertainty. |
| Explanatory diagnostics | Runtime, memory, tail metrics, residuals, ESS, factor/core diagnostics. |
| Not concluded | No broad non-Gaussian validity, no statistical superiority, no HMC readiness. |
| Artifact | P05 aggregate summary and result. |

## Forbidden Claims And Actions

- Do not infer superiority from descriptive tail metrics.
- Do not tune SVD policy.
- Do not continue with a missing comparator.
- Do not claim HMC readiness.

## Exact Next-Phase Handoff Conditions

- `P05_PASS_TO_P06_STIFF_NONLINEAR`: gate passes and P06 subplan reviewed.
- `P05_FAIL_OPTIONAL_OR_REPAIR`: deterministic validity passes but quality gate
  fails.
- `P05_BLOCKED`: no fair executable non-Gaussian/heavy-tail harness exists.

## Stop Conditions

- Missing comparator/reference.
- Deterministic invalidity.
- Trusted GPU unavailable.
- Required artifacts missing or malformed.

## Local Self-Review Of Next Subplan

P06 checks stiff nonlinear behavior and blocks broad claims if stiffness exposes
route fragility.
