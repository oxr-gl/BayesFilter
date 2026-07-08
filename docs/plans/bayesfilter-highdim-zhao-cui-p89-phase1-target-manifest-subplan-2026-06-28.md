# P89 Phase 1 Subplan: Target Manifest And Same-Scalar Branch Contract

Date: 2026-06-28

Status: `REVIEWED_READY_FOR_PHASE1_TARGET_MANIFEST_DESIGN`

## Phase Objective

Freeze the exact Zhao-Cui SIR d18 scalar target and branch contract that all
later value, gradient, FD, HMC, and GPU/XLA phases must use. Phase 1 is a
manifest/design phase only; it does not implement a value bridge, derivative
route, FD ladder, HMC, GPU/XLA, or production code.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result must be reviewed closed.
- P89 master and runbook are reviewed:
  `P89_MASTER_REVIEWED_AGREE` and `P89_VISIBLE_RUNBOOK_REVIEWED_AGREE`.
- Inherited label remains:
  `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`.
- `D18_CORRECTNESS_CANDIDATE` remains blocked until the same-target
  source-backed value bridge passes.
- Source-route full-history analytical derivative readiness remains blocked
  until source-route retained-object derivative propagation is designed,
  implemented, and validated.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase1-target-manifest-result-2026-06-28.md`
- Target manifest draft:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-target-manifest-2026-06-28.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase2-value-bridge-design-subplan-2026-06-28.md`
- Updated execution ledger, Claude review ledger, and stop handoff.
- The target manifest and Phase 1 result must include a field-level anchor
  table with:
  - manifest field;
  - local code or artifact anchor;
  - paper / author-source anchor if any;
  - fixed, unresolved, or intentionally deferred status;
  - whether the field is a source claim or implementation/setup choice.

## Required Checks/Tests/Reviews

Phase 1 is document/code-surface audit only. Allowed checks:

```bash
rg -n "source_route_sequential_negative_log_physical_density|source_route_run_sequential_fixed_hmc|source_route_previous_marginal_log_density|source_route_generate_retained_samples|P88_PHASE4_REVIEWED_NO_RUNTIME_BLOCKER_CLOSED|P88_PHASE5_REVIEWED_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS_CLOSED" bayesfilter/highdim/source_route.py docs/plans/bayesfilter-highdim-zhao-cui-p88*.md
rg -n "basis|rank|order|seed|retained|branch|same scalar|same-scalar|parameterization|source-backed" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
```

Claude Opus max-effort read-only review is required for the Phase 1 result,
target manifest, and Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact scalar and branch contract must all later Zhao-Cui SIR d18 production-promotion tests use? |
| Baseline/comparator | P88 rank/degree-stable source route, P88 correctness blocker, P88 derivative blocker, and local source-route code surfaces. |
| Primary criterion | A manifest names the scalar target identity, parameterization, basis/order/rank, retained objects, seeds/samples/schedules, branch identity, value API, gradient API expectations, and XLA setup-static fields. |
| Veto diagnostics | Missing branch identity; missing retained-object identity; missing parameterization; basis/rank/order allowed to drift without new manifest; FD target not tied to same scalar; value bridge allowed before manifest review; source-faithfulness claimed without anchors. |
| Explanatory diagnostics | Code-surface grep over source-route value functions and P88 blocker artifacts. |
| Not concluded | No value correctness, gradient correctness, FD validation, HMC readiness, GPU readiness, production readiness, or default-policy readiness. |
| Artifact | Phase 1 result, target manifest, refreshed Phase 2 subplan, ledgers, stop handoff. |

## Forbidden Claims/Actions

- Do not claim `D18_CORRECTNESS_CANDIDATE`.
- Do not claim source-route analytical-gradient readiness.
- Do not run value bridge execution, derivative implementation, FD validation,
  HMC/sampler, GPU/CUDA, production benchmark, package/network, TensorFlow/
  JAX/PyTorch, Python experiment, test-suite, or default-policy commands.
- Do not modify algorithmic code.
- Do not treat the target manifest as source correctness or production
  readiness.
- Do not claim source-faithfulness for any implementation choice without paper
  and local author-source anchors.
- Do not begin gradient, FD, HMC, GPU/XLA, production, or promotion work until
  the same-target value bridge has been designed, executed, and validated in
  the designated reviewed follow-on phases.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- Phase 1 result receives Claude `VERDICT: AGREE`;
- target manifest receives Claude `VERDICT: AGREE`;
- Phase 2 value-bridge design subplan receives Claude `VERDICT: AGREE`;
- stop handoff records that `D18_CORRECTNESS_CANDIDATE` remains blocked until
  Phase 3 value bridge validation passes;
- stop handoff records that gradient, FD, HMC, GPU/XLA, production, and final
  promotion phases remain blocked until the same-target value bridge is
  designed, executed, and validated by reviewed phase results.

## Stop Conditions

- The target scalar cannot be specified without crossing source-faithfulness or
  correctness-claim boundaries.
- Required target manifest fields cannot be identified from local artifacts.
- Local checks fail and cannot be repaired within document/code-surface audit.
- Claude review does not converge after five rounds for the same blocker.
- Continuing would require runtime, GPU/HMC, production, package/network,
  default-policy, destructive git/filesystem, or unrelated dirty-worktree
  changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write the Phase 1 result / close record.
3. Write or refresh the target manifest and its field-level anchor table.
4. Draft or refresh the Phase 2 value-bridge design subplan.
5. Review the target manifest and Phase 2 subplan for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
