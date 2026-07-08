# Codex Substitute Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase3-mechanics-canary`
Supervisor/executor: Codex
Reviewer: local Codex substitute reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. This is a substitute review because external Claude review was policy-blocked for private repository context transfer risk. It is weaker than full Claude review.

## Objective

Review the Phase 3 HMC mechanics canary subplan before implementation or execution. Pay special attention to the repaired coordinate convention: TFP HMC runs in an internal unit coordinate `u`, Phase 2 mass is applied by `z = u @ chol(M_z).T`, and Phase 1 target parameters use `theta = center + scale * z`.

## Artifacts To Inspect

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-result-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-subplan-2026-07-08.md`
- `docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Phase 3 sufficient and bounded for a mechanics-only HMC canary using the whitened mass handoff? |
| Baseline/comparator | Phase 2 mass handoff artifact. |
| Primary criterion | Subplan has objective, entry conditions, artifacts, checks/reviews, evidence contract, forbidden claims/actions, exact handoff conditions, stop conditions, and mechanics-only metric roles. |
| Veto diagnostics | Posterior/convergence/default claim, hidden ranking, coordinate/mass convention mismatch, pretending stock TFP HMC directly consumes dense `M_z`, treating `L * epsilon` as correctness proof, missing timeout/stop condition, Phase 4 advancement without finite mechanics telemetry. |
| Explanatory diagnostics | Minor wording or artifact naming suggestions. |
| Not concluded | No posterior correctness, no convergence, no default readiness. |

## Review Questions

1. Does Phase 3 keep mechanics telemetry separate from posterior/convergence claims?
2. Are coordinate and mass conventions explicit enough?
3. Are `L * epsilon` and acceptance diagnostics classified correctly?
4. Are stop and handoff conditions sufficient before a short HMC smoke?
5. Is the exact grid `{(1, 0.10), (2, 0.25), (4, 0.3925)}` sufficiently fixed and bounded for mechanics-only execution?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
