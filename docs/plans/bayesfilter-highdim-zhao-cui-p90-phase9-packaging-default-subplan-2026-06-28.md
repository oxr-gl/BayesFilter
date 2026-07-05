# P90 Phase 9 Subplan: Packaging, CI, And Default-Readiness Blocker Closeout

Date: 2026-06-28

Status: `PHASE8_REVIEW_PENDING_PACKAGING_DEFAULT_BLOCKER_READY`

## Phase Objective

Close packaging, CI, release, and default-readiness as a documentation-only
blocked closeout under the inherited Phase 8 no-GPU/XLA production blocker
state. Phase 9 cannot evaluate readiness under this subplan and must not run
package/network, release, CI, production, GPU/CUDA, TensorFlow/XLA, or
default-policy commands.

If a future reviewed Phase 8 artifact unexpectedly provides a GPU/XLA
production readiness pass, this subplan is invalid/superseded and a new Phase 9
subplan is required before any packaging, CI, release, default-readiness,
production, runtime, or policy action.

## Entry Conditions Inherited From Previous Phase

- Phase 8 result reviewed pass.
- GPU/XLA production readiness remains blocked.
- HMC readiness, full same-scalar FD-gradient validation, and fixed TTSIRT
  proposal/transport derivative readiness remain blocked.
- Value bridge remains positive and deterministic derivative-carry
  implementation remains positive, but those are not packaging/default evidence.
- This Phase 9 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 9 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase9-packaging-default-result-2026-06-28.md`
- Refreshed Phase 10 final-decision subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed local check:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

No package/network, release, CI, production benchmark, GPU/CUDA,
TensorFlow/XLA, HMC, FD, or default-policy command is authorized.

Claude review is required for Phase 9 result and Phase 10 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Given the inherited Phase 8 no-GPU/XLA production blocker, can Phase 9 close packaging/CI/default readiness as a documentation-only blocker without crossing package, CI, release, production, runtime, or default-policy boundaries? |
| Baseline/comparator | Phase 8 no-GPU/XLA production blocker result and upstream FD/HMC blockers. |
| Primary criterion | Phase 9 passes only as no-runtime blocker closeout that preserves the exact inherited blocker basis and records that no prohibited actions were taken. |
| Veto diagnostics | Package/network, release, CI, production, GPU/CUDA, TensorFlow/XLA, HMC, FD, or default-policy command attempted; packaging/default readiness claim; upstream blocker weakened. |
| Explanatory diagnostics | Phase 8 blocker rationale and upstream derivative/FD/HMC blocker ledger. |
| Not concluded | No packaging readiness, CI readiness, release readiness, production readiness, or default-policy change. |
| Artifact | Phase 9 result and refreshed Phase 10 subplan. |

## Forbidden Claims/Actions

- Do not run package/network, release, CI, or default-policy commands.
- Do not run production benchmark, GPU/CUDA, TensorFlow/XLA, HMC, or FD
  commands.
- Do not claim packaging, CI, release, default, production, or GPU/XLA
  readiness.
- Do not treat Phase 3 value bridge or Phase 5 derivative-carry tests as
  package/default evidence.
- Do not hide or weaken unresolved derivative, FD, HMC, or GPU/XLA blockers.

## Exact Next-Phase Handoff Conditions

Phase 10 may start only as final blocked production decision unless:

- Phase 9 result receives Claude `VERDICT: AGREE`;
- Phase 10 subplan receives Claude `VERDICT: AGREE`;
- Phase 10 explicitly preserves all upstream pass/blocker statuses and
  authorizes no runtime, package/network, release, CI, or default-policy action.

The Phase 9 result must record the exact inherited blocker basis, that Phase 9
was a no-runtime/documentation-only closeout, and that no package/network,
release, CI, production, GPU/CUDA, TensorFlow/XLA, HMC, FD, or default-policy
action was taken.

## Stop Conditions

- Any package/network, release, CI, runtime, GPU/CUDA, production, HMC, FD, or
  default-policy command would be needed.
- A readiness claim would require unresolved derivative/FD/HMC/GPU/XLA gates.
- A future reviewed Phase 8 artifact changes GPU/XLA production readiness from
  blocked to passed; stop and replace this subplan before proceeding.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed release/default-policy or unrelated dirty
  worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 9 result / close record.
3. Draft or refresh Phase 10 subplan.
4. Review Phase 9 result and Phase 10 subplan for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
