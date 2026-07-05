# P84 Phase 2 Subplan: Budget-Compliant Fitting

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE1_REPAIR_AND_APPROVAL`

## Phase Objective

Produce or block the first Phase 6 budget-compliant fixed-TTSIRT fit artifact.

## Entry Conditions Inherited From Previous Phase

- Phase 1 basis/domain route is classified and reviewed.
- If Phase 1 is blocked, a reviewed Phase 1 repair or explicit keep-blocked
  decision is required before any production-relevant fitting.
- Exact fitting command, sample count, seeds, artifacts, and runtime posture are
  frozen.
- Explicit human approval is required before any fitting command.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase2-budget-compliant-fitting-result-2026-06-23.md`
- JSON fit manifest under `docs/plans/`.
- Updated execution ledger and Phase 3 subplan.

## Required Checks / Tests / Reviews

Before execution, exact commands must be added.  Design checks:

```bash
rg -n "P_theta|minimum_training_samples|max\\(20 \\* P_theta, 5000\\)|training|holdout|replay|validation|audit|fit_sample_count" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p84-phase2-budget-compliant-fitting-subplan-2026-06-23.md \
  bayesfilter/highdim -S
```

Claude review and explicit human approval are required before fitting.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can a fixed-TTSIRT source-route fit satisfy the Phase 6 budget floor and fit-quality vetoes? |
| Baseline/comparator | Phase 6 budget contract and Phase 1 basis/domain route. |
| Primary criterion | Completed training samples meet `minimum_training_samples = max(20 * P_theta, 5000)`, core statuses OK, finite fit/holdout residuals, and manifest preserves disjoint clouds. |
| Veto diagnostics | Under-budget samples, nonfinite targets, row/condition/memory gate failure, holdout tolerance failure, cloud overlap. |
| Explanatory diagnostics | Fit residual, holdout residual, branch hashes, runtime, memory. |
| Not concluded | No correctness, rank convergence, production readiness, HMC readiness. |
| Artifact | Fit manifest and Phase 2 result. |

## Forbidden Claims / Actions

- Do not treat training loss alone as correctness.
- Do not use audit cloud for tuning.
- Do not run without exact approval.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if at least one budget-compliant fit artifact exists, or
if Phase 2 blocks and Phase 3 is explicitly reframed as blocked.  If Phase 1
author-basis/domain parity remains blocked, Phase 2 must not run
production-relevant fitting.

## Stop Conditions

Stop if budget-compliant fitting cannot be specified, approved, or completed.
