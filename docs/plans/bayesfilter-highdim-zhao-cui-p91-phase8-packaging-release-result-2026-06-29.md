# P91 Phase 8 Result: Packaging, CI, And Release Notes

Date: 2026-06-29

Status: `PASS_P91_PHASE8_PACKAGING_RELEASE_NOTES_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 8 prepared a release-note draft, API/test inventory, CI split guidance, and refreshed Phase 9 final-decision subplan without publishing, changing defaults, or claiming final production promotion. |
| Primary criterion status | Passed locally: release artifacts state validation scope/caveats, smoke versus deliberate GPU/HMC checks, model-specific CPU/GPU recommendations, and default/release boundaries. |
| Veto diagnostic status | Passed locally: no exact likelihood, posterior correctness, universal GPU, Phase 3 full-FD, HMC-overclaim, release/publish, CI mutation, or default-policy action was made. |
| Main uncertainty | Phase 8 is documentation and inventory only. Final production promotion remains a Phase 9 decision from reviewed upstream evidence. |
| Next justified action | Review this Phase 8 result, the release-note draft, and the refreshed Phase 9 final-decision subplan. |
| What is not being concluded | No package publication, release tagging, CI-service mutation, default-policy change, final production promotion, exact likelihood correctness, posterior correctness, full observed-data/filtering score identity, or universal GPU superiority. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are packaging notes, CI split, release notes, caveats, and default-readiness recommendation prepared without overclaiming P91 evidence? |
| Baseline/comparator | Reviewed P91 phase results and repository public API/CI conventions. |
| Primary criterion | Passed locally: artifacts are explicit about scope, caveats, opt-in GPU/HMC checks, and final Phase 9 authority. |
| Veto diagnostics | Passed locally: release text does not claim exact likelihood correctness, posterior correctness, universal GPU superiority, full FD/source-route derivative readiness, or production readiness by itself. |
| Explanatory diagnostics | API inventory, test-marker inventory, release-note draft, focused optional compile/pytest checks. |
| Not concluded | No final production promotion until Phase 9; no release/publish/default action. |
| Artifact | Release-note draft, this result, and refreshed Phase 9 subplan. |

## Skeptical Audit Result

- Wrong-baseline risk controlled by using reviewed P91 phase results as the
  evidence basis, not stale P90 blockers alone and not the Phase 7 smoke alone.
- Proxy metric risk controlled by preserving lane-specific interpretation:
  FD is limited engineering evidence, score identity is local component
  evidence, GPU/XLA is capability/performance evidence, and HMC smoke is an
  implementation smoke.
- Hidden authority risk controlled: Phase 8 did not publish, tag, upload,
  mutate CI, or change defaults.
- Caveat drift risk controlled by explicitly preserving Phase 3 limited-FD
  status, previous-marginal/fixed-TTSIRT derivative blockers, full source-route
  FD blocker, and HMC nonclaims.

## Local Checks

Commands:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
rg -n "zhao_cui_sir_austria_local_complete_data_log_density_xla|zhao_cui_sir_austria_batched_local_complete_data_log_density_xla|evaluate_highdim_score_api_batched|p91_hmc_smoke|p91_performance_benchmark" bayesfilter tests scripts docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
rg -n "posterior correctness|exact likelihood correctness|universal GPU|production readiness|Phase 3 is owner-accepted|BLOCK_FIXED_TTSIRT|BLOCK_FULL_SOURCE_ROUTE_FD|divergence_status" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_gpu_xla_jit_check.py scripts/p91_performance_benchmark.py scripts/p91_hmc_smoke.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p91_batched_score_api.py tests/highdim/test_p91_gpu_xla_local_target.py -q
```

Outcome:

- P91 document diff hygiene passed.
- API/harness inventory passed and found the intended highdim helper, tests,
  scripts, and P91 artifacts.
- Caveat inventory passed and confirmed the required nonclaim/blocker language
  remains visible.
- Optional script compile check passed for all three P91 runtime harnesses.
- Optional focused pytest passed: `7 passed, 2 warnings in 8.40s`.
- Warnings were TensorFlow Probability `distutils` deprecation warnings from
  environment imports; they were not Phase 8 failures.
- CPU-only commands intentionally set `CUDA_VISIBLE_DEVICES=-1`.

One administrative note:

- An exploratory marker inventory initially included missing optional config
  paths (`pyproject.toml`, `setup.cfg`, `tox.ini`), causing `rg` to return exit
  code 2 while still printing `pytest.ini` marker data. The authoritative
  Phase 8 checks above reran against existing files only and passed.

## API And Test Inventory

Highdim subpackage surfaces:

- `evaluate_highdim_score_api`;
- `evaluate_batched_highdim_score_api`;
- `HighDimBatchedScoreAPIResult`;
- `zhao_cui_sir_austria_local_complete_data_log_density_xla`;
- `zhao_cui_sir_austria_batched_local_complete_data_log_density_xla`.

Root package boundary:

- Phase 2 tests verify the new batched API symbols are exported through
  `bayesfilter.highdim` and not through root `bayesfilter`.

Test split:

- fast CPU-only semantic/API/local-target checks live under
  `tests/highdim/test_p91_batched_score_api.py` and
  `tests/highdim/test_p91_gpu_xla_local_target.py`;
- FD and score-identity diagnostics are CPU-only focused harnesses;
- GPU/XLA and HMC evidence live in deliberate scripts and trusted run
  manifests, not default fast CI.

Existing marker policy in `pytest.ini` includes:

- `extended`;
- `hmc`;
- `external`;
- `gpu`.

## Release Draft

Release-note draft:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md`

The draft states:

- P91 scope is approximate high-dimensional score/likelihood, not exact
  likelihood proof;
- artifact-level `Passed` does not mean final production promotion before
  Phase 9;
- the supported wording is scope-first and limited to the highdim API plus
  local complete-data component route;
- Phase 3 is owner-accepted limited FD evidence with caveats, not a full FD
  pass;
- Phase 4 validates local complete-data component score identity only;
- Phase 6 CPU/GPU timing is model/fixture-specific;
- Phase 7 HMC smoke is an implementation smoke only;
- final production promotion is reserved for Phase 9.

## Refreshed Phase 9 Subplan

Refreshed Phase 9 subplan:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md`

Refresh intent:

- make Phase 9 decide from reviewed evidence only;
- allow a final decision/reset memo/stop-handoff, not runtime or release
  actions;
- require caveat/blocker preservation in the final decision;
- keep package publication, CI mutation, release tagging, and default-policy
  changes forbidden.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` for optional CPU-only compile/pytest checks. |
| Conda environment | `tf-gpu` |
| Execution target | Documentation/API/test-inventory and CPU-only focused checks. |
| CPU/GPU status | CPU-only optional checks hid GPU via `CUDA_VISIBLE_DEVICES=-1`; no GPU/HMC runtime was run in Phase 8. |
| Data version | `N/A`; document/API/test inventory only. |
| Random seeds | `N/A`; no random runtime in Phase 8. |
| Wall time | Focused pytest reported `8.40s`; other checks exited 0 with no substantive runtime artifact. |
| Phase 8 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md` |
| Release draft | `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-result-2026-06-29.md` |
| Refreshed Phase 9 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md` |

## Phase 9 Handoff

Phase 9 may proceed only after Claude review agrees on this Phase 8 result, the
release-note draft, and the refreshed Phase 9 final-decision subplan. Phase 9
must make the final P91 decision from reviewed evidence only and must not run
new runtime, GPU/HMC, package/network, release, CI mutation, or default-policy
commands.
