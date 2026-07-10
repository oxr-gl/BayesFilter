# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `bayesfilter-ledh-compact-score-default-launch-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the launch package for the LEDH compact score default program. The
program demotes reverse-record/manual-total-VJP score routes to historical and
wrong for leaderboard score admission, and makes compact forward sensitivity
the only future default score style.

## Artifacts To Inspect

- `docs/plans/bayesfilter-ledh-compact-score-default-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-visible-gated-execution-runbook-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase0-route-demotion-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-visible-execution-ledger-2026-07-08.md`

Context anchors:

- `bayesfilter/highdim/ledh_score_contract.py`
- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the launch package consistent, feasible, and safe to start Phase 0 route demotion? |
| Baseline/comparator | Existing score runbook, LGSSM compact route, actual-SV reverse-record finding, current score validator allowlist. |
| Primary criterion | The package must make compact forward sensitivity the only future default, demote reverse/manual-total routes from admission, require per-phase subplans and reviews, and stop on boundary violations. |
| Veto diagnostics | Old routes still admissible as default; Phase 0 skips inventory; missing evidence contract; missing stop conditions; unsupported score/scientific claims; Claude given authority beyond read-only review. |
| Explanatory diagnostics | Suggestions for clearer sequencing, artifact names, or additional static guards. |
| Not concluded | No implementation correctness, score admission, model port completion, leaderboard readiness, HMC readiness, posterior correctness, or scientific superiority. |

## Review Questions

1. Is there any material correctness or boundary issue in launching Phase 0?
2. Does the plan correctly demote reverse-record/manual-total-VJP routes instead
   of merely renaming them?
3. Are the phase order and handoff conditions feasible for wiring the compact
   style model by model?
4. Are required artifacts and stop conditions sufficient to prevent accidental
   score admission through the old memory-inefficient path?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
