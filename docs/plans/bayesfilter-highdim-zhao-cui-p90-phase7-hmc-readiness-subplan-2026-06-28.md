# P90 Phase 7 Subplan: HMC Readiness Blocker Closeout

Date: 2026-06-28

Status: `PHASE6_REVIEWED_NO_HMC_BLOCKER_READY`

## Phase Objective

Close HMC readiness as blocked unless Phase 6 reviewed result unexpectedly
provides a full same-scalar FD-gradient validation pass. From the current Phase
6 blocker state, Phase 7 must not run HMC.

## Entry Conditions Inherited From Previous Phase

- Phase 6 result reviewed pass.
- Phase 6 did not run FD and did not validate full source-route analytical
  gradients.
- Fixed TTSIRT proposal/transport derivative blockers remain open.
- This Phase 7 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase7-hmc-readiness-result-2026-06-28.md`
- Refreshed Phase 8 GPU/XLA-production subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase8-gpu-xla-production-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed local check:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

No HMC, TensorFlow/Python runtime, GPU/CUDA, production benchmark,
package/network, release, CI, or default-policy command is authorized.

Claude review is required for Phase 7 result and Phase 8 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can HMC readiness be evaluated, or must it close blocked because FD/full-gradient gates remain blocked? |
| Baseline/comparator | Phase 6 blocker/limited-only result and Phase 5 deterministic derivative-carry implementation. |
| Primary criterion | Phase 7 passes only as no-runtime blocker closeout if Phase 6 did not provide full FD-gradient validation. |
| Veto diagnostics | HMC run attempted, sampler readiness claim, speed/ESS ranking, GPU/production command, full-gradient claim, or fixed TTSIRT blocker weakened. |
| Explanatory diagnostics | Phase 6 blocker rationale and derivative blocker ledger. |
| Not concluded | No HMC readiness, posterior correctness, GPU/XLA readiness, production readiness, packaging readiness, or default-policy change. |
| Artifact | Phase 7 result and refreshed Phase 8 subplan. |

## Forbidden Claims/Actions

- Do not run HMC.
- Do not claim HMC readiness.
- Do not rank sampler configurations by speed, ESS, acceptance, or trace
  diagnostics because no sampler run is authorized.
- Do not run GPU/XLA production, packaging, CI, release, or default-policy
  commands.
- Do not weaken fixed TTSIRT proposal/transport derivative blockers.

## Exact Next-Phase Handoff Conditions

Phase 8 may start only as a blocker closeout unless:

- Phase 7 result receives Claude `VERDICT: AGREE`;
- Phase 8 subplan receives Claude `VERDICT: AGREE`;
- Phase 8 explicitly preserves that HMC readiness is blocked and authorizes no
  GPU/XLA production run.

## Stop Conditions

- Any HMC/runtime/GPU/production command would be needed.
- A readiness claim would require unresolved FD/full-gradient gates.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed GPU/package/default-policy or unrelated
  dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 7 result / close record.
3. Draft or refresh Phase 8 subplan.
4. Review Phase 7 result and Phase 8 subplan for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
