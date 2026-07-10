# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `bayesfilter-ledh-compact-score-default-phase0-result-phase1-subplan-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the Phase 0 route-demotion result and Phase 1 shared compact score
contract subplan.

The exact old route token family under review is:

```text
manual_total_vjp_no_autodiff_same_scalar_*
```

## Artifacts To Inspect

- `docs/plans/bayesfilter-ledh-compact-score-default-phase0-route-demotion-result-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase1-contract-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-visible-gated-execution-runbook-2026-07-08.md`

Context anchors:

- `bayesfilter/highdim/ledh_score_contract.py`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- `docs/benchmarks/benchmark_ledh_same_target_predator_prey_score.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 1 safely start validator/static-guard enforcement for compact-only score admission? |
| Baseline/comparator | Phase 0 inventory, current validator allowlist, LGSSM compact route, actual-SV/predator-prey reverse-record hits. |
| Primary criterion | Phase 0 correctly identifies the enforcement gap and Phase 1 has concrete tests/edits to reject old routes from full admission. |
| Veto diagnostics | Old routes still treated as future admissible defaults; Phase 1 would run full score commands before guards; missing stop conditions; broad correctness claims from one-point FD; unsupported target changes. |
| Explanatory diagnostics | Better guard wording, missing files to include, sequencing improvements. |
| Not concluded | No score admission, no model port, no leaderboard completion, no HMC/posterior/scientific claim. |

## Review Questions

1. Is the Phase 0 result accurate relative to the current code anchors?
2. Does Phase 1 directly close the code-level enforcement gap?
3. Are the required checks and stop conditions sufficient before model ports?
4. Are there unsupported claims or authority transfers?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
