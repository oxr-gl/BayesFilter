# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `scalar-filtering-geometry-hmc-phase0`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Claude is not execution authority and cannot approve human, runtime, model-file, funding, product, default-policy, or scientific-claim boundaries.

## Objective

Review Phase 0 governance artifacts for a scalar SSL-LSTM filtering-geometry-to-HMC-readiness program. Decide whether the plan is internally consistent, bounded, and safe to start Phase 1 planning/execution.

## Artifacts To Inspect

Inspect only these bounded local paths:

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-gated-execution-runbook-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-execution-ledger-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-stop-handoff-2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-identifiable-ssl-lstm-oracle-geometry-test-result-2026-07-08.md`

Do not inspect the whole repository. Do not require source-faithfulness anchors unless the plan makes a Zhao-Cui faithfulness claim; the intended verdict should block if such a claim appears unsupported.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the Phase 0 plan/runbook/subplan artifacts sufficient and safe before code or experiment execution begins? |
| Baseline/comparator | Passed complete-data oracle geometry result and current filtering-score path as the next target. |
| Primary criterion | Artifacts include research intent, evidence contract, skeptical audit, stop conditions, review/repair loop, exact handoff conditions, and forbidden claims. |
| Veto diagnostics | Missing stop condition, wrong baseline, proxy metric promoted to HMC/posterior claim, unsupported source-faithfulness claim, hidden default-policy change, hidden authority transfer to Claude, coordinate ambiguity that would invalidate Phase 2. |
| Explanatory diagnostics | Wording clarity, minor artifact naming issues, optional additions that do not block execution. |
| Numeric provenance | `svd_ukf` start is a hypothesis baseline; horizon 100-200 is a pending Phase 1 convenience range; four free parameters are inherited from the oracle diagnostic; `L * epsilon ~= 1.57` is user-provided heuristic only; Claude max 5 rounds is user instruction. |
| Not concluded | No implementation correctness, no filtering-likelihood validity, no HMC readiness, no HMC convergence, no posterior correctness, no default readiness, no Zhao-Cui source-faithfulness. |

## Review Questions

1. Is there any material correctness, baseline, boundary, or evidence-policy issue in starting Phase 1 after this gate?
2. Does the plan keep the complete-data oracle result separate from filtering-likelihood/HMC claims?
3. Are stop conditions and exact handoff conditions sufficient?
4. Does the review/repair loop preserve Codex as supervisor/executor and Claude as read-only reviewer?
5. Are unsupported numeric defaults classified as hypotheses or pending phase choices rather than facts?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
