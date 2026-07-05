# P90 Phase 5 Result: Deterministic Derivative-Carry Implementation

Date: 2026-06-28

Status: `P90_PHASE5_LOCAL_CHECKS_PASSED_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 5 implemented the reviewed deterministic derivative-carry surface and focused tests passed. |
| Primary criterion status | Met locally pending review: binding/carry records and component score helpers cover the manifest minimum target; unresolved fixed TTSIRT transport/proposal derivative owners remain explicit blocker rows. |
| Veto diagnostic status | Passed locally: no branch drift, no target drift, no FD-as-implementation, no hidden autodiff-only readiness claim, no fixed TTSIRT readiness overclaim, no GPU/HMC/production/default-policy command. |
| Main uncertainty | Full source-route analytical-gradient readiness remains blocked by fixed TTSIRT proposal/transport derivative ownership unless a later reviewed phase implements those surfaces. |
| Next justified action | Claude review of implementation artifact, this result, and refreshed Phase 6 subplan. Phase 6 must either be limited to the implemented deterministic carry surface or close as a blocker. |
| What is not being concluded | No full analytical-gradient readiness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, packaging readiness, or default-policy change. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the implementation provide the reviewed deterministic derivative-carry surface for the exact same scalar and branch, without pretending fixed TTSIRT proposal/transport readiness is solved? |
| Baseline/comparator | Reviewed Phase 4 derivative manifest and Phase 3 value bridge. |
| Primary criterion | Passed locally pending review: carry records and component score helpers are implemented; focused tests pass; fixed TTSIRT proposal/transport derivative owners remain blockers. |
| Veto diagnostics | Passed locally: derivative binding hash, target id, parameter indices, component shapes, previous retained hash, previous marginal axes, and blocker statuses fail closed. |
| Explanatory diagnostics | Unit tests, code review artifact, component coverage table. |
| Not concluded | FD validation, HMC readiness, GPU/XLA readiness, and production readiness remain unproven. |
| Artifact | Phase 5 implementation review artifact, this result, and refreshed Phase 6 subplan. |

## Local Checks

Commands:

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest tests/highdim/test_p90_derivative_carry_contract.py --maxfail=1
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Outcomes:

- First pytest attempt found a derivative-binding drift bug in assembly.
- Patched assembly to require exact same `SourceRouteDerivativeBinding` across
  components.
- Final pytest outcome: `5 passed, 2 warnings`.
- Warnings were TensorFlow Probability deprecation warnings.
- P90 docs diff hygiene passed before result writing.

## Implemented Component Coverage

| Component | Status |
| --- | --- |
| Derivative binding | `READY_P90_DETERMINISTIC_DERIVATIVE_BINDING` via `SourceRouteDerivativeBinding`; fixed TTSIRT transport derivative status remains `BLOCK_*`. |
| Transition score carry | `READY_P90_TRANSITION_PARAMETER_SCORE_CARRY`; tested against TensorFlow tape on deterministic SIR d18 fixture. |
| Likelihood score carry | `READY_P90_LIKELIHOOD_PARAMETER_SCORE_CARRY`; tested against TensorFlow tape on deterministic SIR d18 fixture. |
| Negative-log assembly | `READY_P90_DETERMINISTIC_ASSEMBLY_DERIVATIVE_CARRY`; sign and value tests pass. |
| Previous marginal carry | `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`; retained hash and axes drift veto tests pass. |
| Fixed TTSIRT proposal/transport derivative readiness | `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`; no readiness claim. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Focused local TensorFlow deterministic derivative-carry unit tests. |
| CPU/GPU status | CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Runtime/HMC status | No FD validation, HMC, sampler, GPU/XLA, package/network, production benchmark, release, CI, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-subplan-2026-06-28.md` |
| Implementation artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-implementation-review-artifact-2026-06-28.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-result-2026-06-28.md` |

## Phase 6 Handoff

Phase 6 may start only after Claude `VERDICT: AGREE` for:

- Phase 5 implementation review artifact;
- this Phase 5 result;
- `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase6-fd-gradient-validation-subplan-2026-06-28.md`.

If fixed TTSIRT proposal/transport derivative owners remain blocked, Phase 6
must not claim full source-route analytical-gradient readiness or production
readiness. It must either perform a reviewed limited FD check of the
implemented deterministic carry surface or write a blocker closeout.
