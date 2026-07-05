# P91 Phase 1 Result: Score Contract Freeze

Date: 2026-06-29

Status: `P91_PHASE1_SCORE_CONTRACT_LOCAL_READY_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 1 locally freezes the Zhao-Cui SIR d18 score contract as a document/source-inventory artifact. |
| Primary criterion status | Met locally: score sign/scalar convention, parameterization, fixed setup/branch identity, derivative policy, inherited training/basis policy, single/batched API semantics, and downstream release caveats are explicit. |
| Veto diagnostic status | Passed locally: no exact-likelihood score claim, no hidden derivative omission, no ALS revival, no FD/GPU/HMC/runtime/package/default command, and no production-readiness claim. |
| Main uncertainty | Phase 2 must implement or harden the single/batched API; later phases must still validate FD, score identity, GPU/XLA, benchmarks, HMC smoke, packaging, and final decision. |
| Next justified action | Review the score contract, this Phase 1 result, and refreshed Phase 2 batched-API subplan. |
| What is not being concluded | No implementation correctness, FD pass, score-identity pass, GPU/XLA readiness, HMC readiness, benchmark result, packaging readiness, production readiness, exact likelihood correctness, or default-policy change. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can P91 freeze an unambiguous Zhao-Cui score contract suitable for batched API, FD, score identity, GPU/XLA, HMC, and release notes? |
| Baseline/comparator | Reviewed P91 production contract and existing highdim source-route/score API surfaces. |
| Primary criterion | Passed locally: score contract names exact semantics, non-claims, and blockers/diagnostics without authorizing runtime promotion. |
| Veto diagnostics | Passed locally: sign convention, branch identity, inherited ALS/no-ALS policy, derivative omission policy, score identity caveat, setup-identity metadata channel, and batched API requirements are explicit. |
| Explanatory diagnostics | Local source/API grep inventory. |
| Not concluded | No implementation correctness, FD pass, score identity pass, GPU/XLA readiness, HMC readiness, benchmark result, or production readiness. |
| Artifact | Score contract, this Phase 1 result, refreshed Phase 2 subplan. |

## Local Checks

Commands:

```bash
rg -n "SourceRoute|score|basis|rank|ALS|training|batched|batch|derivative|proposal|transport" bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p9*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Additional focused inventory:

```bash
sed -n '1,240p' bayesfilter/highdim/score_api.py
sed -n '240,520p' bayesfilter/highdim/score_api.py
sed -n '90,170p' bayesfilter/highdim/source_route.py
sed -n '1040,1165p' bayesfilter/highdim/source_route.py
sed -n '1310,1545p' bayesfilter/highdim/source_route.py
```

Outcome:

- Existing highdim score API surfaces were found:
  `HighDimScoreAPIResult`, `evaluate_highdim_score_api`, and
  `score_readiness_branch_hash`.
- Existing score API explicitly separates finite value/score from HMC
  readiness.
- P90 value-bridge and derivative-carry surfaces were found and used as score
  contract anchors.
- P90 fixed TTSIRT proposal/transport derivative blockers remain explicit.
- P91 docs diff hygiene passed before result writing and after the score
  contract repair loop.

## Source Inventory Summary

| Topic | Source evidence |
| --- | --- |
| Stable highdim score API | `bayesfilter/highdim/score_api.py:101`, `score_api.py:413`; finite value/score requires `hmc_readiness == "not_claimed"`. |
| P90 target id | `bayesfilter/highdim/source_route.py:110`; target id is `zhao_cui_sir_austria_d18`. |
| P90 value binding | `bayesfilter/highdim/source_route.py:1063`; fail-closed branch/setup identity. |
| P90 derivative binding | `bayesfilter/highdim/source_route.py:1313`; fixed TTSIRT transport derivative status must remain a `BLOCK_*`. |
| P90 component carry | `bayesfilter/highdim/source_route.py:1370`; component scores are finite shape-checked tensors. |
| Negative-log sign convention | `bayesfilter/highdim/source_route.py:1503`; assembly negates component log-density scores. |
| P90 derivative result | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-result-2026-06-28.md`; deterministic carry only, full derivative not concluded. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Document/source-inventory score-contract freeze. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run in Phase 1. |
| Runtime status | No FD, score-identity runtime, HMC, GPU/XLA, package/network, release, CI, production benchmark, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md` |
| Score contract | `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-contract-2026-06-29.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md` |
| Refreshed Phase 2 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md` |

## Phase 2 Handoff

Phase 2 may start only after Claude review agrees on:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-contract-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md`

Phase 2 must implement or harden single and batched value/score APIs under the
score contract or close with an explicit API blocker. It must not run FD,
score identity, GPU/XLA, HMC, benchmark, package/release/CI, production, or
default-policy commands unless the reviewed Phase 2 subplan is refreshed to
authorize a narrower diagnostic.

The reviewed score contract now requires Phase 2 to expose setup identity in a
manifest, diagnostics payload, or return metadata. The initial batched route
must enforce shared setup identity across the batch, or else return per-item
identity metadata and fail closed on ambiguous or mixed metadata.
