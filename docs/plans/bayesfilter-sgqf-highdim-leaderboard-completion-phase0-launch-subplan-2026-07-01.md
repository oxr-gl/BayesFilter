# Phase 0 Subplan: Launch Inventory And SGQF Row Freeze

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Launch the SGQF leaderboard-completion program, freeze the remaining blocked row
identities and governing comparators, and verify that the launch package is
coherent before any SGQF implementation or leaderboard regeneration work
begins.

## Entry Conditions Inherited From Previous Phase

- The authoritative July 1 highdim leaderboard artifact exists.
- The already-complete SGQF rows for affine LGSSM, actual SV, and KSC surrogate
  SV are treated as preserved baselines.
- No implementation or leaderboard mutation authority exists yet for the
  remaining blocked rows.

## Required Artifacts

- master program:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-master-program-2026-07-01.md`
- visible runbook:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-gated-execution-runbook-2026-07-01.md`
- execution ledger:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-execution-ledger-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-claude-review-ledger-2026-07-01.md`
- stop handoff:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-stop-handoff-2026-07-01.md`
- Phase 0 result:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase0-launch-result-2026-07-01.md`
- refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-subplan-2026-07-01.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-master-program-2026-07-01.md
test -f docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-gated-execution-runbook-2026-07-01.md
test -f docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-execution-ledger-2026-07-01.md
test -f docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-claude-review-ledger-2026-07-01.md
test -f docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-stop-handoff-2026-07-01.md
test -f docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json
test -f docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md
rg -n "benchmark_lgssm_exact_oracle_m3_T50|zhao_cui_sv_actual_nongaussian_T1000|zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000|zhao_cui_spatial_sir_austria_j9_T20|zhao_cui_predator_prey_T20|zhao_cui_generalized_sv_synthetic_from_estimated_values|analytical_score_emitted|blocked" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion*.md
git diff --check -- docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion*.md
```

Required read-only Claude reviews:

Core review-gated launch authorities:

- master program,
- visible runbook,
- this Phase 0 subplan,
- then Phase 0 result and refreshed Phase 1 subplan.

Supporting inputs that must exist and be cross-checked locally, but do not
require separate one-path review unless a later bounded review finds an
inconsistency:

- authoritative paired leaderboard artifacts (`.json` plus `.md`),
- visible execution ledger,
- Claude review ledger,
- visible stop handoff.

The execution ledger, Claude review ledger, and stop handoff are launch-tracking
artifacts in Phase 0: they must be updated as part of closeout, but they do not
require separate one-path review unless a later bounded review finds an
inconsistency.

No implementation, runtime, benchmark regeneration, HMC, GPU/XLA, release, CI,
or default-policy command is authorized in Phase 0.

## Skeptical Plan Audit

| Risk Checked | Phase 0 Control |
| --- | --- |
| Wrong baseline | Phase 0 anchors to the July 1 highdim leaderboard artifact and preserves the already-complete SGQF rows as baselines. |
| Proxy metric promoted | Artifact existence and review closure are launch criteria only; they do not admit any new SGQF row. |
| Missing stop condition | Wrong-target scalar promotion, autodiff score promotion, source-scope evaluator gaps, and unexplained approximation gaps are explicit blockers. |
| Unfair comparison | Full-three-way-ready rows and blocked rows are kept separate from launch. |
| Hidden assumption | Phase 0 does not assume that a blocked row is “almost done” just because UKF or Zhao-Cui exists for it. |
| Stale context | Launch package is anchored to the newest authoritative leaderboard artifacts. |
| Environment mismatch | Phase 0 is document-only. |
| Artifact-answer mismatch | Phase 0 must close with reviewed launch artifacts plus a refreshed Phase 1 subplan. |

Audit status: passed for launch preparation if the required artifacts exist,
local checks pass, and the bounded Claude reviews converge.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SGQF leaderboard-completion program safely launch a fresh anti-drift package before any SGQF row implementation or leaderboard regeneration begins? |
| Baseline/comparator | authoritative paired July 1 highdim leaderboard artifacts (`.json` plus `.md`) and preserved SGQF baseline rows. |
| Primary criterion | The launch package is coherent, locally checked, reviewed, and explicit about preserved baseline rows, blocked rows, and analytical-only score policy. |
| Veto diagnostics | wrong-target scalar promotion, stale row-status drift, missing stop conditions, or phase advance without review. |
| Explanatory diagnostics | artifact existence, row-coverage grep checks, and review notes. |
| Not concluded | No new SGQF row admission, no leaderboard regeneration, no HMC readiness, and no production/default claim. |
| Artifact | reviewed launch package, Phase 0 result, and refreshed Phase 1 subplan. |

## Forbidden Claims/Actions

- Do not reopen the already-complete SGQF baseline rows casually.
- Do not ask the user to choose row semantics already fixed by the reviewed
  leaderboard artifact or row contract.
- Do not regenerate the leaderboard in Phase 0.
- Do not run implementation, runtime, benchmark, HMC, GPU/XLA, release, CI, or
  default-policy commands.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- the master program receives Claude `VERDICT: AGREE`;
- the visible runbook receives Claude `VERDICT: AGREE`;
- this Phase 0 subplan receives Claude `VERDICT: AGREE`;
- the Phase 0 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 1 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records Phase 0 as reviewed closed rather than merely
  locally prepared.

## Stop Conditions

- The July 1 leaderboard artifact is contradicted by a higher-ranked reviewed
  artifact.
- A launch artifact silently upgrades a blocked row or downplays an admitted
  baseline row.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require implementation, runtime, GPU/XLA, release, CI,
  default-policy, destructive git/filesystem, or unrelated dirty worktree
  changes.

## End-Of-Phase Requirements

1. Run the required local document checks.
2. Review the launch package with bounded read-only Claude prompts.
3. Write the Phase 0 result.
4. Refresh the Phase 1 subplan.
5. Update the execution ledger, Claude review ledger, and visible stop handoff
   to reflect the reviewed launch state.
