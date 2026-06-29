# P89 Phase 7 Subplan: HMC Readiness Blocker Closeout

Date: 2026-06-28

Status: `REVIEWED_READY_FOR_PHASE7_HMC_READINESS_BLOCKER_CLOSEOUT`

## Phase Objective

Close Phase 7 as a no-runtime HMC-readiness blocker because Phase 6 did not
run FD validation, Phase 5 did not implement source-route analytical
derivatives, and Phase 3 preserved the missing same-target value bridge. Phase
7 must not run HMC, sampler diagnostics, TensorFlow/Python runtime, GPU/CUDA,
production benchmarks, or claim HMC readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 6 result records no FD validation.
- Phase 6 result preserves `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`.
- Phase 6 result records no source-route analytical derivative implementation.
- Phase 6 result preserves that source-route full-history analytical
  derivative readiness remains blocked.
- Phase 6 result and this Phase 7 subplan receive bounded Claude
  `VERDICT: AGREE`.
- `D18_CORRECTNESS_CANDIDATE` remains blocked.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase7-hmc-readiness-result-2026-06-28.md`
- Refreshed Phase 8 GPU/XLA production subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase8-gpu-xla-production-subplan-2026-06-28.md`
- Updated execution ledger, Claude review ledger, and stop handoff.

Phase 7 result must explicitly state that no HMC/sampler diagnostic was run and
that GPU/XLA production readiness is blocked as a promotional phase.

## Required Checks/Tests/Reviews

Phase 7 is document-only. Allowed checks:

```bash
rg -n "P89_PHASE6.*FD|BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING|NO_SOURCE_ROUTE_ANALYTICAL_DERIVATIVE_IMPLEMENTATION|FD validation.*blocked|HMC readiness.*blocked|GPU/XLA.*blocked|Do not run HMC|Do not run TensorFlow|Do not run GPU" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
```

Claude Opus max-effort read-only review is required for the Phase 7 result and
refreshed Phase 8 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can HMC readiness be evaluated or promoted, or must it close as blocked because value, derivative implementation, and FD gates are missing? |
| Baseline/comparator | Reviewed Phase 6 FD blocker, Phase 5 derivative-implementation blocker, Phase 3 value-bridge blocker, and P89 target manifest. |
| Primary criterion | Phase 7 passes only as a no-runtime blocker closeout that preserves value, derivative, and FD blockers and prevents GPU/XLA/production promotion. |
| Veto diagnostics | HMC/sampler run; TensorFlow/Python runtime; GPU/CUDA command; production benchmark; HMC readiness claim; sampler diagnostics ranked despite missing value/gradient gates; value bridge, derivative-implementation, derivative-readiness, or FD-validation blocker weakened. |
| Explanatory diagnostics | Phase 6 no-FD fact and Phase 8 blocked handoff. |
| Not concluded | No HMC readiness, sampler validity, posterior correctness, GPU/XLA readiness, production readiness, LEDH agreement, scale readiness, or default-policy change. |
| Artifact | Phase 7 result, refreshed Phase 8 subplan, ledgers, stop handoff. |

## Forbidden Claims/Actions

- Do not claim `D18_CORRECTNESS_CANDIDATE`.
- Do not claim value correctness, posterior correctness, gradient correctness,
  FD validation, HMC readiness, GPU/XLA readiness, production readiness, LEDH
  agreement, scaling readiness, or default-policy readiness.
- Do not run HMC, sampler diagnostics, TensorFlow/JAX/PyTorch/Python
  experiment commands, tests, FD validation, derivative implementation,
  GPU/CUDA, production benchmark, package/network, or default-policy commands.
- Do not modify algorithmic code.
- Do not weaken, omit, or rephrase away `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`.
- Do not treat short-chain, smoke, ESS, R-hat, speed, fixed-branch, FD/JVP, or
  validation-loss evidence as HMC readiness.

## Exact Next-Phase Handoff Conditions

Phase 8 may start only if:

- Phase 7 result receives Claude `VERDICT: AGREE`;
- refreshed Phase 8 subplan receives Claude `VERDICT: AGREE`;
- Phase 7 result preserves `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`;
- Phase 7 result preserves that no source-route analytical derivative
  implementation exists and source-route derivative readiness remains blocked;
- Phase 7 result preserves that FD validation was not run and the FD gate
  remains blocked;
- Phase 7 result preserves that HMC readiness remains blocked;
- Phase 8 is explicitly a no-runtime GPU/XLA-production blocker closeout and
  not a GPU/CUDA or production benchmark run.

## Stop Conditions

- Phase 6 result is not reviewed or is materially revised.
- A proposed Phase 7 result would imply HMC readiness or sampler validity.
- Local checks fail and cannot be repaired within document-only scope.
- Claude review does not converge after five rounds for the same blocker.
- Continuing would require runtime execution, algorithmic edits, GPU/HMC,
  package/network, default-policy, destructive git/filesystem, or unrelated
  dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write the Phase 7 result / close record.
3. Draft or refresh the Phase 8 GPU/XLA production subplan as a blocked
   no-runtime handoff.
4. Review the Phase 7 result and Phase 8 subplan for consistency,
   correctness, feasibility, artifact coverage, and boundary safety.
