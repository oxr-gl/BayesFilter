# P83 Phase 0 Subplan: Governance Reset

Date: 2026-06-22

Status: `DRAFT_READY_FOR_REVIEW`

## Phase Objective

Open the P83 source-route reset program and make the route boundary visible:
Zhao-Cui validation must target the fixed-TTSIRT retained-object source route,
not the local all-grid/operator route or UKF/FD/JVP diagnostic lanes.

## Entry Conditions Inherited From Previous Phase

- Reset memo loaded:
  `docs/plans/bayesfilter-highdim-zhao-cui-source-route-reset-memo-2026-06-22.md`.
- P56/P57/P58 source-route artifacts are available locally.
- Worktree is dirty; unrelated changes must be preserved.
- No implementation or numerical validation has been authorized by P83 yet.

## Required Artifacts

- P83 master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-source-route-reset-master-program-2026-06-22.md`
- P83 visible gated execution runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-gated-execution-runbook-2026-06-22.md`
- P83 Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- P83 visible execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- P83 visible stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md`
- This Phase 0 subplan.
- Draft/refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-subplan-2026-06-22.md`
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase0-governance-reset-result-2026-06-22.md`

## Required Checks / Tests / Reviews

Local checks:

```bash
rg -n "multistate_tt_grid_retained_filter|ForwardAccumulator|UKF|validation CE|d=18|LEDH|source_faithful|extension_or_invention|fixed_hmc_adaptation" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-* -S

rg -n "VERDICT:|READ-ONLY REVIEW ONLY|Claude|executor|authority|source-route|all-grid|operator" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-* -S

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-source-route-reset-master-program-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-gated-execution-runbook-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase0-governance-reset-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-subplan-2026-06-22.md
```

Review:

- Codex skeptical audit before Phase 0 execution.
- Claude read-only review of compact master/P83-0/P83-1 fact packet.
- If Claude returns `VERDICT: REVISE`, patch the same artifact visibly and
  rerun focused checks/review.  Stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Do the P83 governance artifacts correctly reset the lane to source-route work and prevent wrong-route promotion before inventory or implementation? |
| Baseline/comparator | Reset memo, P56 source-anchor audit, P57/P58 route contracts, and author-source anchor requirements. |
| Primary pass criterion | Artifacts exist, include per-phase subplan/result requirements, classify local/grid/operator route as `extension_or_invention`, keep UKF/FD/JVP diagnostic-only, define Claude as read-only reviewer, and pass local scans plus Claude review. |
| Veto diagnostics | Any d=18/LEDH launch authorization; any claim that Phase 0 proves implementation readiness; any all-grid/operator/UKF/FD/JVP route promoted as source-faithful; missing Phase 1 handoff. |
| Explanatory diagnostics | Markdown search hits, artifact presence, review comments, and dirty-worktree note. |
| Not concluded | No implementation completeness, no transport repair, no analytical derivative readiness, no SIR d=18 validation, no HMC readiness. |
| Artifact preserving result | Phase 0 result file and review ledger entry. |

## Forbidden Claims / Actions

- Do not edit BayesFilter code.
- Do not run numerical experiments, GPU probes, LEDH jobs, or d=18 validation.
- Do not claim source-faithful implementation readiness.
- Do not promote the local all-grid/operator route, UKF lane, FD harness, or
  ForwardAccumulator/JVP diagnostics.
- Do not send whole files to Claude.
- Do not treat Claude as authority or executor.

## Execution Steps

1. Confirm P83 artifacts exist and are scoped to documentation/governance.
2. Run the local checks above.
3. Send compact fact packet to Claude read-only reviewer.
4. If review agrees, write Phase 0 result.
5. Draft or refresh Phase 1 subplan.
6. Perform Codex consistency review of Phase 1 subplan.
7. Update execution ledger and stop handoff status.

## Exact Next-Phase Handoff Conditions

P83-1 may begin only if:

- Phase 0 local checks pass;
- Claude review is `VERDICT: AGREE` or non-material comments are resolved;
- Phase 0 result records no unsupported claims;
- Phase 1 subplan exists and includes objective, inherited entry conditions,
  required artifacts, checks/reviews, evidence contract, forbidden actions,
  next-phase handoff conditions, and stop conditions.

## Stop Conditions

Stop with a Phase 0 blocker result if:

- local checks show the artifacts authorize d=18/LEDH or implementation before
  inventory;
- route-boundary language is internally inconsistent;
- Claude and Codex do not converge after five rounds for the same blocker;
- continuing requires human approval beyond read-only Claude review;
- dirty worktree conflicts require modifying unrelated user changes.
