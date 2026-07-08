# P90 Phase 0 Subplan: Governance Bootstrap And Blocker Inheritance

Date: 2026-06-28

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Phase Objective

Confirm that P90 starts from P89's blocked final decision, preserves the
source-anchor gate and training boundaries, and permits no runtime or
production work before the value-bridge contract is reviewed.

## Entry Conditions Inherited From Previous Phase

- P89 final decision exists and states:
  `ZHAO_CUI_SIR_D18_NOT_PRODUCTION_READY_UNDER_P89`.
- P89 target manifest exists.
- P89 value-bridge blocker exists:
  `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`.
- P89 derivative blocker exists:
  `NO_SOURCE_ROUTE_ANALYTICAL_DERIVATIVE_IMPLEMENTATION`.
- P90 master and runbook have received bounded Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase0-governance-bootstrap-result-2026-06-28.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-visible-execution-ledger-2026-06-28.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-visible-stop-handoff-2026-06-28.md`
- Reviewed or refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Document/code/source-surface checks only:

```bash
rg -n "ZHAO_CUI_SIR_D18_NOT_PRODUCTION_READY_UNDER_P89|BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING|NO_SOURCE_ROUTE_ANALYTICAL_DERIVATIVE_IMPLEMENTATION|D18_SOURCE_ROUTE_RANK_DEGREE_STABLE|training-base|L1 weight tuning|No ALS|source-faithful|source_route_sequential_negative_log_physical_density" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md docs/plans/bayesfilter-highdim-zhao-cui-p90*.md bayesfilter/highdim/source_route.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Claude Opus max-effort read-only review is required for the Phase 0 result and
the Phase 1 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P90 safely bootstrapped from P89 without weakening blockers or authorizing premature runtime/scientific/product work? |
| Baseline/comparator | P89 final decision, P89 reset memo, P89 target manifest, P89 value-bridge blocker, P89 derivative inventory, and local source-route surfaces. |
| Primary criterion | Phase 0 passes only if P90 inherits the correct blockers, preserves source-anchor/training/runtime boundaries, and hands off solely to Phase 1 value-bridge contract design. |
| Veto diagnostics | Missing P89 blocker, production-ready claim, value/gradient/FD/HMC/GPU readiness claim, ALS revival, unanchored source-faithful claim, runtime/GPU/HMC/package/default-policy action, or unrelated dirty-worktree modification. |
| Explanatory diagnostics | Grep inventory of artifacts, source-route value surfaces, and prior blocker labels. |
| Not concluded | No value correctness, derivative readiness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, packaging readiness, or default-policy change. |
| Artifact | Phase 0 result and reviewed Phase 1 subplan. |

## Forbidden Claims/Actions

- Do not claim Zhao-Cui SIR d18 is production-ready.
- Do not claim `D18_CORRECTNESS_CANDIDATE`.
- Do not claim value correctness, source-route correctness, analytical-gradient
  correctness, FD validation, HMC readiness, GPU/XLA readiness, packaging
  readiness, or default-policy readiness.
- Do not run TensorFlow/JAX/PyTorch/Python numerical experiments, FD, HMC,
  GPU/CUDA, package/network, CI, release, production benchmark, or default-
  policy commands.
- Do not modify algorithmic code.
- Do not revive ALS training.
- Do not weaken `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- Phase 0 result receives Claude `VERDICT: AGREE`;
- Phase 1 subplan receives Claude `VERDICT: AGREE`;
- Phase 0 result preserves all inherited blockers;
- Phase 1 is limited to same-target value-bridge contract design, not runtime
  bridge execution.

## Stop Conditions

- P89 artifacts are missing or contradict P90 inheritance.
- Local checks fail and cannot be repaired in document scope.
- Claude review does not converge after five rounds for the same blocker.
- Continuing would require runtime, GPU/CUDA, HMC, package/network, release,
  default-policy, algorithmic code edits, destructive git/filesystem action, or
  unrelated dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 0 result / close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
