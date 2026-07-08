# P91 Phase 8 Subplan: Packaging, CI, And Release Notes

Date: 2026-06-29

Status: `REFRESHED_PENDING_PHASE7_RESULT_REVIEW`

## Phase Objective

Prepare production packaging notes, CI coverage split, public API notes,
release caveats, and a default-readiness recommendation after score identity,
FD, batched API, GPU/XLA, benchmarks, and HMC smoke pass.

This phase is documentation/API/test-inventory work only. It does not publish a
package, change defaults, run broad CI, or claim final production promotion.

## Entry Conditions Inherited From Previous Phase

- Phase 7 HMC smoke result reviewed pass.
- All prior P91 production gates reviewed pass.
- This Phase 8 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Release-note draft:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md`
- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-result-2026-06-29.md`
- Refreshed Phase 9 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Exact local checks authorized by this refreshed subplan:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
rg -n "zhao_cui_sir_austria_local_complete_data_log_density_xla|zhao_cui_sir_austria_batched_local_complete_data_log_density_xla|evaluate_highdim_score_api_batched|p91_hmc_smoke|p91_performance_benchmark" bayesfilter tests scripts docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
rg -n "posterior correctness|exact likelihood correctness|universal GPU|production readiness|Phase 3 is owner-accepted|BLOCK_FIXED_TTSIRT|BLOCK_FULL_SOURCE_ROUTE_FD|divergence_status" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Focused optional checks, if Phase 8 release-note wording references the Python
helpers or smoke harnesses directly:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_gpu_xla_jit_check.py scripts/p91_performance_benchmark.py scripts/p91_hmc_smoke.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p91_batched_score_api.py tests/highdim/test_p91_gpu_xla_local_target.py -q
```

Claude review is required for this refreshed Phase 8 subplan, the release-note
draft, the Phase 8 result, and the Phase 9 subplan.

No human approval is needed for this doc-only Phase 8 scope. Human approval is
still required before any actual package publication, broad CI policy change,
default-policy change, or public release action; those actions are forbidden in
Phase 8.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are packaging notes, CI split, release notes, caveats, and default-readiness recommendation prepared without overclaiming P91 evidence? |
| Baseline/comparator | Reviewed P91 phase results and repository public API/CI conventions. |
| Primary criterion | Release artifacts explicitly state validation scope/caveats, smoke vs expensive tests, model-specific CPU/GPU recommendations, and default policy recommendation without unauthorized release/default action. |
| Veto diagnostics | Exact likelihood claim, posterior correctness claim, universal GPU-speed claim, missing score caveat, missing expensive-test marker, unauthorized package/release/CI/default action. |
| Explanatory diagnostics | API inventory, test marker inventory, release note review. |
| Not concluded | No final production promotion until Phase 9. No release/publish/default action unless separately authorized. |
| Artifact | Release-note draft, Phase 8 result, refreshed Phase 9 subplan. |

## Forbidden Claims/Actions

- Do not publish, release, upload, package-build for distribution, or tag a
  release.
- Do not change defaults in Phase 8.
- Do not hide approximation caveats.
- Do not upgrade Phase 3 from owner-accepted limited FD evidence to a full FD
  pass.
- Do not treat Phase 7 HMC smoke as posterior correctness, convergence, full
  observed-data/filtering target readiness, or production readiness.
- Do not remove preserved blockers for previous-marginal/fixed-TTSIRT
  derivatives or full source-route FD.

## Exact Next-Phase Handoff Conditions

Phase 9 may start only if:

- Phase 8 result receives Claude `VERDICT: AGREE`;
- Phase 9 subplan receives Claude `VERDICT: AGREE`;
- release-note caveats and CI/test split are explicit.

## Stop Conditions

- Required release/default decision exceeds this reviewed doc-only authority.
- Release notes would overclaim exact likelihood/posterior/GPU superiority.
- Local checks fail and cannot be repaired.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks authorized by reviewed Phase 8 refresh.
2. Write Phase 8 result / close record.
3. Draft or refresh Phase 9 subplan.
4. Review Phase 8 result and Phase 9 subplan.
