# Codex Substitute Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase1-subplan`
Supervisor/executor: Codex
Reviewer: local Codex substitute reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. This is a substitute review because external Claude review was policy-blocked for private repository context transfer risk. It is weaker than full Claude review.

## Objective

Review the Phase 1 scalar filtering-likelihood geometry subplan before implementation or diagnostic execution begins.

## Artifacts To Inspect

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-result-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-identifiable-ssl-lstm-oracle-geometry-test-result-2026-07-08.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Phase 1 plan sufficient and bounded for scalar filtering-likelihood geometry, without HMC or posterior claims? |
| Baseline/comparator | Passed complete-data oracle geometry result and current `tf_ssl_lstm_svd_ukf_score` filtering helper. |
| Primary criterion | Phase 1 subplan has objective, entry conditions, artifacts, checks/reviews, evidence contract, forbidden claims/actions, exact handoff conditions, stop conditions, and skeptical audit. |
| Veto diagnostics | Wrong baseline, oracle result promoted to filtering validity, proxy geometry metrics promoted to HMC/posterior claims, missing stop condition, hidden HMC execution, coordinate ambiguity, unsupported numeric default, hidden source-faithfulness claim. |
| Explanatory diagnostics | Minor wording or artifact naming suggestions. |
| Not concluded | No implementation correctness, no filtering-likelihood validity, no HMC readiness, no posterior correctness, no default readiness. |

## Review Questions

1. Does Phase 1 directly test filtering-likelihood geometry rather than relying on the oracle result?
2. Are the hard pass/fail criteria and vetoes sufficient?
3. Are HMC and posterior claims forbidden clearly enough?
4. Are the coordinate-system and mass-handoff preconditions explicit enough for Phase 2?
5. Are numeric choices labeled as inherited, heuristic, or pending rather than facts?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
