# Codex Substitute Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase2-mass-handoff`
Supervisor/executor: Codex
Reviewer: local Codex substitute reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. This is a substitute review because external Claude review was policy-blocked for private repository context transfer risk. It is weaker than full Claude review.

## Objective

Review the Phase 2 geometry-to-mass handoff subplan before implementation or execution.

## Artifacts To Inspect

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-subplan-2026-07-08.md`
- `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Phase 2 sufficient and bounded for converting accepted whitened geometry into a mass handoff artifact without HMC or MAP claims? |
| Baseline/comparator | Phase 1 accepted low-rank geometry artifact. |
| Primary criterion | Subplan has objective, entry conditions, artifacts, checks/reviews, evidence contract, forbidden claims/actions, exact handoff conditions, stop conditions, and coordinate audit. |
| Veto diagnostics | Coordinate mismatch, use of rejected refined center as MAP, hidden HMC execution, SPD/condition checks missing, unsupported HMC/posterior/default/GPU/source-faithfulness claim, Phase 2 advancement without Phase 1 pass. |
| Explanatory diagnostics | Minor wording or artifact naming suggestions. |
| Not concluded | No HMC readiness, no posterior correctness, no convergence, no default readiness. |

## Review Questions

1. Does Phase 2 preserve the whitened coordinate convention from Phase 1?
2. Does it prevent use of the rejected refined center as a MAP center?
3. Are SPD/condition checks and stop conditions sufficient before HMC mechanics?
4. Does it avoid HMC and posterior/default-readiness claims?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
