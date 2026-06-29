# P84 Phase 4 Subplan: Correctness Bridge

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE3`

## Phase Objective

Build or block a source-backed same-target reference bridge for
`d18_correctness_candidate`.

## Entry Conditions Inherited From Previous Phase

- Phase 3 rank convergence passed, or Phase 4 is explicitly a bridge design
  blocker.
- Same target convention and observation setup are frozen.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase4-correctness-bridge-result-2026-06-23.md`
- Reference/bridge manifest if built.
- Updated execution ledger and Phase 5 subplan.

## Required Checks / Tests / Reviews

```bash
rg -n "d18_correctness_candidate|missing_same_target_reference_or_bridge|reference|bridge|target convention|observation" \
  docs/plans \
  bayesfilter/highdim \
  third_party/audit/zhao_cui_tensor_ssm_p10/source -S
```

Claude review is required before any correctness-candidate interpretation.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there a reviewed same-target reference bridge for d=18 correctness-candidate evidence? |
| Baseline/comparator | Author source or reviewed high-fidelity same-target reference. |
| Primary criterion | Reference bridge is source-backed, same-convention, and has predeclared agreement criteria. |
| Veto diagnostics | Target convention mismatch, missing source anchors, weak proxy comparator. |
| Explanatory diagnostics | Agreement residuals, uncertainty intervals, convention ledger. |
| Not concluded | No production readiness without later KR/derivative/HMC/scale gates. |
| Artifact | Bridge manifest and Phase 4 result. |

## Forbidden Claims / Actions

- Do not use UKF or local all-grid/operator route as correctness bridge.
- Do not claim exact likelihood correctness from proxy agreement.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if current KR production status is known and bridge
claims remain properly scoped.

## Stop Conditions

Stop if a same-target reference bridge cannot be anchored.
