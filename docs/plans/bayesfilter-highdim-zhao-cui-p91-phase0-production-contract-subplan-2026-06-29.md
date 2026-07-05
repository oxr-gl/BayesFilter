# P91 Phase 0 Subplan: Production Contract Reframe

Date: 2026-06-29

Status: `DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the revised P91 production-readiness contract. The contract must record
owner decisions that score identity is the primary scientific validation gate,
FD is necessary engineering consistency but not an oracle, GPU/XLA JIT
capability is required for HMC-facing production, CPU/GPU performance is
model-specific, and batched value/score APIs are required.

## Entry Conditions Inherited From Previous Phase

- P90 final decision exists and says Zhao-Cui SIR d18 is not production ready.
- P90 retained positives are value bridge and deterministic derivative-carry
  implementation only.
- User owner amendments from 2026-06-29 are the binding P91 production
  standard.
- P91 master/runbook and this subplan receive Claude `VERDICT: AGREE`.

## Required Artifacts

- Master program reviewed at launch:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-identity-hmc-gpu-production-master-program-2026-06-29.md`
- Visible runbook reviewed at launch:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-gated-execution-runbook-2026-06-29.md`
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md`
- Production contract:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md`
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-result-2026-06-28.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p90-production-repair-reset-memo-2026-06-28.md
rg -n "score identity|FD|GPU/XLA|batched|HMC|default|production|oracle|likelihood" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Claude review is required for the production contract, Phase 0 result, and
refreshed Phase 1 subplan. No runtime, TensorFlow, GPU/CUDA, HMC, FD,
package/network, release, CI, production, or default-policy command is
authorized.

## Skeptical Plan Audit

| Risk Checked | Phase 0 Control |
| --- | --- |
| Wrong baseline | Phase 0 checks exact P90 final decision and reset memo paths before writing the P91 contract. |
| Proxy metric promoted | Phase 0 is document-only and explicitly forbids treating score identity as exact likelihood proof, FD as an oracle, or GPU as universally fastest. |
| Missing stop condition | Stop conditions include missing P90 anchors, overclaiming contract, failed local checks, non-convergent Claude review, and runtime/default boundaries. |
| Unfair comparison | CPU/GPU speed is recorded as model-specific and deferred to Phase 6. |
| Hidden assumption | Root solving and Hessian/information equality are recorded as optional/advisory rather than production gates. |
| Stale context | P90 final/reset artifacts and owner amendments are the only Phase 0 baseline. |
| Environment mismatch | No runtime or GPU command is authorized; GPU/HMC gates remain later phases. |
| Artifact mismatch | The production contract itself, Phase 0 result, and Phase 1 subplan all require review. |

Audit status: passed for Phase 0 launch after master, runbook, and this
subplan receive Claude `VERDICT: AGREE`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the P91 production contract safely reframed from P90 without treating score identity as exact likelihood proof, FD as oracle, or GPU as universally fastest? |
| Baseline/comparator | P90 final blocked decision and user P91 owner amendments. |
| Primary criterion | Phase 0 passes if the production contract explicitly states required gates, non-claims, owner decisions, runtime boundaries, and next-phase handoff. |
| Veto diagnostics | Exact-likelihood claim, FD oracle claim, root-solving requirement, Hessian requirement, universal GPU-speed claim, missing batched route requirement, or default-policy change. |
| Explanatory diagnostics | Local grep coverage and artifact hygiene. |
| Not concluded | No score correctness, FD pass, GPU/XLA readiness, HMC readiness, benchmark result, production readiness, or default-policy change. |
| Artifact | Reviewed production contract, Phase 0 result, refreshed Phase 1 subplan. |

## Forbidden Claims/Actions

- Do not claim Zhao-Cui production readiness.
- Do not claim score identity proves exact likelihood correctness.
- Do not claim FD is a truth oracle.
- Do not require root solving or Hessian/information equality as production
  gates.
- Do not claim GPU is always faster than CPU.
- Do not run runtime/GPU/HMC/FD/package/default commands.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- Phase 0 result receives Claude `VERDICT: AGREE`;
- production contract receives Claude `VERDICT: AGREE`;
- Phase 1 subplan receives Claude `VERDICT: AGREE`;
- production contract path is exact and records score convention work as Phase
  1, not Phase 0.

## Stop Conditions

- P90 closeout anchors are missing or contradicted.
- The revised production contract would weaken owner decisions or overclaim.
- Local checks fail and cannot be repaired in document scope.
- Claude review does not converge after five rounds.
- Continuing would require runtime, GPU/CUDA, package/network, release, CI,
  default-policy, destructive git/filesystem, or unrelated dirty-work changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 0 result / close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 0 result and Phase 1 subplan for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
