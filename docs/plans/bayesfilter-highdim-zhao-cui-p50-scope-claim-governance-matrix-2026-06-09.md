# P50 Scope And Claim Governance Matrix

metadata_date: 2026-06-09
program: P50-hmc-deterministic-filtering
phase: P50-M0
status: ACTIVE_GOVERNANCE

## Scope Decision

P50 targets deterministic, differentiable, HMC-compatible filtering.

The following are explicit non-goals, not remaining gaps:

- adaptive TT/SIRT source-faithful filtering;
- S&P 500 reproduction.

## Route Labels

| Label | Meaning | Allowed claims | Forbidden claims |
| --- | --- | --- | --- |
| `hmc_compatible_deterministic_filtering` | Deterministic differentiable filtering route intended for value and gradient use in HMC-facing workflows. | May claim phase-scoped deterministic value, gradient, model-ladder, or HMC-tier evidence after the corresponding P50 gate passes. | Must not claim source-faithful adaptive TT/SIRT reproduction. |
| `gradient_calibration_diagnostic` | Value/gradient diagnostic or calibration artifact. | May define or test error metrics under declared criteria. | Must not claim HMC readiness by itself. |
| `model_ladder_diagnostic` | SV, generalized SV, spatial SIR, or predator-prey comparison ladder. | May support scoped value/gradient diagnostics for that model. | Must not claim production model readiness unless a production phase is separately defined and passed. |
| `hmc_readiness_tier` | Tiered sampler-readiness evidence. | May claim the exact HMC tier that passed. | Must not promote finite gradients or short-chain speed to full HMC readiness when veto diagnostics fail. |
| `smoothing_boundary` | Boundary for latent-path smoothing/backward conditionals. | May defer smoothing or define a separate latent-path plan. | Must not imply smoothing support from filtering pass tokens. |
| `historical_source_context` | P49/P48/P10/P34 source-audit or source-faithfulness context. | May explain why P50 chooses a deterministic HMC route. | Must not become a P50 blocker, deliverable, or pass criterion. |

## Forbidden Claim Patterns

These patterns are forbidden in P50 result/closeout artifacts unless explicitly
negated, scoped as a non-goal, or used as a veto diagnostic:

- adaptive TT/SIRT source-faithful filtering is a P50 gap;
- S&P 500 reproduction is a P50 gap;
- value agreement proves gradient correctness;
- finite gradients prove HMC readiness;
- short-chain speed proves HMC readiness despite divergences or invalid
  posterior/reference checks;
- diagnostic model ladders prove production spatial SIR, predator-prey, SV, or
  generalized SV readiness;
- filtering support implies smoothing support.

## Static Audit Summary

Codex searched active P50 artifacts for:

```text
adaptive TT/SIRT|adaptive source|source-faithful|S&P|S\&P|HMC readiness|production .*readiness|remaining gap|blocker|pass criterion|required
```

Observed hits were in one of these allowed contexts:

- explicit non-goal;
- veto diagnostic;
- non-claim;
- phase pass/block machinery;
- human-required stop condition;
- smoothing-boundary question.

No active P50 artifact was found that treats adaptive TT/SIRT filtering or S&P
500 reproduction as a required P50 deliverable or remaining gap.

## Carry-Forward Requirement

Every future P50 phase result must state:

- the route label it supports;
- the phase-scoped claim it permits;
- what it does not conclude;
- whether HMC readiness, smoothing support, or model production readiness is
  still unclaimed.
