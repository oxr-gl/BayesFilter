# Phase 0 Subplan: Baseline Freeze And Launch Gate

Date: 2026-07-03

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the July 3 authoritative leaderboard pair, preserve the already-complete
baseline rows, and launch the focused non-Zhao-Cui completion program before any
row-level implementation or regeneration work begins.

## Entry Conditions Inherited From Previous Phase

- The current authoritative leaderboard pair exists.
- The already-complete baseline rows are treated as preserved and not to be
  reopened casually.
- No implementation or regeneration authority exists yet for the remaining
  blocked/value-only rows.

## Required Artifacts

- master program:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-master-program-2026-07-03.md`
- visible runbook:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-gated-execution-runbook-2026-07-03.md`
- execution ledger:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-execution-ledger-2026-07-03.md`
- Claude review ledger:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-claude-review-ledger-2026-07-03.md`
- stop handoff:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-stop-handoff-2026-07-03.md`
- Phase 0 result:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase0-baseline-freeze-result-2026-07-03.md`
- refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase1-spatial-sir-subplan-2026-07-03.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-master-program-2026-07-03.md
test -f docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-gated-execution-runbook-2026-07-03.md
test -f docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-execution-ledger-2026-07-03.md
test -f docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-claude-review-ledger-2026-07-03.md
test -f docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-stop-handoff-2026-07-03.md
test -f docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json
test -f docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md
rg -n "benchmark_lgssm_exact_oracle_m3_T50|zhao_cui_sv_actual_nongaussian_T1000|zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000|zhao_cui_spatial_sir_austria_j9_T20|zhao_cui_predator_prey_T20|zhao_cui_generalized_sv_synthetic_from_estimated_values|executed_value_score|blocked|executed_value_only" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion*.md
git diff --check -- docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion*.md
```

Required read-only Claude reviews:

- master program,
- visible runbook,
- this Phase 0 subplan,
- then Phase 0 result and refreshed Phase 1 subplan.

No implementation, runtime, HMC, GPU/XLA, release, CI, or leaderboard
regeneration command is authorized in Phase 0.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the non-Zhao-Cui completion program safely launch a fresh anti-drift package before any row-level implementation or regeneration begins? |
| Baseline/comparator | authoritative paired July 3 highdim leaderboard artifacts and preserved non-Zhao-Cui baseline rows. |
| Primary criterion | The launch package is coherent, locally checked, reviewed, and explicit about preserved baseline rows, remaining blocked/value-only rows, and analytical-only score policy. |
| Veto diagnostics | wrong-target scalar promotion, silent row-status drift, missing stop conditions, or phase advance without review. |
| Explanatory diagnostics | artifact existence, row-coverage grep checks, and review notes. |
| Not concluded | No new row admission, no final leaderboard regeneration, no HMC readiness, and no production/default claim. |
| Artifact | reviewed launch package, Phase 0 result, and refreshed Phase 1 subplan. |

## Forbidden Claims And Actions

- Do not reopen the already-complete non-Zhao-Cui baseline rows casually.
- Do not ask the user to choose row semantics already fixed by the reviewed row contracts and current artifact.
- Do not regenerate the leaderboard in Phase 0.
- Do not run implementation, runtime, HMC, GPU/XLA, release, CI, or default-policy commands.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- the master program receives Claude `VERDICT: AGREE`;
- the visible runbook receives Claude `VERDICT: AGREE`;
- this Phase 0 subplan receives Claude `VERDICT: AGREE`;
- the Phase 0 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 1 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records Phase 0 as reviewed closed rather than merely locally prepared.

## Stop Conditions

- The July 3 leaderboard artifact is contradicted by a higher-ranked reviewed artifact.
- A launch artifact silently upgrades a blocked/value-only row or downplays a preserved baseline row.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require implementation, runtime, GPU/XLA, release, CI,
  default-policy, destructive git/filesystem, or unrelated dirty worktree
  changes.
