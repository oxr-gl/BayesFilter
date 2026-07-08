# Codex Substitute Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase5-replicated-scalar-hmc`
Supervisor/executor: Codex
Reviewer: local Codex substitute reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. This is a substitute review because external Claude review was policy-blocked for private repository context transfer risk. It is weaker than full Claude review.

## Objective

Review the Phase 5 replicated scalar HMC diagnostic subplan before implementation or execution.

## Artifacts To Inspect

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-result-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-subplan-2026-07-08.md`
- `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Phase 5 sufficient and bounded for a small replicated scalar HMC diagnostic using the Phase 4 fixed kernel? |
| Baseline/comparator | Phase 4 short-smoke artifact. |
| Primary criterion | Subplan has objective, entry conditions, artifacts, checks/reviews, evidence contract, fixed settings, statistical discipline, forbidden claims/actions, exact handoff conditions, stop conditions, and diagnostic-only metric roles. |
| Veto diagnostics | Posterior/convergence/default claim, hidden ranking, coordinate/mass convention mismatch, treating finite short chains/acceptance as convergence, treating native divergence unavailability as zero divergences, missing timeout/stop condition, closeout advancement without finite replicated telemetry. |
| Explanatory diagnostics | Minor wording or artifact naming suggestions. |
| Not concluded | No posterior correctness, no convergence, no tuned kernel, no default readiness. |

## Review Questions

1. Does Phase 5 keep replicated short-chain telemetry separate from posterior/convergence/default-readiness claims?
2. Are the inherited `u -> z -> free` coordinate and fixed-kernel conventions explicit enough?
3. Are stochastic diagnostics and uncertainty limits classified correctly?
4. Are stop and handoff conditions sufficient before Phase 6 closeout?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
