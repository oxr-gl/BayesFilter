# Codex Substitute Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase4-short-hmc-smoke`
Supervisor/executor: Codex
Reviewer: local Codex substitute reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. This is a substitute review because external Claude review was policy-blocked for private repository context transfer risk. It is weaker than full Claude review.

## Objective

Review the Phase 4 short HMC smoke subplan before implementation or execution.

## Artifacts To Inspect

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-result-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-subplan-2026-07-08.md`
- `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Phase 4 sufficient and bounded for a short fixed-kernel HMC smoke using the repaired Phase 3 coordinate composition? |
| Baseline/comparator | Phase 3 mechanics canary artifact. |
| Primary criterion | Subplan has objective, entry conditions, artifacts, checks/reviews, evidence contract, fixed settings, forbidden claims/actions, exact handoff conditions, stop conditions, and smoke-only metric roles. |
| Veto diagnostics | Posterior/convergence/default claim, hidden ranking, coordinate/mass convention mismatch, treating short-chain samples/acceptance as convergence, treating native divergence unavailability as zero divergences, missing timeout/stop condition, Phase 5 advancement without finite smoke telemetry. |
| Explanatory diagnostics | Minor wording or artifact naming suggestions. |
| Not concluded | No posterior correctness, no convergence, no tuned kernel, no default readiness. |

## Review Questions

1. Does Phase 4 keep short-smoke telemetry separate from posterior/convergence claims?
2. Are the inherited `u -> z -> free` coordinate and mass conventions explicit enough?
3. Are acceptance, log-accept, target trace, and native divergence availability classified correctly?
4. Are stop and handoff conditions sufficient before replicated diagnostics?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
