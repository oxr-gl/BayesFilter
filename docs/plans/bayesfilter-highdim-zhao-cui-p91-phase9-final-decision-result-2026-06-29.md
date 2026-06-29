# P91 Phase 9 Result: Final Production Decision

Date: 2026-06-29

Status: `P91_SCOPED_PRODUCTION_READY_CLOSED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Zhao-Cui SIR d18 is recommended as scoped production-ready under P91 for the highdim subpackage API and local complete-data component route, with release-note caveats. |
| Primary criterion status | Passed for scoped promotion: P91 reviewed gates are closed for score contract, batched API, owner-accepted limited FD with caveats, local component score identity, GPU/XLA JIT, CPU/GPU/batched benchmark, HMC smoke, and release-note preparation. |
| Veto diagnostic status | Passed for scoped promotion: final decision does not claim exact likelihood correctness, posterior correctness/convergence, full observed-data/filtering score identity, full source-route FD derivative readiness, universal GPU superiority, package publication, release tagging, CI mutation, or default-policy change. |
| Main uncertainty | The scoped promotion is not a blanket source-route/filtering promotion. Previous-marginal and fixed TTSIRT proposal/transport derivative blockers remain open for full observed-data/filtering score readiness. Phase 3 remains owner-accepted limited FD evidence, not a full source-route FD pass. |
| Next justified action | Treat the scoped route as release-note-ready internally, then separately decide whether to change defaults, publish, tag a release, or run broader CI under a new reviewed authority. |
| What is not being concluded | No exact likelihood correctness, posterior correctness, convergence, full observed-data/filtering HMC readiness, full source-route derivative readiness, universal GPU speed superiority, package publication, release tagging, CI-service mutation, or default-policy change. |

## Final Scope

Promoted scope:

- highdim subpackage API surfaces for Zhao-Cui SIR d18;
- local complete-data component route conditioned on a fixed latent state path
  and observation path;
- three-parameter log-scale surface
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`;
- single and batched score/value API semantics with setup-identity metadata;
- XLA helper route for local complete-data value/score;
- trusted GPU/XLA capability and tiny TFP HMC implementation smoke evidence.

Not promoted:

- full observed-data/filtering score identity through previous marginal and
  fixed TTSIRT proposal/transport derivatives;
- full source-route FD derivative readiness;
- exact likelihood correctness;
- posterior correctness or convergence;
- universal GPU performance superiority;
- top-level package export or root default-policy change;
- package publication, release tagging, or CI-service mutation.

## Reviewed Gate Summary

| Gate | Final Status | Evidence |
| --- | --- | --- |
| Phase 0 production contract | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md`. |
| Phase 1 score contract | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-contract-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md`. |
| Phase 2 batched API | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-local-check-output-2026-06-29.md`. |
| Phase 3 FD | Accepted with caveats | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-local-check-output-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json`. Limited t=1 FD diagnostic remains historical blocked evidence under the arbitrary `5e-5` gate, but owner accepted the small miss for continuation. Not a full source-route FD pass. |
| Phase 4 score identity | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-local-check-output-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json`. Local complete-data component score satisfies `abs(mean score) <= 2 * sample SD` across four regimes and ten seeds each. |
| Phase 5 GPU/XLA JIT | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json`. |
| Phase 6 benchmark | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json`. CPU/GPU single/batched local fixture benchmark completed with no universal GPU claim. |
| Phase 7 HMC smoke | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json`. Tiny trusted GPU/XLA TFP HMC smoke returned finite samples, target values, scalar per-sample gradients, and log-accept ratios. |
| Phase 8 release notes | Passed | `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md`; `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-result-2026-06-29.md`. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What is the final P91 production decision for Zhao-Cui SIR d18? |
| Baseline/comparator | Reviewed P91 phase results, P90 blocked baseline, and owner P91 amendments. |
| Primary criterion | Passed for scoped production readiness: every required P91 scoped gate has a reviewed pass or explicit owner-accepted continuation status with caveats. |
| Veto diagnostics | Passed: no missing blocker, unsupported exact-likelihood/posterior/GPU/default claim, release/default action, or proxy metric promotion across ledgers. |
| Explanatory diagnostics | Phase ledger, FD table, score identity table, GPU/JIT and benchmark summaries, HMC smoke summary, release-note caveats, preserved blocker table. |
| Not concluded | Stronger claims listed in the non-promoted scope remain not concluded. |
| Artifact | This final decision, `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md`, `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-execution-ledger-2026-06-29.md`, `docs/plans/bayesfilter-highdim-zhao-cui-p91-claude-review-ledger-2026-06-29.md`, and `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-stop-handoff-2026-06-29.md`. |

## Preserved Blockers And Caveats

Preserved blocker labels:

- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`;
- `full_observed_data_filtering_score_identity = NOT_CLAIMED`.

Phase 3 caveat:

- The limited FD diagnostic was accepted for continuation because the `5e-5`
  threshold was arbitrary and the miss was consistent with deterministic FD
  truncation.
- The Phase 3 manifest's historical blocked status is not erased.
- The Phase 3 diagnostic is not a full FD pass, not a true-gradient oracle
  check, and not a full source-route derivative-readiness claim.

Phase 4 caveat:

- Score identity is validated only for local complete-data component scores.
- It is not exact likelihood proof and not full observed-data/filtering score
  identity.

Phase 6 caveat:

- The CPU/GPU benchmark is model/fixture-specific.
- It does not prove GPU is universally faster.

Phase 7 caveat:

- HMC smoke is an implementation smoke only.
- It does not prove posterior correctness, convergence, or full
  observed-data/filtering HMC readiness.
- Native boolean divergence status was unavailable in the TFP trace; no ESS,
  speed, or acceptance-rate proxy was used to override hard vetoes.

## Release Readiness Recommendation

Use the reviewed release-note draft if this scoped decision is communicated:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-release-notes-draft-2026-06-29.md`

The release note must remain scope-first:

- supported only for the highdim API and local complete-data Zhao-Cui SIR d18
  component route;
- no exact likelihood correctness;
- no posterior correctness/convergence;
- no full observed-data/filtering score identity;
- no full source-route FD derivative readiness;
- no universal GPU speed superiority.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Execution target | Document-only final decision. |
| CPU/GPU status | No runtime, TensorFlow, GPU/CUDA, XLA, HMC, or benchmark command was run in Phase 9. |
| Runtime/package status | No package/network, release, CI-service, publication, tag, production deployment, or default-policy command was run. |
| Commands | `rg -n "P91|score identity|FD|GPU/XLA|batched|HMC|benchmark|release|default|production" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`; `rg -n "BLOCK_FIXED_TTSIRT|BLOCK_FULL_SOURCE_ROUTE_FD|Phase 3|posterior correctness|exact likelihood correctness|universal GPU|divergence_status|owner-accepted" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`; `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md` |
| Data version | `N/A`; document-only final decision. |
| Random seeds | `N/A`; no runtime in Phase 9. |
| Wall time | `N/A`; Phase 9 was document-only and did not run a timed runtime/benchmark command. Final document checks completed with exit code 0. |
| Phase 9 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md` |
| Final decision | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md` |
| Reset memo | `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md` |
| Stop handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-stop-handoff-2026-06-29.md` |

## Safest Next Action

If the project wants a broader production claim, start a successor program for
full observed-data/filtering score readiness:

1. implement and review previous-marginal derivative ownership;
2. implement and review fixed TTSIRT proposal/transport derivative ownership;
3. rerun full source-route FD and score-identity gates under that broader
   route;
4. only then reopen posterior validation, default-policy, package/release, or
   broader CI actions.

For the P91 scoped route, the next action is not more algorithm repair; it is a
separate product/release/default-governance decision if the owner wants to
publish, tag, broaden CI, or change defaults.
