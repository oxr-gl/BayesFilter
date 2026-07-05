# P83 Phase 6 Subplan: Source-Route Fitting Budget Design

Date: 2026-06-22

Status: `READY_AFTER_PHASE5_DOC_CHECKS`

## Phase Objective

Design the source-route fixed-TTSIRT fitting budget before any real fitting
ladder or d=18 validation run.

Phase 6 is design-only unless a later reviewed subplan explicitly authorizes a
small fitting diagnostic.  It must compute parameter counts, training-sample
minimums, heldout/audit cloud requirements, rank/degree candidates, training
loss diagnostics, and stop conditions for future fitting work.

## Entry Conditions Inherited From Previous Phase

Phase 6 may begin only after Phase 5 passes local checks and review/handoff
requirements.

Inherited boundaries:

- Phase 4 derivative readiness remains blocked;
- Phase 5 was mechanics-only and did not validate d=18 or production source
  correctness;
- current grid-CDF transport is not production KR closure;
- positive defensive mass and `eval_pdf` proposal semantics remain required;
- no GPU, LEDH, d=18, HMC, fitting ladder, validation job, or production claim
  is authorized by this subplan.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- Draft/refreshed Phase 7 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

Skeptical audit before execution.

Read-only/design checks:

```bash
rg -n "FixedTTFitConfig|FixedTTFitter|ranks|degree|parameter_count|sample_count|row adequacy|20 \\*|fit_sample|training|heldout|audit|condition|rank" \
  bayesfilter/highdim \
  tests/highdim \
  docs/plans/bayesfilter-highdim-zhao-cui-p6*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p7*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p8*.md -S

rg -n "fit|approximate|TTSIRT|SIRT|tau|sample|computeL|mainscript|full_sol|setup" \
  third_party/audit/zhao_cui_tensor_ssm_p10/source/models \
  third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src -S

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

Review:

- Claude read-only review of the Phase 6 design and Phase 7 handoff is required
  before any Phase 7 validation subplan can launch.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What source-route fixed-TTSIRT fitting budget, rank/degree ladder, sample minimum, and diagnostics are required before any d=18 validation attempt? |
| Baseline/comparator | Phase 4 blocker, Phase 5 mechanics smoke, P57/P58/P66/P70 fitting/rank artifacts, local `FixedTTFitConfig`/`FixedTTFitter`, and Zhao-Cui author source setup/fit anchors. |
| Primary pass criterion | Design states parameter-count formula, sample minimum at least `20 * number_of_parameters`, candidate rank/degree ladder, training-loss gate, heldout/audit cloud definitions, and stop conditions. |
| Veto diagnostics | Any fitting run launched; budget below minimum; UKF/generated-sample/validation CE promoted as source-route correctness; d=18 validation authorized without fitting artifacts; derivative readiness assumed despite Phase 4 blocker. |
| Explanatory diagnostics | Read-only inventories and design tables. |
| Not concluded | No fit quality, no d=18 correctness, no derivative readiness, no LEDH readiness, no HMC readiness, no production source-route correctness. |
| Artifact preserving result | Phase 6 design result. |

## Forbidden Claims / Actions

- Do not run fitting, d=18 validation, LEDH, HMC, GPU, or MCMC jobs.
- Do not change default numerical policy.
- Do not lower sample minimum below `20 * number_of_parameters`.
- Do not use UKF or generated-sample CE as correctness evidence.
- Do not claim derivative readiness while Phase 4 blocker is active.
- Do not claim production KR closure.

## Exact Next-Phase Handoff Conditions

P83-7 may be drafted but not executed unless:

- Phase 6 design passes local checks and Claude review;
- required fit artifacts and manifests are explicitly named;
- Phase 7 evidence contract has a real comparator and veto diagnostics;
- derivative readiness status is stated as blocked or separately repaired;
- human approval is requested before any long, GPU, d=18, validation, LEDH, or
  fitting run.

## Stop Conditions

Stop with a Phase 6 blocker result if:

- parameter counts cannot be computed from the local fit representation;
- sample budget cannot meet the declared minimum;
- source-route fit artifacts required for validation do not exist;
- heldout/audit clouds cannot be defined without changing the target;
- the design would need derivative readiness, production KR closure, or d=18
  validation to answer the budget question.
