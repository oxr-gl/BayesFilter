# P8m Phase 6 Subplan: Sinkhorn/Epsilon Validation Contract

metadata_date: 2026-06-18
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 6

## Phase Objective

Design and optionally run a validation ladder for lower Sinkhorn iterations or
epsilon changes, clearly separated from exact implementation optimization.

## Entry Conditions Inherited From Previous Phase

- Exact implementation state is closed or blocked.
- There is a documented reason to evaluate tuning settings.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase6-sinkhorn-validation-result-2026-06-18.md`

## Required Checks/Tests/Reviews

Design review before any tuning run:

```bash
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

If runs are launched, all GPU commands must be trusted/escalated and artifacts
must include matched baseline/tuned values and diagnostics.

Claude review is required before promoting any tuning setting.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can lower Sinkhorn iterations or different epsilon be considered as optional tuned settings without hiding value changes? |
| Baseline/comparator | Exact Sinkhorn-10/epsilon-1.0 route unless Phase 5 establishes a new exact baseline. |
| Primary criterion | Validation result reports value differences, runtime, diagnostics, and whether the setting is reject/defer/optional-candidate. |
| Veto diagnostics | Treating speed as adequacy, missing baseline comparison, unstable MC evidence, or default promotion. |
| Explanatory diagnostics | Runtime, log likelihood deltas, ESS if available, seeds, memory, residuals. |
| Not concluded | No default change, no scientific acceptance, no leaderboard readiness. |

## Forbidden Claims/Actions

- Do not call lower iterations an exact implementation optimization.
- Do not promote a tuned setting as default in Phase 6.
- Do not use one-seed or single-repeat evidence for scientific acceptance.

## Exact Next-Phase Handoff Conditions

Phase 7 may proceed if tuning validation is documented as reject, defer, or
optional-candidate with nonclaims.

## Stop Conditions

Stop if the validation question would require a broader statistical adequacy
program not authorized here.
