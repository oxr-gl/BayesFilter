# P90 Phase 6 Subplan: Limited FD Gradient Validation Or Blocker Closeout

Date: 2026-06-28

Status: `PENDING_PHASE5_REVIEW_READY_FOR_PHASE6_REVIEW`

## Phase Objective

Validate, or explicitly block, finite-difference comparison for the exact same
scalar and branch after Phase 5. Because fixed TTSIRT proposal/transport
derivative owners remain blockers unless Phase 5 review says otherwise, Phase
6 may validate only the implemented deterministic derivative-carry surface or
write a blocker closeout. It must not claim full source-route
analytical-gradient readiness while transport/proposal derivative owners are
blocked.

## Entry Conditions Inherited From Previous Phase

- Phase 5 implementation review artifact reviewed pass.
- Phase 5 result reviewed pass.
- Phase 3 value bridge reviewed pass remains valid.
- This Phase 6 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Limited FD validation manifest/output if a limited FD run is reviewed and
  executed.
- Blocker result if fixed TTSIRT proposal/transport derivative blockers prevent
  valid same-scalar full-gradient FD validation.
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase6-fd-gradient-validation-result-2026-06-28.md`
- Refreshed Phase 7 HMC-readiness subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase7-hmc-readiness-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

No FD runtime command is authorized by this subplan yet. Phase 6 must first
choose one of two reviewed routes:

1. limited deterministic carry FD check with exact command, coordinates, step
   sizes, tolerances, and nonclaims added before execution; or
2. no-runtime blocker closeout preserving fixed TTSIRT proposal/transport
   derivative blockers.

Allowed document hygiene command before route choice:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Any TensorFlow/Python runtime command requires exact reviewed authorization.
GPU/CUDA, HMC, production benchmark, package/network, release, CI, and
default-policy commands are forbidden.

Claude review is required for Phase 6 result and Phase 7 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can FD validation be run without overclaiming beyond the implemented deterministic derivative-carry surface, or must Phase 6 close as blocked? |
| Baseline/comparator | Phase 5 deterministic derivative-carry implementation and Phase 3 value bridge. |
| Primary criterion | Either a reviewed limited FD protocol is executed and passes for implemented carry only, or a no-runtime blocker result preserves unresolved fixed TTSIRT proposal/transport derivative blockers. |
| Veto diagnostics | FD uses wrong scalar, branch changes, retained objects change, tolerance changed after seeing results, nonfinite values, fixed TTSIRT readiness overclaim, full-gradient claim while blockers remain, or unreviewed runtime command. |
| Explanatory diagnostics | Step-size sensitivity, coordinate residual table, component residuals if limited FD is reviewed. |
| Not concluded | FD is not source-faithfulness proof and does not establish HMC/GPU/production readiness. Limited FD would not prove full source-route analytical-gradient readiness. |
| Artifact | FD manifest or blocker result, Phase 6 result, and refreshed Phase 7 subplan. |

## Forbidden Claims/Actions

- Do not treat FD as source-faithfulness proof.
- Do not claim full source-route analytical-gradient readiness while fixed
  TTSIRT proposal/transport derivative owners remain blocked.
- Do not run unreviewed FD, HMC, GPU/CUDA, packaging, CI, release, production,
  or default-policy commands.
- Do not change FD tolerances after seeing results.
- Do not use validation/holdout/training clouds as audit clouds.

## Exact Next-Phase Handoff Conditions

Phase 7 may start only if:

- Phase 6 result receives Claude `VERDICT: AGREE`;
- Phase 7 subplan receives Claude `VERDICT: AGREE`;
- value and derivative-carry gates remain valid;
- if Phase 6 closes blocked or limited-only, Phase 7 must also close blocked
  or remain explicitly limited and non-promotional.

## Stop Conditions

- FD validation would require claiming unresolved fixed TTSIRT derivative
  readiness.
- Trusted/reviewed runtime context is unavailable.
- Branch/setup drift occurs.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed HMC/GPU/package/default-policy or
  unrelated dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 6 result / close record.
3. Draft or refresh Phase 7 subplan.
4. Review Phase 7 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
