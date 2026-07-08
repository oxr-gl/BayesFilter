# Phase 1 Subplan: Fixed-Variant Entry Point Inventory

Date: 2026-07-03

Status: `READY_EXECUTED_PHASE1_RESULT_WRITTEN`

## Phase Objective

Identify the exact fixed-variant Zhao-Cui SIR callable(s), tests, and result
artifacts that may support the leaderboard row, and classify the quantity they
compute.

## Entry Conditions Inherited From Previous Phase

- Phase 0 has frozen the current retained-grid demotion and leaderboard
  baseline.
- P91 artifacts are present or missing status is recorded.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase1-entrypoint-inventory-result-2026-07-03.md`
- Inventory table covering:
  `zhao_cui_sir_austria_local_complete_data_log_density_xla`,
  `zhao_cui_sir_austria_batched_local_complete_data_log_density_xla`,
  `tests/highdim/test_p91_score_identity.py`,
  `tests/highdim/test_p91_gpu_xla_local_target.py`,
  P91 Phase 4-7 artifacts.

## Required Checks / Tests / Reviews

- Focused `rg` checks for fixed-variant callable exports and P91 statuses.
- Optional CPU-only focused tests:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p91_score_identity.py tests/highdim/test_p91_gpu_xla_local_target.py`
  if the inventory needs runtime refresh.
- Claude read-only review if the inventory proposes a new production claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which fixed-variant callable computes the row quantity, and what quantity is it? |
| Baseline/comparator | P91 Phase 4-7 artifacts and current `bayesfilter/highdim/models.py` helper functions. |
| Primary criterion | Inventory states whether the callable is local complete-data/component, full observed-data filtering, or unsupported for the requested row. |
| Veto diagnostics | Calling retained-grid production route; treating sidecar timing as full row timing; missing analytical/manual score provenance; full filtering claim without derivative blockers closed. |
| Explanatory diagnostics | Value/score examples from P91 artifacts and existing test names. |
| Not concluded | No final leaderboard admission, no exact likelihood correctness, no full filtering identity unless explicitly shown. |
| Artifact | Phase 1 result. |

## Forbidden Claims / Actions

- Do not change code in Phase 1 unless inventory reveals a broken export.
- Do not claim source-faithfulness without paper/source anchors.
- Do not call Claude an execution authority.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if Phase 1 classifies the fixed-variant route quantity
and names exactly which leaderboard scope is eligible for wiring.

## Stop Conditions

- No fixed-variant callable emits a finite value/score under any declared
  leaderboard-compatible scope.
- The only available callable is the demoted retained-grid route.
- The scope requires human redefinition.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 1 result / close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
