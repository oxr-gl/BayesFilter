# P70 Phase 0 Subplan: Governance And Source-Anchor Reset

metadata_date: 2026-06-16
status: DRAFT_NOT_LAUNCHED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Reset the governing source anchors and claim boundaries before any repair work.
Classify the P69 Phase 5c failure as a current fixed-branch implementation gap:
the desired fixed branch should use UKF only to freeze branch-design objects,
then fit the branch itself with a nondegenerate fitting rule.  Phase 0 does not
implement code, rerun diagnostics, or edit the mathematical chapter.

## Entry Conditions Inherited From Planning

- P70 master program exists.
- P70 visible runbook exists.
- P70 visible execution ledger exists.
- P70 Claude review ledger exists.
- P70 stop handoff exists.
- P69 Phase 5c result exists and states that rank-channel activity is inactive
  in the realized current fit.
- p50 fixed-branch and UKF-scout sections are available.
- Current code anchors for constant-path initialization, one-sweep fitting, and
  UKF scout nonclaims are available.
- Author source anchors are available under
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase0-governance-source-anchor-reset-result-2026-06-16.md`.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-subplan-2026-06-16.md`.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-gated-execution-runbook-2026-06-16.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-claude-review-ledger-2026-06-16.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-stop-handoff-2026-06-16.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-phase0-governance-source-anchor-reset-subplan-2026-06-16.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-subplan-2026-06-16.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5c-rank-activity-degree-normalizer-result-2026-06-15.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex
test -f third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m
test -f third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m
test -f third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m
test -f third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m
test -f third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m
rg -n "scout_not_truth|UKF is diagnostic only|max_sweeps=1|_source_route_constant_path_initial_cores" bayesfilter/highdim
rg -n "d = 0;|m = 18;|max_rank|full_sol" third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m
rg -n "push_samples|computeL|TTSIRT|log\\(sirt\\.z\\)|fun_into_sirt" third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m
rg -n "w = w/sum\\(w\\)|chol|scaleL|ESS" third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m
rg -n "defaultTau|TTFun|round\\(approx\\)" third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m
rg -n "fun_z|obj\\.z = obj\\.fun_z \\+ obj\\.tau" third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m
rg -n "low/high branch closeness|adaptive parity|d18 correctness|HMC readiness" docs/plans/bayesfilter-highdim-zhao-cui-p70-*.md
```

Claude review:

- Review the Phase 0 result and refreshed Phase 1 subplan.
- Check source-anchor coverage, claim-boundary discipline, and whether Phase 0
  produced the exact Phase 1 entry conditions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the P70 source anchors, bug classification, and claim boundaries sufficient to begin a mathematical fixed-branch contract audit? |
| Baseline/comparator | p50 fixed-branch/UKF sections, P57/P61/P69 results, current code anchors, and author source anchors listed in the master program. |
| Primary criterion | Produce a Phase 0 result that classifies the current failure, lists allowed/forbidden claims, and gives Phase 1 exact entry conditions without launching code repair. |
| Veto diagnostics | Missing author-source anchors; UKF promoted to truth; adaptive parity language; low/high closeness gate; Phase 1 requires a repair that Phase 1 is supposed to design; detached execution. |
| Explanatory diagnostics | Text scans, anchor inventory, dependency-matrix check, dirty-worktree note. |
| Not concluded | No implementation repair, no diagnostic rerun, no validation, no scaling, no HMC readiness. |
| Artifact preserving result | Phase 0 result plus updated ledgers. |

## Forbidden Claims/Actions

- Do not edit algorithmic code.
- Do not edit p50 in Phase 0.
- Do not run the P69 Phase 5c diagnostic.
- Do not launch Phase 1 automatically unless the runbook has been launched and
  Phase 0 passes review.
- Do not say the author code has a bug.
- Do not call the UKF-guided fixed branch source-faithful unless source anchors
  prove that specific route.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if Phase 0 produces:

- an anchor inventory with p50, code, and author-source line anchors;
- a bug/gap classification for the current rank-channel and normalizer
  behavior;
- a claim-boundary table distinguishing `source_faithful`,
  `fixed_hmc_adaptation`, and `extension_or_invention`;
- a threshold-provenance placeholder that states which later phase must freeze
  each normalizer, holdout/replay, channel-activity, and ladder threshold before
  observing repaired diagnostic results;
- a refreshed Phase 1 subplan whose entry conditions are exactly the Phase 0
  products;
- local planning checks pass;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- the author source tree or p50 anchor is missing;
- source-governance language cannot be made consistent;
- Phase 1 would require implementation evidence that does not yet exist;
- Claude and Codex do not converge after five rounds;
- continuing requires user approval not already granted.

## Skeptical Plan Audit

Known risk: making the repair target a prerequisite.  Phase 0 is allowed to
identify the current gap and define Phase 1 entry conditions; it must not
require the UKF-guided fixed-branch repair to already exist.
