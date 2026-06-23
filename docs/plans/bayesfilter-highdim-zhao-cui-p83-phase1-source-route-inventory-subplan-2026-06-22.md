# P83 Phase 1 Subplan: Anchored Source-Route Inventory

Date: 2026-06-22

Status: `DRAFT_AFTER_PHASE0`

## Phase Objective

Produce a concrete implemented/partial/missing/diagnostic-only inventory for the
documented Zhao-Cui fixed-TTSIRT retained-object source route.  Every row must
include code anchors, paper/project anchors where applicable, author-source
anchors where applicable, and an honest route classification.

## Entry Conditions Inherited From Previous Phase

- P83-0 governance reset passed local checks and read-only review.
- P83 master program and visible runbook are active.
- The local all-grid/operator route is classified as `extension_or_invention`
  for Zhao-Cui source-faithfulness.
- UKF is scout/initializer only.
- FD and ForwardAccumulator/JVP are diagnostic-only unless a later source-backed
  analytical route is found.
- No implementation edits or numerical validation have been authorized.

## Required Artifacts

- Phase 1 inventory result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- Draft/refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md`

## Inventory Targets

Local code and tests:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/transport.py`
- `bayesfilter/highdim/squared_tt.py`
- `bayesfilter/highdim/rank_budget.py`
- `bayesfilter/highdim/fitting.py` if needed for fixed TT/SIRT fit status
- `tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py`
- `tests/highdim/test_p57_m3_proposition2_marginalization.py`
- `tests/highdim/test_p57_m4_source_kr_cdf_maps.py`
- `tests/highdim/test_p57_m5_proposal_density_retained_sampling.py`
- `tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py`
- `tests/highdim/test_p58_m9_source_route_pipeline_readiness.py`
- `tests/highdim/test_p59_author_sir_*`

Documents:

- P50 LaTeX source-route sections.
- P56 source-anchor audit.
- P57-M2/M6/M7 results.
- P58-M9 repair result.
- P61 source-faithfulness reaudit if needed for defensive-mass status.
- P81/P82 local-grid/JVP closeout artifacts only as boundary evidence.

Author source:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_irt_reference.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_rt_reference.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_cirt_reference.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m`

## Required Checks / Tests / Reviews

Read-only inventory commands:

```bash
rg -n "source_faithful|fixed_hmc_adaptation|extension_or_invention|FixedTTSIRT|TTSIRT|marginalise|marginalize|eval_pdf|Algorithm 5|Proposition 2|multistate_tt_grid_retained_filter|ForwardAccumulator" \
  docs/plans bayesfilter/highdim tests/highdim -S

rg -n "full_sol|computeL|TTSIRT|marginalise|marginalize|eval_pdf|eval_irt|eval_rt|eval_cirt" \
  third_party/audit/zhao_cui_tensor_ssm_p10/source -S

rg -n "FixedTTSIRTTransport|source_route_run_sequential_fixed_hmc|source_route_retained_object_manifest|p58_m9_source_route_pipeline_readiness|P57_FIXED_TTSIRT_ROUTE_CLASS" \
  bayesfilter/highdim tests/highdim docs/plans -S
```

Focused artifact checks after writing result/subplan:

```bash
rg -n "source_faithful|fixed_hmc_adaptation|extension_or_invention|implemented|partial|missing|diagnostic_only|BLOCK_SOURCE_UNGROUNDED" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md -S

rg -n "multistate_tt_grid_retained_filter|ForwardAccumulator|UKF|validation CE|LEDH|d=18" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md -S

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md
```

Review:

- Codex skeptical audit before inventory execution.
- Claude read-only review of compact inventory fact packet and Phase 2 subplan
  summary.
- Repair loop up to five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What source-route pieces are implemented, partial, missing, or diagnostic-only, and what repair should Phase 2 design? |
| Baseline/comparator | P50/P56 source-route operations, P57/P58 local contracts, and Zhao-Cui author source. |
| Primary pass criterion | Every inventory row has local code/test anchors, paper/project anchors where applicable, author-source anchors where applicable, status, classification, and next repair action. |
| Veto diagnostics | Any unanchored `source_faithful` label; any old local/operator route, UKF, FD, validation CE, or JVP evidence promoted as source-route closure; missing Phase 2 handoff. |
| Explanatory diagnostics | Search coverage, line anchors, prior result artifacts, dirty-worktree note, and review comments. |
| Not concluded | No code correctness, no d=18 success, no transport repair, no analytical derivative readiness, no LEDH readiness. |
| Artifact preserving result | Phase 1 inventory result and updated review/execution ledgers. |

## Forbidden Claims / Actions

- Do not edit implementation code or tests in Phase 1.
- Do not run numerical tests or GPU jobs.
- Do not claim d=18 validation readiness.
- Do not use local/grid/operator results to close source-route gaps.
- Do not promote UKF, FD agreement, validation CE, or ForwardAccumulator/JVP.
- Do not send whole files to Claude.

## Required Inventory Table Columns

- Source-route component.
- Required Zhao-Cui operation.
- Local implementation anchor.
- Paper/project anchor.
- Author-source anchor.
- Status: `implemented`, `partial`, `missing`, or `diagnostic_only`.
- Classification: `source_faithful`, `fixed_hmc_adaptation`, or
  `extension_or_invention`.
- Next repair action.

## Exact Next-Phase Handoff Conditions

P83-2 may begin only if:

- Phase 1 result table is complete enough to identify the narrow transport and
  marginalization repair scope;
- every source-route claim has anchors or is downgraded;
- Phase 2 subplan exists and includes fixed TT/SIRT core representation,
  defensive density, normalizer, Proposition-2 mass-matrix/QR marginalization,
  `eval_pdf`/potential semantics, forward/inverse/conditional KR APIs, proposal
  correction denominator, retained-object manifest, branch identity, checks,
  forbidden grid/base-density substitutes, and stop conditions;
- local checks pass;
- Claude review agrees or non-material comments are resolved.

## Stop Conditions

Stop with a Phase 1 blocker result if:

- author-source anchors cannot be located for a claimed source-route operation;
- the local code state is too inconsistent to classify without implementation
  inspection beyond read-only inventory;
- Phase 2 would have to rely only on tensor-product grid conditional
  integration or base-density-only proposal correction;
- Claude and Codex do not converge after five rounds for the same blocker;
- continuing requires implementation, GPU, network, package, or destructive git
  action not authorized by this phase.
