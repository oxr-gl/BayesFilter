# P8i Phase 8 Subplan: Closeout, Artifact Index, And Repo Boundary

Date: 2026-06-16

Status: `REVIEWED_READY_FOR_PHASE8`

## Phase Objective

Close P8i by preserving artifacts, remaining blockers, and a commit boundary
that stays separate from unrelated Zhao-Cui, monograph, and P8h historical
changes.

## Entry Conditions

- Phase 7 result and refreshed Phase 8 subplan have been accepted by
  read-only review.
- Phase 7 preserves no filter ranking, no generic high-dimensional LEDH
  readiness, and no default sampler policy.

## Required Artifacts

- P8i artifact index.
- P8i reset memo.
- P8i repo-boundary manifest.
- Phase 8 result.

## Required Checks, Tests, Reviews

- JSON validation for generated index/manifest artifacts.
- `git diff --check` over intended P8i files.
- `git status --short` grouping.
- Read-only review of boundary.
- Boundary checks must include P8i docs plus the touched runner/tests:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-artifact-index-2026-06-16.json
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-repo-boundary-manifest-2026-06-16.json
git status --short
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P8i artifacts and code changes, if any, be preserved without pulling in unrelated lanes or overclaiming results? |
| Baseline/comparator | P8i reviewed results, current worktree, and P8h Phase 10 boundary manifest only as historical repo-boundary context. |
| Primary criterion | Write a boundary manifest separating intended P8i files from unrelated dirty groups and preserving all nonclaims/blockers. |
| Veto diagnostics | Unrelated Zhao-Cui/monograph/user work included without explicit approval; missing result artifacts; commit/push attempted without fresh request. |
| Explanatory diagnostics | Git status grouping, diff checks, artifact index. |
| Not concluded | Remote synchronization, merge safety, bit-for-bit reproduction, production readiness, final ranking, or default policy. |

## Forbidden Claims And Actions

- Do not commit or push unless the user explicitly requests it after reviewing
  the boundary.
- Do not hide blockers.

## Exact Next-Phase Handoff Conditions

P8i closes after Phase 8 records the boundary and review disposition.

## Stop Conditions

- Intended P8i files cannot be separated from unrelated dirty work.
- Read-only review does not accept the Phase 7 no-ranking/no-default-policy
  decision or the Phase 8 boundary plan.
- Any commit/push, package install, network fetch, destructive action, or
  default-policy code change would be required.
