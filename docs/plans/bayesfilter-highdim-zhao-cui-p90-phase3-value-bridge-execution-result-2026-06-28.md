# P90 Phase 3 Result: Value Bridge Execution

Date: 2026-06-28

Status: `P90_PHASE3_VALUE_BRIDGE_PASSED_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 3 executed the reviewed CPU-only same-target source-scalar-vs-author-replay value bridge node and it passed. |
| Primary criterion status | Met locally pending review: source-route scalar and independent author-formula replay matched within pinned tolerance for the reviewed deterministic `t=2` case. |
| Veto diagnostic status | Passed locally: no branch/setup/tolerance mismatch, no nonfinite value, no proxy comparator, no tolerance change after result, and no GPU/HMC/FD/production/default-policy command was run. |
| Main uncertainty | This is a value bridge for one reviewed deterministic case. It does not establish analytical-gradient correctness, FD validation, HMC readiness, GPU/XLA readiness, or production readiness. |
| Next justified action | Claude review of this Phase 3 result and Phase 4 derivative-carry design subplan. If both agree, Phase 4 may design derivative carry for the exact same scalar and branch. |
| What is not being concluded | No analytical-gradient correctness, FD validation, HMC readiness, GPU/XLA readiness, runtime/performance/memory/cost result, production readiness, packaging readiness, or default-policy change. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the local Zhao-Cui SIR d18 value match the source-backed author-formula replay bridge for the exact same scalar and branch within pinned tolerances? |
| Baseline/comparator | Reviewed same-target author-formula replay bridge reference. |
| Primary criterion | Passed locally pending review: source scalar and replay scalar matched with max absolute residual `0.0`, tolerance `1.0e-9`. |
| Veto diagnostics | Passed locally: finite values, same target id, same previous retained hash, same transport branch hash, same coordinate-frame hash, same tolerance version, and no proxy comparator. |
| Explanatory diagnostics | JSON execution manifest with source/replay values, hashes, tolerance, residual, and nonclaims. |
| Not concluded | No analytical-gradient correctness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, or default-policy change. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-2026-06-28.json` and this result. |

## Local Checks

Commands:

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest tests/highdim/test_p90_value_bridge_execution.py::test_p90_phase3_source_scalar_matches_author_formula_replay --maxfail=1
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Outcomes:

- First Phase 3 attempt failed before scalar execution because the wrapper
  imported `tests.highdim...`, but `tests/highdim` is not a package.
- Wrapper was repaired to load the Phase 2 helper by file path.
- Rerun outcome: `1 passed, 2 warnings`.
- Warnings were TensorFlow Probability deprecation warnings.
- The JSON manifest was written and records `max_abs_residual = 0.0`.
- P90 docs diff hygiene passed before result writing.

## Execution Manifest Summary

| Field | Value |
| --- | --- |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-2026-06-28.json` |
| Target id | `zhao_cui_sir_austria_d18` |
| Time index | `2` |
| Status | `P90_PHASE3_VALUE_BRIDGE_SOURCE_SCALAR_REPLAY_MATCH` |
| Binding hash | `ee33515fda3eeee2f8d16d66ae0a7fd4bb677cfe169d1f88cec9b758afbed5b3` |
| Previous retained hash | `bdb098b891bf0e65b12ea0ff7b26b18006fb368965f5c141df2237b40b32dca1` |
| Transport branch hash | `4c5002bac80539ae944ef263b8c1c8711d13fc08759b36d23e9485cfd6c5caaa` |
| Coordinate-frame hash | `e977eb09971b18e591ee42f6aa9a4811d8d98fc4b9bdcd4994b29bb738ed1db5` |
| Tolerance version | `p90.value_bridge.tolerances.v1` |
| Max absolute residual | `0.0` |
| Tolerance | `1.0e-9` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Focused local TensorFlow value-bridge node. |
| CPU/GPU status | CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Runtime/HMC status | No FD, derivative implementation, HMC, sampler, GPU/XLA, package/network, production benchmark, release, CI, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-subplan-2026-06-28.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-result-2026-06-28.md` |

## Phase 4 Handoff

Phase 4 may start only after Claude `VERDICT: AGREE` for:

- this Phase 3 result;
- `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-subplan-2026-06-28.md`.

Phase 4 must design derivative carry for the same scalar and branch. It must
not implement derivatives, run FD, run HMC, run GPU/CUDA, run production,
package/release/CI, or change default policy.
