# P91 Phase 2 Result: Batched Value/Score API

Date: 2026-06-29

Status: `P91_PHASE2_BATCHED_API_LOCAL_PASS_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 2 locally added a stable highdim subpackage batched value/score API and focused tests. |
| Primary criterion status | Passed locally: batched values/scores match looped single API outputs on deterministic fixtures; setup identity metadata is exposed through diagnostics and branch manifests; ambiguous/missing batched identity fails closed. |
| Veto diagnostic status | Passed locally: no root-level export, no hidden setup identity, no batch/single mismatch, no nonfinite values/scores, no shape/dtype drift, no FD/GPU/XLA/HMC/benchmark/package/default command, and no production-readiness claim. |
| Main uncertainty | Phase 2 validates API semantics only. Later phases must still bind Zhao-Cui SIR d18 scalar/score to FD, score identity, GPU/XLA, benchmarks, HMC smoke, release notes, and final decision. |
| Next justified action | Review this Phase 2 result and refreshed Phase 3 FD subplan. |
| What is not being concluded | No FD consistency, score identity, GPU/XLA readiness, HMC readiness, CPU/GPU performance, package/release/CI readiness, default-policy readiness, production readiness, exact likelihood correctness, posterior correctness, or universal GPU superiority. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the highdim subpackage expose a batched value/score API whose outputs match looped single calls and whose setup identity metadata fails closed? |
| Baseline/comparator | Existing `evaluate_highdim_score_api` looped over deterministic scalar value functions under the same theta and setup identity. |
| Primary criterion | Passed locally: batched values/scores equal looped single values/scores on deterministic fixtures, with stable shape/dtype, branch identities, and setup identity metadata. |
| Veto diagnostics | Passed locally: missing/ambiguous identity, per-item identity length mismatch, matrix theta, non-scalar value, disconnected score, and root export cases are covered by tests. |
| Explanatory diagnostics | Per-item branch hashes, batch identity mode, batch size, and P91-style setup identity fixture. |
| Not concluded | FD consistency, score identity, GPU/XLA readiness, HMC readiness, CPU/GPU performance, packaging/release/CI readiness, default-policy readiness, production readiness, exact likelihood correctness, posterior correctness, or universal GPU superiority. |
| Artifact | Code/test diff, preserved local-check output artifact, this result, refreshed Phase 3 subplan. |

## Cross-Artifact Consistency

This close record satisfies the reviewed Phase 2 subplan and implementation
artifact checkpoints as follows:

| Reviewed checkpoint | Phase 2 result evidence |
| --- | --- |
| Add batched highdim value/score result/evaluator | `HighDimBatchedScoreAPIResult` and `evaluate_batched_highdim_score_api` added in `bayesfilter/highdim/score_api.py`. |
| Preserve existing single API behavior | Existing P51 stable score API tests rerun and passed. Optional `setup_identity` is keyword-only and existing calls remain valid. |
| Expose setup identity through auditable metadata | Batched result diagnostics require `setup_identity_channel == "diagnostics_and_branch_manifest"` and per-item branch manifests include `setup_identity`. |
| Shared setup identity mode | Focused test checks batched values/scores against looped single calls with shared P91-style setup identity. |
| Per-item setup identity mode | Focused test checks per-item identity metadata and distinct branch hashes for differing fixture metadata. |
| Fail closed on missing/ambiguous identity | Focused tests cover missing identity, simultaneous shared/per-item identity, and per-item length mismatch. |
| Keep exports subpackage-only | Focused test verifies new symbols are present in `bayesfilter.highdim` and absent from root `bayesfilter`. |
| Avoid broader runtime/scientific claims | This result records no FD, score identity, GPU/XLA, HMC, benchmark, package/release/CI, default-policy, exact-likelihood, or production claim. |

## Implementation Summary

Code changes:

- Added `HighDimBatchedScoreAPIResult` to
  `bayesfilter/highdim/score_api.py`.
- Added `evaluate_batched_highdim_score_api` to
  `bayesfilter/highdim/score_api.py`.
- Added optional keyword-only `setup_identity` metadata to
  `evaluate_highdim_score_api` for looped single comparator manifests while
  preserving existing call behavior.
- Exported the new batched result/evaluator through `bayesfilter.highdim`
  only.
- Added `tests/highdim/test_p91_batched_score_api.py`.

Important worktree note:

- `bayesfilter/highdim/__init__.py` already contains broader uncommitted
  highdim export changes in this dirty research worktree. Phase 2 touched only
  the `HighDimBatchedScoreAPIResult` and `evaluate_batched_highdim_score_api`
  import/export lines in that file and preserved the surrounding dirty work.

## Local Checks

Commands:

```bash
git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p91_batched_score_api.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p51_stable_score_api.py tests/highdim/test_p91_batched_score_api.py -q
```

Outcome:

- `git diff --check`: passed.
- Focused pytest: `10 passed, 2 warnings in 3.53s`.
- Warnings were TensorFlow Probability `distutils` deprecation warnings from
  environment imports; they were not Phase 2 failures.
- Preserved output artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-local-check-output-2026-06-29.md`

CPU/GPU status:

- The pytest command intentionally set `CUDA_VISIBLE_DEVICES=-1` before
  TensorFlow import. Phase 2 performed CPU-only semantic/API checks and did not
  run GPU/CUDA/XLA/HMC.

## Test Coverage

`tests/highdim/test_p91_batched_score_api.py` covers:

- subpackage-only export of `HighDimBatchedScoreAPIResult` and
  `evaluate_batched_highdim_score_api`;
- shared setup identity parity against looped `evaluate_highdim_score_api`;
- per-item setup identity metadata and distinct branch hashes for differing
  fixture metadata;
- fail-closed behavior for missing identity, simultaneous shared/per-item
  identity, per-item length mismatch, matrix theta, non-scalar value output,
  and disconnected scores.

Existing `tests/highdim/test_p51_stable_score_api.py` was rerun to confirm the
original single-call stable score API behavior remains intact.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Conda environment | `tf-gpu` |
| Execution target | CPU-only semantic/API parity and metadata tests. |
| CPU/GPU status | CPU-only; `CUDA_VISIBLE_DEVICES=-1` intentionally set for pytest. |
| Commands | `git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p91_batched_score_api.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`; `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p51_stable_score_api.py tests/highdim/test_p91_batched_score_api.py -q` |
| Data version | `N/A`; deterministic algebraic fixtures only. |
| Random seeds | `N/A`; deterministic algebraic fixtures only. |
| Wall time | Pytest reported `3.53s`; diff check completed with exit code 0 and no output. |
| Runtime status | No FD, score identity, GPU/CUDA, XLA, HMC, benchmark, package/network, release, CI, production, or default-policy command was run. |
| Local check output | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-local-check-output-2026-06-29.md` |
| Phase 2 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md` |
| Implementation artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-implementation-artifact-2026-06-29.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md` |
| Refreshed Phase 3 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md` |

## Phase 3 Handoff

Phase 3 may start only after Claude review agrees on:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md`

Phase 3 must first bind exact FD scalar/score commands, tolerances, step-size
ladder, setup identity fixture, and artifact paths in a reviewed FD
implementation manifest before any FD runtime command. Phase 3 must not treat
FD as a truth oracle and must not run score identity, GPU/XLA, HMC, benchmarks,
package/release/CI, production, or default-policy commands unless a reviewed
subplan refresh explicitly changes scope.
