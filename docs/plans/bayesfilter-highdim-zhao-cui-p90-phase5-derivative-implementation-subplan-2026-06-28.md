# P90 Phase 5 Subplan: Deterministic Derivative-Carry Implementation

Date: 2026-06-28

Status: `PENDING_PHASE4_REVIEW_READY_FOR_PHASE5_REVIEW`

## Phase Objective

Implement the reviewed minimum deterministic derivative-carry surface for the
exact same scalar and branch that passed Phase 3, while preserving explicit
blocker rows for fixed TTSIRT proposal/transport derivative readiness if those
source-backed derivative surfaces are not implemented.

## Entry Conditions Inherited From Previous Phase

- Phase 3 value bridge reviewed pass remains valid.
- Phase 4 derivative manifest reviewed pass:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-derivative-carry-manifest-2026-06-28.md`
- Phase 4 result reviewed pass:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-result-2026-06-28.md`
- This Phase 5 subplan has Claude `VERDICT: AGREE`.

## Required Artifacts

- Code changes implementing deterministic derivative binding/carry records and
  component score helpers required by the Phase 4 manifest.
- Focused implementation tests:
  `tests/highdim/test_p90_derivative_carry_contract.py`
- Phase 5 implementation review artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-implementation-review-artifact-2026-06-28.md`
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-result-2026-06-28.md`
- Refreshed Phase 6 FD-validation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase6-fd-gradient-validation-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed implementation/check commands after Phase 4 review:

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest tests/highdim/test_p90_derivative_carry_contract.py --maxfail=1
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

The pytest command is CPU-only with GPU hidden before TensorFlow import.
GPU/CUDA, FD validation, HMC, production benchmark, package/network, release,
CI, and default-policy commands are forbidden in Phase 5.

Claude review is required for the implementation review artifact, Phase 5
result, and Phase 6 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the implementation provide the reviewed deterministic derivative-carry surface for the exact same scalar and branch, without pretending fixed TTSIRT proposal/transport readiness is solved? |
| Baseline/comparator | Reviewed Phase 4 derivative manifest and Phase 3 value bridge. |
| Primary criterion | Binding/carry records and component score helpers cover the manifest minimum target; focused tests pass; unresolved fixed TTSIRT transport/proposal derivative owners remain explicit blocker rows. |
| Veto diagnostics | Missing branch binding, target drift, missing component score carry, hidden FD-as-implementation, hidden autodiff-only readiness claim, fixed TTSIRT proposal/transport readiness overclaim, nonfinite gradient, or Phase 3 value bridge invalidation. |
| Explanatory diagnostics | Unit tests, code review, component coverage table. |
| Not concluded | FD validation, HMC readiness, GPU/XLA readiness, and production readiness remain unproven until later phases. |
| Artifact | Phase 5 implementation review artifact, Phase 5 result, and refreshed Phase 6 subplan. |

## Forbidden Claims/Actions

- Do not run FD validation before Phase 5 passes.
- Do not claim full source-route analytical-gradient readiness unless every
  fixed TTSIRT proposal/transport derivative owner is implemented and tested.
- Do not claim HMC/GPU/production readiness.
- Do not run HMC, GPU/CUDA, packaging, CI, release, or default-policy
  commands.
- Do not revive ALS training.
- Do not change the Phase 3 value scalar, branch hashes, retained-object hash,
  coordinate-frame hash, or tolerance version.
- Do not use FD, JVP, reverse-mode autodiff, or fixed-branch evidence as a
  substitute for source-route derivative ownership.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if:

- implementation tests pass;
- Phase 5 implementation review artifact receives Claude `VERDICT: AGREE`;
- Phase 5 result receives Claude `VERDICT: AGREE`;
- Phase 6 subplan receives Claude `VERDICT: AGREE`;
- if any fixed TTSIRT proposal/transport derivative owner remains blocked,
  Phase 6 must either be a reviewed blocker closeout or explicitly limit FD to
  the implemented deterministic derivative-carry surface without production
  readiness claims.

## Stop Conditions

- Required deterministic derivative-carry component cannot be implemented.
- Tests fail and cannot be repaired within scope.
- Implementation changes target/branch/setup fields.
- Fixed TTSIRT proposal/transport derivative readiness would be claimed without
  implementation evidence.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed runtime/GPU/HMC/package/default-policy or
  unrelated dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 5 implementation review artifact and result / close record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
