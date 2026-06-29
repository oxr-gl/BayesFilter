# P90 Phase 8 Subplan: GPU/XLA Production Readiness Blocker Closeout

Date: 2026-06-28

Status: `PHASE7_REVIEW_PENDING_NO_GPU_XLA_BLOCKER_READY`

## Phase Objective

Close GPU/XLA production readiness as blocked unless Phase 7 reviewed result
unexpectedly provides an HMC readiness pass. From the current Phase 7
no-runtime blocker state, Phase 8 must not run GPU/CUDA or production
diagnostics.

## Entry Conditions Inherited From Previous Phase

- Phase 7 result reviewed pass.
- HMC readiness remains blocked.
- Value bridge remains positive, but full-gradient, FD, and HMC gates remain
  blocked or limited.
- This Phase 8 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase8-gpu-xla-production-result-2026-06-28.md`
- Refreshed Phase 9 packaging/default subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase9-packaging-default-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed local check:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

No GPU/CUDA, TensorFlow/Python runtime, HMC, FD, production benchmark,
package/network, release, CI, or default-policy command is authorized.

Claude review is required for Phase 8 result and Phase 9 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can GPU/XLA production readiness be evaluated, or must it close blocked because HMC/full-gradient gates remain blocked? |
| Baseline/comparator | Phase 7 no-HMC blocker result and upstream derivative/FD blockers. |
| Primary criterion | Phase 8 passes only as no-runtime blocker closeout if HMC readiness did not pass. |
| Veto diagnostics | GPU/CUDA run attempted, production readiness claim, runtime/memory/speed claim, package/default command, or upstream blocker weakened. |
| Explanatory diagnostics | Phase 7 blocker rationale and upstream derivative/FD blocker ledger. |
| Not concluded | No GPU/XLA readiness, production readiness, packaging readiness, release/CI readiness, or default-policy change. |
| Artifact | Phase 8 result and refreshed Phase 9 subplan. |

## Forbidden Claims/Actions

- Do not run GPU/CUDA or TensorFlow/XLA runtime.
- Do not claim GPU/XLA production readiness.
- Do not treat prior CPU-only value/derivative tests as GPU/XLA evidence.
- Do not run packaging, release, CI, package/network, or default-policy
  commands.
- Do not weaken HMC, FD, or fixed TTSIRT derivative blockers.

## Exact Next-Phase Handoff Conditions

Phase 9 may start only as packaging/default blocker closeout unless:

- Phase 8 result receives Claude `VERDICT: AGREE`;
- Phase 9 subplan receives Claude `VERDICT: AGREE`;
- Phase 9 explicitly preserves that GPU/XLA and HMC readiness are blocked and
  authorizes no packaging/default/release/CI action.

## Stop Conditions

- Any GPU/CUDA/runtime/production/package command would be needed.
- A readiness claim would require unresolved HMC/full-gradient gates.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed package/release/default-policy or
  unrelated dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 8 result / close record.
3. Draft or refresh Phase 9 subplan.
4. Review Phase 8 result and Phase 9 subplan for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
